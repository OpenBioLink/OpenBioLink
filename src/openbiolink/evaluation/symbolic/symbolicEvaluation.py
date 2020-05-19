from openbiolink import globalConfig as globConf
from openbiolink.evaluation import evalConfig as evalConf
import numpy as np

import openbiolink.evaluation.evaluationIO as io
from openbiolink.evaluation.metricTypes import RankMetricType, ThresholdMetricType

from openbiolink.evaluation.metrics import Metrics

from openbiolink.evaluation.symbolic.models.model import Model
from openbiolink.evaluation.dataset import Dataset

import os


class SymbolicEvaluation:

    def __init__(self, model: Model, dataset: Dataset):
        self.model = model
        self.dataset = dataset

    def evaluate(self, metrics: list, ks=None):
        self.model.predict()

        if not ks:
            ks = evalConf.DEFAULT_HITS_AT_K
        os.makedirs(os.path.join(globConf.WORKING_DIR, evalConf.EVAL_OUTPUT_FOLDER_NAME), exist_ok=True)

        threshold_metrics = [m for m in ThresholdMetricType]
        num_threshold_metrics = len([x for x in threshold_metrics if x in metrics])
        ranked_metrics = [m for m in RankMetricType]
        num_ranked_metrics = len([x for x in ranked_metrics if x in metrics])

        unfiltered_metrics = [RankMetricType.MRR_UNFILTERED, RankMetricType.HITS_AT_K_UNFILTERED]
        num_ranked_unfiltered_metrics = len([x for x in unfiltered_metrics if x in metrics])
        filtered_options = bool(num_ranked_metrics - num_ranked_unfiltered_metrics)
        unfiltered_options = bool(num_ranked_unfiltered_metrics)
        metrics_results = {}

        prediction_paths = self.get_prediction_paths(self.model.config["path_predicitions"])
        for prediction_path in prediction_paths:
            predictions = self.read_prediction(prediction_path)

            if num_ranked_metrics > 0:
                ranked_metrics_results = self.evaluate_ranked_metrics(ks, metrics, predictions)
                metrics_results.update(ranked_metrics_results)

            if num_threshold_metrics > 0:
                threshold_metrics_results = self.evaluate_threshold_metrics(metrics, predictions)
                metrics_results.update(threshold_metrics_results)
            io.write_metric_results(metrics_results)

    @staticmethod
    def get_prediction_paths(predictions_path: str):
        """
        if "|" in predictions_path:
            prefix, values, _ = predictions_path.split("|")
            postfixes = values.split(",")
            predictions_path = list()
            for postfix in postfixes:
                predictions_path.append(prefix + postfix)
        else:
            predictions_path = [predictions_path]
        return predictions_path
        """
        return os.path.join(predictions_path, "prediction")

    @staticmethod
    def read_prediction(prediction_path: str):
        with open(prediction_path) as pred_file:
            file_content = pred_file.readlines()
        file_content = [x.strip() for x in file_content]
        predictions = list()
        for i in range(0, len(file_content), 3):
            triple = file_content[i].split(" ")
            heads = list(filter(None, file_content[i + 1][7:].strip("\t").split("\t")))
            tails = list(filter(None, file_content[i + 2][7:].strip("\t").split("\t")))

            head_nodes = list()
            head_confidences = list()
            for j in range(0, len(heads), 2):
                head_nodes.append(heads[j])
                head_confidences.append(heads[j + 1])

            tail_nodes = list()
            tail_confidences = list()
            for j in range(0, len(tails), 2):
                tail_nodes.append(tails[j])
                tail_confidences.append(tails[j + 1])
            predictions.append(
                Prediction(triple[0], triple[1], triple[2], head_nodes, head_confidences, tail_nodes, tail_confidences))
        return predictions

    @staticmethod
    def evaluate_ranked_metrics(ks, metrics, predictions):

        ranks_head = list()
        ranks_tail = list()
        num_examples = len(predictions)

        for prediction in predictions:
            if prediction.head_rank != float('inf'):
                ranks_head.append(prediction.head_rank)
            if prediction.tail_rank != float('inf'):
                ranks_tail.append(prediction.tail_rank)

        metric_results = {}
        # HITS@K
        if RankMetricType.HITS_AT_K in metrics:
            metric_results[RankMetricType.HITS_AT_K] = Metrics.calculate_hits_at_k(
                ks=ks,
                ranks_corrupted_heads=ranks_head,
                ranks_corrupted_tails=ranks_tail,
                num_examples=num_examples,
            )
        # HITS@K unfiltered
        if RankMetricType.HITS_AT_K_UNFILTERED in metrics:
            metric_results[RankMetricType.HITS_AT_K_UNFILTERED] = Metrics.calculate_hits_at_k(
                ks=ks,
                ranks_corrupted_heads=ranks_head,
                ranks_corrupted_tails=ranks_tail,
                num_examples=num_examples,
            )
        if RankMetricType.HITS_AT_K_REL in metrics:
            results = {}
            for prediction in predictions:
                if prediction.relation not in results.keys():
                    results[prediction.relation] = list()
                results[prediction.relation].append((prediction.head_rank, prediction.tail_rank))

            metric_results[RankMetricType.HITS_AT_K_REL] = dict()
            for relation in results.keys():
                results[relation] = list(zip(*results[relation]))

                metric_results[RankMetricType.HITS_AT_K_REL][relation] = Metrics.calculate_hits_at_k(
                    ks=ks,
                    ranks_corrupted_heads=results[relation][0],
                    ranks_corrupted_tails=results[relation][1],
                    num_examples=len(results[relation][0])
                )
        # MRR
        if RankMetricType.MRR in metrics:
            metric_results[RankMetricType.MRR] = Metrics.calculate_mrr(
                ranks_corrupted_heads=ranks_head,
                ranks_corrupted_tails=ranks_tail,
                num_examples=num_examples,
            )
        # MRR unfiltered
        if RankMetricType.MRR_UNFILTERED in metrics:
            metric_results[RankMetricType.MRR] = Metrics.calculate_mrr(
                ranks_corrupted_heads=ranks_head,
                ranks_corrupted_tails=ranks_tail,
                num_examples=num_examples,
            )
        return metric_results

    @staticmethod
    def evaluate_threshold_metrics(metrics, predictions):

        scores = list()
        labels = list()

        for prediction in predictions:
            labels = labels + prediction.head_labels
            scores = scores + prediction.head_confidences
            labels = labels + prediction.tail_labels
            scores = scores + prediction.tail_confidences

        metric_results = {}
        # ROC Curve
        if ThresholdMetricType.ROC in metrics:
            fpr, tpr = Metrics.calculate_roc_curve(labels=labels, scores=scores)
            metric_results[ThresholdMetricType.ROC] = (fpr, tpr)
        # Precision Recall Curve
        if ThresholdMetricType.PR_REC_CURVE in metrics:
            pr, rec = Metrics.calculate_pr_curve(labels, scores)
            metric_results[ThresholdMetricType.PR_REC_CURVE] = (pr, rec)
        # ROC AUC
        if ThresholdMetricType.ROC_AUC:
            if ThresholdMetricType.ROC in metric_results.keys():
                fpr, tpr = metric_results[ThresholdMetricType.ROC]
            else:
                fpr, tpr = Metrics.calculate_roc_curve(labels=labels, scores=scores)
                # todo ? auch unique?
            roc_auc = Metrics.calculate_auc(fpr, tpr)
            metric_results[ThresholdMetricType.ROC_AUC] = roc_auc
        # Precision Recall AUC
        if ThresholdMetricType.PR_AUC:
            if ThresholdMetricType.PR_AUC in metric_results.keys():
                pr, rec = metric_results[ThresholdMetricType.PR_REC_CURVE]
            else:
                pr, rec = Metrics.calculate_pr_curve(labels=labels, scores=scores)
                pr = np.asarray(pr)
                rec = np.asarray(rec)
            _, indices = np.unique(pr, return_index=True)
            pr_unique = pr[indices]
            rec_unique = rec[indices]
            pr_auc = Metrics.calculate_auc(pr_unique, rec_unique)
            metric_results[ThresholdMetricType.PR_AUC] = pr_auc
        return metric_results

class Prediction:

    def __init__(self, head, relation, tail, head_predictions, head_confidences, tail_predictions, tail_confidences):
        self.head = head
        self.relation = relation
        self.tail = tail

        self.head_predictions = head_predictions
        self.head_confidences = list(map(float, head_confidences))
        self.head_rank, self.head_labels = self.calc_rank_and_labels(head, head_predictions)

        self.tail_predictions = tail_predictions
        self.tail_confidences = list(map(float, tail_confidences))
        self.tail_rank, self.tail_labels = self.calc_rank_and_labels(tail, tail_predictions)

    @staticmethod
    def calc_rank_and_labels(true: str, predictions: list):
        labels = [0 for i in range(len(predictions))]
        for i in range(len(predictions)):
            if predictions[i] == true:
                labels[i] = 1
                return i + 1, labels
        return float('inf'), labels
