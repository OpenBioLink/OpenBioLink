from abc import ABC, abstractmethod
import pandas


class Model (ABC):

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    def train(self, examples):
        ...

    @abstractmethod
    def get_prediction_scores(self):
        ...

    def _split_list_in_batches(self, input_list, batch_size):
        return [input_list[i:i + batch_size] for i in range(0, len(input_list), batch_size)]

