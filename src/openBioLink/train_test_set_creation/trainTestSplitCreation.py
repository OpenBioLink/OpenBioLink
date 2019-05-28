import math
import random
import logging
import numpy
import pandas

from .. import graphProperties as graphProp
from .. import utils
from .sampler import NegativeSampler
from .trainTestSetWriter import TrainTestSetWriter

RANDOM_STATE = 42  # do not change for reproducibility
random.seed(RANDOM_STATE)
numpy.random.seed(RANDOM_STATE)
COL_NAMES_EDGES = ['id1', 'edgeType', 'id2', 'qscore']
COL_NAMES_SAMPLES = ['id1', 'edgeType', 'id2', 'qscore', 'value']


# TODO: no self loops in neg samples, not reproducible(?)


class TrainTestSetCreation():
    def __init__(self,
                 graph_path,
                 tn_graph_path,
                 nodes_path,
                 sep='\t',
                 #meta_edge_triples=None, #todo split for subsample of edges
                 t_minus_one_graph_path=None,
                 t_minus_one_tn_graph_path=None,
                 t_minus_one_nodes_path=None):

        meta_edge_triples = None #todo split for subsample of edges


        with open(nodes_path) as file:
            self.nodes = pandas.read_csv(file, sep=sep, names=['id', 'nodeType'])

        with open(graph_path) as file:
            self.all_tp = pandas.read_csv(file, sep=sep, names=COL_NAMES_EDGES)
            self.all_tp['value'] = 1
        self.tp_edgeTypes = list(self.all_tp['edgeType'].unique())

        with open(tn_graph_path) as file:
            self.all_tn = pandas.read_csv(file, sep=sep, names=COL_NAMES_EDGES)
            self.all_tn['value'] = 0
        self.tn_edgeTypes = list(self.all_tn['edgeType'].unique())

        self.meta_edges_dic = {}
        if not meta_edge_triples:
            from ..graph_creation.metadata_edge import edgeMetadata as meta
            for metaEdge in utils.get_leaf_subclasses(meta.EdgeMetadata):
                edgeType =  str(metaEdge.EDGE_INMETA_CLASS.EDGE_TYPE)
                node1Type = str(metaEdge.EDGE_INMETA_CLASS.NODE1_TYPE)
                node2Type = str(metaEdge.EDGE_INMETA_CLASS.NODE2_TYPE)
                if edgeType in self.tp_edgeTypes:
                    self.meta_edges_dic['%s_%s_%s'%(node1Type,edgeType,node2Type)] = (node1Type, edgeType, node2Type)
        else:
            for node1Type, edgeType, node2Type in meta_edge_triples:
                self.meta_edges_dic['%s_%s_%s' % (node1Type, edgeType, node2Type)] = (node1Type, edgeType, node2Type)
                #todo does this work?

        # check for transient onto edges
        transitiv_IS_A_edges = utils.check_for_transitive_edges(self.all_tp[self.all_tp['edgeType'] == 'IS_A'])
        transitiv_PART_OF_edges = utils.check_for_transitive_edges(self.all_tp[self.all_tp['edgeType'] == 'PART_OF'])
        if transitiv_IS_A_edges:
            print('WARNING: transient edges in IS_A: ({a},b,c) for a IS_A b and a IS_A c', transitiv_IS_A_edges)
        if transitiv_PART_OF_edges:
            print('WARNING: transient edges in PART_OF: ({a},b,c) for a PART_OF b and a PART_OF c',
                  transitiv_PART_OF_edges)

        #for time slices
        if not ((bool(t_minus_one_graph_path) == bool(t_minus_one_tn_graph_path)) == (bool(t_minus_one_nodes_path))):
            logging.error('either all three or none of these variables must be provided') #todo better + exit
        if t_minus_one_nodes_path and t_minus_one_graph_path and t_minus_one_tn_graph_path:
            with open(t_minus_one_nodes_path) as file:
                self.tmo_nodes = pandas.read_csv(file, sep=sep, names=['id', 'nodeType'])

            with open(t_minus_one_graph_path) as file:
                self.tmo_all_tp = pandas.read_csv(file, sep=sep, names=COL_NAMES_EDGES)
                self.tmo_all_tp['value'] = 1
            self.tmo_tp_edgeTypes = list(self.all_tp['edgeType'].unique())

            with open(t_minus_one_tn_graph_path) as file:
                self.tmo_all_tn = pandas.read_csv(file, sep=sep, names=COL_NAMES_EDGES)
                self.tmo_all_tn['value'] = 1
            self.tmo_tn_edgeTypes = list(self.all_tp['edgeType'].unique())



    def random_edge_split(self, test_frac=None, val=None, crossval=None):
        if not val:
            val = 0.2
        if not test_frac:
            test_frac = 0.2

        # create positive and negative examples
        positive_samples = self.all_tp
        negative_sampler = NegativeSampler(self.meta_edges_dic,self.tn_edgeTypes,self.all_tn, self.nodes, COL_NAMES_EDGES)
        negative_samples = negative_sampler.generate_random_neg_samples(positive_samples)
        all_samples = (positive_samples.append(negative_samples, ignore_index=True)).reset_index(drop=True)

        # generate, train-, test-, validation-sets
        test_set = all_samples.sample(frac=test_frac, random_state=RANDOM_STATE)
        train_val_set = all_samples.drop(list(test_set.index.values))
        nodes_in_train_val_set = train_val_set['id1'].tolist()+train_val_set['id2'].tolist()
        new_test_nodes = self.get_additional_nodes(old_nodes_list=nodes_in_train_val_set,
                                                   new_nodes_list=self.nodes['id'].tolist())
        if graphProp.DIRECTED:
            train_val_set = utils.remove_bidir_edges(remain_set=train_val_set, remove_set=test_set)
        if crossval:
            train_val_set_tuples = self.create_cross_val(train_val_set, val)
            new_val_nodes = [self.get_additional_nodes(t['id1'].tolist()+t['id2'].tolist(), nodes_in_train_val_set)
                             for t,v, in train_val_set_tuples]
        else:
            #train_set = train_val_set.sample(frac=(1 - val_frac), random_state=RANDOM_STATE)
            #val_set = train_val_set.drop(list(train_set.index.values))
            train_val_set_tuples = [(train_val_set, pandas.DataFrame())]
            new_val_nodes = None
        if graphProp.DIRECTED:
            train_val_set_tuples = [(utils.remove_bidir_edges(remain_set=t, remove_set=v),v)
                                    for t,v in train_val_set_tuples]
        writer = TrainTestSetWriter(COL_NAMES_SAMPLES)
        writer.print_sets(train_val_set_tuples=train_val_set_tuples,
                          new_val_nodes=new_val_nodes,
                          test_set=test_set,
                          new_test_nodes=new_test_nodes)
        #todo remove examples with new nodes?
        return (train_val_set_tuples, test_set)



    def time_slice_split(self):
        new_test_nodes = self.get_additional_nodes(self.tmo_nodes['id'].tolist(), self.nodes['id'].tolist())
        tmo_positive_samples = self.tmo_all_tp
        tmo_negative_sampler = NegativeSampler(self.meta_edges_dic,
                                           self.tmo_tn_edgeTypes,
                                           self.tmo_all_tn,
                                           self.tmo_nodes,
                                           COL_NAMES_EDGES)
        tmo_negative_samples = tmo_negative_sampler.generate_random_neg_samples(tmo_positive_samples)
        tmo_all_samples = (tmo_positive_samples.append(tmo_negative_samples, ignore_index=True)).reset_index(drop=True)
        train_set = tmo_all_samples
        test_positive_samples, vanished_positive_samples = utils.get_diff(self.all_tp, self.tmo_all_tp)
        test_tn_samples, vanished_tn_samples = utils.get_diff(self.all_tn, self.tmo_all_tn)
        test_negative_sampler = NegativeSampler(self.meta_edges_dic,
                                           self.tn_edgeTypes,
                                           test_tn_samples,
                                           self.nodes,
                                           COL_NAMES_EDGES)
        #todo like that, neg samples are restricted to edge_types appearing in test_sample --> good idea?
        test_negative_samples = test_negative_sampler.generate_random_neg_samples(test_positive_samples)

        test_set = (test_positive_samples.append(test_negative_samples, ignore_index=True)).reset_index(drop=True)
        if graphProp.DIRECTED:
            train_set = utils.remove_bidir_edges(remain_set=train_set, remove_set=test_set)

        train_val_set_tuple = (train_set,pandas.DataFrame())
        writer = TrainTestSetWriter(COL_NAMES_SAMPLES)
        writer.print_sets(train_val_set_tuples=[train_val_set_tuple],
                          test_set=test_set,
                          new_test_nodes=new_test_nodes)
        return (train_val_set_tuple, test_set)

        #todo diff zwischen nodes --> warning / info
        # diff zwischen time slices
        # slice size?
        # extra nur für diff? --> eig nciht --> eig schon weil nur pos



    @staticmethod
    def get_additional_nodes(old_nodes_list: list, new_nodes_list:list):
        old_set = set(old_nodes_list)
        new_set = set(new_nodes_list)
        return new_set-old_set


    @staticmethod
    def create_cross_val(df, n_folds):
        nel_total, _ = df.shape
        if n_folds < 1: #n_folds is fraction
            n_folds = math.ceil(1/n_folds)
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
