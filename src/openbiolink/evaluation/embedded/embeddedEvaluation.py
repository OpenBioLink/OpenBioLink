import multiprocessing
import os
from multiprocessing import Pool

import numpy as np

import openbiolink.evaluation.evalConfig as evalConst
import openbiolink.evaluation.evaluationIO as io
from openbiolink import globalConfig as globConst
from openbiolink.evaluation.metricTypes import RankMetricType, ThresholdMetricType
from openbiolink.evaluation.embedded.models.model import Model
from openbiolink.evaluation.metrics import Metrics

import openbiolink.evaluation.embedded.utils as utils
from openbiolink.evaluation.dataset import Dataset


class EmbeddedEvaluation:

    def __init__(self, model: Model, dataset: Dataset):
        self.model = model
        self.dataset = dataset

    def evaluate(self, metrics: list, ks=None):
        if not ks:
            ks = evalConst.DEFAULT_HITS_AT_K
        os.makedirs(os.path.join(globConst.WORKING_DIR, evalConst.EVAL_OUTPUT_FOLDER_NAME), exist_ok=True)

        threshold_metrics = [m for m in ThresholdMetricType]
        num_threshold_metrics = len([x for x in threshold_metrics if x in metrics])
        ranked_metrics = [m for m in RankMetricType]
        num_ranked_metrics = len([x for x in ranked_metrics if x in metrics])

        unfiltered_metrics = [RankMetricType.MRR_UNFILTERED, RankMetricType.HITS_AT_K_UNFILTERED]
        num_ranked_unfiltered_metrics = len([x for x in unfiltered_metrics if x in metrics])
        filtered_options = bool(num_ranked_metrics - num_ranked_unfiltered_metrics)
        unfiltered_options = bool(num_ranked_unfiltered_metrics)
        metrics_results = {}

        if num_ranked_metrics > 0:
            ranked_metrics_results = self.evaluate_ranked_metrics(
                metrics=metrics, ks=ks, filtered_setting=filtered_options, unfiltered_setting=unfiltered_options
            )
            metrics_results.update(ranked_metrics_results)

        if num_threshold_metrics > 0:
            threshold_metrics_results = self.evaluate_threshold_metrics(metrics=metrics)
            metrics_results.update(threshold_metrics_results)

        io.write_metric_results(metrics_results)

        return metrics_results

    # ---------------------------- START -----------------------------------------
    def evaluate_ranked_metrics(self, ks, metrics, unfiltered_setting=True, filtered_setting=False):
        metric_results = {}

        # get corrupted triples
        pos_test_examples = self.dataset.test_examples[self.dataset.test_examples[globConst.VALUE_COL_NAME] == 1]
        pos_test_examples_array = pos_test_examples.values
        nodes_array = self.dataset.nodes.values

        mapped_pos_triples, mapped_nodes = self.dataset.get_mapped_triples_and_nodes(
            triples=pos_test_examples_array, nodes=nodes_array
        )

        node_types = np.unique(mapped_nodes[:, 1])
        nodes_dic = {nodeType: mapped_nodes[np.where(mapped_nodes[:, 1] == nodeType)][:, 0] for nodeType in node_types}

        print("calculating corrupted triples")

        p = Pool(processes=multiprocessing.cpu_count() - 1)
        params = [
            (pos_example, mapped_nodes, nodes_dic, mapped_pos_triples, filtered_setting, unfiltered_setting)
            for pos_example in mapped_pos_triples
        ]
        # print(params) #todo here
        rank_lists = p.map(self.get_rank_lists, params)
        filtered_ranks_corrupted_heads = [
            filtered_head for (unfiltered_head, unfiltered_tail, filtered_head, filtered_tail) in rank_lists
        ]
        filtered_ranks_corrupted_tails = [
            filtered_tail for (unfiltered_head, unfiltered_tail, filtered_head, filtered_tail) in rank_lists
        ]
        unfiltered_ranks_corrupted_heads = [
            unfiltered_head for (unfiltered_head, unfiltered_tail, filtered_head, filtered_tail) in rank_lists
        ]
        unfiltered_ranks_corrupted_tails = [
            unfiltered_tail for (unfiltered_head, unfiltered_tail, filtered_head, filtered_tail) in rank_lists
        ]

        filtered_num_examples = len(filtered_ranks_corrupted_heads)
        unfiltered_num_examples = len(unfiltered_ranks_corrupted_heads)

        # HITS@K
        if RankMetricType.HITS_AT_K in metrics:
            metric_results[RankMetricType.HITS_AT_K] = Metrics.calculate_hits_at_k(
                ks=ks,
                ranks_corrupted_heads=filtered_ranks_corrupted_heads,
                ranks_corrupted_tails=filtered_ranks_corrupted_tails,
                num_examples=filtered_num_examples,
            )
        # HITS@K unfiltered
        if RankMetricType.HITS_AT_K_UNFILTERED in metrics:
            metric_results[RankMetricType.HITS_AT_K_UNFILTERED] = Metrics.calculate_hits_at_k(
                ks=ks,
                ranks_corrupted_heads=unfiltered_ranks_corrupted_heads,
                ranks_corrupted_tails=unfiltered_ranks_corrupted_tails,
                num_examples=unfiltered_num_examples,
            )
        # MRR
        if RankMetricType.MRR in metrics:
            metric_results[RankMetricType.MRR] = Metrics.calculate_mrr(
                ranks_corrupted_heads=filtered_ranks_corrupted_heads,
                ranks_corrupted_tails=filtered_ranks_corrupted_tails,
                num_examples=filtered_num_examples,
            )
        # MRR unfiltered
        if RankMetricType.MRR_UNFILTERED in metrics:
            metric_results[RankMetricType.MRR] = Metrics.calculate_mrr(
                ranks_corrupted_heads=unfiltered_ranks_corrupted_heads,
                ranks_corrupted_tails=unfiltered_ranks_corrupted_tails,
                num_examples=unfiltered_num_examples,
            )
        return metric_results

    def get_rank_lists(self, params):
        unfiltered_head_ranks = None
        unfiltered_tail_ranks = None
        filtered_head_ranks = None
        filtered_tail_ranks = None
        pos_example, mapped_nodes, nodes_dic, mapped_pos_triples, filtered_setting, unfiltered_setting = params
        (
            unfiltered_corrupted_head,
            unfiltered_corrupted_tail,
            filtered_corrupted_head,
            filtered_corrupted_tail,
        ) = utils.calc_corrupted_triples(
            pos_example=pos_example,
            nodes=mapped_nodes,
            nodes_dic=nodes_dic,
            filtered=filtered_setting,
            pos_examples=mapped_pos_triples,
        )
        if unfiltered_setting:
            unfiltered_head_ranks = self.get_rank_for_corrupted_examples(unfiltered_corrupted_head, pos_example)
            unfiltered_tail_ranks = self.get_rank_for_corrupted_examples(unfiltered_corrupted_tail, pos_example)
        if filtered_setting:
            filtered_head_ranks = self.get_rank_for_corrupted_examples(filtered_corrupted_head, pos_example)
            filtered_tail_ranks = self.get_rank_for_corrupted_examples(filtered_corrupted_tail, pos_example)
        return unfiltered_head_ranks, unfiltered_tail_ranks, filtered_head_ranks, filtered_tail_ranks

    def evaluate_threshold_metrics(self, metrics):
        metric_results = {}
        mapped_test_examples, _ = self.dataset.get_mapped_triples_and_nodes(
            triples=self.dataset.test_examples.values
        )  # , nodes=nodes_array) #todo change here
        values = self.dataset.test_examples.values[:, 4].tolist()
        mapped_test_examples = np.column_stack((mapped_test_examples, values))
        ranked_test_examples, sorted_indices = self.model.get_ranked_and_sorted_predictions(mapped_test_examples)
        ranked_scores = ranked_test_examples[:, 4].tolist()
        ranked_labels = ranked_test_examples[:, 3].tolist()  # todo change here!!
        # ROC Curve
        if ThresholdMetricType.ROC in metrics:
            fpr, tpr = Metrics.calculate_roc_curve(labels=ranked_labels, scores=ranked_scores)
            metric_results[ThresholdMetricType.ROC] = (fpr, tpr)
        # Precision Recall Curve
        if ThresholdMetricType.PR_REC_CURVE in metrics:
            pr, rec = Metrics.calculate_pr_curve(ranked_labels, ranked_scores)
            metric_results[ThresholdMetricType.PR_REC_CURVE] = (pr, rec)
        # ROC AUC
        if ThresholdMetricType.ROC_AUC:
            if ThresholdMetricType.ROC in metric_results.keys():
                fpr, tpr = metric_results[ThresholdMetricType.ROC]
            else:
                fpr, tpr = Metrics.calculate_roc_curve(labels=ranked_labels, scores=ranked_scores)
                # todo ? auch unique?
            roc_auc = Metrics.calculate_auc(fpr, tpr)
            metric_results[ThresholdMetricType.ROC_AUC] = roc_auc
        # Precision Recall AUC
        if ThresholdMetricType.PR_AUC:
            if ThresholdMetricType.PR_AUC in metric_results.keys():
                pr, rec = metric_results[ThresholdMetricType.PR_REC_CURVE]
            else:
                pr, rec = Metrics.calculate_pr_curve(labels=ranked_labels, scores=ranked_scores)
                pr = np.asarray(pr)
                rec = np.asarray(rec)
            _, indices = np.unique(pr, return_index=True)
            pr_unique = pr[indices]
            rec_unique = rec[indices]
            pr_auc = Metrics.calculate_auc(pr_unique, rec_unique)
            metric_results[ThresholdMetricType.PR_AUC] = pr_auc
        return metric_results

    def get_rank_for_corrupted_examples(self, corrupted_examples, true_triple):
        corrupted_examples = np.row_stack((corrupted_examples, (list(true_triple) + [1])))
        ranked_examples, sorted_indices = self.model.get_ranked_and_sorted_predictions(corrupted_examples)
        # testme
        # ranked_examples.reset_index(drop=True, inplace=True)
        # ranked_labels = corrupted_examples[globConst.VALUE_COL_NAME][sorted_indices]
        return self.get_first_positive_rank(ranked_examples[:, 3])

    @staticmethod
    def get_first_positive_rank(labels):
        rank = next(i for i, l in enumerate(labels) if l == 1)
        return rank + 1
