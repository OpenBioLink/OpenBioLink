import os
import numpy as np
import openbiolink.evaluation.evalConfig as evalConst
import openbiolink.evaluation.evaluationIO as io
from openbiolink import globalConfig as globConst
import openbiolink.evaluation.embedded.utils as utils


class Mapping:

    def __init__(self):
        self.node_label_to_id = None
        self.node_types_to_id = None
        self.relation_label_to_id = None

    def create_mapping(self, training_examples, test_examples, nodes):
        relation_labels = set()
        relation_labels.update(set(test_examples[globConst.EDGE_TYPE_COL_NAME]))
        relation_labels.update(set(training_examples[globConst.EDGE_TYPE_COL_NAME]))

        self.relation_label_to_id = utils.create_mappings(relation_labels)
        if nodes is not None:
            self.node_label_to_id = utils.create_mappings(np.unique(nodes.values[:, 0]))
            self.node_types_to_id = utils.create_mappings(np.unique(nodes.values[:, 1]))
        else:
            node_labels = set()
            node_labels.update(set(test_examples[globConst.NODE1_ID_COL_NAME]))
            node_labels.update(set(test_examples[globConst.NODE2_ID_COL_NAME]))
            node_labels.update(set(training_examples[globConst.NODE1_ID_COL_NAME]))
            node_labels.update(set(training_examples[globConst.NODE2_ID_COL_NAME]))
            self.node_label_to_id = utils.create_mappings(node_labels)

        # output mappings
        io.write_mappings(
            node_label_to_id=self.node_label_to_id,
            node_types_to_id=self.node_types_to_id,
            relation_label_to_id=self.relation_label_to_id,
        )

    def read_mapping(self):
        output_directory = os.path.join(
            os.path.join(globConst.WORKING_DIR, evalConst.EVAL_OUTPUT_FOLDER_NAME), evalConst.MODEL_DIR
        )
        self.node_label_to_id = io.read_mapping(
            os.path.join(output_directory, evalConst.MODEL_ENTITY_NAME_MAPPING_NAME)
        )
        node_type_path = os.path.join(output_directory, evalConst.MODEL_ENTITY_TYPE_MAPPING_NAME)
        self.node_types_to_id = io.read_mapping(node_type_path)
        self.relation_label_to_id = io.read_mapping(
            os.path.join(output_directory, evalConst.MODEL_RELATION_TYPE_MAPPING_NAME)
        )

    def get_mapped_triples_and_nodes(self, triples=None, nodes=None):
        mapped_triples = None
        mapped_nodes = None
        if nodes is not None:
            mapped_nodes = np.column_stack(
                (
                    utils.map_elements(nodes[:, 0:1], self.node_label_to_id),
                    utils.map_elements(nodes[:, 1:2], self.node_types_to_id),
                )
            )
        if triples is not None:
            mapped_triples = np.column_stack(
                (
                    utils.map_elements(triples[:, 0:1], self.node_label_to_id),
                    utils.map_elements(triples[:, 1:2], self.relation_label_to_id),
                    utils.map_elements(triples[:, 2:3], self.node_label_to_id),
                )
            )
        return mapped_triples, mapped_nodes
