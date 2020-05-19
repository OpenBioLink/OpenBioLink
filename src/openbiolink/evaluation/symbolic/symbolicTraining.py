from openbiolink.evaluation.symbolic.models.model import Model
from openbiolink.evaluation.dataset import Dataset


class SymbolicTraining:

    def __init__(self, model: Model, dataset: Dataset):
        self.model = model
        self.dataset = dataset

    def train(self):
        self.model.train()