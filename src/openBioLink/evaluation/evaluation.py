import os

import numpy as np
import pandas
from tqdm import tqdm

import evaluation.evalConfig as evalConst
import evaluation.evaluationIO as io
import globalConfig as globConst
import utils
from .metricTypes import RankMetricType, ThresholdMetricType
from .models.model import Model


class Evaluation:
    def __init__(self, model: Model, training_set_path=None, test_set_path=None):
        self.model = model
        if training_set_path:
            self.training_examples = pandas.read_csv(training_set_path, sep="\t",
                                                     names=globConst.COL_NAMES_SAMPLES)
        else:
            self.training_examples = pandas.DataFrame(columns=globConst.COL_NAMES_SAMPLES)
        if test_set_path:
            self.test_examples = pandas.read_csv(test_set_path, sep="\t",
                                       names=globConst.COL_NAMES_SAMPLES)
        else:
            self.test_examples = pandas.DataFrame(columns=globConst.COL_NAMES_SAMPLES)
        relation_labels = set()
        relation_labels.update(set(self.test_examples[globConst.EDGE_TYPE_COL_NAME]))
        relation_labels.update(set(self.training_examples[globConst.EDGE_TYPE_COL_NAME]))

        self.node_label_to_id = None
        self.node_types_to_id = None
        self.relation_label_to_id = utils.create_mappings(relation_labels)



    def train(self):
        self.model.train(self.training_examples)


    def evaluate(self,
                 metrics: list,
                 ks=None,
                 nodes_path=None,
                 ):
        if not ks:
            ks=evalConst.DEFAULT_HITS_AT_K 
        os.makedirs(os.path.join(globConst.WORKING_DIR, evalConst.EVAL_OUTPUT_FOLDER_NAME),exist_ok = True)

        threshold_metrics = [m for m in ThresholdMetricType]
        num_threshold_metrics = len([x for x in threshold_metrics if x in metrics])
        ranked_metrics = [m for m in RankMetricType]

        unfiltered_metrics = [RankMetricType.MRR_UNFILTERED, RankMetricType.HITS_AT_K_UNFILTERED]
        num_ranked_metrics = len([x for x in ranked_metrics if x in metrics])
        num_ranked_unfiltered_metrics = len([x for x in unfiltered_metrics if x in metrics])
        filtered_options = bool(num_ranked_metrics-num_ranked_unfiltered_metrics)
        unfiltered_options = bool(num_ranked_unfiltered_metrics)
        metrics_results = {}

        if num_ranked_metrics > 0:
            ranked_metrics_results = self.evaluate_ranked_metrics(metrics=metrics,
                                                                  ks=ks,
                                                                  nodes_path=nodes_path,
                                                                  filtered_setting=filtered_options,
                                                                  unfiltered_setting=unfiltered_options)
            metrics_results.update(ranked_metrics_results)

        if  num_threshold_metrics > 0:
            threshold_metrics_results = self.evaluate_threshold_metrics(metrics=metrics,nodes_path=nodes_path) #todo change here!!!
            metrics_results.update(threshold_metrics_results)

        io.write_metric_results(metrics_results)

        return metrics_results
    #fixme unfiltered setting according to max outcome


    def evaluate_ranked_metrics(self, ks, metrics, nodes_path=None, unfiltered_setting = True, filtered_setting = False):
        metric_results = {}

        #get corrupted triples


        pos_test_examples = self.test_examples[self.test_examples[globConst.VALUE_COL_NAME] == 1]
        pos_test_examples_array = pos_test_examples.values
        nodes = pandas.read_csv(nodes_path, sep="\t", names=globConst.COL_NAMES_NODES)
        nodes_array = nodes.values

        mapped_pos_triples, mapped_nodes = self.get_mapped_triples_and_nodes(triples = pos_test_examples_array, nodes=nodes_array)

        nodeTypes = np.unique(mapped_nodes[:, 1])
        nodes_dic = {nodeType: mapped_nodes[np.where(mapped_nodes[:, 1] == nodeType)][:, 0] for nodeType in nodeTypes}

        filtered_ranks_corrupted_heads = []
        filtered_ranks_corrupted_tails = []
        unfiltered_ranks_corrupted_heads = []
        unfiltered_ranks_corrupted_tails = []
        ######################
        print('calculating corrupted triples')

        from multiprocessing import Pool
        import multiprocessing
        p = Pool(multiprocessing.cpu_count())
        params = [(pos_example, mapped_nodes, nodes_dic, mapped_pos_triples, filtered_setting, unfiltered_setting) for pos_example in mapped_pos_triples]
        rank_lists = p.map(self.get_rank_lists,params)
        filtered_ranks_corrupted_heads = [filtered_head for (unfiltered_head, unfiltered_tail, filtered_head, filtered_tail) in rank_lists]
        filtered_ranks_corrupted_tails = [filtered_tail for (unfiltered_head, unfiltered_tail, filtered_head, filtered_tail) in rank_lists]
        unfiltered_ranks_corrupted_heads = [unfiltered_head for (unfiltered_head, unfiltered_tail, filtered_head, filtered_tail) in rank_lists]
        unfiltered_ranks_corrupted_tails = [unfiltered_tail for (unfiltered_head, unfiltered_tail, filtered_head, filtered_tail) in rank_lists]

        #for pos_example in tqdm(mapped_pos_triples, total=mapped_pos_triples.shape[0]):
        #    unfiltered_corrupted_head, \
        #    unfiltered_corrupted_tail, \
        #    filtered_corrupted_head, \
        #    filtered_corrupted_tail = utils.calc_corrupted_triples(
        #        pos_example=pos_example,
        #        nodes=mapped_nodes,
        #        nodes_dic = nodes_dic,
        #        filtered=filtered_setting,
        #    pos_examples=mapped_pos_triples)
        #    if unfiltered_setting:
        #        unfiltered_ranks_corrupted_heads.append(self.get_rank_for_corrupted_examples(unfiltered_corrupted_head, pos_example))
        #        unfiltered_ranks_corrupted_tails.append(self.get_rank_for_corrupted_examples(unfiltered_corrupted_tail, pos_example))
        #    if filtered_setting:
        #        filtered_ranks_corrupted_heads.append(self.get_rank_for_corrupted_examples(filtered_corrupted_head, pos_example))
        #        filtered_ranks_corrupted_tails.append(self.get_rank_for_corrupted_examples(filtered_corrupted_tail, pos_example))

        filtered_num_examples = len(filtered_ranks_corrupted_heads)
        unfiltered_num_examples = len(unfiltered_ranks_corrupted_heads)

            #########################


        # HITS@K
        if RankMetricType.HITS_AT_K in metrics:
            metric_results[RankMetricType.HITS_AT_K] = self.calculate_hits_at_k(ks= ks,
                                                                                ranks_corrupted_heads=filtered_ranks_corrupted_heads,
                                                                                ranks_corrupted_tails=filtered_ranks_corrupted_tails,
                                                                                num_examples=filtered_num_examples)
        # HITS@K unfiltered
        if RankMetricType.HITS_AT_K_UNFILTERED in metrics:
            metric_results[RankMetricType.HITS_AT_K_UNFILTERED] = self.calculate_hits_at_k(ks= ks,
                                                                                ranks_corrupted_heads=unfiltered_ranks_corrupted_heads,
                                                                                ranks_corrupted_tails=unfiltered_ranks_corrupted_tails,
                                                                                num_examples=unfiltered_num_examples)
        # MRR
        if RankMetricType.MRR in metrics:
            metric_results[RankMetricType.MRR] = self.calculate_mrr(ranks_corrupted_heads=filtered_ranks_corrupted_heads,
                                                                    ranks_corrupted_tails=filtered_ranks_corrupted_tails,
                                                                    num_examples=filtered_num_examples)
        # MRR unfiltered
        if RankMetricType.MRR_UNFILTERED in metrics:
            metric_results[RankMetricType.MRR] = self.calculate_mrr(ranks_corrupted_heads=unfiltered_ranks_corrupted_heads,
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
        return (unfiltered_head_ranks, unfiltered_tail_ranks, filtered_head_ranks, filtered_tail_ranks )



    def evaluate_threshold_metrics(self, metrics, nodes_path):
        metric_results={}
        #nodes = pandas.read_csv(nodes_path, sep="\t", names=globConst.COL_NAMES_NODES) #todo change here
        #tn_nodes = pandas.read_csv("C:/Users/anna/PycharmProjects/masterthesis/this_is_a_test\\graph_files\\TN_nodes.csv", sep="\t", names=globConst.COL_NAMES_NODES)
        #new_nodes = pandas.read_csv("C:/Users/anna/PycharmProjects/masterthesis/this_is_a_test\\graph_files\\TN_nodes.csv", sep="\t", names=globConst.COL_NAMES_NODES)
        #nodes = nodes.append(tn_nodes)

        #new_node_in_edge = test_set[globalConfig.NODE1_ID_COL_NAME].isin(new_test_nodes) \
        #                   | test_set[globalConfig.NODE2_ID_COL_NAME].isin(new_test_nodes)
        #edges_with_new_nodes = test_set.loc[new_node_in_edge]
        #test_set = test_set.drop(list(edges_with_new_nodes.index.values))
       #
        #nodes_array = nodes.values

        mapped_test_examples, _ = self.get_mapped_triples_and_nodes(triples=self.test_examples.values) #, nodes=nodes_array) #todo change here
        values = self.test_examples.values[:,4].tolist()
        mapped_test_examples = np.column_stack((mapped_test_examples,  values ))
        ranked_test_examples, sorted_indices = self.model.get_ranked_predictions(mapped_test_examples)
        ranked_scores = ranked_test_examples[:,4].tolist()
        ranked_labels = ranked_test_examples[:,3].tolist() #todo change here!!
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
                #todo ? auch unique?
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


    #def get_filtered_and_unfiltered_ranks(self, corrupted_dict, filtered=True, unfiltered=True):
    #    filtered_ranks=[]
    #    unfiltered_ranks=[]
    #    for true_triple, corrupted_df in corrupted_dict.items():
    #        corrupted_df.loc[len(corrupted_df)] = list(true_triple) + [1]
    #        ranked_examples, sorted_indices = self.model.get_ranked_predictions(corrupted_df)
    #        #testme
    #        #ranked_examples.reset_index(drop=True, inplace=True)
    #        ranked_labels = corrupted_df[globConst.VALUE_COL_NAME][sorted_indices]
    #        if filtered:
    #            filtered_ranks.append(self.get_rank_of_triple(true_triple, ranked_examples))
    #        if unfiltered:
    #            unfiltered_ranks.append(self.get_first_positive_rank(ranked_labels))
    #    return filtered_ranks, unfiltered_ranks


    def get_rank_for_corrupted_examples(self, corrupted_examples, true_triple):
        corrupted_examples = np.row_stack((corrupted_examples, (list(true_triple) + [1])))
        ranked_examples, sorted_indices = self.model.get_ranked_predictions(corrupted_examples)
        #testme
        #ranked_examples.reset_index(drop=True, inplace=True)
        #ranked_labels = corrupted_examples[globConst.VALUE_COL_NAME][sorted_indices]
        return(self.get_first_positive_rank(ranked_examples[:,3]))


    #def get_rank_of_triple (self, triple_value, ranked_predictions):
    #    head, relation, tail = triple_value
    #    index = ranked_predictions.index[(ranked_predictions[globConst.NODE1_ID_COL_NAME] == head)
    #                             & (ranked_predictions[globConst.EDGE_TYPE_COL_NAME]==relation)
    #                             & (ranked_predictions[globConst.NODE2_ID_COL_NAME]==tail)].tolist()[0] #todo check for multiple returns
    #    return index+1


    def get_first_positive_rank (self, labels):
        rank = next(i for i, l in enumerate(labels) if l==1)
        return rank+1

    def get_mapped_triples_and_nodes(self, triples=None, nodes=None):
        mapped_triples = None
        mapped_nodes = None
        if nodes is not None:
            if self.node_label_to_id is None or self.node_types_to_id is None:
                node_labels = np.unique(nodes[:, 0])
                node_types = np.unique(nodes[:, 1])
                self.node_label_to_id = utils.create_mappings(node_labels)
                self.node_types_to_id = utils.create_mappings(node_types)

            mapped_nodes = np.column_stack((utils.map_elements(nodes[:, 0:1], self.node_label_to_id),
                                           utils.map_elements(nodes[:, 1:2], self.node_types_to_id)))
        if triples is not None:
            if self.relation_label_to_id is None:
                relations = triples[:, 1]
                self.relation_label_to_id = utils.create_mappings(relations)
            if self.node_label_to_id is None:
                node_labels = np.unique(np.concatenate([triples[:, 0], triples[:, 2]]))
                self.node_label_to_id = utils.create_mappings(node_labels)


            mapped_triples = np.column_stack((utils.map_elements(triples[:, 0:1], self.node_label_to_id),
                                             utils.map_elements(triples[:, 1:2], self.relation_label_to_id),
                                             utils.map_elements(triples[:, 2:3], self.node_label_to_id)))
        return mapped_triples, mapped_nodes


    ###### calculate metrics ######

    def calculate_hits_at_k(self, ks, ranks_corrupted_heads, ranks_corrupted_tails, num_examples):
        corrupted_heads_hits_at_k = dict()
        corrupted_tails_hits_at_k = dict()
        for k in ks:
            corrupted_heads_hits_at_k[k] = len([x for x in ranks_corrupted_heads if x <= k]) / num_examples
            corrupted_tails_hits_at_k[k] = len([x for x in ranks_corrupted_tails if x <= k]) / num_examples
        return corrupted_heads_hits_at_k, corrupted_tails_hits_at_k


    def calculate_mrr(self,ranks_corrupted_heads, ranks_corrupted_tails, num_examples):
        inverse_ranks_corrupted_heads = [1 / n for n in ranks_corrupted_heads]
        inverse_ranks_corrupted_tails = [1 / n for n in ranks_corrupted_tails]
        mrr_heads = sum(inverse_ranks_corrupted_heads) / num_examples
        mrr_tails = sum(inverse_ranks_corrupted_tails) / num_examples
        return mrr_heads, mrr_tails


    def calculate_roc_curve(self, labels, scores ):
        from sklearn.metrics import roc_curve
        fpr, tpr, _ = roc_curve(labels, scores)
        return  list(fpr), list(tpr)


    def calculate_pr_curve(self, labels, scores ):
        from sklearn.metrics import  precision_recall_curve
        precision, recall, thresholds = precision_recall_curve(labels, scores)
        return  list(precision), list(recall)


    def calculate_auc(self, x_values, y_values):
        from sklearn.metrics import auc
        auc_value = auc(x_values, y_values)
        return auc_value
