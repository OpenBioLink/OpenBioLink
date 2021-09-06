import time
import os
import torch
from tqdm import tqdm
from openbiolink.obl2021 import OBL2021Dataset, OBL2021Evaluator

from dglke.models.infer import ScoreInfer
from dglke.utils import load_model_config


def main():
    model_path = r"C:\Users\ottsi\OneDrive\MedUni\OpenBioLink\ckpts\TransE_l2_OBL_1"
    entity_to_id_path = r"C:\Users\ottsi\OneDrive\MedUni\OpenBioLink\ckpts\entities.tsv"
    relation_to_id_path = r"C:\Users\ottsi\OneDrive\MedUni\OpenBioLink\ckpts\relations.tsv"

    dl = OBL2021Dataset(entity_to_id_path=entity_to_id_path, relation_to_id_path=relation_to_id_path)
    ev = OBL2021Evaluator()


    config = load_model_config(os.path.join(model_path, 'config.json'))

    model = ScoreInfer(-1, config, model_path)
    model.load_model()
    model = model.model


    head_neg_score = model.score_func.create_neg(True)
    tail_neg_score = model.score_func.create_neg(False)
    head_neg_prepare = model.score_func.create_neg_prepare(True)
    tail_neg_prepare = model.score_func.create_neg_prepare(False)

    entity_emb = model.entity_emb(torch.arange(dl.num_entities).long())
    relation_emb = model.relation_emb(torch.arange(dl.num_relations).long())

    start = time.time()
    n_batches, batches = dl.get_test_batches(100)

    top10_tails = None
    top10_heads = None

    for batch in tqdm(batches, total=n_batches):
        pos_head_emb = entity_emb[batch[:, 0], :]
        pos_tail_emb = entity_emb[batch[:, 2], :]
        pos_rel = batch[:, 1].long()
        pos_rel_emb = relation_emb[pos_rel, :]

        neg_head, tail = head_neg_prepare(pos_rel, 1, entity_emb, pos_tail_emb, -1, False)
        scores_head = head_neg_score(neg_head, pos_rel_emb, tail,
                                     1, len(batch), dl.num_entities).squeeze(0)
        head, neg_tail = tail_neg_prepare(pos_rel, 1, pos_head_emb, entity_emb, -1, False)
        scores_tail = tail_neg_score(head, pos_rel_emb, neg_tail,
                                     1, len(batch), dl.num_entities).squeeze(0)

        scores_head = dl.filter_scores(
            batch,
            scores_head,
            0,
            float('-Inf')
        )
        scores_tail = dl.filter_scores(
            batch,
            scores_tail,
            2,
            float('-Inf')
        )

        top10_heads_batch = torch.topk(scores_head, 10)[1]
        if top10_heads is None:
            top10_heads = top10_heads_batch
        else:
            top10_heads = torch.cat((top10_heads, top10_heads_batch), dim=0)

        top10_tails_batch = torch.topk(scores_tail, 10)[1]
        if top10_tails is None:
            top10_tails = top10_tails_batch
        else:
            top10_tails = torch.cat((top10_tails, top10_tails_batch), dim=0)

    res = ev.eval(top10_heads, top10_tails, dl.testing)
    print(res)
    print('Evaluation took {:.3f} seconds'.format(time.time() - start))


if __name__ == "__main__":

    r"""
    #main()

    entity_to_id_path = r"C:\Users\ottsi\OneDrive\MedUni\OpenBioLink\ckpts\entities.tsv"
    relation_to_id_path = r"C:\Users\ottsi\OneDrive\MedUni\OpenBioLink\ckpts\relations.tsv"

    dl = OBL2021Dataset(entity_to_id_path=entity_to_id_path, relation_to_id_path=relation_to_id_path)

    import numpy as np
    pred_top10 = torch.tensor(np.load(r"C:\Users\ottsi\OpenBioLink\src\openbiolink\evaluation\pred_OBL2021.npz")["pred_top10"])

    print(pred_top10.shape)

    triples = dl.testing
    h_correct_index = triples[:, 0]
    t_correct_index = triples[:, 2]
    correct_index = torch.cat((t_correct_index, h_correct_index), dim=0)
    print(triples[0:5])
    print(pred_top10[0:5])
    print(correct_index[0:5])

    total_h10 = torch.sum(torch.any(correct_index.view(-1, 1) == pred_top10, dim=1))

    print(float(total_h10 / correct_index.shape[0]))
    
    """

    entity_to_id_path = r"C:\Users\ottsi\OneDrive\MedUni\OpenBioLink\ckpts\entities.tsv"
    relation_to_id_path = r"C:\Users\ottsi\OneDrive\MedUni\OpenBioLink\ckpts\relations.tsv"
    dl = OBL2021Dataset(entity_to_id_path=entity_to_id_path, relation_to_id_path=relation_to_id_path)
    dl.save_as_triples("")