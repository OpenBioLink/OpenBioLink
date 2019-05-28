from .models.model import Model

class Evaluation():
    def __init__(self, model: Model):
        self.model = model

    def train(self,examples):
        self.model.train(examples)



