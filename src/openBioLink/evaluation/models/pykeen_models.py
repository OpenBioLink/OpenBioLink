import json
import os
import pickle

import numpy as np
import pandas
import pykeen.constants as keenConst
import pykeen.utilities.pipeline as pipeline
import torch
import torch.optim as optim

from .model import Model


## ** code adapted from pykeen: https://github.com/SmartDataAnalytics/PyKEEN **


class PyKeen_BasicModel (Model):
    def __init__(self, config=None):
        super().__init__()
        import torch
        import os
        self.config=config
        self.device = torch.device('cpu')
        self.kge_model = None
        self.entity_to_id_train = None
        self.rel_to_id_train = None
        self.output_directory = "C:\\Users\\anna\\PycharmProjects\\masterthesis\\results"
        os.makedirs(self.output_directory, exist_ok=True)

    def train(self, examples=None):
        ### prepare input examples
        if not examples:
            examples = pandas.read_csv(self.config[keenConst.TRAINING_SET_PATH], sep="\t",
                                      names=['id1', 'edge', 'id2', 'qscore', 'value'])

        pos_examples = examples[examples['value'] == 1]
        neg_examples = examples[examples['value'] == 0]

        pos_triples = pos_examples[['id1', 'edge', 'id2']].values
        neg_triples = neg_examples[['id1', 'edge', 'id2']].values
        all_triples = examples[['id1', 'edge', 'id2']].values

        self.entity_to_id, self.rel_to_id = pipeline.create_mappings(triples=all_triples)

        mapped_pos_train_triples, _, _ = pipeline.create_mapped_triples(
            triples=pos_triples,
            entity_label_to_id=self.entity_to_id,
            relation_label_to_id=self.rel_to_id,
        )

        mapped_neg_train_triples, _, _ = pipeline.create_mapped_triples(
            triples=neg_triples,
            entity_label_to_id=self.entity_to_id,
            relation_label_to_id=self.rel_to_id
        )

        self.config[keenConst.NUM_ENTITIES] = len(self.entity_to_id)
        self.config[keenConst.NUM_RELATIONS] = len(self.rel_to_id)

        ### prepare model
        self.kge_model = pipeline.get_kge_model(config=self.config)
        self.kge_model = self.kge_model.to(self.device)

        optimizer = optim.SGD(self.kge_model.parameters(), lr=self.config[keenConst.LEARNING_RATE])
        loss_per_epoch = []
        num_pos_examples = mapped_pos_train_triples.shape[0]

        ### train model
        for _ in range(self.config[keenConst.NUM_EPOCHS]):
            # create batches
            indices_pos = np.arange(num_pos_examples)
            np.random.shuffle(indices_pos)
            mapped_pos_train_triples = mapped_pos_train_triples[indices_pos]
            pos_batches = self._split_list_in_batches(input_list=mapped_pos_train_triples,
                                                      batch_size=self.config["batch_size"])
            indices_neg = np.arange(num_pos_examples)
            np.random.shuffle(indices_neg)
            mapped_neg_train_triples = mapped_neg_train_triples[indices_neg]
            neg_batches = self._split_list_in_batches(input_list=mapped_neg_train_triples,
                                                      batch_size=self.config["batch_size"])

            current_epoch_loss = 0.

            for pos_batch, neg_batch in zip(pos_batches, neg_batches):
                if len(pos_batch) == len(neg_batch):
                    current_batch_size = len(pos_batch)
                else:
                    current_batch_size = len(pos_batch)
                    pass
                    # fixme error?

                pos_batch_tensor = torch.tensor(pos_batch, dtype=torch.long, device=self.device)
                neg_batch_tensor = torch.tensor(neg_batch, dtype=torch.long, device=self.device)
                # Recall that torch *accumulates* gradients. Before passing in a
                # new instance, you need to zero out the gradients from the old instance
                optimizer.zero_grad()
                loss = self.kge_model(pos_batch_tensor, neg_batch_tensor)
                current_epoch_loss += (loss.item() * current_batch_size)

                loss.backward()
                optimizer.step()

            loss_per_epoch.append(current_epoch_loss / len(mapped_pos_train_triples))

        ### pepare results for output
        id_to_entity = {value: key for key, value in self.entity_to_id.items()}
        id_to_rel = {value: key for key, value in self.rel_to_id.items()}
        entity_to_embedding = {
            id_to_entity[id]: embedding.detach().cpu().numpy()
            for id, embedding in enumerate(self.kge_model.entity_embeddings.weight)
        }
        relation_to_embedding = {
            id_to_rel[id]: embedding.detach().cpu().numpy()
            for id, embedding in enumerate(self.kge_model.relation_embeddings.weight)
        }

        results = pipeline._make_results(
            trained_model=self.kge_model,
            loss_per_epoch=loss_per_epoch,
            entity_to_embedding=entity_to_embedding,
            relation_to_embedding=relation_to_embedding,
            metric_results=None,
            entity_to_id=self.entity_to_id,
            rel_to_id=self.rel_to_id,
            params=self.config,
        )

        #### output results
        self.output_train_results(results)

        return self.kge_model, loss_per_epoch


    def get_ranked_predictions(self):

        #fixme load trained model

        ### prepare input examples
        examples = pandas.read_csv(self.config[keenConst.TEST_SET_PATH], sep="\t",
                                   names=['id1', 'edge', 'id2', 'qscore', 'value'])

        test_triples = examples[['id1', 'edge', 'id2']].values

        self.entity_to_id, self.rel_to_id = pipeline.create_mappings(triples=test_triples)
        id_to_entity = {value: key for key, value in self.entity_to_id.items()}
        id_to_rel = {value: key for key, value in self.rel_to_id.items()}

        mapped_test_triples, _, _ = pipeline.create_mapped_triples(
            triples=test_triples,
            entity_label_to_id=self.entity_to_id,
            relation_label_to_id=self.rel_to_id,
        )

        predicted_scores = self.kge_model.predict(mapped_test_triples)
        _, sorted_indices = torch.sort(torch.tensor(predicted_scores, dtype=torch.float),
                                       descending=False)

        sorted_indices = sorted_indices.cpu().numpy()
        ranked_mapped_test_triples = mapped_test_triples[sorted_indices,:]

        ranked_subject_column = np.vectorize(id_to_entity.get)(ranked_mapped_test_triples[:, 0:1])
        ranked_predicate_column = np.vectorize(id_to_rel.get)(ranked_mapped_test_triples[:, 1:2])
        ranked_object_column = np.vectorize(id_to_entity.get)(ranked_mapped_test_triples[:, 2:3])
        ranked_scores = np.reshape(predicted_scores[sorted_indices], newshape=(-1, 1))

        ranked_triples = np.concatenate([ranked_subject_column,ranked_predicate_column, ranked_object_column , ranked_scores], axis=1)

        return ranked_triples


    def output_train_results(self, results):
        with open(os.path.join(self.output_directory, 'configuration.json'), 'w') as file:
            json.dump(results[keenConst.FINAL_CONFIGURATION], file, indent=2)

        with open(os.path.join(self.output_directory, 'entities_to_embeddings.pkl'), 'wb') as file:
            pickle.dump(results[keenConst.ENTITY_TO_EMBEDDING], file, protocol=pickle.HIGHEST_PROTOCOL)

        with open(os.path.join(self.output_directory, 'entities_to_embeddings.json'), 'w') as file:
            json.dump(
                {
                    key: list(map(float, array))
                    for key, array in results[keenConst.ENTITY_TO_EMBEDDING].items()
                },
                file,
                indent=2,
                sort_keys=True
            )

        if results[keenConst.RELATION_TO_EMBEDDING] is not None:
            with open(os.path.join(self.output_directory, 'relations_to_embeddings.pkl'), 'wb') as file:
                pickle.dump(results[keenConst.RELATION_TO_EMBEDDING], file, protocol=pickle.HIGHEST_PROTOCOL)

            with open(os.path.join(self.output_directory, 'relations_to_embeddings.json'), 'w') as file:
                json.dump(
                    {
                        key: list(map(float, array))
                        for key, array in results[keenConst.RELATION_TO_EMBEDDING].items()
                    },
                    file,
                    indent=2,
                    sort_keys=True,
                )

        with open(os.path.join(self.output_directory, 'entity_to_id.json'), 'w') as file:
            json.dump(results[keenConst.ENTITY_TO_ID], file, indent=2, sort_keys=True)

        with open(os.path.join(self.output_directory, 'relation_to_id.json'), 'w') as file:
            json.dump(results[keenConst.RELATION_TO_ID], file, indent=2, sort_keys=True)

        with open(os.path.join(self.output_directory, 'losses.json'), 'w') as file:
            json.dump(results[keenConst.LOSSES], file, indent=2, sort_keys=True)

        # Save trained model
        torch.save(
            results[keenConst.TRAINED_MODEL].state_dict(),
            os.path.join(self.output_directory, 'trained_model.pkl'),
        )




class TransE_PyKeen (PyKeen_BasicModel):

    def __init__(self, config = None):
        super().__init__(config)
        if not config:
            self.config = dict(
                training_set_path = "C:\\Users\\anna\\PycharmProjects\\masterthesis\\cross_val\\fold_0\\train_sample.csv",
                #test_set_path = "C:\\Users\\anna\\PycharmProjects\\masterthesis\\cross_val\\fold_0\\val_sample.csv",
                execution_mode= "Training_mode",
                random_seed= 42,
                kg_embedding_model_name= "TransE",
                embedding_dim= 5,
                margin_loss= 1,
                learning_rate= 0.01,
                scoring_function= 1,
                normalization_of_entities=2,
                num_epochs= 20,
                batch_size= 8,
                preferred_device= "cpu"
            )
        #todo if config is string --> load json, if json is dic --> alles gut
        # todo check if device available



class TransR_PyKeen(PyKeen_BasicModel):

    def __init__(self, config=None):
        super().__init__(config)

        if not config:
            self.config = dict(
                training_set_path="C:\\Users\\anna\\PycharmProjects\\masterthesis\\cross_val\\fold_0\\train_sample.csv",
                # test_set_path = "C:\\Users\\anna\\PycharmProjects\\masterthesis\\cross_val\\fold_0\\val_sample.csv",
                execution_mode="Training_mode",
                random_seed=42,
                kg_embedding_model_name="TransR",
                embedding_dim=5,
                relation_embedding_dim=5,
                margin_loss=1,
                learning_rate=0.01,
                scoring_function=1,
                normalization_of_entities=2,
                num_epochs=20,
                batch_size=8,
                preferred_device="cpu"
            )
        self.output_directory = "C:\\Users\\anna\\PycharmProjects\\masterthesis\\results"
        os.makedirs(self.output_directory, exist_ok=True)
        self.device = torch.device('cpu')
        self.kge_model = None
        # todo check if device available





py = TransR_PyKeen()
py.train()