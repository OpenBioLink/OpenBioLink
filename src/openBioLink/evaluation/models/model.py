from abc import abstractmethod, ABCMeta

import numpy as np


class RequiredAttrMeta(ABCMeta):
        required_attributes = []
        def __call__(self, *args, **kwargs):
            obj = super().__call__(*args, **kwargs)
            for attr_name in obj.required_attributes:
                    getattr(obj, attr_name)
            return obj


class Model (metaclass=RequiredAttrMeta):

    required_attributes = ['kge_model']

    @abstractmethod
    def __init__(self):
        ...

    @staticmethod
    @abstractmethod
    def load_model(config_path:str):
        ...

    @abstractmethod
    def train(self, pos_triples:np.array, neg_triples:np.array):
        ...

    @abstractmethod
    def get_ranked_and_sorted_predictions(self, examples):
        # returns ranked_test_triples, sorted_indices
        ...

    @abstractmethod
    def output_model(self, path):
        ...

    def _split_list_in_batches(self, input_list, batch_size):
        return [input_list[i:i + batch_size] for i in range(0, len(input_list), batch_size)]

#todo check if num embedding == #nodes
