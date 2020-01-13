import multiprocessing
import os
import random
from multiprocessing import Pool

import numpy as np
import pandas
from sortedcontainers import SortedList
from tqdm import tqdm

import openbiolink.evaluation.evalConfig as evalConst
import openbiolink.evaluation.evaluationIO as io
from openbiolink import globalConfig as globConst
from openbiolink import utils
from openbiolink.evaluation.metricTypes import RankMetricType, ThresholdMetricType
from openbiolink.evaluation.models.model import Model


class Evaluation:
    def __init__(self, model: Model, training_set_path=None, test_set_path=None, nodes_path=None, mappings_avail=False):
        self.model = model
        if training_set_path:
            self.training_examples = pandas.read_csv(training_set_path, sep="\t", names=globConst.COL_NAMES_SAMPLES)
        else:
            self.training_examples = pandas.DataFrame(columns=globConst.COL_NAMES_SAMPLES)
        if test_set_path:
            self.test_examples = pandas.read_csv(test_set_path, sep="\t", names=globConst.COL_NAMES_SAMPLES)
        else:
            self.test_examples = pandas.DataFrame(columns=globConst.COL_NAMES_SAMPLES)
        if nodes_path is not None:
            self.nodes = pandas.read_csv(nodes_path, sep="\t", names=globConst.COL_NAMES_NODES)
        else:
            self.nodes = None

        if not mappings_avail:
            relation_labels = set()
            relation_labels.update(set(self.test_examples[globConst.EDGE_TYPE_COL_NAME]))
            relation_labels.update(set(self.training_examples[globConst.EDGE_TYPE_COL_NAME]))

            self.node_label_to_id = None
            self.node_types_to_id = None
            self.relation_label_to_id = utils.create_mappings(relation_labels)
            if self.nodes is not None:
                self.node_label_to_id = utils.create_mappings(np.unique(self.nodes.values[:, 0]))
                self.node_types_to_id = utils.create_mappings(np.unique(self.nodes.values[:, 1]))
            else:
                node_labels = set()
                node_labels.update(set(self.test_examples[globConst.NODE1_ID_COL_NAME]))
                node_labels.update(set(self.test_examples[globConst.NODE2_ID_COL_NAME]))
                node_labels.update(set(self.training_examples[globConst.NODE1_ID_COL_NAME]))
                node_labels.update(set(self.training_examples[globConst.NODE2_ID_COL_NAME]))
                self.node_label_to_id = utils.create_mappings(node_labels)

            # output mappings
            io.write_mappings(node_label_to_id=self.node_label_to_id,
                              node_types_to_id=self.node_types_to_id,
                              relation_label_to_id=self.relation_label_to_id)

        else:
            # testme
            output_directory = os.path.join(os.path.join(globConst.WORKING_DIR, evalConst.EVAL_OUTPUT_FOLDER_NAME),
                                            evalConst.MODEL_DIR)
            self.node_label_to_id = io.read_mapping(
                os.path.join(output_directory, evalConst.MODEL_ENTITY_NAME_MAPPING_NAME))
            node_type_path = os.path.join(output_directory, evalConst.MODEL_ENTITY_TYPE_MAPPING_NAME)
            if os.path.exists(node_type_path):
                self.node_types_to_id = io.read_mapping(node_type_path)
            elif self.nodes is not None:
                self.node_types_to_id = utils.create_mappings(np.unique(self.nodes.values[:, 1]))
                io.write_mappings(node_types_to_id=self.node_types_to_id)
            else:
                pass  # fixme error nodes must be provided when eval
            self.relation_label_to_id = io.read_mapping(
                os.path.join(output_directory, evalConst.MODEL_RELATION_TYPE_MAPPING_NAME))

    def train(self):
        ### prepare input examples
        pos_examples = self.training_examples[self.training_examples[globConst.VALUE_COL_NAME] == 1]
        neg_examples = self.training_examples[self.training_examples[globConst.VALUE_COL_NAME] == 0]
        # pos and neg must be same length! but also, all entities must still be present!
        num_examples = min(len(neg_examples), len(pos_examples))
        pos_examples = self.save_remove_n_edges(pos_examples, len(pos_examples) - num_examples)
        neg_examples = self.save_remove_n_edges(neg_examples, len(neg_examples) - num_examples)
        pos_triples = pos_examples[globConst.COL_NAMES_TRIPLES].values
        neg_triples = neg_examples[globConst.COL_NAMES_TRIPLES].values
        mapped_pos_triples, _ = self.get_mapped_triples_and_nodes(triples=pos_triples)
        mapped_neg_triples, _ = self.get_mapped_triples_and_nodes(triples=neg_triples)

        self.model.train(pos_triples=mapped_pos_triples, neg_triples=mapped_neg_triples)
        output_directory = os.path.join(os.path.join(globConst.WORKING_DIR, evalConst.EVAL_OUTPUT_FOLDER_NAME),
                                        evalConst.MODEL_DIR)

        os.makedirs(output_directory, exist_ok=True)
        model_path = os.path.join(output_directory, evalConst.MODEL_TRAINED_NAME)
        self.model.output_model(model_path)

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
            ranked_metrics_results = self.evaluate_ranked_metrics_2(metrics=metrics,
                                                                    ks=ks,
                                                                    filtered_setting=filtered_options,
                                                                    unfiltered_setting=unfiltered_options)
            metrics_results.update(ranked_metrics_results)

        if num_threshold_metrics > 0:
            threshold_metrics_results = self.evaluate_threshold_metrics(metrics=metrics)
            metrics_results.update(threshold_metrics_results)

        io.write_metric_results(metrics_results)

        return metrics_results

    # ---------------------------- START -----------------------------------------
    def evaluate_ranked_metrics_3(self, ks, metrics, unfiltered_setting=True, filtered_setting=False):
        metric_results = {}
        k_raw_corrupted_head = []
        for _ in ks:
            k_raw_corrupted_head.append([])
        k_raw_corrupted_tail = []
        for _ in ks:
            k_raw_corrupted_tail.append([])

        # get corrupted triples
        pos_test_examples = self.test_examples[self.test_examples[globConst.VALUE_COL_NAME] == 1]
        pos_test_examples_array = pos_test_examples.values
        nodes_array = self.nodes.values

        mapped_pos_triples, mapped_nodes = self.get_mapped_triples_and_nodes(triples=pos_test_examples_array,
                                                                             nodes=nodes_array)
        nodeTypes = np.unique(mapped_nodes[:, 1])
        nodes_dic = {nodeType: np.unique(mapped_nodes[np.where(mapped_nodes[:, 1] == nodeType)][:, 0]) for nodeType in
                     nodeTypes}
        head_tuples = mapped_pos_triples[:, 0:2]
        head_tuples = np.unique(head_tuples, axis=0)
        tail_tuples = mapped_pos_triples[:, 1:3]
        tail_tuples = np.unique(tail_tuples, axis=0)
        head_ranks = []
        # corrupting tail
        for head, relation in tqdm(head_tuples):
            data = mapped_pos_triples[np.where((mapped_pos_triples[:, 0] == head) *
                                               (mapped_pos_triples[:, 1] == relation))]

            ranked_pos_examples, _ = self.model.get_ranked_and_sorted_predictions(data)
            _, corrupted_examples, _, _ = utils.calc_corrupted_triples(
                pos_example=data[0],
                nodes=mapped_nodes,
                nodes_dic=nodes_dic,
                filtered=False,
                pos_examples=mapped_pos_triples)
            all_examples = np.unique(np.row_stack((corrupted_examples, np.column_stack((data, [0] * len(data))))),
                                     axis=0)  # todo VERY WRONG!
            ranked_all_examples, _ = self.model.get_ranked_and_sorted_predictions(all_examples)
            increase_search_frame_by = [0] * len(ks)
            for example in ranked_pos_examples:
                search_data = ranked_all_examples[0:ks[-1] + 1, :]  # fixme this should be more?
                for i, k in enumerate(ks):
                    current_k = k + increase_search_frame_by[i]
                    current_k = min(current_k, len(search_data))
                    index = np.where(search_data[:, 2] == example[2])[0]
                    if index <= current_k:
                        k_raw_corrupted_tail[i].append(1)
                        increase_search_frame_by[i] += 1
                    else:
                        k_raw_corrupted_tail[i].append(0)

        # corrupting head
        for relation, tail in tqdm(tail_tuples):
            data = mapped_pos_triples[np.where((mapped_pos_triples[:, 1] == relation) *
                                               (mapped_pos_triples[:, 2] == tail))]

            ranked_pos_examples, _ = self.model.get_ranked_and_sorted_predictions(data)
            corrupted_examples, _, _, _ = utils.calc_corrupted_triples(
                pos_example=data[0],
                nodes=mapped_nodes,
                nodes_dic=nodes_dic,
                filtered=False,
                pos_examples=mapped_pos_triples)
            all_examples = np.unique(np.row_stack((corrupted_examples, np.column_stack((data, [0] * len(data))))),
                                     axis=0)  # todo VERY WRONG!
            ranked_all_examples, _ = self.model.get_ranked_and_sorted_predictions(all_examples)
            increase_search_frame_by = [0] * len(ks)
            for example in ranked_pos_examples:
                search_data = ranked_all_examples[0:ks[-1] + 1, :]
                for i, k in enumerate(ks):
                    current_k = k + increase_search_frame_by[i]
                    current_k = min(current_k, len(search_data))
                    index = np.where(search_data[:, 0] == example[0])[0] + 1
                    if index <= current_k:
                        k_raw_corrupted_head[i].append(1)
                        increase_search_frame_by[i] += 1
                    else:
                        k_raw_corrupted_head[i].append(0)
        k_results_corrupted_head = []
        for i, k in enumerate(ks):
            k_results_corrupted_head.append(sum(k_raw_corrupted_head[i]) / len(k_raw_corrupted_head[i]))
        k_results_corrupted_tail = []
        for i, k in enumerate(ks):
            k_results_corrupted_tail.append(sum(k_raw_corrupted_tail[i]) / len(k_raw_corrupted_tail[i]))

        metric_results[RankMetricType.HITS_AT_K] = (k_results_corrupted_head, k_results_corrupted_tail)
        return metric_results

    def evaluate_ranked_metrics_2(self, ks, metrics, unfiltered_setting=True, filtered_setting=False):
        metric_results = {}

        # get corrupted triples
        pos_test_examples = self.test_examples[self.test_examples[globConst.VALUE_COL_NAME] == 1]
        pos_test_examples_array = pos_test_examples.values
        nodes_array = self.nodes.values

        mapped_pos_triples, mapped_nodes = self.get_mapped_triples_and_nodes(triples=pos_test_examples_array,
                                                                             nodes=nodes_array)

        node_types = np.unique(mapped_nodes[:, 1])
        nodes_dic = {nodeType: mapped_nodes[np.where(mapped_nodes[:, 1] == nodeType)][:, 0] for nodeType in node_types}

        print('calculating corrupted triples')

        p = Pool(processes=multiprocessing.cpu_count() - 1)
        params = [(pos_example, mapped_nodes, nodes_dic, mapped_pos_triples, filtered_setting, unfiltered_setting) for
                  pos_example in mapped_pos_triples]
        # print(params) #todo here
        rank_lists = p.map(self.get_rank_lists, params)
        filtered_ranks_corrupted_heads = [filtered_head for
                                          (unfiltered_head, unfiltered_tail, filtered_head, filtered_tail) in
                                          rank_lists]
        filtered_ranks_corrupted_tails = [filtered_tail for
                                          (unfiltered_head, unfiltered_tail, filtered_head, filtered_tail) in
                                          rank_lists]
        unfiltered_ranks_corrupted_heads = [unfiltered_head for
                                            (unfiltered_head, unfiltered_tail, filtered_head, filtered_tail) in
                                            rank_lists]
        unfiltered_ranks_corrupted_tails = [unfiltered_tail for
                                            (unfiltered_head, unfiltered_tail, filtered_head, filtered_tail) in
                                            rank_lists]

        filtered_num_examples = len(filtered_ranks_corrupted_heads)
        unfiltered_num_examples = len(unfiltered_ranks_corrupted_heads)

        # HITS@K
        if RankMetricType.HITS_AT_K in metrics:
            metric_results[RankMetricType.HITS_AT_K] = self.calculate_hits_at_k(ks=ks,
                                                                                ranks_corrupted_heads=filtered_ranks_corrupted_heads,
                                                                                ranks_corrupted_tails=filtered_ranks_corrupted_tails,
                                                                                num_examples=filtered_num_examples)
        # HITS@K unfiltered
        if RankMetricType.HITS_AT_K_UNFILTERED in metrics:
            metric_results[RankMetricType.HITS_AT_K_UNFILTERED] = self.calculate_hits_at_k(ks=ks,
                                                                                           ranks_corrupted_heads=unfiltered_ranks_corrupted_heads,
                                                                                           ranks_corrupted_tails=unfiltered_ranks_corrupted_tails,
                                                                                           num_examples=unfiltered_num_examples)
        # MRR
        if RankMetricType.MRR in metrics:
            metric_results[RankMetricType.MRR] = self.calculate_mrr(
                ranks_corrupted_heads=filtered_ranks_corrupted_heads,
                ranks_corrupted_tails=filtered_ranks_corrupted_tails,
                num_examples=filtered_num_examples)
        # MRR unfiltered
        if RankMetricType.MRR_UNFILTERED in metrics:
            metric_results[RankMetricType.MRR] = self.calculate_mrr(
                ranks_corrupted_heads=unfiltered_ranks_corrupted_heads,
                ranks_corrupted_tails=unfiltered_ranks_corrupted_tails,
                num_examples=unfiltered_num_examples)
        return metric_results

    def evaluate_ranked_metrics_1(self, ks, metrics, unfiltered_setting=True, filtered_setting=False):
        metric_results = {}

        # get corrupted triples
        pos_test_examples = self.test_examples[self.test_examples[globConst.VALUE_COL_NAME] == 1]
        pos_test_examples_array = pos_test_examples.values
        nodes_array = self.nodes.values

        mapped_pos_triples, mapped_nodes = self.get_mapped_triples_and_nodes(triples=pos_test_examples_array,
                                                                             nodes=nodes_array)

        node_types = np.unique(mapped_nodes[:, 1])
        nodes_dic = {nodeType: mapped_nodes[np.where(mapped_nodes[:, 1] == nodeType)][:, 0] for nodeType in node_types}

        filtered_ranks_corrupted_heads = []
        filtered_ranks_corrupted_tails = []
        unfiltered_ranks_corrupted_heads = []
        unfiltered_ranks_corrupted_tails = []

        print('calculating corrupted triples')

        for pos_example in tqdm(mapped_pos_triples, total=mapped_pos_triples.shape[0]):
            unfiltered_corrupted_head, \
            unfiltered_corrupted_tail, \
            filtered_corrupted_head, \
            filtered_corrupted_tail = utils.calc_corrupted_triples(
                pos_example=pos_example,
                nodes=mapped_nodes,
                nodes_dic=nodes_dic,
                filtered=filtered_setting,
                pos_examples=mapped_pos_triples)
            if unfiltered_setting:
                unfiltered_ranks_corrupted_heads.append(
                    self.get_rank_for_corrupted_examples(unfiltered_corrupted_head, pos_example))
                unfiltered_ranks_corrupted_tails.append(
                    self.get_rank_for_corrupted_examples(unfiltered_corrupted_tail, pos_example))
            if filtered_setting:
                filtered_ranks_corrupted_heads.append(
                    self.get_rank_for_corrupted_examples(filtered_corrupted_head, pos_example))
                filtered_ranks_corrupted_tails.append(
                    self.get_rank_for_corrupted_examples(filtered_corrupted_tail, pos_example))

        filtered_num_examples = len(filtered_ranks_corrupted_heads)
        unfiltered_num_examples = len(unfiltered_ranks_corrupted_heads)

        # HITS@K
        if RankMetricType.HITS_AT_K in metrics:
            metric_results[RankMetricType.HITS_AT_K] = self.calculate_hits_at_k(ks=ks,
                                                                                ranks_corrupted_heads=filtered_ranks_corrupted_heads,
                                                                                ranks_corrupted_tails=filtered_ranks_corrupted_tails,
                                                                                num_examples=filtered_num_examples)
        # HITS@K unfiltered
        if RankMetricType.HITS_AT_K_UNFILTERED in metrics:
            metric_results[RankMetricType.HITS_AT_K_UNFILTERED] = self.calculate_hits_at_k(ks=ks,
                                                                                           ranks_corrupted_heads=unfiltered_ranks_corrupted_heads,
                                                                                           ranks_corrupted_tails=unfiltered_ranks_corrupted_tails,
                                                                                           num_examples=unfiltered_num_examples)
        # MRR
        if RankMetricType.MRR in metrics:
            metric_results[RankMetricType.MRR] = self.calculate_mrr(
                ranks_corrupted_heads=filtered_ranks_corrupted_heads,
                ranks_corrupted_tails=filtered_ranks_corrupted_tails,
                num_examples=filtered_num_examples)
        # MRR unfiltered
        if RankMetricType.MRR_UNFILTERED in metrics:
            metric_results[RankMetricType.MRR] = self.calculate_mrr(
                ranks_corrupted_heads=unfiltered_ranks_corrupted_heads,
                ranks_corrupted_tails=unfiltered_ranks_corrupted_tails,
                num_examples=unfiltered_num_examples)
        return metric_results

    def get_rank_lists(self, params):
        unfiltered_head_ranks = None
        unfiltered_tail_ranks = None
        filtered_head_ranks = None
        filtered_tail_ranks = None
        pos_example, mapped_nodes, nodes_dic, mapped_pos_triples, filtered_setting, unfiltered_setting = params
        unfiltered_corrupted_head, \
        unfiltered_corrupted_tail, \
        filtered_corrupted_head, \
        filtered_corrupted_tail = utils.calc_corrupted_triples(
            pos_example=pos_example,
            nodes=mapped_nodes,
            nodes_dic=nodes_dic,
            filtered=filtered_setting,
            pos_examples=mapped_pos_triples)
        if unfiltered_setting:
            unfiltered_head_ranks = self.get_rank_for_corrupted_examples(unfiltered_corrupted_head, pos_example)
            unfiltered_tail_ranks = self.get_rank_for_corrupted_examples(unfiltered_corrupted_tail, pos_example)
        if filtered_setting:
            filtered_head_ranks = self.get_rank_for_corrupted_examples(filtered_corrupted_head, pos_example)
            filtered_tail_ranks = self.get_rank_for_corrupted_examples(filtered_corrupted_tail, pos_example)
        return unfiltered_head_ranks, unfiltered_tail_ranks, filtered_head_ranks, filtered_tail_ranks

    def evaluate_threshold_metrics(self, metrics):
        metric_results = {}
        mapped_test_examples, _ = self.get_mapped_triples_and_nodes(
            triples=self.test_examples.values)  # , nodes=nodes_array) #todo change here
        values = self.test_examples.values[:, 4].tolist()
        mapped_test_examples = np.column_stack((mapped_test_examples, values))
        ranked_test_examples, sorted_indices = self.model.get_ranked_and_sorted_predictions(mapped_test_examples)
        ranked_scores = ranked_test_examples[:, 4].tolist()
        ranked_labels = ranked_test_examples[:, 3].tolist()  # todo change here!!
        # ROC Curve
        if ThresholdMetricType.ROC in metrics:
            fpr, tpr = self.calculate_roc_curve(labels=ranked_labels, scores=ranked_scores)
            metric_results[ThresholdMetricType.ROC] = (fpr, tpr)
        # Precision Recall Curve
        if ThresholdMetricType.PR_REC_CURVE in metrics:
            pr, rec = self.calculate_pr_curve(ranked_labels, ranked_scores)
            metric_results[ThresholdMetricType.PR_REC_CURVE] = (pr, rec)
        # ROC AUC
        if ThresholdMetricType.ROC_AUC:
            if ThresholdMetricType.ROC in metric_results.keys():
                fpr, tpr = metric_results[ThresholdMetricType.ROC]
            else:
                fpr, tpr = self.calculate_roc_curve(labels=ranked_labels, scores=ranked_scores)
                # todo ? auch unique?
            roc_auc = self.calculate_auc(fpr, tpr)
            metric_results[ThresholdMetricType.ROC_AUC] = roc_auc
        # Precision Recall AUC
        if ThresholdMetricType.PR_AUC:
            if ThresholdMetricType.PR_AUC in metric_results.keys():
                pr, rec = metric_results[ThresholdMetricType.PR_REC_CURVE]
            else:
                pr, rec = self.calculate_pr_curve(labels=ranked_labels, scores=ranked_scores)
                pr = np.asarray(pr)
                rec = np.asarray(rec)
            _, indices = np.unique(pr, return_index=True)
            pr_unique = pr[indices]
            rec_unique = rec[indices]
            pr_auc = self.calculate_auc(pr_unique, rec_unique)
            metric_results[ThresholdMetricType.PR_AUC] = pr_auc
        return metric_results

    def get_rank_for_corrupted_examples(self, corrupted_examples, true_triple):
        corrupted_examples = np.row_stack((corrupted_examples, (list(true_triple) + [1])))
        ranked_examples, sorted_indices = self.model.get_ranked_and_sorted_predictions(corrupted_examples)
        # testme
        # ranked_examples.reset_index(drop=True, inplace=True)
        # ranked_labels = corrupted_examples[globConst.VALUE_COL_NAME][sorted_indices]
        return self.get_first_positive_rank(ranked_examples[:, 3])

    def get_mapped_triples_and_nodes(self, triples=None, nodes=None):
        mapped_triples = None
        mapped_nodes = None
        if nodes is not None:
            mapped_nodes = np.column_stack((utils.map_elements(nodes[:, 0:1], self.node_label_to_id),
                                            utils.map_elements(nodes[:, 1:2], self.node_types_to_id)))
        if triples is not None:
            mapped_triples = np.column_stack((utils.map_elements(triples[:, 0:1], self.node_label_to_id),
                                              utils.map_elements(triples[:, 1:2], self.relation_label_to_id),
                                              utils.map_elements(triples[:, 2:3], self.node_label_to_id)))
        return mapped_triples, mapped_nodes

    def create_mappings(self, relations, node_types, node_labels=None):
        self.node_label_to_id = utils.create_mappings(node_labels)
        self.node_types_to_id = utils.create_mappings(node_types)
        self.relation_label_to_id = utils.create_mappings(relations)

    @staticmethod
    def get_first_positive_rank(labels):
        rank = next(i for i, l in enumerate(labels) if l == 1)
        return rank + 1

    @staticmethod
    def save_remove_n_edges(edges: pandas.DataFrame, n):
        """
        removes n edges from 'edges' so that no node is removed in the process, i.e. the total number
        of nodes in 'edges' stays the same
        :param edges: original edges
        :param n: number of how many edges should be removed
        :return:
        """
        if n < 1:
            return edges
        all_edges = SortedList(list(edges[globConst.NODE1_ID_COL_NAME].append(edges[globConst.NODE2_ID_COL_NAME])))
        edges_list = set(all_edges)
        edges_count_dict = {x: all_edges.count(x) for x in edges_list}
        i = 0

        for _ in range(1000):
            drop_indices_candidates = random.sample(edges.index.values.tolist(), n)
            drop_indices = []
            for drop_index in tqdm(drop_indices_candidates):
                if i == n:
                    break
                drop_edge_candidate = edges.loc[drop_index]
                if edges_count_dict[drop_edge_candidate[globConst.NODE1_ID_COL_NAME]] > 1 \
                        and edges_count_dict[drop_edge_candidate[globConst.NODE2_ID_COL_NAME]] > 1:
                    drop_indices.append(drop_index)
                    i += 1
            edges.drop(inplace=True, index=drop_indices)
            if i == n:
                break
        edges.reset_index(drop=True, inplace=True)
        return edges

    ###### calculate metrics ######

    @staticmethod
    def calculate_hits_at_k(ks, ranks_corrupted_heads, ranks_corrupted_tails, num_examples):
        corrupted_heads_hits_at_k = dict()
        corrupted_tails_hits_at_k = dict()
        for k in ks:
            corrupted_heads_hits_at_k[k] = len([x for x in ranks_corrupted_heads if x <= k]) / num_examples
            corrupted_tails_hits_at_k[k] = len([x for x in ranks_corrupted_tails if x <= k]) / num_examples
        return corrupted_heads_hits_at_k, corrupted_tails_hits_at_k

    @staticmethod
    def calculate_mrr(ranks_corrupted_heads, ranks_corrupted_tails, num_examples):
        inverse_ranks_corrupted_heads = [1 / n for n in ranks_corrupted_heads]
        inverse_ranks_corrupted_tails = [1 / n for n in ranks_corrupted_tails]
        mrr_heads = sum(inverse_ranks_corrupted_heads) / num_examples
        mrr_tails = sum(inverse_ranks_corrupted_tails) / num_examples
        return mrr_heads, mrr_tails

    @staticmethod
    def calculate_roc_curve(labels, scores):
        from sklearn.metrics import roc_curve
        fpr, tpr, _ = roc_curve(labels, scores)
        return list(fpr), list(tpr)

    @staticmethod
    def calculate_pr_curve(labels, scores):
        from sklearn.metrics import precision_recall_curve
        precision, recall, thresholds = precision_recall_curve(labels, scores)
        return list(precision), list(recall)

    @staticmethod
    def calculate_auc(x_values, y_values):
        from sklearn.metrics import auc
        auc_value = auc(x_values, y_values)
        return auc_value
