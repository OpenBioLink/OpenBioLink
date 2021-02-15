
from abc import ABC, abstractmethod
import numpy as np
import torch.multiprocessing as mp
import time
from typing import Dict, Tuple

from pykeen.evaluation.evaluator import create_sparse_positive_filter_, filter_scores_

from openbiolink.evaluation.dataLoader import DataLoader

from tqdm import tqdm

try:
    import torch
except ImportError:
    torch = None


### Evaluator for link property prediction
class Evaluator(ABC):

    """
        :param dl:
            Dataloader containing the OpenBioLink dataset
    """

    def __init__(self, dl : DataLoader):
        

        self.dl : DataLoader = dl
        """Dataloader containing the OpenBioLink dataset"""
        self.entities : torch.Tensor = torch.arange(self.dl.num_entities)
        """1-D tensor of all entities in the dataset (to be used to corrupt the head/tail of a positive triple)"""
        self.relations : torch.Tensor = torch.arange(self.dl.num_relations)
        """1-D tensor of all relations in the dataset"""
        self.num_neg : int = self.dl.num_entities
        """Number of negative samples used for evaluation (equals to the number of entities in the dataset)"""

    def get_ranking(self, y_pred_pos_head, y_pred_neg_head, y_pred_pos_tail, y_pred_neg_tail):
        ranking_head = torch.sum(y_pred_neg_head >= y_pred_pos_head.view(-1,1), dim=1) + 1
        ranking_tail = torch.sum(y_pred_neg_tail >= y_pred_pos_tail.view(-1,1), dim=1) + 1
        ranking_list = torch.cat([ranking_head, ranking_tail], dim=0)
        return ranking_list

    def get_result(self, ranking_lists : list):
        hits1 = 0.
        hits3 = 0.
        hits10 = 0.
        mrr = 0.
        count = 0

        for ranking_list in ranking_lists:
            hits1 = hits1 + (ranking_list <= 1).sum()
            hits3 = hits3 + (ranking_list <= 3).sum()
            hits10 = hits10 + (ranking_list <= 10).sum()
            mrr = mrr + (1. / ranking_list).sum()
            count = count + ranking_list.shape[0]

        return {'hits@1': hits1 / count,
                'hits@3': hits3 / count,
                'hits@10': hits10 / count,
                'mrr': mrr / count}

    def filter_scores(self, batch, filter_col, scores):
        positive_filter, relation_filter = create_sparse_positive_filter_(
            hrt_batch=batch,
            all_pos_triples=self.dl.all,
            filter_col = filter_col
        )
        return filter_scores_(
            scores=scores,
            filter_batch=positive_filter,
        )

    def evaluate(self, batch_size=100, cpu=-1, filtering=True) -> Dict[str, float]:
        """Evaluates a model by retrieving scores from the (implemented) score_batch function.

            :param batch_size:
                Size of a test batch
            :param cpu:
                Number of processors to use, -1 means all processors are used.

            :return:
                Dictionary containing the evaluation results (keys: 'hits@1', 'hits@3', 'hits@10', 'mrr')
        """
        self.filtering = filtering

        start = time.time()
        n_batches, batches = self.dl.get_test_batches(batch_size)

        if cpu == 1 or cpu == 0:
            result = []
            for batch in tqdm(batches, total=n_batches):
                result.append(self.evaluate_batch(batch))
        elif cpu == -1:
            pool = mp.Pool(mp.cpu_count())
            result = pool.map(self.evaluate_batch, batches)
        else:
            pool = mp.Pool(cpu)
            result = pool.map(self.evaluate_batch, batches)
        print('Evaluation took {:.3f} seconds'.format(time.time() - start))
        return self.get_result(result)

    def evaluate_batch(self, batch):
        pos_scores_head, neg_scores_head, pos_scores_tail, neg_scores_tail = self.score_batch(batch)
        if self.filtering:
            neg_scores_head = self.filter_scores(batch, 0, neg_scores_head)
            neg_scores_tail = self.filter_scores(batch, 2, neg_scores_tail)
        return self.get_ranking(pos_scores_head, neg_scores_head, pos_scores_tail, neg_scores_tail)

    @abstractmethod
    def score_batch(self, batch: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """ Abstract function to be implemented: Should return the positive and negative head and tail scores of a batch of test data from a model.

            :param batch:
                Batch of test data of size (batch_size,3)

            :return:
                *   positive head scores (batch_size,)
                *   negative head scores (batch_size, num_entities), where the value at [i,j] is the score of the triple batch[i], where the head was corrupted with the entity j.
                *   positive tail scores (batch_size,)
                *   negative tail scores (batch_size, num_entities), where the value at [i,j] is the score of the triple batch[i], where the tail was corrupted with the entity j.
        """
        raise NotImplementedError
