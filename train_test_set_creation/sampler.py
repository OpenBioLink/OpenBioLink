import pandas
import numpy

RANDOM_STATE = 42
COL_NAMES_EDGES = ['id1', 'edgeType', 'id2', 'qscore']


class Sampler():
    def __init__(self, meta_edges_dic,col_names_edges, nodes):
        self.meta_edges_dic = meta_edges_dic
        global COL_NAMES_EDGES
        COL_NAMES_EDGES = col_names_edges
        self.nodes= nodes


    def generate_n_random_samples(self, n, nodeType1, edgeType, nodeType2, exclude_df):
        #nodeType1, edgeType, nodeType2 = self.meta_edges_dic[meta_edge_triple_key]
        samples = pandas.DataFrame(columns=COL_NAMES_EDGES)
        nodes_nodeType1 = self.nodes.loc[self.nodes['nodeType'] == nodeType1]
        num_nodes1, _ = nodes_nodeType1.shape
        nodes_nodeType2 = self.nodes.loc[self.nodes['nodeType'] == nodeType2]
        num_nodes2, _ = nodes_nodeType2.shape

        i = 0
        while True:
            node1 = nodes_nodeType1.sample(n=1, random_state=(RANDOM_STATE+i))
            node1.reset_index()
            node2 = nodes_nodeType2.sample(n=1, random_state=(RANDOM_STATE+((i+100)%13)))
            node2.reset_index()
            if not (((exclude_df['id1'] == node1.iloc[0].id) &
                     (exclude_df['id2'] == node2.iloc[0].id) &
                     (exclude_df['edgeType'] == edgeType)).any() or
                    (node1.iloc[0].id == node2.iloc[0].id)):  # no self loops
                samples = samples.append(pandas.DataFrame([[node1.iloc[0].id, edgeType, node2.iloc[0].id, 0]],
                                                          columns=COL_NAMES_EDGES),
                                         ignore_index=True)
                exclude_df = exclude_df.append(pandas.DataFrame([[node1.iloc[0].id, edgeType, node2.iloc[0].id, 0]],
                                                                columns=COL_NAMES_EDGES),
                                               ignore_index=True)
                num_samples, _ = samples.shape
                if num_samples >= n:
                    break
            i += 1
            if i >= num_nodes1 * num_nodes2:
                # fixme throw error not enough samples could be genereated from set
                break
        return samples



class NegativeSampler(Sampler):
    def __init__(self, meta_edges_dic, tn_edgeTypes, all_tn, nodes, col_names_edges):

        super().__init__(meta_edges_dic, col_names_edges, nodes)
        self.meta_edges_dic = meta_edges_dic
        self.tn_edgeTypes = tn_edgeTypes
        self.all_tn = all_tn

    def generate_random_neg_samples(self, pos_samples, distrib ='orig'):
        neg_samples = pandas.DataFrame(columns=list(pos_samples))

        # generate random distribution of meta_edge types for negative samples
        meta_edges = list(self.meta_edges_dic.keys())
        meta_edges.sort()
        neg_samples_count_metaEdges = {}
        if distrib == 'uni':
            num_tp_examples, _ = pos_samples.shape
            neg_samples_metaEdges = (list(numpy.random.choice(meta_edges, num_tp_examples)))
            neg_samples_metaEdges.sort()
            neg_samples_count_metaEdges = {e: neg_samples_metaEdges.count(e) for e in
                                                set(neg_samples_metaEdges)}
        elif distrib =='orig':
            for key, value in self.meta_edges_dic.items():
                nodeType1, edgeType, nodeType2 = value
                neg_samples_count_metaEdges[key] = len(pos_samples.loc[(pos_samples['id1'].str.startswith(nodeType1)) &
                                                       (pos_samples['edgeType'] == edgeType) &
                                                       (pos_samples['id2'].str.startswith(nodeType2))])
                # todo count positive examples with edgetype

        # generate a negative sub-sample for each negative meta_edge type
        for meta_edge_triple_key, count in sorted(neg_samples_count_metaEdges.items()):
            nodeType1, edgeType, nodeType2 = self.meta_edges_dic[meta_edge_triple_key]
            pos_samples_of_meta_edge = pos_samples.loc[(pos_samples['id1'].str.startswith(nodeType1)) &
                                                       (pos_samples['edgeType'] == edgeType) &
                                                       (pos_samples['id2'].str.startswith(nodeType2))]
            #todo why don't we need this?
            #exclude_df = exclude_df.append(neg_samples,ignore_index=True)
            if edgeType in self.tn_edgeTypes: #only onto edgesTypes can appear multiple times, there should be no onto tn
                neg_samples = neg_samples.append(self.subsample_with_tn(meta_edge_triple_key=meta_edge_triple_key,
                                                                        count=count,
                                                                        col_names=list(pos_samples),
                                                                        exclude_df=pos_samples_of_meta_edge))
            else:
                neg_samples = neg_samples.append(self.generate_n_random_samples(n=count,
                                                                                        nodeType1=nodeType1,
                                                                                        edgeType=edgeType,
                                                                                        nodeType2=nodeType2,
                                                                                        exclude_df=pos_samples_of_meta_edge)
                                                           , ignore_index=True)
        neg_samples['value'] = 0

        return neg_samples



    def subsample_with_tn(self, meta_edge_triple_key, count, col_names, exclude_df):
        neg_samples = pandas.DataFrame(columns=col_names)
        nodeType1, edgeType, nodeType2 = self.meta_edges_dic[meta_edge_triple_key]
        tn_examples = self.all_tn.loc[(self.all_tn['id1'].str.startswith(nodeType1)) &
                                              (self.all_tn['edgeType'] == edgeType)&
                                              (self.all_tn['id2'].str.startswith(nodeType2))]
        count_existing_tn, _ = tn_examples.shape
        if count <= count_existing_tn:
            random_tn_sample = tn_examples.sample(n=count, random_state=RANDOM_STATE)
            neg_samples = neg_samples.append(random_tn_sample, ignore_index=True)
        else:
            random_tn_sample = tn_examples.sample(n=count_existing_tn, random_state=RANDOM_STATE)
            exclude_df = exclude_df.append(random_tn_sample)
            neg_samples = neg_samples.append(random_tn_sample, ignore_index=True)
            neg_samples = neg_samples.append(
                self.generate_n_random_samples(n=(count - count_existing_tn),
                                                       nodeType1=nodeType1,
                                                       edgeType=edgeType,
                                                       nodeType2=nodeType2,
                                                       exclude_df=exclude_df)
                , ignore_index=True)
        return neg_samples


    def generate_corrupted_neg_samples(self):
        pass