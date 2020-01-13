from abc import ABC, abstractmethod

import numpy as np


class Model(ABC):

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def train(self, pos_triples: np.array, neg_triples: np.array):
        ...

    @abstractmethod
    def get_ranked_and_sorted_predictions(self, examples):
        ...

    @abstractmethod
    def output_model(self, path):
        ...

    def _split_list_in_batches(self, input_list, batch_size):
        return [input_list[i:i + batch_size] for i in range(0, len(input_list), batch_size)]

# todo check if num embedding == #nodes
