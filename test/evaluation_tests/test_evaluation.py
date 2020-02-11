import os
from io import StringIO
from unittest import TestCase
from unittest.mock import MagicMock, patch

import pandas

from src.openbiolink.evaluation.evaluation import Evaluation
from src.openbiolink.evaluation.metricTypes import ThresholdMetricType, RankMetricType
from src.openbiolink.evaluation.models.pykeen_models import TransR_PyKeen
from src.openbiolink.globalConfig import *


class TestEvaluation(TestCase):
    @patch("src.openbiolink.evaluation.evaluation.utils.calc_corrupted_triples")
    def test_evaluate(self, mocked_calc_corrupted_triples):
        # given
        col_names_ranked_examples = [NODE1_ID_COL_NAME, EDGE_TYPE_COL_NAME, NODE2_ID_COL_NAME, SCORE_COL_NAME]
        ranked_examples_head = pandas.read_csv(
            StringIO(
                "GO_GO:0000006,PART_OF,GO_GO:0000006,1.922283\n"
                + "GO_GO:0000003,PART_OF,GO_GO:0000006,2.189748\n"
                + "GO_GO:0000002,PART_OF,GO_GO:0000006,3.179066\n"
                + "GO_GO:0000001,PART_OF,GO_GO:0000006,3.620234\n"
            ),
            names=col_names_ranked_examples,
        )
        sorted_indices_head = [0, 3, 2, 1]

        ranked_examples_head2 = pandas.read_csv(
            StringIO(
                "GO_GO:0000001,PART_OF,GO_GO:0000002,1.263816\n"
                + "GO_GO:0000002,PART_OF,GO_GO:0000002,2.264960\n"
                + "GO_GO:0000006,PART_OF,GO_GO:0000002,3.537443\n"
                + "GO_GO:0000003,PART_OF,GO_GO:0000002,4.244024\n"
            ),
            names=col_names_ranked_examples,
        )
        sorted_indices_head2 = [3, 2, 0, 1]

        ranked_examples_tail = pandas.read_csv(
            StringIO(
                "GO_GO:0000003,PART_OF,GO_GO:0000003,2.264960\n"
                + "GO_GO:0000003,PART_OF,GO_GO:0000002,4.244024\n"
                + "GO_GO:0000003,PART_OF,GO_GO:0000006,4.899477\n"
                + "GO_GO:0000003,PART_OF,GO_GO:0000001,5.633906\n"
            ),
            names=col_names_ranked_examples,
        )
        sorted_indices_tail = [1, 2, 3, 0]

        ranked_examples_tail2 = pandas.read_csv(
            StringIO(
                "GO_GO:0000001,PART_OF,GO_GO:0000002,1.263816\n"
                + "GO_GO:0000001,PART_OF,GO_GO:0000003,1.605833\n"
                + "GO_GO:0000001,PART_OF,GO_GO:0000001,2.264960\n"
                + "GO_GO:0000001,PART_OF,GO_GO:0000006,2.484512\n"
            ),
            names=col_names_ranked_examples,
        )
        sorted_indices_tail2 = [3, 2, 1, 0]

        example_col_names = [NODE1_ID_COL_NAME, EDGE_TYPE_COL_NAME, NODE2_ID_COL_NAME, VALUE_COL_NAME]
        examples_head = pandas.read_csv(
            StringIO(
                "GO_GO:0000006,PART_OF,GO_GO:0000006,0\n"
                + "GO_GO:0000003,PART_OF,GO_GO:0000006,1\n"
                + "GO_GO:0000002,PART_OF,GO_GO:0000006,0\n"
                + "GO_GO:0000001,PART_OF,GO_GO:0000006,0\n"
            ),
            names=example_col_names,
        )

        examples_head2 = pandas.read_csv(
            StringIO(
                "GO_GO:0000001,PART_OF,GO_GO:0000002,1\n"
                + "GO_GO:0000002,PART_OF,GO_GO:0000002,0\n"
                + "GO_GO:0000006,PART_OF,GO_GO:0000002,0\n"
                + "GO_GO:0000003,PART_OF,GO_GO:0000002,0\n"
            ),
            names=example_col_names,
        )

        examples_tail = pandas.read_csv(
            StringIO(
                "GO_GO:0000003,PART_OF,GO_GO:0000003,1\n"
                + "GO_GO:0000003,PART_OF,GO_GO:0000002,0\n"
                + "GO_GO:0000003,PART_OF,GO_GO:0000006,1\n"
                + "GO_GO:0000003,PART_OF,GO_GO:0000001,0\n"
            ),
            names=example_col_names,
        )

        examples_tail2 = pandas.read_csv(
            StringIO(
                "GO_GO:0000001,PART_OF,GO_GO:0000002,1\n"
                + "GO_GO:0000001,PART_OF,GO_GO:0000003,0\n"
                + "GO_GO:0000001,PART_OF,GO_GO:0000001,0\n"
                + "GO_GO:0000001,PART_OF,GO_GO:0000006,0\n"
            ),
            names=example_col_names,
        )

        corrupted_heads_dict = {
            ("GO_GO:0000003", "PART_OF", "GO_GO:0000006"): examples_head,
            ("GO_GO:0000001", "PART_OF", "GO_GO:0000002"): examples_head2,
        }
        corrupted_tails_dict = {
            ("GO_GO:0000003", "PART_OF", "GO_GO:0000006"): examples_tail,
            ("GO_GO:0000001", "PART_OF", "GO_GO:0000002"): examples_tail2,
        }
        mocked_calc_corrupted_triples.return_value = (corrupted_heads_dict, corrupted_tails_dict)

        test_examples = pandas.concat([examples_head, examples_tail]).reset_index(drop=True)
        ranked_test_examples = pandas.concat([ranked_examples_head, ranked_examples_tail]).reset_index(drop=True)
        sorted_test_indices = sorted_indices_head + [x + len(sorted_indices_head) for x in sorted_indices_tail]

        model = TransR_PyKeen()
        model.get_ranked_and_sorted_predictions = MagicMock(
            side_effect=lambda x: (ranked_examples_head, sorted_indices_head)
            if x is examples_head
            else (ranked_examples_head2, sorted_indices_head2)
            if x is examples_head2
            else (ranked_examples_tail, sorted_indices_tail)
            if x is examples_tail
            else (ranked_examples_tail2, sorted_indices_tail2)
            if x is examples_tail2
            else (ranked_test_examples, sorted_test_indices)
            if x is test_examples
            else None
        )
        metrics = [
            RankMetricType.HITS_AT_K,
            RankMetricType.HITS_AT_K_UNFILTERED,
            RankMetricType.MRR,
            RankMetricType.MRR_UNFILTERED,
            ThresholdMetricType.ROC,
            ThresholdMetricType.ROC_AUC,
            ThresholdMetricType.PR_REC_CURVE,
            ThresholdMetricType.PR_AUC,
        ]

        # when
        path = os.path.dirname(os.path.abspath(__file__))
        e = Evaluation(model, test_set_path=os.path.join(path, "foo2.csv"))
        e.test_examples = test_examples
        result = e.evaluate(metrics, nodes_path=os.path.join(path, "foo.csv"))

        # then
        assert result is not None
