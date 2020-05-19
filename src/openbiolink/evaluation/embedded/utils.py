import random
import pandas as pd
import numpy as np
from sortedcontainers import SortedList
from tqdm import tqdm
from openbiolink import globalConfig as globConst
from openbiolink.gui.tqdmbuf import TqdmBuffer


def save_remove_n_edges(edges: pd.DataFrame, n):
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
        tqdmbuffer = TqdmBuffer() if globConst.GUI_MODE else None
        for drop_index in tqdm(drop_indices_candidates, file=tqdmbuffer):
            if i == n:
                break
            drop_edge_candidate = edges.loc[drop_index]
            if (
                    edges_count_dict[drop_edge_candidate[globConst.NODE1_ID_COL_NAME]] > 1
                    and edges_count_dict[drop_edge_candidate[globConst.NODE2_ID_COL_NAME]] > 1
            ):
                edges_count_dict[drop_edge_candidate[globConst.NODE1_ID_COL_NAME]] = edges_count_dict[
                                                                                         drop_edge_candidate[
                                                                                             globConst.NODE1_ID_COL_NAME]] - 1
                edges_count_dict[drop_edge_candidate[globConst.NODE2_ID_COL_NAME]] = edges_count_dict[
                                                                                         drop_edge_candidate[
                                                                                             globConst.NODE2_ID_COL_NAME]] - 1
                drop_indices.append(drop_index)
                i += 1
        edges.drop(inplace=True, index=drop_indices)
        if i == n:
            break
    edges.reset_index(drop=True, inplace=True)
    return edges


def calc_corrupted_triples(pos_example, nodes, nodes_dic, filtered=False, path=None, pos_examples=None):
    """"
    calculates the corrupted triples (both corrupted heads as well as corrupted tails) for given true positive example
        Parameters
        ----------
            pos_examples : pandas.DataFrame #todo
                DataFrame with true examples of edges, columns = [node1_id, edgeType, node2_id]
            nodes : pandas.DataFrame #todo #todo
                DataFrame with all nodes of the graph columns = [node_id, node_type]
            filtered : bool, optional, default = True
                if filtered is true, filtered corrupted triples are created; that means, that only those corrupted triples,
                that do not exist in the graph, are kept
                if filtered is false, unfiltered corrupted triples are created; this means, that all corrupted triples are
                kept, even if they exist in the graph
            path : str, optional
                if provided, the corrupted triples are saved as csv files in the provided path; one file contains the corrupted heads, grouped by


        Returns
        ----------
    """
    filtered_corrupted_heads = None
    filtered_corrupted_tails = None
    head, relation, tail = pos_example
    head_node_type = nodes[np.where(nodes[:, 0] == head)][0, 1]
    corrupted_head_nodes = nodes_dic[head_node_type]
    corrupted_head_nodes = corrupted_head_nodes[corrupted_head_nodes != head]
    tail_node_type = nodes[np.where(nodes[:, 0] == tail)][0, 1]
    corrupted_tail_nodes = nodes_dic[tail_node_type]
    corrupted_tail_nodes = corrupted_tail_nodes[corrupted_tail_nodes != tail]

    # corrupting heads
    tail_array = np.full(len(corrupted_head_nodes), tail)
    relation_array = np.full(len(corrupted_head_nodes), relation)
    value_array = np.zeros(len(corrupted_head_nodes))
    unfiltered_corrupted_heads = np.column_stack((corrupted_head_nodes, relation_array, tail_array, value_array))

    # corrupting tails
    head_array = np.full(len(corrupted_tail_nodes), head)
    relation_array = np.full(len(corrupted_tail_nodes), relation)
    value_array = np.zeros(len(corrupted_tail_nodes))
    unfiltered_corrupted_tails = np.column_stack((head_array, relation_array, corrupted_tail_nodes, value_array))

    if filtered:
        filtered_corrupted_heads = _get_corrupted_examples(unfiltered_corrupted_heads[:, 0:3], pos_examples, True)
        filtered_corrupted_tails = _get_corrupted_examples(unfiltered_corrupted_tails[:, 0:3], pos_examples, True)

    # if path: #todo change to numpy #fixme what to do?
    #    all_corrupted_head = _group_corrupted_examples(unfiltered_corrupted_head_dict,
    #                                                   [evalConst.CORRUPTED_GROUP_COL_NAME]+list(pos_example)+[globConst.VALUE_COL_NAME])
    #    all_corrupted_tail = _group_corrupted_examples(unfiltered_corrupted_tail_dict,
    #                                                   [evalConst.CORRUPTED_GROUP_COL_NAME]+list(pos_example)+[globConst.VALUE_COL_NAME])
    #    all_corrupted_head.to_csv(os.path.join(path, evalConst.CORRUPTED_HEADS_FILE_NAME), sep='\t', index=False, header=False)
    #    all_corrupted_tail.to_csv(os.path.join(path, evalConst.CORRUPTED_TAILS_FILE_NAME), sep='\t', index=False, header=False)

    return unfiltered_corrupted_heads, unfiltered_corrupted_tails, filtered_corrupted_heads, filtered_corrupted_tails


def _get_corrupted_examples(corrupted_triples, pos_examples, filtered):
    """"
    Creates a dataset of corrupted triples according to the 'filtered' setting
        Parameters
        ----------
            corrupted_triples_df : pandas.DataFrame
                DataFrame with corrupted triples of one positive example, columns = [node1_id, edgeType, node2_id]
            pos_examples_df : pandas.DataFrame #todo
                DataFrame with all edges that are present in the graph (= positive examples), columns = [node1_id, edgeType, node2_id]
            filtered : bool
                if true, filtered setting is applied; that means, that only those corrupted triples, that do not exist in the graph, are kept
                if false, unfiltered setting is applied; this means, that all corrupted triples are kept, even if they exist in the graph

        Returns
        ----------
            corrupted_triples : pandas.DataFrame
                DataFrame contains all valid corrupted triples, incl value (1 for positive example, 0 for negative example)
                columns = [node1_id, edgeType, node2_id, value]
    """
    corrupted_triples_df = pd.DataFrame(corrupted_triples, columns=globConst.COL_NAMES_TRIPLES)
    pos_examples_df = pd.DataFrame(pos_examples, columns=globConst.COL_NAMES_TRIPLES)
    if filtered:
        corrupted_triples_df.reset_index(drop=True, inplace=True)
        import openbiolink.utils as ut
        true_neg_triples, _ = ut.get_diff(corrupted_triples_df, pos_examples_df)
        corrupted_triples_df = true_neg_triples
        corrupted_triples_df[globConst.VALUE_COL_NAME] = 0
    else:
        corrupted_triples_df[globConst.VALUE_COL_NAME] = 0
        # corrupted_triples[globConst.VALUE_COL_NAME][neg_indices] = 0
    return corrupted_triples_df.astype(float).astype(int).values


def _group_corrupted_examples(corrupted_dict, col_names):
    """"
     Parameters
     ----------
        corrupted_dict : dictionary
            dictionary of all corrupted triples, triple (head_id, relation_id, tail_id) as key,
            pandas.DataFrame with columns [head, relation, tail, value]
        col_names : list
            list of column names for [group, head_id, relation_id, tail_id, value]
            where value determines whether the triple exists (1) or not (0) in the graph
     Returns
     ----------
        all_corrupted : pandas.DataFrame
            pandas DataFrame of all triples grouped by true positive triple
            columns are [group, head_id, relation_id, tail_id, value, tp]
            the true positive example (tp) is always the first on a group of corrupted triples
    """
    i = 0
    # col_names = col_names + ['tp']
    all_corrupted = pd.DataFrame(columns=col_names)
    for key, df in sorted(corrupted_dict.items()):
        h, r, t = key
        true_example = pd.DataFrame([[h, r, t]], columns=list(df))
        # true_example['tp'] = 1
        true_example[col_names[4]] = 1
        true_example[col_names[0]] = i
        # todo should there be an extra column for tp?
        # df['tp'] = 0
        df[col_names[0]] = i
        all_corrupted = all_corrupted.append(true_example)
        all_corrupted = all_corrupted.append(df)
        i += 1
    return all_corrupted


def create_mappings(elements):
    element_label_to_id = {element_label: id for id, element_label in enumerate(elements)}
    return element_label_to_id


def map_elements(elements, mapping):
    return np.vectorize(mapping.get)(elements)
