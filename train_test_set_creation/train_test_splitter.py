import math
import random

import numpy
import pandas

import graph_creation.graphCreationConfig as glob
import graph_creation.utils as utils

RANDOM_STATE = 42 # do not change for reproducibility
random.seed(RANDOM_STATE)
numpy.random.seed(RANDOM_STATE)
COL_NAMES_EDGES = ['id1', 'edgeType', 'id2', 'qscore']


# TODO: random per edgeType (equally dist vs original dist)

def random_edge_split(graph_path, tn_graph_path, nodes_path, val_frac=None, test_frac = None, crossval= None, folds = None, meta_edge_triples=None): #todo change to list of graph and tn graph files

    if not val_frac:
        val_frac = 0.2
    if not test_frac:
        test_frac = 0.2
    known_meta_edges = False
    if not meta_edge_triples:
        import graph_creation.metadata_edge.edgeMetadata as meta
        meta_edge_triples = [( str(x.EDGE_INMETA_CLASS.NODE1_TYPE), str(x.EDGE_INMETA_CLASS.EDGE_TYPE), str(x.EDGE_INMETA_CLASS.NODE2_TYPE) )
                             for x in utils.get_leaf_subclasses(meta.EdgeMetadata)]         #todo ? maybe convert all types to enums ?
        known_meta_edges=True

    # get nodes and node types
    with open(nodes_path) as file:
        nodes = pandas.read_csv(file, sep='\t', names=['id', 'nodeType'])

    # get all positive examples
    with open(graph_path) as file:
        positive_samples = pandas.read_csv(file, sep='\t', names=COL_NAMES_EDGES)
        positive_samples['value'] = 1
        #todo ? maybe convert all types to enums ?
    #edgeTypes = list(positive_samples['edgeType'].unique())
    meta_edges_dic = {edge_type : (node1_type, node2_type) for node1_type, edge_type, node2_type in meta_edge_triples if edge_type in edgeTypes}
    #fixme list of triples

    #get true negative examples
    negative_samples = pandas.DataFrame(columns=list(positive_samples))
    with open(tn_graph_path) as file:
        all_tn = pandas.read_csv(file, sep='\t', names=COL_NAMES_EDGES)
        all_tn['value'] = 0
    tn_edgeTypes = list(all_tn['edgeType'].unique())
    #fixme list of triples

    #todo per edgeType

    # generate random distribution of meta_edge types for negative samples
    num_tp_examples, _ = positive_samples.shape
    negative_samples_metaEdges = (list(numpy.random.choice(edgeTypes,num_tp_examples)))
    negative_samples_metaEdges.sort()
    negative_samples_count_metaEdges = {e: negative_samples_metaEdges.count(e) for e in set(negative_samples_metaEdges)}

    #generate a negative sub-sample for each negative meta_edge type
    # TODO: no self loops in neg samples, not reproducible(?)
    for edgeType, count in sorted(negative_samples_count_metaEdges.items()):
        if edgeType in tn_edgeTypes:
            edgeType_tn = all_tn.loc[all_tn['edgeType'] == edgeType]
            count_existing_tn, _ = edgeType_tn.shape
            if count <= count_existing_tn:
                random_tn_sample = edgeType_tn.sample(n=count, random_state=RANDOM_STATE)
                negative_samples = negative_samples.append(random_tn_sample, ignore_index=True)
            else:
                random_tn_sample = edgeType_tn.sample(n=count_existing_tn, random_state=RANDOM_STATE)
                negative_samples= negative_samples.append(random_tn_sample, ignore_index=True)
                exclude_df = positive_samples.loc[positive_samples['edgeType'] == edgeType].append( negative_samples, ignore_index=True)
                negative_samples = negative_samples.append(generate_n_random_samples(n=(count - count_existing_tn),
                                                                  nodes=nodes, nodeTypes=meta_edges_dic[edgeType],
                                                                  edgeType=edgeType, exclude_df=exclude_df)
                                                           ,ignore_index=True )
        else:
            exclude_df = positive_samples.loc[positive_samples['edgeType'] == edgeType].append(negative_samples,
                                                                                               ignore_index=True)

            negative_samples = negative_samples.append(generate_n_random_samples(n=count,nodes=nodes,
                                                                                 nodeTypes=meta_edges_dic[edgeType],
                                                                                 edgeType=edgeType,exclude_df=exclude_df)
                                                       ,ignore_index=True )
            #todo why are id1 and edgeType wrong order

    negative_samples['value'] = 0
    all_samples = (positive_samples.append(negative_samples, ignore_index=True)).reset_index(drop=True)

    #generate, train-, test-, validation-sets
    test_set = None
    train_val_set_tuples = None
    if glob.DIRECTED: #todo change here
        test_set = all_samples.sample(frac= test_frac, random_state=RANDOM_STATE)
        train_set = all_samples.drop(list(test_set.index.values))
        train_set= remove_bidir_edges(remain_set=train_set, remove_set=test_set)

         #fixme implement biased random split
    else:
        test_set = all_samples.sample(frac= test_frac, random_state= RANDOM_STATE)
        train_set = all_samples.drop(list(test_set.index.values))
        if crossval:
            if folds:
                train_val_set_tuples = create_cross_val(train_set, folds)
            else:
                train_val_set_tuples = create_cross_val(train_set, val_frac)
        else:
            train_set = train_set.sample(frac=(1-val_frac), random_state=RANDOM_STATE)
            val_set = train_set.drop(list(train_set.index.values))
            train_val_set_tuples = [(train_set, val_set)]
        # (sub)sample negative examples
        # only provided TN
        # provided + equally distributed
        # original distribution + providing (some) tn ?

    return (train_val_set_tuples, test_set)


def remove_parent_child_edges():
    pass


def remove_bidir_edges(remain_set, remove_set):
    remain_set = remain_set.drop(list(remove_set.index.values),errors='ignore')
    #todo better?
    remove_set.columns = ['edgeType','id2',  'id1', 'qscore', 'value']
    temp = pandas.merge(remain_set, remove_set,how='left', left_on=['id1', 'id2', 'edgeType'], right_on=['id1', 'id2','edgeType'] ).set_index(remain_set.index)
    remove = temp[(temp['value_x']==temp['value_y'])] #todo value should always be different? are there examples with diff qscore?
    remain = remain_set.drop(remove.index.values)
    return remain




def create_cross_val (df, n):
    #fixme append should not be inplace??
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


def generate_n_random_samples(n, nodes, nodeTypes, edgeType, exclude_df):
    samples = pandas.DataFrame(columns=COL_NAMES_EDGES)
    nodeType1, nodeType2 = nodeTypes
    nodes_nodeType1 = nodes.loc[nodes['nodeType']==nodeType1]
    num_nodes1, _ = nodes_nodeType1.shape
    nodes_nodeType2 = nodes.loc[nodes['nodeType']==nodeType2]
    num_nodes2, _ = nodes_nodeType2.shape

    i=0
    while True:
        node1 = nodes_nodeType1.sample(n=1, random_state=(RANDOM_STATE+i))
        node1.reset_index() #increment random_state so each loop generates new example
        node2 = nodes_nodeType2.sample(n=1, random_state=(RANDOM_STATE+50000+i))
        node2.reset_index() #choose different random_state in case nodeTypes are the same (no self_loops)
        if not ( ((exclude_df['id1'] == node1.iloc[0].id) &
                  (exclude_df['id2'] == node2.iloc[0].id )&
                  (exclude_df['edgeType'] == edgeType)).any() or
                 (node1.iloc[0].id == node2.iloc[0].id) ) : #no self loops
            samples = samples.append(pandas.DataFrame([[node1.iloc[0].id, edgeType, node2.iloc[0].id,0]],
                                            columns=COL_NAMES_EDGES), ignore_index=True )
            exclude_df = exclude_df.append(pandas.DataFrame([[node1.iloc[0].id, edgeType, node2.iloc[0].id, 0]],
                                                      columns=COL_NAMES_EDGES), ignore_index=True)
            num_samples, _ = samples.shape
            if num_samples>= n:
                break
        i+=1
        if i >= num_nodes1*num_nodes2:
            #fixme throw error not enough samples could be genereated from set
            break
    return samples








