import os
import openbiolink.evaluation.evalConfig as evalConst
from openbiolink import globalConfig as globConst
from openbiolink.evaluation.embedded.models.model import Model
import openbiolink.evaluation.embedded.utils as utils
from openbiolink.evaluation.dataset import Dataset


class EmbeddedTraining:
    def __init__(self, model: Model, dataset: Dataset):
        self.model = model
        self.dataset = dataset

    def train(self):
        # prepare input examples
        pos_examples = self.dataset.training_examples[self.dataset.training_examples[globConst.VALUE_COL_NAME] == 1]
        neg_examples = self.dataset.training_examples[self.dataset.training_examples[globConst.VALUE_COL_NAME] == 0]
        # pos and neg must be same length! but also, all entities must still be present!
        num_examples = min(len(neg_examples), len(pos_examples))
        pos_examples = utils.save_remove_n_edges(pos_examples, len(pos_examples) - num_examples)
        neg_examples = utils.save_remove_n_edges(neg_examples, len(neg_examples) - num_examples)
        pos_triples = pos_examples[globConst.COL_NAMES_TRIPLES].values
        neg_triples = neg_examples[globConst.COL_NAMES_TRIPLES].values
        mapped_pos_triples, _ = self.dataset.mapping.get_mapped_triples_and_nodes(triples=pos_triples)
        mapped_neg_triples, _ = self.dataset.mapping.get_mapped_triples_and_nodes(triples=neg_triples)

        self.model.train(pos_triples=mapped_pos_triples, neg_triples=mapped_neg_triples)
        output_directory = os.path.join(
            os.path.join(globConst.WORKING_DIR, evalConst.EVAL_OUTPUT_FOLDER_NAME), evalConst.MODEL_DIR
        )

        os.makedirs(output_directory, exist_ok=True)
        model_path = os.path.join(output_directory, evalConst.MODEL_TRAINED_NAME)
        self.model.output_model(model_path)
