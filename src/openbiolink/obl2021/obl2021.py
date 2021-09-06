import os
import pickle
import urllib
import zipfile
from os import path
from typing import cast, Iterable, Tuple

import numpy as np
import pandas as pd
import torch
from openbiolink.utils import split_list_in_batches_iter
from tqdm import tqdm

from openbiolink.graph_creation.file_downloader import FileDownloader


class OBL2021Dataset(object):
    """
    Args:
        root: Pathlike string to directory in which dataset files should be stored
    """

    def __init__(self, root: str = 'obl2021'):

        self._dataset_path = root
        self._url = r"https://zenodo.org/record/5361324/files/KGID_HQ_DIR.zip"
        self._download()

        self._entity_label_to_id = None
        self._id_to_entity_label = None
        self._relation_label_to_id = None
        self._id_to_relation_label = None

        node_mapping = pd.read_csv(os.path.join(self._dataset_path, "entities.tsv"), sep="\t", header=None)
        self._entity_label_to_id = {label: id for label, id in
                                    zip(node_mapping[1], node_mapping[0])}
        self._id_to_entity_label = {
            id: label
            for label, id in self._entity_label_to_id.items()
        }

        relation_mapping = pd.read_csv(os.path.join(self._dataset_path, "relations.tsv"), sep="\t", header=None)
        self._relation_label_to_id = {label: id for label, id in
                                      zip(relation_mapping[1],
                                          relation_mapping[0])}
        self._id_to_relation_label = {
            id: label
            for label, id in self._relation_label_to_id.items()
        }

        self._training = self._load(os.path.join(self._dataset_path, "train.tsv"))
        self._validation = self._load(os.path.join(self._dataset_path, "valid.tsv"))
        self._testing = self._load(os.path.join(self._dataset_path, "test.tsv"))

        self._num_entities = len(self._entity_label_to_id)
        self._num_relations = len(self._relation_label_to_id)

        with open(os.path.join(self._dataset_path, '_dict_of_heads.pkl'), 'rb') as f:
            self._dict_of_heads = pickle.load(f)
        with open(os.path.join(self._dataset_path, '_dict_of_tails.pkl'), 'rb') as f:
            self._dict_of_tails = pickle.load(f)

    def _download(self):
        if not path.isdir(self._dataset_path):
            os.mkdir(self._dataset_path)

        # check if exists
        if not path.isdir(self._dataset_path) or not os.listdir(self._dataset_path):
            print(
                f"Dataset not found, downloading to {os.path.abspath(self._dataset_path)} ...")
            url = self._url
            filename = url.split('/')[-1]
            with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=filename) as t:
                zip_path, _ = urllib.request.urlretrieve(url, reporthook=FileDownloader.download_progress_hook(t))
                with zipfile.ZipFile(zip_path, "r") as f:
                    f.extractall(self._dataset_path)
        else:
            print(f"Dataset found in {os.path.abspath(self._dataset_path)}, omitting download...")

    def _load(self, path_):
        with open(path_) as file:
            df = pd.read_csv(
                file,
                usecols=[0, 1, 2],
                header=None,
                sep="\t",
            )
            return torch.tensor(df.values)

    @property
    def num_entities(self) -> int:
        """Number of entities in the dataset"""
        return self._num_entities

    @property
    def num_relations(self) -> int:
        """Number of relations in the dataset"""
        return self._num_relations

    @property
    def training(self) -> torch.Tensor:
        """Set of training triples. Shape `(num_train, 3)`"""
        return self._training

    @property
    def testing(self) -> torch.Tensor:
        """Set of test triples. Shape `(num_test, 3)`"""
        return self._testing

    @property
    def validation(self) -> torch.Tensor:
        """Set of validation triples. Shape `(num_val, 3)`"""
        return self._validation

    @property
    def candidates(self) -> torch.Tensor:
        """Set of unfiltered candidates that can substitute for `?` in `(h,r,?)` and `(?,r,t)`. Shape (num_entities,)"""
        return torch.arange(self.num_entities).long()

    @property
    def stats(self) -> str:
        msg = "# Triples: ".ljust(15) + "\n"
        msg = msg + "".ljust(5) + "Train ".ljust(6) + str(self.training.size()[0]) + "\n"
        msg = msg + "".ljust(5) + "Valid ".ljust(6) + str(self.validation.size()[0]) + "\n"
        msg = msg + "".ljust(5) + "Test ".ljust(6) + str(self._testing.size()[0]) + "\n"
        msg = msg + "# Relations: ".ljust(15) + str(self.num_relations) + "\n"
        msg = msg + "# Entities: ".ljust(15) + str(self.num_entities) + "\n"
        return msg

    def filter_scores(self, batch, scores, filter_col, filter_val=float('-Inf')) -> torch.Tensor:
        """
        Filter scores by setting true scores to `filter_val`.

        For simplicity, only the head-side is described, i.e. filter_col=0. The tail-side is processed alike.
        For each (h, r, t) triple in the batch, the entity identifiers are computed such that (h', r, t) exists in all
        positive triples.

        Args:
            batch: Batch of triples. Shape `(batch_size,3)`
            scores: The scores for all corrupted triples (including the currently considered true triple). Are modified *in-place*. Shape `(batch_size,num_entities)`
            filter_col: The column along which to filter. Allowed are {0, 2}, where 0 corresponds to filtering head-based and 2
            corresponds to filtering tail-based.
            filter_val: Value to which scores of already known triples are set, default -Inf

        Returns:
            A reference to the filtered scores, which have been updated in-place.
        """
        for i in range(batch.size()[0]):
            if filter_col == 0:
                true_targets = self._dict_of_heads[batch[i, 2].item(), batch[i, 1].item()].copy()
                true_targets.remove(batch[i, 0].item())
                true_targets = torch.tensor(list(true_targets)).long()
            else:
                true_targets = self._dict_of_tails[batch[i, 0].item(), batch[i, 1].item()].copy()
                true_targets.remove(batch[i, 2].item())
                true_targets = torch.tensor(list(true_targets)).long()
            scores[i][true_targets] = filter_val
        return scores

    def get_test_batches(self, batch_size=100) -> Tuple[int, Iterable[torch.Tensor]]:
        """Splits the test set into batches of fixed size

        Args:
            batch_size: Size of a batch
        Returns:
            A tuple containing the number of batches and an iterable to the batches.
        """
        num_bat = int(np.ceil(len(self._testing) / batch_size))
        return num_bat, cast(Iterable[torch.Tensor],
                             split_list_in_batches_iter(input_list=self._testing, batch_size=batch_size))


class OBL2021Evaluator:

    def eval(self, h_pred_top10, t_pred_top10, triples, save_submission=True):
        """
        Evaluates ranked lists of head and tail entity predictions for a set of evaluation triples. By default creates a submission file.

        Args:
            h_pred_top10: Top 10 predictions for the head entity. The value at (i,j) is the ID of the predicted head entity with rank `j+1` for the triple `triples[i]`. Shape `(num_eval_triplets,10)`
            t_pred_top10: Top 10 predictions for the tail entity. The value at (i,j) is the ID of the predicted tail entity with rank `j+1` for the triple `triples[i]`. Shape `(num_eval_triplets,10)`
            triples: Set of evaluation triples. Shape `(num_eval_triplets,3)`
            save_submission: If true a submission file is created. Default: True
        """

        assert t_pred_top10.shape[1] == h_pred_top10.shape[1] == 10 and t_pred_top10.shape[0] == h_pred_top10.shape[
            0] == triples.shape[0]

        # h,r->t
        t_pred_top10 = self._to_torch(t_pred_top10)
        t_correct_index = self._to_torch(triples[:, 2])
        h_pred_top10 = self._to_torch(h_pred_top10)
        h_correct_index = self._to_torch(triples[:, 0])
        pred_top10 = torch.cat((t_pred_top10, h_pred_top10), dim=0)
        correct_index = torch.cat((t_correct_index, h_correct_index), dim=0)

        h10 = self._calculate_h10(correct_index.to(pred_top10.device), pred_top10)
        if save_submission is True:
            self._save_test_submission(pred_top10)

        print("Please copy also the following line in the respective field of the submission form:")
        print({'h10': h10})

    def _to_torch(self, container):
        if not isinstance(container, torch.Tensor):
            container = torch.from_numpy(container)
        return container

    def _calculate_mrr(self, correct_index, pred_top10):
        # extract indices where correct_index is within top10
        tmp = torch.nonzero(correct_index.view(-1, 1) == pred_top10, as_tuple=False)

        # reciprocal rank
        # if rank is larger than 10, then set the reciprocal rank to 0.
        rr = torch.zeros(len(correct_index)).to(tmp.device)
        rr[tmp[:, 0]] = 1. / (tmp[:, 1].float() + 1.)

        # mean reciprocal rank
        return float(rr.mean().item())

    def _calculate_h10(self, correct_index, pred_top10):
        # extract indices where correct_index is within top10
        total_h10 = torch.sum(torch.any(correct_index.view(-1, 1) == pred_top10, dim=1))

        return float(total_h10 / correct_index.shape[0])

    def _save_test_submission(self, pred_top10):

        #assert (pred_top10.shape == (361928, 10)), "Shape not (361928, 10) but " + str(pred_top10.shape)
        print("Shape not (361928, 10) but " + str(pred_top10.shape))

        if isinstance(pred_top10, torch.Tensor):
            pred_top10 = pred_top10.cpu().numpy()
        pred_top10 = pred_top10.astype(np.int32)

        filename = os.path.abspath('pred_OBL2021')
        np.savez_compressed(filename, pred_top10=pred_top10)
        print("Submission file saved here: " + filename + ".npz")
