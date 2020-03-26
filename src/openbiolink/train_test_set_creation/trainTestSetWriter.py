import logging
import os

import pandas
import shutil

import openbiolink.train_test_set_creation.ttsConfig as ttsConst
from openbiolink import globalConfig as globConst


class TrainTestSetWriter:
    def __init__(self, identifier2type):
        self.folder_path = os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME)
        self.identifier2type = identifier2type
        if os.path.isdir(self.folder_path):
            os.rename(self.folder_path, self.folder_path + "_del")
            shutil.rmtree(self.folder_path + "_del")
        os.makedirs(self.folder_path, exist_ok=True)

    def get_fold_path(self, fold_i):
        return os.path.join(self.folder_path, ttsConst.FOLD_FOLDER_PREFIX + str(fold_i))

    """
    def write_train_test_set(self, train_set, train_nodes, test_set, test_nodes, new_test_nodes):
        self.write_set(test_set, ttsConst.TEST_FILE_NAME)
        self.write_nodes(set(test_nodes), ttsConst.TEST_NODES_FILE_NAME)
        self.write_new_nodes(new_test_nodes, ttsConst.NEW_TEST_NODES_FILE_NAME)
        self.write_set(train_set, ttsConst.TRAIN_FILE_NAME)
        self.write_nodes(set(train_nodes), ttsConst.TRAIN_VAL_NODES_FILE_NAME)

    def write_train_val_set(self, train_set, val_set, new_val_nodes, fold_i):
        fold_folder_path = self.get_fold_path(fold_i)
        os.makedirs(fold_folder_path, exist_ok=True)
        self.write_set(train_set, ttsConst.TRAIN_FILE_NAME, fold_folder_path)
        self.write_set(val_set, ttsConst.VAL_FILE_NAME, fold_folder_path)
        self.write_new_nodes(new_val_nodes, ttsConst.NEW_VAL_NODES_FILE_NAME, fold_folder_path)
    """

    def write_set(self, samples, filename, path=None):
        logging.info(f"Writing {filename} ...")
        if path is None:
            path = self.folder_path
        samples[globConst.COL_NAMES_SAMPLES].to_csv(
            os.path.join(path, filename), sep="\t", index=False, header=False
        )

    def write_nodes(self, nodes, filename, path=None):
        logging.info(f"Writing {filename} ...")
        if path is None:
            path = self.folder_path
        train_val_nodes_df = pandas.DataFrame({"id": list(nodes)})
        train_val_nodes_df["nodeType"] = [self.identifier2type[x[0]] for x in
                                          train_val_nodes_df["id"].str.split(":")]
        train_val_nodes_df.to_csv(
            os.path.join(path, filename), sep="\t", index=False, header=False
        )

    def write_new_nodes(self, nodes, filename, path=None):
        logging.info(f"Writing {filename} ...")
        if path is None:
            path = self.folder_path
        with open(os.path.join(path, filename), "w", newline="\n") as file:
            file.writelines(list("\n".join(nodes)))

    def print_vanished_edges(self, vanished_edges):
        self.folder_path = os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME)
        vanished_edges.to_csv(
            os.path.join(self.folder_path, ttsConst.VANISHED_FILE_NAME), sep="\t", index=False, header=False
        )
