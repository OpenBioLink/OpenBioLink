import csv
import os

from tqdm import tqdm

import graph_creation.graphCreationConfig as glob
import graph_creation.utils as utils
from edge import Edge
from node import Node


class GraphCreator():



    def meta_edges_to_graph(self, edge_metadata_list, tn = None):
        edges_dic = {}
        nodes_dic = {}
        for d in tqdm(edge_metadata_list):
            nodes1, nodes2, edges = self.create_nodes_and_edges(d, tn)
            if str(d.edgeType) in edges_dic:
                edges_dic[str(d.edgeType)].update(edges)
            else:
                edges_dic[str(d.edgeType)] = edges
            if str(d.node1_type) in nodes_dic :
                nodes_dic[str(d.node1_type)].update(nodes1)
            else:
                nodes_dic[str(d.node1_type)] = nodes1
            if str(d.node2_type) in nodes_dic :
                nodes_dic[str(d.node2_type)].update(nodes2)
            else:
                nodes_dic[str(d.node2_type)] = nodes2
        return nodes_dic, edges_dic



    def create_nodes_and_edges (self, edge_metadata, tn= None):
        if not os.path.isfile(edge_metadata.edges_file_path):
            print('\nWARNING: File does not exist: ' + edge_metadata.edges_file_path)
            print('Edgetype ' + str(edge_metadata.edgeType)+ ' will not be created')
            #sys.exit() #todo also fo mapping files
            return set(), set(), set()

        # --- mapping ---
        mapping1 = utils.db_mapping_file_to_dic(edge_metadata.mapping1_file, edge_metadata.map1_sourceindex, edge_metadata.map1_targetindex)
        mapping2 = utils.db_mapping_file_to_dic(edge_metadata.mapping2_file, edge_metadata.map2_sourceindex, edge_metadata.map2_targetindex)
        altid_mapping1 = utils.db_mapping_file_to_dic(edge_metadata.altid_mapping1_file, edge_metadata.altid_map1_sourceindex, edge_metadata.altid_map1_targetindex)
        altid_mapping2 = utils.db_mapping_file_to_dic(edge_metadata.altid_mapping2_file, edge_metadata.altid_map2_sourceindex, edge_metadata.altid_map2_targetindex)

        # --- edges ---
        nodes1 = set() #todo list and only before return set?
        nodes2 = set()
        edges = set()
        ids1_no_mapping = set()
        ids2_no_mapping = set()
        ids1 = set()
        ids2 = set()
        nr_edges = 0
        nr_edges_after_mapping = 0
        nr_edges_with_dup = 0
        nr_edges_below_cutoff = 0
        nr_edges_no_mapping = 0

        with open(edge_metadata.edges_file_path, "r", encoding="utf8") as edge_content:

            reader = csv.reader(edge_content, delimiter = ";")

            for row in reader:
                raw_id1 = row[edge_metadata.colindex1]
                raw_id2 = row[edge_metadata.colindex2]
                if edge_metadata.colindex_qscore is not None:
                    qscore = row[edge_metadata.colindex_qscore]
                else:
                    qscore = None
                edge_id1 = None
                edge_id2 = None
                ids1.add(raw_id1)
                ids2.add(raw_id2)

                #apply mapping
                if (edge_metadata.mapping1_file is not None and raw_id1 in mapping1):
                    edge_id1 = mapping1.get(raw_id1)
                elif(edge_metadata.mapping1_file is None):
                    edge_id1 = [raw_id1]
                if (edge_metadata.mapping2_file is not None and raw_id2 in mapping2):
                    edge_id2 = mapping2.get(raw_id2)
                elif (edge_metadata.mapping2_file is None):
                    edge_id2 = [raw_id2]

                #if mapped successfully
                if edge_id1 is not None and edge_id2 is not None:
                    for id1 in edge_id1:
                        #apply alt_id mapping 1
                        if (edge_metadata.altid_mapping1_file is not None and id1 in altid_mapping1):
                            id1 = altid_mapping1[id1][0] #todo there should only be one
                        for id2 in edge_id2:
                            # apply alt_id mapping 2
                            if (edge_metadata.altid_mapping2_file is not None and id2 in altid_mapping2):
                                id2 = altid_mapping2[id2][0] #todo there should only be one
                            #check for quality cutoff
                            if (edge_metadata.cutoff_num is None and edge_metadata.cutoff_txt is None) or \
                                     (edge_metadata.cutoff_num is not None and float(qscore) > edge_metadata.cutoff_num) or \
                                     (edge_metadata.cutoff_txt is not None and qscore not in edge_metadata.cutoff_txt):
                                bimeg_id1 = edge_metadata.node1_type.name + '_' + id1
                                bimeg_id2 = edge_metadata.node2_type.name + '_' + id2
                                edges.add(Edge(bimeg_id1, edge_metadata.edgeType, bimeg_id2, None, qscore))
                                # add an edge in the other direction when edge is undirectional and graph is directional
                                if not edge_metadata.is_directional and glob.DIRECTED:
                                    edges.add(Edge(bimeg_id2, edge_metadata.edgeType, bimeg_id1, None, qscore)) #todo test
                                nodes1.add(Node(bimeg_id1, edge_metadata.node1_type)) #fixme add prefix to id
                                nodes2.add(Node(bimeg_id2, edge_metadata.node2_type))

                                nr_edges_with_dup += 1
                            else:
                                nr_edges_below_cutoff += 1

                #if not mapped successfully
                else:
                    nr_edges_no_mapping += 1
                    if (edge_id1 is None and edge_metadata.mapping1_file is not None):
                        ids1_no_mapping.add(raw_id1)
                    if (edge_id2 is None and edge_metadata.mapping2_file is not None):
                        ids2_no_mapping.add(raw_id2)
                nr_edges += 1

        nr_edges_after_mapping = len(edges)

        # print statistics #todo not here
        edgeType = edge_metadata.edgeType
        if tn:
            path_no_mappings = os.path.join(glob.FILE_PATH, glob.TN_ID_NO_MAPPING_FILE_NAME)
            path_stats = os.path.join(glob.FILE_PATH, glob.TN_STATS_FILE_NAME)
        else:
            path_no_mappings = os.path.join(glob.FILE_PATH, glob.ID_NO_MAPPING_FILE_NAME)
            path_stats = os.path.join(glob.FILE_PATH, glob.STATS_FILE_NAME)
        if not os.path.isfile(path_no_mappings):
            open(path_no_mappings, 'w').close()
        if not os.path.isfile(path_stats):
            open(path_stats, 'w').close()
        with open(path_no_mappings, 'a') as out_file: #fixme empty the file at very beginning
            for id in ids1_no_mapping:
                out_file.write('%s\t%s\n' %(id, edgeType))
            for id in ids2_no_mapping:
                out_file.write('%s\t%s\n' % (id, edgeType))
            out_file.close()

        stats_string = '\nEdge Type: ' + str(edgeType) + '\n' + \
                       'Node1 Type: ' + str(edge_metadata.node1_type) + '\n' + \
                       'Node1 Type: ' + str(edge_metadata.node2_type) + '\n' + \
                       'Nr edges: ' + str(nr_edges) + '\n' + \
                       'Nr edges no mapping: ' + str(nr_edges_no_mapping) + '\n' + \
                       'Nr edges below cutoff: ' + str(nr_edges_below_cutoff) + '\n' + \
                       'Edges coverage: ' + str(1-(nr_edges_no_mapping/ nr_edges)) + '\n' + \
                       'Duplicated edges: ' + str(nr_edges_with_dup-nr_edges_after_mapping) + '\n' + \
                       'Nr edges after mapping (final nr): ' + str(nr_edges_after_mapping) + '\n' + \
                       'Nr nodes1 no mapping: ' + str(len(ids1_no_mapping)) + '\n' + \
                       'Nr nodes2 no mapping: ' + str(len(ids2_no_mapping)) + '\n' + \
                       'Nr nodes1: ' + str(len(ids1)) + '\n' + \
                       'Nr nodes2: ' + str(len(ids2)) + '\n' + \
                       'nodes1 coverage: ' + str(1-(len(ids1_no_mapping)/ len(ids1))) + '\n' + \
                       'nodes2 coverage: ' + str(1-(len(ids2_no_mapping)/ len(ids2))) + '\n' + \
                       '######################################################################################\n'
        # print(stats_string)
        with open(path_stats, 'a') as out_file:
            out_file.write(stats_string)

        return nodes1, nodes2, edges


# ----------- helper functions ----------


#
    #