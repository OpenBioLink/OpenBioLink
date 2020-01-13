import json
import os
import pickle

import numpy as np
import pykeen.constants as keenConst
import pykeen.utilities.pipeline as pipeline
import torch
import torch.optim as optim
from tqdm import tqdm

import openbiolink.evaluation.evalConfig as evalConst
import openbiolink.train_test_set_creation.ttsConfig as ttsConst
from openbiolink import globalConfig as globConst
from openbiolink.evaluation.models.model import Model


## ** code adapted from pykeen: https://github.com/SmartDataAnalytics/PyKEEN **


class PyKeen_BasicModel(Model):
    def __init__(self, config=None):
        super().__init__()
        if type(config) == str:
            with open(config) as file:
                content = file.read()
                self.config = json.loads(content)
        else:
            self.config = config
        self.device = torch.device('cpu')

        self.config[keenConst.NUM_ENTITIES] = None
        self.config[keenConst.NUM_RELATIONS] = None

        self.kge_model = None

    @staticmethod
    def load_model(config):  # todo
        if type(config) == str:
            with open(config) as file:
                content = file.read()
                model_dir = os.path.abspath(os.path.join(config, os.pardir))
        else:
            model_dir = None
        with open(os.path.join(model_dir, 'configuration.json')) as f:
            config = json.load(f)

        kge_model = pipeline.get_kge_model(config=config)

        if model_dir is not None:
            path_to_model = os.path.join(model_dir, 'trained_model.pkl')
            kge_model.load_state_dict(torch.load(path_to_model))
        return kge_model

    def train(self, pos_triples: np.array, neg_triples: np.array):

        all_triples = np.concatenate((pos_triples, neg_triples))

        # testme
        self.config[keenConst.NUM_ENTITIES] = len(np.unique(np.concatenate((all_triples[:, 0], all_triples[:, 2]))))
        self.config[keenConst.NUM_RELATIONS] = len(np.unique(all_triples[:, 1]))

        ## prepare model
        self.kge_model = pipeline.get_kge_model(config=self.config)
        self.kge_model = self.kge_model.to(self.device)

        optimizer = optim.SGD(self.kge_model.parameters(), lr=self.config[keenConst.LEARNING_RATE])
        loss_per_epoch = []
        num_pos_examples = pos_triples.shape[0]
        num_neg_examples = neg_triples.shape[0]

        ### train model
        for _ in tqdm(range(self.config[keenConst.NUM_EPOCHS])):
            # create batches
            indices_pos = np.arange(num_pos_examples)
            np.random.shuffle(indices_pos)
            pos_triples = pos_triples[indices_pos]
            pos_batches = self._split_list_in_batches(input_list=pos_triples,
                                                      batch_size=self.config["batch_size"])
            indices_neg = np.arange(num_neg_examples)
            np.random.shuffle(indices_neg)
            neg_triples = neg_triples[indices_neg]
            neg_batches = self._split_list_in_batches(input_list=neg_triples,
                                                      batch_size=self.config["batch_size"])
            current_epoch_loss = 0.

            for pos_batch, neg_batch in tqdm(zip(pos_batches, neg_batches), total=len(neg_batches)):
                current_batch_size = len(pos_batch)

                # if not len(pos_batch) == len(neg_batch):
                #    raise RuntimeError('Pos and neg batches are not the same length')

                pos_batch_tensor = torch.tensor(pos_batch, dtype=torch.long, device=self.device)
                neg_batch_tensor = torch.tensor(neg_batch, dtype=torch.long, device=self.device)
                # Recall that torch *accumulates* gradients. Before passing in a
                # new instance, you need to zero out the gradients from the old instance
                optimizer.zero_grad()
                loss = self.kge_model(pos_batch_tensor, neg_batch_tensor)
                current_epoch_loss += (loss.item() * current_batch_size)

                loss.backward()
                optimizer.step()

            loss_per_epoch.append(current_epoch_loss / len(pos_triples))

        ### prepare results for output
        entity_to_embedding = {
            id: embedding.detach().cpu().numpy()
            for id, embedding in enumerate(self.kge_model.entity_embeddings.weight)
        }
        relation_to_embedding = {
            id: embedding.detach().cpu().numpy()
            for id, embedding in enumerate(self.kge_model.relation_embeddings.weight)
        }

        results = {
            "trained_model": self.kge_model,
            "loss_per_epoch": loss_per_epoch,
            "entity_to_embedding": entity_to_embedding,
            "relation_to_embedding": relation_to_embedding,
            "config": self.config
        }
        self.output_results(results)

        return self.kge_model

    def get_ranked_and_sorted_predictions(self, mapped_test_triples):
        # ** original code can be found in utilities/prediction_utils.py

        mapped_test_triples = torch.tensor(mapped_test_triples, dtype=torch.long, device=self.device)
        borders = []
        i = 0
        while True:  # todo #fixme explore further size limitations
            borders.append(min(i * 1000, len(mapped_test_triples)))
            if i * 1000 > len(mapped_test_triples):
                break
            i += 1
        predicted_scores = []
        [predicted_scores.extend(self.kge_model.predict(mapped_test_triples[borders[i - 1]:borders[i]])) for i, _ in
         enumerate(borders) if i > 0]  # todo maybe here a loop and batches?
        predicted_scores = np.array(predicted_scores)
        _, sorted_indices = torch.sort(torch.tensor(predicted_scores, dtype=torch.float),
                                       descending=False)

        sorted_indices = sorted_indices.cpu().numpy()
        ranked_test_triples = mapped_test_triples[sorted_indices, :]
        ranked_test_triples = np.array(ranked_test_triples)
        ranked_scores = np.reshape(predicted_scores[sorted_indices], newshape=(-1, 1))
        ranked_test_triples = np.column_stack((ranked_test_triples, ranked_scores))

        # ranked_triples = np.concatenate([ranked_subject_column,ranked_predicate_column, ranked_object_column , ranked_scores], axis=1)
        # ranked_triples = pandas.DataFrame({globConst.NODE1_ID_COL_NAME:[x for sublist in ranked_subject_column.tolist() for x in sublist],
        #                                   globConst.EDGE_TYPE_COL_NAME: [x for sublist in ranked_predicate_column.tolist() for x in sublist],
        #                                   globConst.NODE2_ID_COL_NAME:[x for sublist in ranked_object_column.tolist() for x in sublist],
        #                                   globConst.SCORE_COL_NAME : [x for sublist in ranked_scores.tolist() for x in sublist]})
        return ranked_test_triples, sorted_indices

    def output_results(self, results):
        output_directory = os.path.join(os.path.join(globConst.WORKING_DIR, evalConst.EVAL_OUTPUT_FOLDER_NAME),
                                        evalConst.MODEL_DIR)

        with open(os.path.join(output_directory, 'configuration.json'), 'w') as file:
            json.dump(results["config"], file, indent=2)

        with open(os.path.join(output_directory, 'entities_to_embeddings.pkl'), 'wb') as file:
            pickle.dump(results['entity_to_embedding'], file, protocol=pickle.HIGHEST_PROTOCOL)

        with open(os.path.join(output_directory, 'entities_to_embeddings.json'), 'w') as file:
            json.dump(
                {
                    key: list(map(float, array))
                    for key, array in results['entity_to_embedding'].items()
                },
                file,
                indent=2,
                sort_keys=True
            )

        if results[keenConst.RELATION_TO_EMBEDDING] is not None:
            with open(os.path.join(output_directory, 'relations_to_embeddings.pkl'), 'wb') as file:
                pickle.dump(results["relation_to_embedding"], file, protocol=pickle.HIGHEST_PROTOCOL)

            with open(os.path.join(output_directory, 'relations_to_embeddings.json'), 'w') as file:
                json.dump(
                    {
                        key: list(map(float, array))
                        for key, array in results["relation_to_embedding"].items()
                    },
                    file,
                    indent=2,
                    sort_keys=True,
                )

        with open(os.path.join(output_directory, 'losses.json'), 'w') as file:
            json.dump(results['loss_per_epoch'], file, indent=2, sort_keys=True)

    def output_model(self, path):
        torch.save(
            self.kge_model.state_dict(),
            path,
        )


class TransE_PyKeen(PyKeen_BasicModel):

    def __init__(self, config=None):
        if not config:
            self.config = dict(
                training_set_path=os.path.join(os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME),
                                               ttsConst.TRAIN_FILE_NAME),
                test_set_path=os.path.join(os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME),
                                           ttsConst.TEST_FILE_NAME),
                execution_mode="Training_mode",
                random_seed=42,
                kg_embedding_model_name="TransE",
                embedding_dim=5,
                margin_loss=1,
                learning_rate=0.01,
                scoring_function=1,
                normalization_of_entities=2,
                num_epochs=1,
                batch_size=256,
                preferred_device="cpu"
            )
        else:
            self.config = config
        super().__init__(self.config)


class TransR_PyKeen(PyKeen_BasicModel):

    def __init__(self, config=None):

        if not config:
            self.config = dict(
                training_set_path=os.path.join(os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME),
                                               ttsConst.TRAIN_FILE_NAME),
                test_set_path=os.path.join(os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME),
                                           ttsConst.TEST_FILE_NAME),
                execution_mode="Training_mode",
                random_seed=42,
                kg_embedding_model_name="TransR",
                embedding_dim=5,
                relation_embedding_dim=5,
                margin_loss=1,
                learning_rate=0.01,
                scoring_function=1,
                normalization_of_entities=2,
                num_epochs=1,
                batch_size=256,
                preferred_device="cpu"
            )
        else:
            self.config = config
        super().__init__(self.config)


class TransD_PyKeen(PyKeen_BasicModel):

    def __init__(self, config=None):

        if not config:
            self.config = dict(
                training_set_path=os.path.join(os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME),
                                               ttsConst.TRAIN_FILE_NAME),
                test_set_path=os.path.join(os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME),
                                           ttsConst.TEST_FILE_NAME),
                execution_mode="Training_mode",
                random_seed=42,
                kg_embedding_model_name="TransD",
                embedding_dim=5,
                relation_embedding_dim=5,
                margin_loss=1,
                learning_rate=0.01,
                scoring_function=1,
                normalization_of_entities=2,
                num_epochs=1,
                batch_size=256,
                preferred_device="cpu"
            )
        else:
            self.config = config
        super().__init__(self.config)


class TransH_PyKeen(PyKeen_BasicModel):

    def __init__(self, config=None):

        if not config:
            self.config = dict(
                training_set_path=os.path.join(os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME),
                                               ttsConst.TRAIN_FILE_NAME),
                test_set_path=os.path.join(os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME),
                                           ttsConst.TEST_FILE_NAME),
                execution_mode="Training_mode",
                random_seed=42,
                kg_embedding_model_name="TransH",
                embedding_dim=5,
                margin_loss=1,
                learning_rate=0.01,
                scoring_function=1,
                soft_constraints_weight=0.015625,
                normalization_of_entities=2,
                num_epochs=1,
                batch_size=256,
                preferred_device="cpu"
            )
        else:
            self.config = config
        super().__init__(self.config)


class DistMult_PyKeen(PyKeen_BasicModel):

    def __init__(self, config=None):

        if not config:
            self.config = dict(
                training_set_path=os.path.join(os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME),
                                               ttsConst.TRAIN_FILE_NAME),
                test_set_path=os.path.join(os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME),
                                           ttsConst.TEST_FILE_NAME),
                execution_mode="Training_mode",
                random_seed=42,
                kg_embedding_model_name="DistMult",
                embedding_dim=5,
                relation_embedding_dim=5,
                margin_loss=1,
                learning_rate=0.01,
                num_epochs=1,
                batch_size=256,
                preferred_device="cpu"
            )
        else:
            self.config = config
        super().__init__(self.config)


class Unstructured_PyKeen(PyKeen_BasicModel):

    def __init__(self, config=None):

        if not config:
            self.config = dict(
                training_set_path=os.path.join(os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME),
                                               ttsConst.TRAIN_FILE_NAME),
                test_set_path=os.path.join(os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME),
                                           ttsConst.TEST_FILE_NAME),
                execution_mode="Training_mode",
                random_seed=42,
                kg_embedding_model_name="UM",
                embedding_dim=5,
                margin_loss=1,
                learning_rate=0.01,
                scoring_function=1,
                normalization_of_entities=2,
                num_epochs=1,
                batch_size=256,
                preferred_device="cpu"
            )
        else:
            self.config = config
        super().__init__(self.config)


class SE_PyKeen(PyKeen_BasicModel):

    def __init__(self, config=None):

        if not config:
            self.config = dict(
                training_set_path=os.path.join(os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME),
                                               ttsConst.TRAIN_FILE_NAME),
                test_set_path=os.path.join(os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME),
                                           ttsConst.TEST_FILE_NAME),
                execution_mode="Training_mode",
                random_seed=42,
                kg_embedding_model_name="SE",
                embedding_dim=5,
                margin_loss=1,
                learning_rate=0.01,
                scoring_function=1,
                normalization_of_entities=2,
                num_epochs=1,
                batch_size=256,
                preferred_device="cpu"
            )
        else:
            self.config = config
        super().__init__(self.config)


class Rescal_PyKeen(PyKeen_BasicModel):

    def __init__(self, config=None):

        if not config:
            self.config = dict(
                training_set_path=os.path.join(os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME),
                                               ttsConst.TRAIN_FILE_NAME),
                test_set_path=os.path.join(os.path.join(globConst.WORKING_DIR, ttsConst.TTS_FOLDER_NAME),
                                           ttsConst.TEST_FILE_NAME),
                execution_mode="Training_mode",
                random_seed=42,
                kg_embedding_model_name="RESCAL",
                embedding_dim=5,
                margin_loss=1,
                learning_rate=0.01,
                scoring_function=1,
                num_epochs=1,
                batch_size=256,
                preferred_device="cpu"
            )
        else:
            self.config = config
        super().__init__(self.config)
