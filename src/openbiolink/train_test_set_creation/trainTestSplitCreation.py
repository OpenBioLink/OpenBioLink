import logging
import math
import os
import random
import sys
from typing import Optional

import numpy as np
import pandas

import openbiolink.graphProperties as graphProp
from openbiolink import globalConfig, globalConfig as glob, utils
from openbiolink.graph_creation.metadata_edge import edgeMetadata as meta
from openbiolink.train_test_set_creation.sampler import NegativeSampler
from openbiolink.train_test_set_creation.trainTestSetWriter import TrainTestSetWriter
from openbiolink.train_test_set_creation import ttsConfig as ttsConf

random.seed(glob.RANDOM_STATE)
np.random.seed(glob.RANDOM_STATE)


class TrainTestSetCreation:
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

    def __init__(
            self,
            global_config: dict,
            graph_path,
            tn_graph_path,
            all_nodes_path,
            sep: Optional[str] = None,
            # meta_edge_triples=None, #nicetohave (1) split for subsample of edges, define own meta edges
            t_minus_one_graph_path=None,
            t_minus_one_tn_graph_path=None,
            t_minus_one_nodes_path=None,
            neg_train_val=False,
            neg_test=False
    ):
        self.neg_train_val = neg_train_val
        self.neg_test = neg_test

        if sep is None:
            sep = "\t"
        if _not_csv(graph_path):
            logging.error("graph path must be a csv file")
            sys.exit()
        if _not_csv(tn_graph_path):
            logging.error("tn_graph path must be a csv file")
            sys.exit()
        if _not_csv(all_nodes_path):
            logging.error("all_nodes path must be a csv file")
            sys.exit()
        if t_minus_one_graph_path is not None and _not_csv(t_minus_one_graph_path):
            logging.error("t_minus_one_graph path must be a csv file")
            sys.exit()
        if t_minus_one_tn_graph_path is not None and _not_csv(t_minus_one_tn_graph_path):
            logging.error("t_minus_one_tn_graph path must be a csv file")
            sys.exit()
        if t_minus_one_nodes_path is not None and _not_csv(t_minus_one_nodes_path):
            logging.error("t_minus_one_nodes path must be a csv file")
            sys.exit()

        self.identifier2type = global_config["IDENTIFIER_2_TYPE"]
        self.col_names_nodes = global_config["COL_NAMES_NODES"]
        self.col_names_edges = global_config["COL_NAMES_EDGES"]
        self.edge_type_col_name = global_config["EDGE_TYPE_COL_NAME"]
        self.value_col_name = global_config["VALUE_COL_NAME"]

        logging.info(f"loading nodes from {all_nodes_path}")
        self.all_nodes = pandas.read_csv(all_nodes_path, sep=sep, names=self.col_names_nodes)

        logging.info(f"loading positive edges from {graph_path}")
        self.all_tp = pandas.read_csv(graph_path, sep=sep, names=self.col_names_edges)
        self.all_tp[self.value_col_name] = 1
        self.tp_edgeTypes = list(self.all_tp[self.edge_type_col_name].unique())

        logging.info(f"loading negative edges from {tn_graph_path}")
        self.all_tn = pandas.read_csv(tn_graph_path, sep=sep, names=self.col_names_edges)
        self.all_tn[self.value_col_name] = 0

        self.tn_edgeTypes = list(self.all_tn[self.edge_type_col_name].unique())

        self.meta_edges_dic = {}

        for metaEdge in utils.get_leaf_subclasses(meta.EdgeMetadata):
            edge_type = str(metaEdge.EDGE_INMETA_CLASS.EDGE_TYPE)
            node1_type = str(metaEdge.EDGE_INMETA_CLASS.NODE1_TYPE)
            node2_type = str(metaEdge.EDGE_INMETA_CLASS.NODE2_TYPE)
            if edge_type in self.tp_edgeTypes:
                self.meta_edges_dic[f"{node1_type}_{edge_type}_{node2_type}"] = (node1_type, edge_type, node2_type)

        self.writer = TrainTestSetWriter(self.identifier2type)

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
            logging.error("either all three or none of these variables must be provided")
            sys.exit()
        if (
                t_minus_one_nodes_path is not None
                and t_minus_one_graph_path is not None
                and t_minus_one_tn_graph_path is not None
        ):
            self.tmo_nodes = pandas.read_csv(t_minus_one_nodes_path, sep=sep, names=self.col_names_nodes)

            self.tmo_all_tp = pandas.read_csv(t_minus_one_graph_path, sep=sep, names=self.col_names_edges,
                                              usecols=range(4))
            self.tmo_all_tp[self.value_col_name] = 1
            self.tmo_tp_edgeTypes = list(self.all_tp[self.edge_type_col_name].unique())

            self.tmo_all_tn = pandas.read_csv(t_minus_one_tn_graph_path, sep=sep, names=self.col_names_edges,
                                              usecols=range(4))
            self.tmo_all_tn[self.value_col_name] = 0
            self.tmo_tn_edgeTypes = list(self.all_tp[self.edge_type_col_name].unique())

    def random_edge_split(self, test_frac=None, val=None, crossval=None):
        logging.info(f"Creating random edge split with test_frac: {test_frac}, val_frac: {val}, crossval: {crossval}")
        # create positive and negative examples
        logging.info("Removing inconsistent edges from positive edges...")
        positive_samples = self.all_tp.copy()
        if self.neg_train_val or self.neg_test:
            logging.info("Generating negative samples")
            negative_sampler = NegativeSampler(self.meta_edges_dic, self.tn_edgeTypes, self.all_tn.copy(),
                                               self.all_nodes, self.identifier2type)
            negative_samples = negative_sampler.generate_random_neg_samples(positive_samples)
            all_samples = (positive_samples.append(negative_samples, ignore_index=True)).reset_index(drop=True)
        else:
            all_samples = positive_samples
        all_samples = utils.remove_inconsistent_edges(all_samples).reset_index(drop=True)

        # generate, train-, test-, validation-sets
        logging.info("Creating testset...")
        test_set = all_samples.sample(frac=test_frac, random_state=globalConfig.RANDOM_STATE)
        train_val_set = all_samples.drop(list(test_set.index.values))

        logging.info("Removing parent duplicates and reverses from testset...")
        test_set = utils.remove_parent_duplicates_and_reverses(remain_set=test_set, remove_set=train_val_set)

        train_val_nodes = self.get_nodes(train_val_set, self.neg_train_val)

        test_set, new_test_nodes = self.filter(train_val_set, self.neg_train_val, test_set, self.neg_test, "test")

        if graphProp.DIRECTED:
            logging.info("Removing reverse edges from train-val set")
            train_val_set = utils.remove_reverse_edges(remain_set=train_val_set, remove_set=test_set)

        # single train/test/val split
        if 0 < val < 1 and not float(val).is_integer() and not crossval:
            logging.info("Creating validation set ...")
            rand_index = list(train_val_set.index)
            random.shuffle(rand_index)

            val_indices, train_indices = np.array_split(rand_index, [int(len(rand_index) * val)])

            train_set, val_set, new_val_nodes = self.perform_val_split(train_val_set, train_val_nodes, train_indices, val_indices)

            train_nodes = self.get_nodes(train_set, self.neg_train_val)
            val_nodes = self.get_nodes(val_set, self.neg_train_val)
            
            test_set, new_test_nodes = self.filter(train_set, self.neg_train_val, test_set, self.neg_test, "test")
            test_set_nodes = self.get_nodes(test_set, self.neg_test)

            positive_train_samples, negative_train_samples = self.split_positive_negative(train_set)
            positive_test_samples, negative_test_samples = self.split_positive_negative(test_set)
            positive_val_samples, negative_val_samples = self.split_positive_negative(val_set)

            # write train set
            self.writer.write_set(positive_train_samples, ttsConf.TRAIN_FILE_NAME)
            self.writer.write_nodes(set(train_nodes), ttsConf.TRAIN_NODES_FILE_NAME)

            # write test set
            self.writer.write_set(positive_test_samples, ttsConf.TEST_FILE_NAME)
            self.writer.write_nodes(set(test_set_nodes), ttsConf.TEST_NODES_FILE_NAME)
            self.writer.write_new_nodes(new_test_nodes, ttsConf.NEW_TEST_NODES_FILE_NAME)

            # write val set
            self.writer.write_set(positive_val_samples, ttsConf.VAL_FILE_NAME)
            self.writer.write_nodes(set(val_nodes), ttsConf.VAL_NODES_FILE_NAME)
            self.writer.write_new_nodes(new_val_nodes, ttsConf.NEW_VAL_NODES_FILE_NAME)

            if self.neg_train_val:
                self.writer.write_set(negative_train_samples, ttsConf.NEGATIVE_PREFIX + ttsConf.TRAIN_FILE_NAME)
                self.writer.write_set(negative_val_samples, ttsConf.NEGATIVE_PREFIX + ttsConf.VAL_FILE_NAME)
            if self.neg_test:
                self.writer.write_set(negative_test_samples, ttsConf.NEGATIVE_PREFIX + ttsConf.TEST_FILE_NAME)


        # only train/test split or crossval
        else:
            test_set, new_test_nodes = self.filter(train_val_set, self.neg_train_val, test_set, self.neg_test, "test")
            test_set_nodes = self.get_nodes(test_set, self.neg_test)
            
            positive_train_val_samples, negative_train_val_samples = self.split_positive_negative(train_val_set)
            positive_test_samples, negative_test_samples = self.split_positive_negative(test_set)

            # write train_val set
            self.writer.write_set(positive_train_val_samples, ttsConf.TRAIN_FILE_NAME)
            self.writer.write_nodes(set(train_val_nodes), ttsConf.TRAIN_VAL_NODES_FILE_NAME)

            # write test set
            self.writer.write_set(positive_test_samples, ttsConf.TEST_FILE_NAME)
            self.writer.write_nodes(set(test_set_nodes), ttsConf.TEST_NODES_FILE_NAME)
            self.writer.write_new_nodes(new_test_nodes, ttsConf.NEW_TEST_NODES_FILE_NAME)

            # generate and write negative samples
            if self.neg_train_val:
                self.writer.write_set(negative_train_val_samples, ttsConf.NEGATIVE_PREFIX + ttsConf.TRAIN_FILE_NAME)
            if self.neg_test:
                self.writer.write_set(negative_test_samples, ttsConf.NEGATIVE_PREFIX + ttsConf.TEST_FILE_NAME)

            if 0 < val < 1 and not float(val).is_integer() and crossval:
                # split with crossvalidation
                logging.info("Performing cross validation on trainingset...")
                self.create_and_write_cross_val(train_val_set, train_val_nodes, test_set, val)
        logging.info("Done splitting!")
        # nicetohave (3) option to remove examples with new nodes

    def split_positive_negative(self, samples):
        # return positive, negative
        return samples.loc[lambda x: x[self.value_col_name] == 1], samples.loc[lambda x: x[self.value_col_name] == 0]
        
    def filter(self, remain_df, include_negative_remain, filter_df, include_negative_filter, filter_name):
        new_nodes = set(self.get_nodes(filter_df, include_negative_filter)) - set(self.get_nodes(remain_df, include_negative_remain))
        if len(new_nodes) > 0:
            logging.info(
                f"The {filter_name} set contains nodes, that are not present in the trainings-set. These edges will be dropped."
            )  # nicetohave (6): option to keep edges with new nodes
            filter_df = self.remove_edges_with_nodes(filter_df, new_nodes)
        return(filter_df, new_nodes)

    def get_nodes(self, samples, negatives_included):
        if negatives_included:
            return samples[globalConfig.NODE1_ID_COL_NAME].tolist() + samples[globalConfig.NODE2_ID_COL_NAME].tolist()
        else:
            return samples.loc[lambda x: x[self.value_col_name] == 1][globalConfig.NODE1_ID_COL_NAME].tolist() + \
                   samples.loc[lambda x: x[self.value_col_name] == 1][globalConfig.NODE2_ID_COL_NAME].tolist()


    def time_slice_split(self):
        # nicetohave (4) like that, neg samples are restricted to edge_types appearing in test_sample --> good idea?
        # nicetohave (4) idea: calculate nodes like above, then tmo_nodes= test_nodes --> mehr auswahl bei neg examples
        tmo_positive_samples = self.tmo_all_tp
        tmo_negative_sampler = NegativeSampler(
            self.meta_edges_dic, self.tmo_tn_edgeTypes, self.tmo_all_tn, self.tmo_nodes, self.identifier2type
        )
        tmo_negative_samples = tmo_negative_sampler.generate_random_neg_samples(tmo_positive_samples)
        # todo remove not consistent edges
        tmo_negative_samples[globalConfig.VALUE_COL_NAME] = 0
        tmo_all_samples = (tmo_positive_samples.append(tmo_negative_samples, ignore_index=True)).reset_index(
            drop=True
        )  # todo ist append nicht in pace?
        train_set = tmo_all_samples
        test_positive_samples, vanished_positive_samples = utils.get_diff(
            self.all_tp, self.tmo_all_tp, ignore_qscore=True
        )
        test_tn_samples, vanished_tn_samples = utils.get_diff(self.all_tn, self.tmo_all_tn, ignore_qscore=True)
        if not vanished_positive_samples.empty or not vanished_tn_samples.empty:
            logging.info("Some edges existing in the first time slice are no longer present in the second one")
            self.writer.print_vanished_edges(vanished_positive_samples.append(vanished_tn_samples))
        test_negative_sampler = NegativeSampler(self.meta_edges_dic, self.tn_edgeTypes, test_tn_samples, self.all_nodes,
                                                self.identifier2type)
        test_negative_samples = test_negative_sampler.generate_random_neg_samples(test_positive_samples)
        test_negative_samples[globalConfig.VALUE_COL_NAME] = 0

        test_set = (test_positive_samples.append(test_negative_samples, ignore_index=True)).reset_index(drop=True)
        test_set = utils.remove_parent_duplicates_and_reverses(remain_set=test_set, remove_set=train_set)
        new_test_nodes = self.get_additional_nodes(
            old_nodes_list=self.tmo_nodes[globalConfig.ID_NODE_COL_NAME].tolist(),
            new_nodes_list=self.all_nodes[globalConfig.ID_NODE_COL_NAME].tolist(),
        )
        if new_test_nodes:
            logging.info(
                "The test set contains nodes that are not present in the trainings-set. These edges will be removed."
            )  # nicetohave (6)
            test_set = self.remove_edges_with_nodes(test_set, new_test_nodes)

        if graphProp.DIRECTED:
            train_set = utils.remove_reverse_edges(remain_set=train_set, remove_set=test_set)

        train_set_nodes = (
                train_set[globalConfig.NODE1_ID_COL_NAME].tolist() + train_set[globalConfig.NODE2_ID_COL_NAME].tolist()
        )
        test_set_nodes = (
                test_set[globalConfig.NODE1_ID_COL_NAME].tolist() + test_set[globalConfig.NODE2_ID_COL_NAME].tolist()
        )

        self.writer.write_set(train_set, ttsConf.TRAIN_FILE_NAME)
        self.writer.write_nodes(set(train_set_nodes), ttsConf.TRAIN_VAL_NODES_FILE_NAME)
        self.writer.write_set(test_set, ttsConf.TEST_FILE_NAME)
        self.writer.write_nodes(set(test_set_nodes), ttsConf.TEST_NODES_FILE_NAME)
        self.writer.write_new_nodes(new_test_nodes, ttsConf.NEW_TEST_NODES_FILE_NAME)

        # niceToHave (5) slice size?
        # extra nur für diff? --> eig nciht --> eig schon weil nur pos

    @staticmethod
    def remove_edges_with_nodes(samples: pandas.DataFrame, nodes: set):
        """
        :param samples: pandas.DataFrame containing edges of the samples, node col names according to globalConfig
        :param nodes: list of new nodes
        :return: returns samples pandas.DataFrame with all edges, that contain a node from new_nodes, removed
        """
        new_node_in_edge = samples[globalConfig.NODE1_ID_COL_NAME].isin(nodes) | samples[
            globalConfig.NODE2_ID_COL_NAME
        ].isin(nodes)
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

    def create_and_write_cross_val(self, train_val_set: pandas.DataFrame, nodes_in_train_val_set, test_set: pandas.DataFrame, n_folds):
        nel_total, _ = train_val_set.shape
        if n_folds == 0 or n_folds == 1 or (n_folds > 1 and not float(n_folds).is_integer()):
            logging.error("provided folds are not possible!")
            raise Exception(
                "fold entry must be either an int>1 (number of folds) or a float >0 and <1 (validation fraction)"
            )

        if n_folds < 1:  # n_folds is fraction
            n_folds = math.ceil(1 / n_folds)
        n_folds = int(n_folds)

        rand_index = list(train_val_set.index)
        random.shuffle(rand_index)
        chunks = np.array_split(rand_index, n_folds)

        for i in range(n_folds):
            logging.info(f"Creating fold number {i + 1} ...")
            # train_chunk_indices and val_chunk_index are the indices of the respective chunks
            # f.e. for the first fold of a 10 crossval: train_chunk_indices = [0,1,2,3,4,5,6,7,8]; val_chunk_index = 9
            train_chunk_indices = [(x + i) % n_folds for x in range(n_folds - 1)]
            val_chunk_index = (n_folds - 1 + i) % n_folds
            train_indices = [element for chunk_index in train_chunk_indices for element in chunks[chunk_index]]
            val_indices = chunks[val_chunk_index]

            train_set, val_set, new_val_nodes = self.perform_val_split(train_val_set, nodes_in_train_val_set, train_indices, val_indices)
            
            test_set, new_test_nodes = self.filter(train_set, self.neg_train_val, test_set, self.neg_test, "test")

            train_set_nodes = self.get_nodes(train_set, self.neg_train_val)
            val_set_nodes = self.get_nodes(val_set, self.neg_train_val)
            test_set_nodes = self.get_nodes(test_set, self.neg_test)

            fold_folder_path = self.writer.get_fold_path(i)
            os.makedirs(fold_folder_path, exist_ok=True)

            positive_train_samples = train_set.loc[lambda x: x[self.value_col_name] == 1]
            positive_val_samples = val_set.loc[lambda x: x[self.value_col_name] == 1]
            positive_test_samples = test_set.loc[lambda x: x[self.value_col_name] == 1]
            negative_train_samples = train_set.loc[lambda x: x[self.value_col_name] == 0]
            negative_val_samples = val_set.loc[lambda x: x[self.value_col_name] == 0]
            negative_test_samples = test_set.loc[lambda x: x[self.value_col_name] == 0]
            
            self.writer.write_set(positive_train_samples, ttsConf.TRAIN_FILE_NAME, fold_folder_path)
            self.writer.write_nodes(set(train_set_nodes), ttsConf.TRAIN_NODES_FILE_NAME, fold_folder_path)

            self.writer.write_set(positive_val_samples, ttsConf.VAL_FILE_NAME, fold_folder_path)
            self.writer.write_nodes(set(val_set_nodes), ttsConf.VAL_NODES_FILE_NAME, fold_folder_path)
            self.writer.write_new_nodes(new_val_nodes, ttsConf.NEW_VAL_NODES_FILE_NAME, fold_folder_path)
            
            self.writer.write_set(positive_test_samples, ttsConf.TEST_FILE_NAME, fold_folder_path)
            self.writer.write_nodes(set(test_set_nodes), ttsConf.TEST_NODES_FILE_NAME, fold_folder_path)
            self.writer.write_new_nodes(new_test_nodes, ttsConf.NEW_TEST_NODES_FILE_NAME, fold_folder_path)

            if self.neg_train_val:
                self.writer.write_set(negative_train_samples, ttsConf.NEGATIVE_PREFIX + ttsConf.TRAIN_FILE_NAME,
                                      fold_folder_path)
                self.writer.write_set(negative_val_samples, ttsConf.NEGATIVE_PREFIX + ttsConf.VAL_FILE_NAME,
                                      fold_folder_path)
            if self.neg_test:
                self.writer.write_set(negative_test_samples, ttsConf.NEGATIVE_PREFIX + ttsConf.TEST_FILE_NAME, 
                                      fold_folder_path)

    def perform_val_split(self, train_val_set, nodes_in_train_val_set, train_indices, val_indices):
        train_set = train_val_set.loc[train_indices]
        val_set = train_val_set.loc[val_indices]

        new_val_nodes = self.get_additional_nodes(
            old_nodes_list=train_set[globalConfig.NODE1_ID_COL_NAME].tolist()
                           + train_set[globalConfig.NODE2_ID_COL_NAME].tolist(),
            new_nodes_list=nodes_in_train_val_set,
        )
        if len(new_val_nodes) > 0:  # nicetohave (6)
            logging.info(
                f"Validation set contains nodes that are"
                f" not present in the training set. These edges will be dropped."
            )
            val_set = self.remove_edges_with_nodes(val_set, new_val_nodes)
        if graphProp.DIRECTED:
            train_set = utils.remove_reverse_edges(remain_set=train_set, remove_set=val_set)
        val_set = utils.remove_parent_duplicates_and_reverses(remain_set=val_set, remove_set=train_set)
        return train_set, val_set, new_val_nodes


def _not_csv(f):
    return os.path.splitext(f)[1] not in {".csv", ".tsv"}
