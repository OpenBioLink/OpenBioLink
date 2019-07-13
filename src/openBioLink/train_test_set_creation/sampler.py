import pandas
import numpy

import globalConfig
import globalConfig as globConst

class Sampler():
    def __init__(self, meta_edges_dic, nodes):
        self.meta_edges_dic = meta_edges_dic
        self.nodes= nodes


    def generate_n_random_samples(self, n, nodeType1, edgeType, nodeType2, exclude_df):
        samples = pandas.DataFrame(columns=globalConfig.COL_NAMES_EDGES)
        nodes_nodeType1 = self.nodes.loc[self.nodes[globConst.NODE_TYPE_COL_NAME] == nodeType1]
        num_nodes1, _ = nodes_nodeType1.shape
        nodes_nodeType2 = self.nodes.loc[self.nodes[globConst.NODE_TYPE_COL_NAME] == nodeType2]
        num_nodes2, _ = nodes_nodeType2.shape

        i = 0
        while True:
            #todo better way of selecing two random but reproducable nodes
            node1 = nodes_nodeType1.sample(n=1, random_state=(globConst.RANDOM_STATE + i))
            node1.reset_index()
            node2 = nodes_nodeType2.sample(n=1, random_state=(globConst.RANDOM_STATE + ((i + 100) % 13)))
            node2.reset_index()
            if not (((exclude_df[globConst.NODE1_ID_COL_NAME] == node1.iloc[0].id) &
                     (exclude_df[globConst.NODE2_ID_COL_NAME] == node2.iloc[0].id) &
                     (exclude_df[globConst.EDGE_TYPE_COL_NAME] == edgeType)) or #testme if works without any
                    (node1.iloc[0].id == node2.iloc[0].id)):  # no self loops
                samples = samples.append(pandas.DataFrame([[node1.iloc[0].id, edgeType, node2.iloc[0].id, 0]],
                                                          columns=globalConfig.COL_NAMES_EDGES),
                                         ignore_index=True)
                exclude_df = exclude_df.append(pandas.DataFrame([[node1.iloc[0].id, edgeType, node2.iloc[0].id, 0]],
                                                                columns=globalConfig.COL_NAMES_EDGES),
                                               ignore_index=True)
                num_samples, _ = samples.shape
                if num_samples >= n:
                    break
            i += 1
            if i >= num_nodes1 * num_nodes2:
                # testme

                message = 'Not enough examples could be generated for edge type %s %s %s, num_nodes1=%d, num_nodes2=%d'
                if globConst.GUI_MODE:
                    import gui.gui as gui
                    gui.askForExit(message)
                    break
                elif globConst.INTERACTIVE_MODE:
                    import cli.Cli as cli #testme
                    cli.ask_for_exit(message)
                    break
                else:
                    import sys
                    sys.exit()

        return samples



class NegativeSampler(Sampler):
    def __init__(self, meta_edges_dic, tn_edgeTypes, all_tn, nodes):
        super().__init__(meta_edges_dic, nodes)
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
                                                set(neg_samples_metaEdges) if neg_samples_metaEdges.count(e)> 0}
        elif distrib =='orig':
            for key, value in self.meta_edges_dic.items():
                nodeType1, edgeType, nodeType2 = value
                num_entry = len(pos_samples.loc[(pos_samples[globConst.NODE1_ID_COL_NAME].str.startswith(nodeType1)) &
                                                       (pos_samples[globConst.EDGE_TYPE_COL_NAME] == edgeType) &
                                                       (pos_samples[globConst.NODE2_ID_COL_NAME].str.startswith(nodeType2))])
                if num_entry>0:
                    neg_samples_count_metaEdges[key] = num_entry
                # todo count positive examples with edgetype

        # generate a negative sub-sample for each negative meta_edge type
        for meta_edge_triple_key, count in sorted(neg_samples_count_metaEdges.items()):
            nodeType1, edgeType, nodeType2 = self.meta_edges_dic[meta_edge_triple_key]
            pos_samples_of_meta_edge = pos_samples.loc[(pos_samples[globConst.NODE1_ID_COL_NAME].str.startswith(nodeType1)) &
                                                       (pos_samples[globConst.EDGE_TYPE_COL_NAME] == edgeType) &
                                                       (pos_samples[globConst.NODE2_ID_COL_NAME].str.startswith(nodeType2))]
            #testme why don't we need this?
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
        neg_samples[globConst.VALUE_COL_NAME] = 0

        return neg_samples



    def subsample_with_tn(self, meta_edge_triple_key, count, col_names, exclude_df):
        neg_samples = pandas.DataFrame(columns=col_names)
        nodeType1, edgeType, nodeType2 = self.meta_edges_dic[meta_edge_triple_key]
        tn_examples = self.all_tn.loc[(self.all_tn[globConst.NODE1_ID_COL_NAME].str.startswith(nodeType1)) &
                                              (self.all_tn[globConst.EDGE_TYPE_COL_NAME] == edgeType)&
                                              (self.all_tn[globConst.NODE2_ID_COL_NAME].str.startswith(nodeType2))]
        count_existing_tn, _ = tn_examples.shape
        if count <= count_existing_tn:
            random_tn_sample = tn_examples.sample(n=count, random_state=globConst.RANDOM_STATE)
            neg_samples = neg_samples.append(random_tn_sample, ignore_index=True)
        else:
            random_tn_sample = tn_examples.sample(n=count_existing_tn, random_state=globConst.RANDOM_STATE)
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