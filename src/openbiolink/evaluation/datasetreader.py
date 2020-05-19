import pandas as pd
from openbiolink import globalConfig as globConst
from openbiolink.evaluation.embedded.mapping import Mapping
from openbiolink import globalConfig as globConf
import openbiolink.evaluation.evalConfig as evalConf
import os


class Reader:
    def __init__(self,
                 training_set_path=None,
                 negative_training_set_path=None,
                 test_set_path=None,
                 negative_test_set_path=None,
                 valid_set_path=None,
                 negative_valid_set_path=None,
                 nodes_path=None,
                 mappings_avail=False,
                 write_triples=False
                 ):
        # read positive and negative trainingset
        if training_set_path:
            self.training_examples = pd.read_csv(training_set_path, sep="\t", names=globConst.COL_NAMES_SAMPLES)
        else:
            self.training_examples = pd.DataFrame(columns=globConst.COL_NAMES_SAMPLES)
        if negative_training_set_path:
            negative_training_samples = pd.read_csv(negative_training_set_path, sep="\t",
                                                    names=globConst.COL_NAMES_SAMPLES)
            self.training_examples = self.training_examples.append(negative_training_samples, ignore_index=True)

        # read positive and negative test set
        if test_set_path:
            self.test_examples = pd.read_csv(test_set_path, sep="\t", names=globConst.COL_NAMES_SAMPLES)
        else:
            self.test_examples = pd.DataFrame(columns=globConst.COL_NAMES_SAMPLES)
        if negative_test_set_path:
            negative_test_samples = pd.read_csv(negative_test_set_path, sep="\t", names=globConst.COL_NAMES_SAMPLES)
            self.test_examples = self.test_examples.append(negative_test_samples, ignore_index=True)

        # read positive and negative validation set
        if valid_set_path:
            self.validation_examples = pd.read_csv(valid_set_path, sep="\t", names=globConst.COL_NAMES_SAMPLES)
        else:
            self.validation_examples = pd.DataFrame(columns=globConst.COL_NAMES_SAMPLES)
        if negative_valid_set_path:
            negative_valid_samples = pd.read_csv(negative_valid_set_path, sep="\t", names=globConst.COL_NAMES_SAMPLES)
            self.validation_examples = self.test_examples.append(negative_valid_samples, ignore_index=True)

        # read all nodes
        if nodes_path is not None:
            self.nodes = pd.read_csv(nodes_path, sep="\t", names=globConst.COL_NAMES_NODES)

            # fix for obl 2020
            if len(self.training_examples) > 0:
                sample_nodes = set(self.training_examples[globConst.NODE1_ID_COL_NAME].tolist() +
                                   self.training_examples[globConst.NODE2_ID_COL_NAME].tolist())
                self.nodes = self.nodes[self.nodes[globConst.ID_NODE_COL_NAME].isin(sample_nodes)]
        else:
            self.nodes = None

        if mappings_avail:
            self.mapping = Mapping().read_mapping()
        else:
            self.mapping = Mapping().create_mapping(self.training_examples, self.test_examples, self.nodes)

        if write_triples:
            self.write_triples()

    def get_mapped_triples_and_nodes(self, triples=None, nodes=None):
        if self.mapping is None:
            raise Exception("Mapping is None, create or read mapping first")
        else:
            return self.mapping.get_mapped_triples_and_nodes(self, triples, nodes)

    def get_train_triples(self):
        return self.training_examples[globConf.COL_NAMES_TRIPLES]

    def get_test_triples(self):
        return self.test_examples[globConf.COL_NAMES_TRIPLES]

    def get_validation_triples(self):
        return self.validation_examples[globConf.COL_NAMES_TRIPLES]

    def write_triples(self):
        evaluation_path = os.path.join(globConf.WORKING_DIR, evalConf.EVAL_OUTPUT_FOLDER_NAME)
        self.training_examples[globConf.COL_NAMES_TRIPLES].get_train_triples().to_csv(
            os.path.join(evaluation_path, "dataset", "train.txt"),
            sep="\t",
            index=False,
            header=False
        )
        self.test_examples[globConf.COL_NAMES_TRIPLES].get_test_triples().to_csv(
            os.path.join(evaluation_path, "dataset", "test.txt"),
            sep="\t",
            index=False,
            header=False
        )
        self.validation_examples[globConf.COL_NAMES_TRIPLES].get_validation_triples().to_csv(
            os.path.join(evaluation_path, "dataset", "valid.txt"),
            sep="\t",
            index=False,
            header=False)
