import os
import pickle
import urllib
import zipfile
from collections import defaultdict
from os import path
from typing import cast, Iterable

import numpy as np
import pandas as pd
import torch
from openbiolink.utils import split_list_in_batches_iter
from tqdm import tqdm

from openbiolink.graph_creation.file_downloader import FileDownloader


class DataLoader(object):
    """
    :param root:
        Pathlike string to directory in which dataset files should be stored
    """

    def __init__(self, root: str = 'dataset', name: str = "HQ_DIR", entity_to_id_path=None, relation_to_id_path=None):
        self._root = root
        self._dataset_path = path.join(root, name)
        self._relative_training_path = f'train_test_data/train_sample.csv'
        self._relative_testing_path = f'train_test_data/test_sample.csv'
        self._relative_validation_path = f'train_test_data/val_sample.csv'
        self._url = f"https://zenodo.org/record/3834052/files/{name}.zip"

        self._download()

        self._entity_label_to_id = None
        self._id_to_entity_label = None
        self._relation_label_to_id = None
        self._id_to_relation_label = None

        if entity_to_id_path:
            node_mapping = pd.read_csv(entity_to_id_path, sep="\t", header=None)
            self._entity_label_to_id = {label: id for label, id in
                                        zip(node_mapping[1], node_mapping[0])}
            self._id_to_entity_label = {
                id: label
                for label, id in self._entity_label_to_id.items()
            }

        if relation_to_id_path:
            relation_mapping = pd.read_csv(relation_to_id_path, sep="\t", header=None)
            self._relation_label_to_id = {label: id for label, id in
                                          zip(relation_mapping[1],
                                              relation_mapping[0])}
            self._id_to_relation_label = {
                id: label
                for label, id in self._relation_label_to_id.items()
            }

        self._training = self._load(self._relative_training_path,
                                    True if (relation_to_id_path is None and entity_to_id_path is None) else False)
        self._validation = self._load(self._relative_validation_path)
        self._testing = self._load(self._relative_testing_path)

        self._num_entities = len(self._entity_label_to_id)
        self._num_relations = len(self._relation_label_to_id)

        self._dict_of_heads = defaultdict(set)
        self._dict_of_tails = defaultdict(set)
        self._generate_dicts()

    def _download(self):
        if not path.isdir(self._root):
            os.mkdir(self._root)

        # check if exists
        if not path.isdir(self._dataset_path) or not os.listdir(self._dataset_path):
            print(
                f"Dataset not found in {os.path.abspath(self._dataset_path)}, downloading to {os.path.abspath(self._dataset_path)} ...")
            url = self._url
            filename = url.split('/')[-1]
            with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=filename) as t:
                zip_path, _ = urllib.request.urlretrieve(url, reporthook=FileDownloader.download_progress_hook(t))
                with zipfile.ZipFile(zip_path, "r") as f:
                    f.extractall(self._root)
        else:
            print(f"Dataset found in {os.path.abspath(self._dataset_path)}, skipping download...")

    def _load(self, path_, create_index=False):
        with open(path.join(self._dataset_path, path_)) as file:
            df = pd.read_csv(
                file,
                usecols=[0, 1, 2],
                header=None,
                sep="\t",
            )

            if create_index:
                self._create_mapping(df.values)
            return self._map_triples(df.values)

    def _create_mapping(self, triples):
        # Split triples
        heads, relations, tails = triples[:, 0], triples[:, 1], triples[:, 2]
        # Sorting ensures consistent results when the triples are permuted
        entity_labels = sorted(set(heads).union(tails))
        relation_labels = sorted(set(relations))
        # Create mapping
        self._entity_label_to_id = {
            str(label): i
            for (i, label) in enumerate(entity_labels)
        }
        self._id_to_entity_label = {
            id: label
            for label, id in self._entity_label_to_id.items()
        }
        self._relation_label_to_id = {
            str(label): i
            for (i, label) in enumerate(relation_labels)
        }
        self._id_to_relation_label = {
            id: label
            for label, id in self._relation_label_to_id.items()
        }

    def _map_triples(self, triples):
        # When triples that don't exist are trying to be mapped, they get the id "-1"
        entity_getter = np.vectorize(self._entity_label_to_id.get)
        head_column = entity_getter(triples[:, 0:1], [-1])
        tail_column = entity_getter(triples[:, 2:3], [-1])
        relation_getter = np.vectorize(self._relation_label_to_id.get)
        relation_column = relation_getter(triples[:, 1:2], [-1])

        # Filter all non-existent triples
        head_filter = head_column < 0
        relation_filter = relation_column < 0
        tail_filter = tail_column < 0
        non_mappable_triples = (head_filter | relation_filter | tail_filter)
        head_column = head_column[~non_mappable_triples, None]
        relation_column = relation_column[~non_mappable_triples, None]
        tail_column = tail_column[~non_mappable_triples, None]

        triples_of_ids = np.concatenate([head_column, relation_column, tail_column], axis=1)
        return torch.tensor(triples_of_ids, dtype=torch.long)

    def _generate_dicts(self):
        _all = torch.cat((self._training, self._validation, self._testing), 0)

        for i in tqdm(range(_all.size()[0])):
            self._dict_of_heads[(_all[i, 2].item(),
                                 _all[i, 1].item())].add(_all[i, 0].item())
            self._dict_of_tails[(_all[i, 0].item(),
                                 _all[i, 1].item())].add(_all[i, 2].item())

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
    def stats(self):
        msg = "# Triples: ".ljust(15) + "\n"
        msg = msg + "".ljust(5) + "Train ".ljust(6) + str(self.training.size()[0]) + "\n"
        msg = msg + "".ljust(5) + "Valid ".ljust(6) + str(self.validation.size()[0]) + "\n"
        msg = msg + "".ljust(5) + "Test ".ljust(6) + str(self._testing.size()[0]) + "\n"
        msg = msg + "# Relations: ".ljust(15) + str(self.num_relations) + "\n"
        msg = msg + "# Entities: ".ljust(15) + str(self.num_entities) + "\n"
        return msg

    def filter_scores(self, batch, scores, filter_col, filter_val=float('nan')):
        """
        Filters true positive .

        :param batch:
            Batch of triples. Shape `(batch_size,3)`
        :param scores:
            Batch of triples. Shape `(batch_size,num_entities)`
        :param filter_col:
            Batch of triples. Shape `(batch_size,num_entities)`
        :param filter_val:
            Batch of triples. Shape `(batch_size,num_entities)`, default NaN

        :return:
            filtered_scores: `torch.tensor` where the value at [i,j] is the score of the triple `(j, batch[i][1], batch[i][2])`. Shape `(batch_size, num_entities)`
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

    def get_test_batches(self, batch_size=100) -> (int, Iterable[torch.Tensor]):
        """Splits the test set into batches of fixed size
            :param batch_size:
                Size of a batch
            :return:
                number of batches, iterable of batches
        """
        num_bat = int(np.ceil(len(self._testing) / batch_size))
        return num_bat, cast(Iterable[torch.Tensor],
                             split_list_in_batches_iter(input_list=self._testing, batch_size=batch_size))

    def save_as_kgid(self, path='dataset', sep='\t'):
        pd.DataFrame(self._training.numpy()).to_csv(os.path.join(path, 'train.tsv'), sep=sep, header=False, index=False)
        pd.DataFrame(self._testing.numpy()).to_csv(os.path.join(path, 'test.tsv'), sep=sep, header=False, index=False)
        pd.DataFrame(self._validation.numpy()).to_csv(os.path.join(path, 'valid.tsv'), sep=sep, header=False,
                                                      index=False)
        pd.DataFrame.from_dict(data=self._id_to_entity_label, orient='index').to_csv(path, 'entities.tsv', sep=sep,
                                                                                     header=False)
        pd.DataFrame.from_dict(data=self._id_to_relation_label, orient='index').to_csv(path, 'relations.tsv', sep=sep,
                                                                                       header=False)
        with open(os.path.join(path, '_dict_of_heads.pkl'), 'wb') as f:
            pickle.dump(self._dict_of_heads, f, pickle.HIGHEST_PROTOCOL)
        with open(os.path.join(path, '_dict_of_tails.pkl'), 'wb') as f:
            pickle.dump(self._dict_of_tails, f, pickle.HIGHEST_PROTOCOL)
