import urllib.request
import zipfile

import pandas as pd
import os
from os import path
from collections import defaultdict

from tqdm import tqdm

from openbiolink.graph_creation.file_downloader.fileDownloader import FileDownloader


class Paths:
    def __init__(self,
                 path_node_mapping,
                 path_relation_mapping,
                 path_training_positive,
                 path_test_positive,
                 path_valid_positive,
                 path_training_negative,
                 path_test_negative,
                 path_valid_negative
                 ):
        self.node_mapping = path_node_mapping
        self.relation_mapping = path_relation_mapping
        self.training_positive = path_training_positive
        self.test_positive = path_test_positive
        self.valid_positive = path_valid_positive
        self.training_negative = path_training_negative
        self.test_negative = path_test_negative
        self.valid_negative = path_valid_negative


class DataLoader:

    def __init__(
            self,
            name="HQ_DIR",
            root='datasets',
            paths: Paths = None
    ):
        if not path.isdir(root):
            os.mkdir(root)
        if paths is None:
            self.dataset_path = path.join(root, name)
            # check if exists
            if not path.isdir(self.dataset_path) or not os.listdir(self.dataset_path):
                print(f"Dataset not found in, downloading to {os.path.abspath(self.dataset_path)} ...")
                url = r"https://zenodo.org/record/3834052/files/" + name +".zip"
                filename = url.split('/')[-1]
                with tqdm(unit = 'B', unit_scale = True, unit_divisor = 1024, miniters = 1, desc = filename) as t:
                    zip_path, _ = urllib.request.urlretrieve(url, reporthook = FileDownloader.download_progress_hook(t))
                    with zipfile.ZipFile(zip_path, "r") as f:
                        f.extractall(root)
            else:
                print(f"Dataset found in {os.path.abspath(self.dataset_path)}, skipping download...")


            paths = Paths(
                path_node_mapping=self.dataset_path + r"/train_test_data/node_mapping.csv",
                path_relation_mapping=self.dataset_path + r"/train_test_data/relation_mapping.csv",
                path_training_positive=self.dataset_path + r"/train_test_data/train_sample.csv",
                path_test_positive=self.dataset_path + r"/train_test_data/test_sample.csv",
                path_valid_positive=self.dataset_path + r"/train_test_data/val_sample.csv",
                path_training_negative=self.dataset_path + r"/train_test_data/negative_train_sample.csv",
                path_test_negative=self.dataset_path + r"/train_test_data/negative_test_sample.csv",
                path_valid_negative=self.dataset_path + r"/train_test_data/negative_val_sample.csv",
            )

        print("Loading dataset ...")
        self.data = {}
        self.nodes = set()
        self.relations = set()
        self.mappings = defaultdict(dict)

        # Load dataset edges
        try:
            self.data["train_positive"] = pd.read_csv(paths.training_positive, sep="\t", header=None)[[0,1,2]]
            self.data["test_positive"] = pd.read_csv(paths.test_positive, sep="\t", header=None)[[0,1,2]]
            self.data["valid_positive"] = pd.read_csv(paths.valid_positive, sep="\t", header=None)[[0,1,2]]
            if paths.training_negative:
                self.data["train_negative"] = pd.read_csv(paths.training_negative, sep="\t", header=None)[[0,1,2]]
            if paths.test_negative:
                self.data["test_negative"] = pd.read_csv(paths.test_negative, sep="\t", header=None)[[0,1,2]]
            if paths.valid_negative:
                self.data["valid_negative"] = pd.read_csv(paths.valid_negative, sep="\t", header=None)[[0,1,2]]
        except FileNotFoundError as e:
            print(e)
            exit(-1)

        # Create sets of nodes and relations
        for data in self.data.values():
            self.nodes.update(data[0].tolist())
            self.relations.update(data[1].tolist())
            self.nodes.update(data[2].tolist())

        # Creates mappings if not exist otherwise loads
        if path.exists(paths.node_mapping):
            node_mapping = pd.read_csv(paths.node_mapping, sep="\t", header=None)
            self.mappings["nodes"]["label2id"] = {label: id for label, id in zip(node_mapping[0], node_mapping[1])}
            self.mappings["nodes"]["id2label"] = {id: label for label, id in zip(node_mapping[0], node_mapping[1])}
        else:
            node_enum = enumerate(self.nodes)
            self.mappings["nodes"]["label2id"] = {label: id for id, label in node_enum}
            self.mappings["nodes"]["id2label"] = {id: label for id, label in node_enum}
            self.save_mapping(paths.node_mapping, self.mappings["nodes"])

        if path.exists(paths.relation_mapping):
            relation_mapping = pd.read_csv(paths.relation_mapping, sep="\t", header=None)
            self.mappings["relations"]["label2id"] = {label: id for label, id in zip(relation_mapping[0], relation_mapping[1])}
            self.mappings["relations"]["id2label"] = {id: label for label, id in zip(relation_mapping[0], relation_mapping[1])}
        else:
            relation_enum = enumerate(self.relations)
            self.mappings["relations"]["label2id"] = {label: id for id, label in relation_enum}
            self.mappings["relations"]["id2label"] = {id: label for id, label in relation_enum}
            self.save_mapping(paths.relation_mapping, self.mappings["relations"])

        # Map string data to integer ids
        self.map("train_positive")
        self.map("test_positive")
        self.map("valid_positive")
        if paths.training_negative:
            self.map("train_negative")
        if paths.test_negative:
            self.map("test_negative")
        if paths.valid_negative:
            self.map("valid_negative")

        self.nodes = self.map_nodes(self.nodes)
        self.relations = self.map_relations(self.relations)

        print("Done!")

    def save_mapping(self, mapping_path, mapping):
        df = pd.DataFrame(mapping["label2id"].items())
        df.to_csv(mapping_path, sep="\t", index=False, header=False)

    def map(self, ds):
        self.data[ds][0] = self.map_nodes(self.data[ds][0])
        self.data[ds][1] = self.map_relations(self.data[ds][1])
        self.data[ds][2] = self.map_nodes(self.data[ds][2])

    def map_nodes(self, nodes):
        return [self.mappings["nodes"]["label2id"][x] for x in nodes]

    def map_relations(self, relations):
        return [self.mappings["relations"]["label2id"][x] for x in relations]

    @property
    def structure(self):
        desc = "Structure of the dataloader:\n"
        desc += "nodes: integer id list of unique entities in the graph\n"
        desc += "relations: integer id list of unique entities in the graph \n"
        desc += "data['train_positive']: pd.DataFrame containing triples of the positive training set (triples are mapped to integer ids)\n"
        desc += "data['test_positive']: pd.DataFrame containing triples of the positive test set (triples are mapped to integer ids)\n"
        desc += "data['valid_positive']: pd.DataFrame containing triples of the positive validation set (triples are mapped to integer ids)\n"
        desc += "data['train_negative']: pd.DataFrame containing triples of the negative training set (triples are mapped to integer ids)\n"
        desc += "data['test_negative']: pd.DataFrame containing triples of the negative test set (triples are mapped to integer ids)\n"
        desc += "data['valid_negative']: pd.DataFrame containing triples of the negative validation set (triples are mapped to integer ids)\n"
        desc += "mappings['nodes']['label2id']: Dictionary mapping node labels to ids\n"
        desc += "mappings['nodes']['id2label']: Dictionary mapping ids to node labels\n"
        desc += "mappings['relation']['label2id']: Dictionary mapping relation labels to ids\n"
        desc += "mappings['relation']['id2label']: Dictionary mapping ids to relation labels\n"
        return desc

if __name__ == '__main__':
    dl = DataLoader("HQ_DIR")
    print(dl.structure)

    train = dl.data["train_positive"]
    test = dl.data["test_positive"]
    valid = dl.data["valid_positive"]

    neg_train = dl.data["train_negative"]
    neg_test = dl.data["test_negative"]
    neg_valid = dl.data["valid_negative"]
