import math
import random

import numpy
import pandas

import graphProperties as graphProp
import graph_creation.utils as graph_utils
import train_test_set_creation.utils as tts_utils
from .trainTestSetWriter import TrainTestSetWriter
from .sampler import NegativeSampler


RANDOM_STATE = 42  # do not change for reproducibility
random.seed(RANDOM_STATE)
numpy.random.seed(RANDOM_STATE)
COL_NAMES_EDGES = ['id1', 'edgeType', 'id2', 'qscore']
COL_NAMES_SAMPLES = ['id1', 'edgeType', 'id2', 'qscore', 'value']


# TODO: random per edgeType (equally dist vs original dist)
# TODO: no self loops in neg samples, not reproducible(?)

# (sub)sample negative examples
# only provided TN
# provided + equally distributed
# original distribution + providing (some) tn ?


class TrainTestSetCreation():
    def __init__(self, graph_path, tn_graph_path, nodes_path, meta_edge_triples=None):

        with open(nodes_path) as file:
            self.nodes = pandas.read_csv(file, sep='\t', names=['id', 'nodeType'])

        with open(graph_path) as file:
            self.all_tp = pandas.read_csv(file, sep='\t', names=COL_NAMES_EDGES)
            self.all_tp['value'] = 1
        self.tp_edgeTypes = list(self.all_tp['edgeType'].unique())

        with open(tn_graph_path) as file:
            self.all_tn = pandas.read_csv(file, sep='\t', names=COL_NAMES_EDGES)
            self.all_tn['value'] = 0
        self.tn_edgeTypes = list(self.all_tn['edgeType'].unique())

        self.meta_edges_dic = {}
        if not meta_edge_triples:
            import graph_creation.metadata_edge.edgeMetadata as meta
            for metaEdge in graph_utils.get_leaf_subclasses(meta.EdgeMetadata):
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
        transitiv_IS_A_edges = tts_utils.check_for_transitive_edges(self.all_tp[self.all_tp['edgeType'] == 'IS_A'])
        transitiv_PART_OF_edges = tts_utils.check_for_transitive_edges(self.all_tp[self.all_tp['edgeType'] == 'PART_OF'])
        if transitiv_IS_A_edges:
            print('WARNING: transient edges in IS_A: ({a},b,c) for a IS_A b and a IS_A c', transitiv_IS_A_edges)
        if transitiv_PART_OF_edges:
            print('WARNING: transient edges in PART_OF: ({a},b,c) for a PART_OF b and a PART_OF c',
                  transitiv_PART_OF_edges)


    def random_edge_split(self, val_frac=None, test_frac=None, crossval=None, folds=None):  # todo change to list of graph and tn graph files
        if not val_frac:
            val_frac = 0.2
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
        if graphProp.DIRECTED:
            train_val_set = tts_utils.remove_bidir_edges(remain_set=train_val_set, remove_set=test_set)
        if crossval:
            if folds:
                train_val_set_tuples = self.create_cross_val(train_val_set, folds)
            else:
                train_val_set_tuples = self.create_cross_val(train_val_set, val_frac)
        else:
            train_set = train_val_set.sample(frac=(1 - val_frac), random_state=RANDOM_STATE)
            val_set = train_val_set.drop(list(train_set.index.values))
            train_val_set_tuples = [(train_set, val_set)]
        if graphProp.DIRECTED:
            train_val_set_tuples = [(tts_utils.remove_bidir_edges(remain_set=t, remove_set=v),v)
                                    for t,v in train_val_set_tuples]
        writer = TrainTestSetWriter(COL_NAMES_SAMPLES)
        writer.print_sets(train_val_set_tuples,test_set)
        return (train_val_set_tuples, test_set)


    def time_slice_split(self):
        #todo
        pass


    def create_cross_val(self, df, n_folds):
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
