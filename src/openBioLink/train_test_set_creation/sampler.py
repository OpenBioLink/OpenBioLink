import numpy
import pandas
from tqdm import tqdm

import openbiolink.train_test_set_creation.ttsConfig as ttsConst
from openbiolink import globalConfig as globConst
from openbiolink import utils


class Sampler():

    def __init__(self, meta_edges_dic, nodes):
        self.meta_edges_dic = meta_edges_dic
        self.nodes = nodes

    def generate_n_random_samples(self, n, node_type_1, edge_type, node_type_2, exclude_df):
        exclude_df = exclude_df[globConst.COL_NAMES_EDGES]
        samples = pandas.DataFrame(columns=globConst.COL_NAMES_EDGES)
        nodes_nodeType1 = self.nodes.loc[self.nodes[globConst.NODE_TYPE_COL_NAME] == node_type_1]
        num_nodes1, _ = nodes_nodeType1.shape
        nodes_nodeType2 = self.nodes.loc[self.nodes[globConst.NODE_TYPE_COL_NAME] == node_type_2]
        num_nodes2, _ = nodes_nodeType2.shape
        i = 0
        while len(samples) < n:
            if i > 100:
                break
            num_examples = n - len(samples)
            node1_list = nodes_nodeType1.sample(n=num_examples, random_state=(globConst.RANDOM_STATE + i), replace=True)
            node1_list = node1_list.id.tolist()
            node2_list = nodes_nodeType2.sample(n=num_examples, random_state=(globConst.RANDOM_STATE + (i + 100)),
                                                replace=True)
            node2_list = node2_list.id.tolist()
            sample_candidates = pandas.DataFrame(data={globConst.NODE1_ID_COL_NAME: node1_list,
                                                       globConst.EDGE_TYPE_COL_NAME: [edge_type] * num_examples,
                                                       globConst.NODE2_ID_COL_NAME: node2_list,
                                                       })
            _, sub_samples = utils.get_diff(exclude_df[globConst.COL_NAMES_TRIPLES], sample_candidates)
            sub_samples.drop_duplicates(inplace=True)
            sub_samples[globConst.QSCORE_COL_NAME] = [None] * len(sub_samples)
            samples = samples.append(sub_samples, ignore_index=True)
            exclude_df = exclude_df.append(pandas.DataFrame(sub_samples))
            i += 1
            # todo auswirkungen if num neg examples != num pos examples
        return samples


class NegativeSampler(Sampler):
    def __init__(self, meta_edges_dic, tn_edgeTypes, all_tn, nodes):
        super().__init__(meta_edges_dic, nodes)
        self.meta_edges_dic = meta_edges_dic
        self.tn_edgeTypes = tn_edgeTypes
        self.all_tn = all_tn
        self.all_tn = self.add_edge_type_key_column(all_tn)

    def add_edge_type_key_column(self, df):
        df[ttsConst.EDGE_TYPE_KEY_NAME] = df[globConst.NODE1_ID_COL_NAME].str.split('_').map(lambda x: x[0]) \
                                          + '_' + df[globConst.EDGE_TYPE_COL_NAME] + '_' \
                                          + df[globConst.NODE2_ID_COL_NAME].str.split('_').map(lambda x: x[0])
        return df

    def generate_random_neg_samples(self, pos_samples, distrib='orig'):
        col_names = globConst.COL_NAMES_EDGES
        pos_samples = pos_samples[col_names]
        neg_samples = pandas.DataFrame(columns=col_names)
        pos_samples = self.add_edge_type_key_column(pos_samples)

        # generate distribution of meta_edge types for negative samples
        meta_edges = list(self.meta_edges_dic.keys())
        meta_edges.sort()
        neg_samples_count_meta_edges = {}
        if distrib == 'uni':
            num_tp_examples, _ = pos_samples.shape
            neg_samples_metaEdges = (list(numpy.random.choice(meta_edges, num_tp_examples)))
            neg_samples_metaEdges.sort()
            neg_samples_count_meta_edges = {e: neg_samples_metaEdges.count(e) for e in
                                            set(neg_samples_metaEdges) if neg_samples_metaEdges.count(e) > 0}
        elif distrib == 'orig':
            for key in self.meta_edges_dic.keys():
                num_entry = len(pos_samples.loc[(pos_samples[ttsConst.EDGE_TYPE_KEY_NAME] == key)])
                if num_entry > 0:
                    neg_samples_count_meta_edges[key] = num_entry

        # generate a negative sub-sample for each negative meta_edge type
        for meta_edge_triple_key, count in tqdm(sorted(neg_samples_count_meta_edges.items())):
            node_type_1, edge_type, node_type_2 = self.meta_edges_dic[meta_edge_triple_key]
            pos_samples_of_meta_edge = pos_samples.loc[
                (pos_samples[ttsConst.EDGE_TYPE_KEY_NAME] == meta_edge_triple_key)]

            if edge_type in self.tn_edgeTypes:  # only onto edgesTypes can appear multiple times, there should be no onto tn
                neg_samples = neg_samples.append(self.subsample_with_tn(meta_edge_triple_key=meta_edge_triple_key,
                                                                        subsample_size=count,
                                                                        exclude_df=pos_samples_of_meta_edge[col_names])
                                                 , ignore_index=True)
            else:
                neg_samples = neg_samples.append(self.generate_n_random_samples(n=count,
                                                                                node_type_1=node_type_1,
                                                                                edge_type=edge_type,
                                                                                node_type_2=node_type_2,
                                                                                exclude_df=pos_samples_of_meta_edge[
                                                                                    col_names])
                                                 , ignore_index=True)
        neg_samples[globConst.VALUE_COL_NAME] = 0

        return neg_samples[col_names + [globConst.VALUE_COL_NAME]]

    def subsample_with_tn(self, meta_edge_triple_key, subsample_size, exclude_df, col_names=globConst.COL_NAMES_EDGES):
        node_type_1, edge_type, node_type_2 = self.meta_edges_dic[meta_edge_triple_key]
        tn_examples = self.all_tn.loc[self.all_tn[ttsConst.EDGE_TYPE_KEY_NAME] == meta_edge_triple_key]  # testme
        count_existing_tn, _ = tn_examples.shape
        if subsample_size <= count_existing_tn:
            neg_samples = tn_examples.sample(n=subsample_size, random_state=globConst.RANDOM_STATE)
        else:
            exclude_df = exclude_df.append(tn_examples)
            neg_samples = tn_examples
            neg_samples = neg_samples.append(self.generate_n_random_samples(n=(subsample_size - count_existing_tn),
                                                                            node_type_1=node_type_1,
                                                                            edge_type=edge_type,
                                                                            node_type_2=node_type_2,
                                                                            exclude_df=exclude_df))
        neg_samples.reset_index(inplace=True)

        return neg_samples[col_names]
