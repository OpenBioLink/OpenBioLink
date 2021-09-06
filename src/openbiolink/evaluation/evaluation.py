
import time
from abc import ABC, abstractmethod
from typing import Dict, Tuple

import torch
from tqdm import tqdm

from openbiolink.evaluation.dataLoader import DataLoader


class Evaluator(ABC):
    """
        :param dl: Dataloader containing the OpenBioLink dataset
        :param higher_is_better: Boolean which should be set to `True` if higher scores are considered better, `False` otherwise.
    """

    def __init__(self, dl: DataLoader, higher_is_better: bool = True):
        self.dl: DataLoader = dl
        self.higher_is_better = higher_is_better

    def _get_ranking(self, y_pred_pos_head, y_pred_neg_head, y_pred_pos_tail, y_pred_neg_tail):
        if self.higher_is_better:
            ranking_head = torch.sum(y_pred_neg_head >= y_pred_pos_head.view(-1, 1), dim=1) + 1
            ranking_tail = torch.sum(y_pred_neg_tail >= y_pred_pos_tail.view(-1, 1), dim=1) + 1
        else:
            ranking_head = torch.sum(y_pred_neg_head <= y_pred_pos_head.view(-1, 1), dim=1) + 1
            ranking_tail = torch.sum(y_pred_neg_tail <= y_pred_pos_tail.view(-1, 1), dim=1) + 1
        ranking_list = torch.cat([ranking_head, ranking_tail], dim=0)
        return ranking_list

    def _get_result(self, ranking_lists: list):
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

    def _evaluate_batch(self, batch):
        scores_head, scores_tail = self.score_batch(batch)
        pos_scores_head = scores_head.gather(1, batch[:, 0].view(-1, 1)).view(-1, 1)
        pos_scores_tail = scores_tail.gather(1, batch[:, 2].view(-1, 1)).view(-1, 1)
        neg_scores_head = self.dl.filter_scores(
            batch,
            0,
            scores_head,
            float('nan') if self.higher_is_better else float('Inf')
        )
        neg_scores_tail = self.dl.filter_scores(
            batch,
            2,
            scores_tail,
            float('nan') if self.higher_is_better else float('Inf')
        )
        return self._get_ranking(pos_scores_head, neg_scores_head, pos_scores_tail, neg_scores_tail)

    def evaluate(self, batch_size=100) -> Dict[str, float]:
        """Evaluates a model by retrieving scores from the (implemented) score_batch function.

        :param batch_size:
            Integer determining the size of the test batch which is passed to function `score_batch`

        :return:
            Dictionary containing the evaluation results (keys: 'hits@1', 'hits@3', 'hits@10', 'mrr')
        """

        start = time.time()
        n_batches, batches = self.dl.get_test_batches(batch_size)

        result = []
        for batch in tqdm(batches, total=n_batches):
            result.append(self._evaluate_batch(batch))

        print('Evaluation took {:.3f} seconds'.format(time.time() - start))
        return self._get_result(result)

    @abstractmethod
    def score_batch(self, batch: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Abstract function, has to be implemented. Should return two arrays containing the head and tail scores of a batch of test data from a model.

        :param batch:
            Batch of test data. Shape `(batch_size,3)`

        :return:
            + head_scores: `torch.tensor` where the value at [i,j] is the score of the triple `(j, batch[i][1], batch[i][2])`. Shape `(batch_size, num_entities)`
            + tail_scores: `torch.tensor` where the value at [i,j] is the score of the triple `(batch[i][0], batch[i][1], j)`. Shape `(batch_size, num_entities)`
        """
        raise NotImplementedError
