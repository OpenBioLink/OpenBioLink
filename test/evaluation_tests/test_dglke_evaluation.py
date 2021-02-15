import torch
import os
import numpy as np

from openbiolink.evaluation.dataLoader import DataLoader
from openbiolink.evaluation.evaluation import Evaluator

from dglke.models.infer import ScoreInfer
from dglke.utils import load_model_config


class FakeEdge(object):
    def __init__(self, head_emb, rel_emb, tail_emb):
        self._hobj = {}
        self._robj = {}
        self._tobj = {}
        self._hobj['emb'] = head_emb
        self._robj['emb'] = rel_emb
        self._tobj['emb'] = tail_emb

    @property
    def src(self):
        return self._hobj

    @property
    def dst(self):
        return self._tobj

    @property
    def data(self):
        return self._robj


class DglkeEvaluator(Evaluator):

    def __init__(self, dataset_name, model_path, entity_to_id_path, relation_to_id_path):
        dl = DataLoader(dataset_name, entity_to_id_path=entity_to_id_path, relation_to_id_path=relation_to_id_path)
        super().__init__(dl)

        config = load_model_config(os.path.join(model_path, 'config.json'))
        model = ScoreInfer(-1, config, model_path)
        model.load_model()
        self.model = model.model

        self.entity_emb = self.model.entity_emb(self.entities.long())
        self.entity_emb.share_memory_()
        self.relation_emb = self.model.relation_emb(self.relations.long())
        self.relation_emb.share_memory_()

    def score_batch(self, batch):
        head_neg_score = self.model.score_func.create_neg(True)
        tail_neg_score = self.model.score_func.create_neg(False)
        head_neg_prepare = self.model.score_func.create_neg_prepare(True)
        tail_neg_prepare = self.model.score_func.create_neg_prepare(False)

        pos_head_emb = self.entity_emb[batch[:, 0], :]
        pos_tail_emb = self.entity_emb[batch[:, 2], :]
        pos_rel = batch[:, 1].long()
        pos_rel_emb = self.model.relation_emb(pos_rel)

        edata = FakeEdge(pos_head_emb, pos_rel_emb, pos_tail_emb)
        pos_score = self.model.score_func.edge_func(edata)['score']

        neg_head, tail = head_neg_prepare(pos_rel, 1, self.entity_emb, pos_tail_emb, -1, False)
        neg_scores_head = head_neg_score(neg_head, pos_rel_emb, tail,
                                         1, len(batch), self.num_neg)

        head, neg_tail = tail_neg_prepare(pos_rel, 1, pos_head_emb, self.entity_emb, -1, False)
        neg_scores_tail = tail_neg_score(head, pos_rel_emb, neg_tail,
                                         1, len(batch), self.num_neg)

        return pos_score, neg_scores_head.squeeze(0), pos_score, neg_scores_tail.squeeze(0)


if __name__ == "__main__":
    torch.manual_seed(145)
    np.random.seed(145)

    model_path = r"G:\ckpts\TransE_l2_FB15k_0"
    entity_to_id_path = r"G:\triples\entities.tsv"
    relation_to_id_path = r"G:\triples\relations.tsv"

    evaluator = DglkeEvaluator("HQ_DIR", model_path, entity_to_id_path, relation_to_id_path)
    result = evaluator.evaluate(100, 1)
    print(result)
