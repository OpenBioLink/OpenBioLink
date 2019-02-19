import math

import pandas
import random

import graph_creation.globalConstant as glob
RANDOM_STATE = 42 # do not change for reproducibility
random.seed(RANDOM_STATE)

def random_edge_split(graph_path, tn_graph_path, val_frac=None, test_frac = None, crossval= None, folds = None):
    ''' not weighted, just random split of all edges '''
    if not val_frac:
        val_frac = 0.2
    if not test_frac:
        test_frac = 0.2

    with open(graph_path) as file:
        graph = pandas.read_csv(file, sep='\t', names=['id1, edgeType, id2, qscore'])
    with open(tn_graph_path) as file:
        tn_graph = pandas.read_csv(file, sep='\t', names=['id1, edgeType, id2, qscore'])

    if glob.DIRECTED:
        pass
    else:
        test_set = graph.sample(frac= test_frac, random_state= RANDOM_STATE)

        train_val_graph = graph.drop(list(test_set.index.values))
        if crossval:
            if folds:
                train_val_set_tuples = create_cross_val(train_val_graph, folds)
            else:
                train_val_set_tuples = create_cross_val(train_val_graph, val_frac)
        else:
            train_set = train_val_graph.sample(frac=(1-val_frac), random_state=RANDOM_STATE)
            val_set = train_val_graph.drop(list(train_set.index.vales))
            train_val_set_tuples = [(train_set, val_set)]
    #todo insert output (0 and 1)
    #todo generate negative exapmles
    return (train_val_set_tuples, test_set)

def remove_parent_child_edges():
    pass

def remove_bidir_edges():
    pass


def create_cross_val (df, n):
    nol, _ = len(df.index.list(df.index.values))
    # n can be n-fold or fraction
    if n<1:
        n = math.ceil(n*nol)
    nel_per_chunk = math.ceil(nol / n)

    #shuffle indices
    rand_index = random.shuffle(list(df.index.values))

    # create bounds for n chunks
    bounds = []
    for i in range(n):
        bounds.append(i*nel_per_chunk)
    bounds.append(nol)

    #create n index chunks
    chunks = []
    for i in range(n):
        chunks.append(rand_index[bounds[i]: bounds[i+1]])

    # create n folds with indices for (train_set, val_set)
    folds = []
    for i in range(n):
        train = [element for group_i in [(x+i)%n for x in range(n-1)] for element in chunks[group_i]]
        val = chunks[(n-1+i)%n]
        folds.append((train,val))

    # convert index folds to df folds
    df_folds= []
    for train, val in folds:
        df_folds.append((df.loc[train], df.loc[val]))

    return df_folds

