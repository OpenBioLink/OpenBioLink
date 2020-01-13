import logging
import math
import random
import sys

import numpy
import pandas

import openbiolink.graphProperties as graphProp
from openbiolink import globalConfig
from openbiolink import globalConfig as glob
from openbiolink import utils
from openbiolink.graph_creation.metadata_edge import edgeMetadata as meta
from openbiolink.train_test_set_creation.sampler import NegativeSampler
from openbiolink.train_test_set_creation.trainTestSetWriter import TrainTestSetWriter

random.seed(glob.RANDOM_STATE)
numpy.random.seed(glob.RANDOM_STATE)


class TrainTestSetCreation():
    """
    Manager class for handling the creation of train test splits given a graph

        Attributes
                ----------
                    all_nodes : pandas.DataFrame
                        DataFrame with all nodes, columns = globalConfig.COL_NAMES_NODES
                    all_tp : pandas.DataFrame
                        DataFrame with edges from the positive graph, i.e. all positive examples
                        columns = globalConfig.COL_NAMES_EDGES + globalConfig.VALUE_COL_NAME
                    tp_edgeTypes : [str]
                        list of all edge types present in the positive examples
                    all_tn : pandas.DataFrame
                        DataFrame with edges from the negative graph, i.e. all negative examples
                        columns = globalConfig.COL_NAMES_EDGES + globalConfig.VALUE_COL_NAME
                    tn_edgeTypes : [str]
                        list of all edge types present in the negative examples
                    meta_edges_dic : {str: (str, str, str)}
                        dictionary for all possible h,r,t combinations, mapped to their types. The key consists of
                        %s_%s_%s'%(node1Type,edgeType,node2Type) the value (node1Type, edgeType, node2Type)
                    tmo_nodes : pandas.DataFrame
                        DataFrame with all nodes present in the t-1 graph, columns = globalConfig.COL_NAMES_NODES
                    tmo_all_tp : pandas.DataFrame
                        DataFrame with edges from the positive t-1 graph, i.e. all positive t-1 examples
                        columns = globalConfig.COL_NAMES_EDGES + globalConfig.VALUE_COL_NAME
                    tmo_tp_edgeTypes : [str]
                        list of all edge types present in the positive t-1 examples
                    tmo_all_tn : pandas.DataFrame
                        DataFrame with edges from the negative t-1 graph, i.e. all negative t-1 examples
                        columns = globalConfig.COL_NAMES_EDGES + globalConfig.VALUE_COL_NAME
                    tmo_tn_edgeTypes : [str]
                        list of all edge types present in the negative t-1 examples

    """

    def __init__(self,
                 graph_path,
                 tn_graph_path,
                 all_nodes_path,
                 sep='\t',
                 # meta_edge_triples=None, #nicetohave (1) split for subsample of edges, define own meta edges
                 t_minus_one_graph_path=None,
                 t_minus_one_tn_graph_path=None,
                 t_minus_one_nodes_path=None):

        self.writer = TrainTestSetWriter()
        with open(all_nodes_path) as file:
            self.all_nodes = pandas.read_csv(file, sep=sep, names=globalConfig.COL_NAMES_NODES)
            self.all_nodes = self.all_nodes.sort_values(by=globalConfig.COL_NAMES_NODES).reset_index(drop=True)

        with open(graph_path) as file:
            self.all_tp = pandas.read_csv(file, sep=sep, names=globalConfig.COL_NAMES_EDGES)
            self.all_tp[globalConfig.VALUE_COL_NAME] = 1
            self.all_tp = self.all_tp.sort_values(by=globalConfig.COL_NAMES_EDGES).reset_index(drop=True)
        self.tp_edgeTypes = list(self.all_tp[globalConfig.EDGE_TYPE_COL_NAME].unique())

        with open(tn_graph_path) as file:
            self.all_tn = pandas.read_csv(file, sep=sep, names=globalConfig.COL_NAMES_EDGES)
            self.all_tn[globalConfig.VALUE_COL_NAME] = 0
            self.all_tn = self.all_tn.sort_values(by=globalConfig.COL_NAMES_EDGES).reset_index(drop=True)

        self.tn_edgeTypes = list(self.all_tn[globalConfig.EDGE_TYPE_COL_NAME].unique())

        self.meta_edges_dic = {}

        for metaEdge in utils.get_leaf_subclasses(meta.EdgeMetadata):
            edgeType = str(metaEdge.EDGE_INMETA_CLASS.EDGE_TYPE)
            node1Type = str(metaEdge.EDGE_INMETA_CLASS.NODE1_TYPE)
            node2Type = str(metaEdge.EDGE_INMETA_CLASS.NODE2_TYPE)
            if edgeType in self.tp_edgeTypes:
                self.meta_edges_dic['%s_%s_%s' % (node1Type, edgeType, node2Type)] = (node1Type, edgeType, node2Type)

        # nicetohave (2) check for transient onto edges
        # transitiv_IS_A_edges = utils.check_for_transitive_edges(self.all_tp[self.all_tp[ttsConst.EDGE_TYPE_COL_NAME] == 'IS_A'])
        # transitiv_PART_OF_edges = utils.check_for_transitive_edges(self.all_tp[self.all_tp[ttsConst.EDGE_TYPE_COL_NAME] == 'PART_OF'])
        # if transitiv_IS_A_edges:
        #    print('WARNING: transient edges in IS_A: ({a},b,c) for a IS_A b and a IS_A c', transitiv_IS_A_edges)
        # if transitiv_PART_OF_edges:
        #    print('WARNING: transient edges in PART_OF: ({a},b,c) for a PART_OF b and a PART_OF c',
        #          transitiv_PART_OF_edges)

        # for time slices
        if not (bool(t_minus_one_graph_path) == bool(t_minus_one_tn_graph_path) == (bool(t_minus_one_nodes_path))):
            logging.error('either all three or none of these variables must be provided')
            sys.exit()
        if t_minus_one_nodes_path and t_minus_one_graph_path and t_minus_one_tn_graph_path:
            with open(t_minus_one_nodes_path) as file:
                self.tmo_nodes = pandas.read_csv(file, sep=sep, names=globalConfig.COL_NAMES_NODES)
                self.tmo_nodes = self.tmo_nodes.sort_values(by=globalConfig.COL_NAMES_NODES).reset_index(drop=True)

            with open(t_minus_one_graph_path) as file:
                self.tmo_all_tp = pandas.read_csv(file, sep=sep, names=globalConfig.COL_NAMES_EDGES)
                self.tmo_all_tp[globalConfig.VALUE_COL_NAME] = 1
                self.tmo_all_tp = self.tmo_all_tp.sort_values(by=globalConfig.COL_NAMES_EDGES).reset_index(drop=True)
            self.tmo_tp_edgeTypes = list(self.all_tp[globalConfig.EDGE_TYPE_COL_NAME].unique())

            with open(t_minus_one_tn_graph_path) as file:
                self.tmo_all_tn = pandas.read_csv(file, sep=sep, names=globalConfig.COL_NAMES_EDGES)
                self.tmo_all_tn[globalConfig.VALUE_COL_NAME] = 0
                self.tmo_all_tn = self.tmo_all_tn.sort_values(by=globalConfig.COL_NAMES_EDGES).reset_index(drop=True)
            self.tmo_tn_edgeTypes = list(self.all_tp[globalConfig.EDGE_TYPE_COL_NAME].unique())

    def random_edge_split(self, test_frac=None, val=None, crossval=None):
        if not val:
            val = 0.2
        if not test_frac:
            test_frac = 0.2

        # create positive and negative examples
        positive_samples = self.all_tp.copy()
        negative_sampler = NegativeSampler(self.meta_edges_dic, self.tn_edgeTypes, self.all_tn.copy(), self.all_nodes)
        negative_samples = negative_sampler.generate_random_neg_samples(positive_samples)
        all_samples = (positive_samples.append(negative_samples, ignore_index=True)).reset_index(drop=True)
        all_samples = utils.remove_inconsistent_edges(all_samples).reset_index(drop=True)

        # generate, train-, test-, validation-sets
        test_set = all_samples.sample(frac=test_frac, random_state=glob.RANDOM_STATE)
        train_val_set = all_samples.drop(list(test_set.index.values))
        test_set = utils.remove_parent_duplicates_and_reverses(remain_set=test_set, remove_set=train_val_set)

        nodes_in_train_val_set = train_val_set[globalConfig.NODE1_ID_COL_NAME].tolist() \
                                 + train_val_set[globalConfig.NODE2_ID_COL_NAME].tolist()
        new_test_nodes = self.get_additional_nodes(old_nodes_list=nodes_in_train_val_set,
                                                   new_nodes_list=self.all_nodes[
                                                       globalConfig.ID_NODE_COL_NAME].tolist())
        if new_test_nodes:
            logging.info(
                'The test set contains nodes, that are not present in the trainings-set. These edges will be dropped.')  # nicetohave (6): option to keep edges with new nodes
            test_set = self.remove_edges_with_nodes(test_set, new_test_nodes)
        nodes_in_test_set = test_set[globalConfig.NODE1_ID_COL_NAME].tolist() \
                            + test_set[globalConfig.NODE2_ID_COL_NAME].tolist()
        if graphProp.DIRECTED:
            train_val_set = utils.remove_reverse_edges(remain_set=train_val_set, remove_set=test_set)

        if crossval:
            train_val_set_tuples = self.create_cross_val(train_val_set, val)
            new_val_nodes = None
            for i, train_val_set_tuple in enumerate(train_val_set_tuples):
                train_set, val_set = train_val_set_tuple
                new_val_nodes = self.get_additional_nodes(
                    old_nodes_list=train_set[globalConfig.NODE1_ID_COL_NAME].tolist()
                                   + train_set[globalConfig.NODE2_ID_COL_NAME].tolist(),
                    new_nodes_list=nodes_in_train_val_set)
                if new_val_nodes:  # nicetohave (6)
                    logging.info(
                        'Validation set %d contains nodes, that are not present in the trainings-set. These edges will be dropped.' % i)
                    val_set = self.remove_edges_with_nodes(val_set, new_val_nodes)
                    train_val_set_tuples[i] = (train_set, val_set)

        else:
            train_val_set_tuples = [(train_val_set, pandas.DataFrame())]
            new_val_nodes = None
        if graphProp.DIRECTED:
            train_val_set_tuples = [(utils.remove_reverse_edges(remain_set=t, remove_set=v), v)
                                    for t, v in train_val_set_tuples]
        train_val_set_tuples = [(t, utils.remove_parent_duplicates_and_reverses(remain_set=v, remove_set=t))
                                for t, v in train_val_set_tuples]

        self.writer.print_sets(train_val_set_tuples=train_val_set_tuples,
                               new_val_nodes=new_val_nodes,
                               test_set=test_set,
                               new_test_nodes=new_test_nodes,
                               nodes_in_train_val_set=set(nodes_in_train_val_set),
                               nodes_in_test_set=set(nodes_in_test_set))
        # nicetohave (3) option to remove examples with new nodes
        return train_val_set_tuples, test_set

    def time_slice_split(self):

        # nicetohave (4) like that, neg samples are restricted to edge_types appearing in test_sample --> good idea?
        # nicetohave (4) idea: calculate nodes like above, then tmo_nodes= test_nodes --> mehr auswahl bei neg examples
        tmo_positive_samples = self.tmo_all_tp
        tmo_negative_sampler = NegativeSampler(self.meta_edges_dic,
                                               self.tmo_tn_edgeTypes,
                                               self.tmo_all_tn,
                                               self.tmo_nodes)
        tmo_negative_samples = tmo_negative_sampler.generate_random_neg_samples(tmo_positive_samples)
        # todo remove not consistent edges
        tmo_negative_samples[globalConfig.VALUE_COL_NAME] = 0
        tmo_all_samples = (tmo_positive_samples.append(tmo_negative_samples, ignore_index=True)).reset_index(
            drop=True)  # todo ist append nicht in pace?
        train_set = tmo_all_samples
        test_positive_samples, vanished_positive_samples = utils.get_diff(self.all_tp, self.tmo_all_tp,
                                                                          ignore_qscore=True)
        test_tn_samples, vanished_tn_samples = utils.get_diff(self.all_tn, self.tmo_all_tn, ignore_qscore=True)
        if not vanished_positive_samples.empty or not vanished_tn_samples.empty:
            logging.info('Some edges existing in the first time slice are no longer present in the second one')
            self.writer.print_vanished_edges(vanished_positive_samples.append(vanished_tn_samples))
        test_negative_sampler = NegativeSampler(self.meta_edges_dic,
                                                self.tn_edgeTypes,
                                                test_tn_samples,
                                                self.all_nodes)
        test_negative_samples = test_negative_sampler.generate_random_neg_samples(test_positive_samples)
        test_negative_samples[globalConfig.VALUE_COL_NAME] = 0

        test_set = (test_positive_samples.append(test_negative_samples, ignore_index=True)).reset_index(drop=True)
        test_set = utils.remove_parent_duplicates_and_reverses(remain_set=test_set, remove_set=train_set)
        new_test_nodes = self.get_additional_nodes(
            old_nodes_list=self.tmo_nodes[globalConfig.ID_NODE_COL_NAME].tolist(),
            new_nodes_list=self.all_nodes[globalConfig.ID_NODE_COL_NAME].tolist())
        if new_test_nodes:
            logging.info(
                'The test set contains nodes, that are not present in the trainings-set. These edges will be removed.')  # nicetohave (6)
            test_set = self.remove_edges_with_nodes(test_set, new_test_nodes)

        if graphProp.DIRECTED:
            train_set = utils.remove_reverse_edges(remain_set=train_set, remove_set=test_set)

        train_val_set_tuples = [(train_set, pandas.DataFrame())]
        nodes_in_train_set = train_set[globalConfig.NODE1_ID_COL_NAME].tolist() \
                             + train_set[globalConfig.NODE2_ID_COL_NAME].tolist()
        nodes_in_test_set = test_set[globalConfig.NODE1_ID_COL_NAME].tolist() \
                            + test_set[globalConfig.NODE2_ID_COL_NAME].tolist()
        self.writer.print_sets(train_val_set_tuples=train_val_set_tuples,
                               test_set=test_set,
                               nodes_in_train_val_set=nodes_in_train_set,
                               nodes_in_test_set=nodes_in_test_set,
                               new_test_nodes=new_test_nodes)
        return (train_val_set_tuples, test_set)

        # niceToHave (5) slice size?
        # extra nur für diff? --> eig nciht --> eig schon weil nur pos

    @staticmethod
    def remove_edges_with_nodes(samples: pandas.DataFrame, nodes: set):
        """
        :param samples: pandas.DataFrame containing edges of the samples, node col names according to globalConfig
        :param nodes: list of new nodes
        :return: returns samples pandas.DataFrame with all edges, that contain a node from new_nodes, removed
        """
        new_node_in_edge = samples[globalConfig.NODE1_ID_COL_NAME].isin(nodes) \
                           | samples[globalConfig.NODE2_ID_COL_NAME].isin(nodes)
        edges_with_new_nodes = samples.loc[new_node_in_edge]
        return samples.drop(list(edges_with_new_nodes.index.values))

    @staticmethod
    def get_additional_nodes(old_nodes_list: list, new_nodes_list: list):
        """

        :param old_nodes_list:
        :param new_nodes_list:
        :return: returns a set containing all nodes that are in new_nodes_list but not in old_nodes_list
        """
        old_set = set(old_nodes_list)
        new_set = set(new_nodes_list)
        return new_set - old_set

    @staticmethod
    def create_cross_val(df: pandas.DataFrame, n_folds):
        nel_total, _ = df.shape
        if n_folds == 0 or n_folds == 1 or (n_folds > 1 and not float(n_folds).is_integer()):
            logging.error("provided folds are not possible!")
            raise Exception(
                "fold entry must be either an int>1 (number of folds) or a float >0 and <1 (validation fraction)")

        if n_folds < 1:  # n_folds is fraction
            n_folds = math.ceil(1 / n_folds)
        n_folds = int(n_folds)
        nel_per_chunk = math.ceil(nel_total / n_folds)
        rand_index = list(df.index.values)
        random.shuffle(rand_index)

        bounds = []
        for i in range(n_folds):
            bounds.append(i * nel_per_chunk)
        bounds.append(nel_total)

        chunks = []
        for i in range(n_folds):
            chunks.append(rand_index[bounds[i]: bounds[i + 1]])

        folds_indices = []
        for i in range(n_folds):
            train_chunk_indices = [(x + i) % n_folds for x in range(n_folds - 1)]
            val_chunk_index = (n_folds - 1 + i) % n_folds
            train_indices = [element for chunk_index in train_chunk_indices for element in chunks[chunk_index]]
            val_indices = chunks[val_chunk_index]
            folds_indices.append((train_indices, val_indices))

        folds = []
        for train_indices, val_indices in folds_indices:
            folds.append((df.loc[train_indices], df.loc[val_indices]))

        return folds
