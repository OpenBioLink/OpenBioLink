from abc import ABC, abstractmethod

import numpy as np


class Model(ABC):
    @abstractmethod
    def __init__(self):
        self.config = None
        ...

    @abstractmethod
    def train(self):
        ...

    @abstractmethod
    def predict(self):
        pass


# todo check if num embedding == #nodes
