import logging
import os
import urllib
from itertools import chain
from os import path
import zipfile
from typing import Optional, cast, Iterable, Tuple

from pykeen.evaluation.evaluator import create_sparse_positive_filter_, filter_scores_
from pykeen.utils import split_list_in_batches_iter
from tqdm import tqdm

import torch
import pandas as pd
import numpy as np
from pykeen.datasets.base import LazyDataset
from pykeen.triples import TriplesFactory

from openbiolink.graph_creation.file_downloader import FileDownloader


class DataLoader(LazyDataset):
    """Downloads and creates mappings for the OpenBioLink dataset. If mapping files are already 
    
        :param name:
            Version of the OpenBioLink dataset to load, possible values HQ_DIR, HQ_UNDIR, ALL_DIR, ALL_UNDIR
        :param root:
            Dictionary used to store the downloaded dataset
        :param entity_to_id_path:
            Path to an external dictionary file mapping entities to IDs. If none specified, a mapping is created.
        :param relation_to_id_path:
            Path to an external dictionary file mapping relation to IDs. If none specified, a mapping is created.
        :param entity_to_id_sep:
            Seperator used in the entity dictionary file (only required if entity_to_id_path is given)
        :param entity_to_id_id_col:
            Column index of the integer identifiers in the entity dictionary file (only required if entity_to_id_path is given)
        :param entity_to_id_label_col:
            Column index of the labels in the entity dictionary file (only required if entity_to_id_path is given)
        :param relation_to_id_sep:
            Seperator used in the relation dictionary file (only required if relation_to_id_path is given)
        :param relation_to_id_id_col:
            Column index of the integer identifiers in the relation dictionary file (only required if relation_to_id_path is given)
        :param relation_to_id_label_col:
            Column index of the labels in the relation dictionary file (only required if relation_to_id_path is given)
    
    """

    head_column: int = 0
    relation_column: int = 1
    tail_column: int = 2
    sep = '\t'
    header = None

    relative_training_path = f'train_test_data/train_sample.csv'
    relative_testing_path = f'train_test_data/test_sample.csv'
    relative_validation_path = f'train_test_data/val_sample.csv'

    def __init__(
            self,
            name: str = "HQ_DIR",
            root: str = "datasets",
            eager: bool = False,
            entity_to_id_path: Optional[str] = None,
            relation_to_id_path: Optional[str] = None,
            entity_to_id_sep: str = "\t",
            entity_to_id_id_col: int = 0,
            entity_to_id_label_col: int = 1,
            relation_to_id_sep: str = "\t",
            relation_to_id_id_col: int = 0,
            relation_to_id_label_col: int = 1
    ):

        self.root = root
        self.dataset_path = path.join(root, name)
        self.url = r"https://zenodo.org/record/3834052/files/" + name + ".zip"
        self.name=f'{name}.zip'

        self.entity_to_id_path = entity_to_id_path
        self.relation_to_id_path = relation_to_id_path

        self.entity_to_id_sep = entity_to_id_sep
        self.entity_to_id_id_col = entity_to_id_id_col
        self.entity_to_id_label_col = entity_to_id_label_col
        self.relation_to_id_sep = relation_to_id_sep
        self.relation_to_id_id_col = relation_to_id_id_col
        self.relation_to_id_label_col = relation_to_id_label_col

        if not path.isdir(root):
            os.mkdir(root)

        # check if exists
        if not path.isdir(self.dataset_path) or not os.listdir(self.dataset_path):
            print(f"Dataset not found in, downloading to {os.path.abspath(self.dataset_path)} ...")
            url = r"https://zenodo.org/record/3834052/files/" + name + ".zip"
            filename = url.split('/')[-1]
            with tqdm(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=filename) as t:
                zip_path, _ = urllib.request.urlretrieve(url, reporthook=FileDownloader.download_progress_hook(t))
                with zipfile.ZipFile(zip_path, "r") as f:
                    f.extractall(root)
        else:
            print(f"Dataset found in {os.path.abspath(self.dataset_path)}, skipping download...")

        if eager:
            self._load()
            self._load_validation()

        self.all = torch.cat((self.training.mapped_triples, self.testing.mapped_triples, self.validation.mapped_triples), 0)
        self.all.share_memory_()


    def _load(self) -> None:  # noqa: D102
        self._training = self._load_helper(self.relative_training_path)
        self._testing = self._load_helper(self.relative_testing_path)

    def _load_validation(self) -> None:
        self._validation = self._load_helper(self.relative_validation_path)

    def _load_helper(self, relative_path) -> TriplesFactory:
        relative_path = path.join(self.dataset_path,relative_path)

        with open(relative_path) as file:
            df = pd.read_csv(
                file,
                usecols=[self.head_column, self.relation_column, self.tail_column],
                header=self.header,
                sep=self.sep,
            )

            entity_to_id = None
            relation_to_id = None

            if self.entity_to_id_path:
                node_mapping = pd.read_csv(self.entity_to_id_path, sep=self.entity_to_id_sep, header=None)
                entity_to_id = {label: id for label, id in
                                                      zip(node_mapping[self.entity_to_id_label_col], node_mapping[self.entity_to_id_id_col])}

            if self.relation_to_id_path:
                relation_mapping = pd.read_csv(self.relation_to_id_path, sep=self.relation_to_id_sep, header=None)
                relation_to_id = {label: id for label, id in
                                                          zip(relation_mapping[self.relation_to_id_label_col], relation_mapping[self.relation_to_id_id_col])}

            rv = TriplesFactory.from_labeled_triples(
                triples=df.values,
                entity_to_id=entity_to_id,
                relation_to_id=relation_to_id
            )

            rv.path = relative_path
            return rv

    def get_test_batches(self, batch_size = 100):
        """Splits the test set into batches of fixed size

            :param batch_size:
                Size of a batch

            :return:
                number of batches, iterable of batches
        """
        return int(np.ceil(len(self.testing.mapped_triples) / batch_size)), cast(Iterable[np.ndarray], split_list_in_batches_iter(input_list=self.testing.mapped_triples, batch_size=batch_size))



if __name__ == '__main__':



    dl = DataLoader("HQ_DIR")
    print(len(dl.all))
