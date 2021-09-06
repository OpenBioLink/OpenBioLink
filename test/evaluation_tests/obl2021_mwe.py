"""
Import of the OpenBioLink Dataset and Evaluator.
"""
import torch
from tqdm import tqdm
from openbiolink.obl2021 import OBL2021Dataset, OBL2021Evaluator
from numpy.random import default_rng

class MockupModel:
    def __init__(self):
        self.rng = default_rng(0)

    def getTop10Heads(self, batch):
        rand = []
        for i in range(batch.shape[0]):
            rand.append(self.rng.choice(180992, 10, replace=False))
        return torch.tensor(rand)

    def getTop10Tails(self, batch):
        rand = []
        for i in range(batch.shape[0]):
            rand.append(self.rng.choice(180992, 10, replace=False))
        return torch.tensor(rand)

def main():
    # Mockup Model
    model = MockupModel()

    # Initialize dataset and evaluator
    dl = OBL2021Dataset()
    ev = OBL2021Evaluator()

    top10_heads = []
    top10_tails = []

    n_batches, batches = dl.get_test_batches(100)
    for batch in tqdm(batches, total=n_batches):
        top10_tails.append(model.getTop10Heads(batch))
        top10_heads.append(model.getTop10Tails(batch))
    top10_heads = torch.cat(top10_heads, dim=0)
    top10_tails = torch.cat(top10_tails, dim=0)

    ev.eval(top10_heads, top10_tails, dl.testing)

if __name__ == "__main__":
    main()
