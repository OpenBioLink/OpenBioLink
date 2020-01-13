import csv
import logging
import os

from tqdm import tqdm

import openbiolink.graphProperties as graphProp
from openbiolink import globalConfig
from openbiolink import globalConfig as globConst
from openbiolink import utils
from openbiolink.cli import Cli
from openbiolink.edge import Edge
from openbiolink.graph_creation import graphCreationConfig as gcConst
from openbiolink.node import Node


class GraphCreator():

    def __init__(self):
        output_dir = os.path.join(globConst.WORKING_DIR, gcConst.GRAPH_FILES_FOLDER_NAME)
        self.tn_path_no_mappings = os.path.join(output_dir, gcConst.TN_ID_NO_MAPPING_FILE_NAME)
        self.tn_path_stats = os.path.join(output_dir, gcConst.TN_STATS_FILE_NAME)
        self.path_no_mappings = os.path.join(output_dir, gcConst.ID_NO_MAPPING_FILE_NAME)
        self.path_stats = os.path.join(output_dir, gcConst.STATS_FILE_NAME)
        os.makedirs(output_dir, exist_ok=True)
        open(self.tn_path_no_mappings, "w").close()
        with open(self.tn_path_stats, "w", encoding="utf8") as file:
            file.write('Edge Type' + '\t' + \
                       'Node1 Type' + '\t' + \
                       'Node2 Type' + '\t' + \
                       'Nr edges' + '\t' + \
                       'Nr edges no mapping' + '\t' + \
                       'Nr edges below cutoff' + '\t' + \
                       'Edges coverage' + '\t' + \
                       'Duplicated edges' + '\t' + \
                       'Nr edges return direction' + '\t' + \
                       'Nr edges after mapping (final nr)' + '\t' + \
                       'Nr nodes1 no mapping' + '\t' + \
                       'Nr nodes2 no mapping' + '\t' + \
                       'Nr nodes1' + '\t' + \
                       'Nr nodes2' + '\t' + \
                       'nodes1 coverage' + '\t' + \
                       'nodes2 coverage' +
                       '\n')
        open(self.path_no_mappings, 'w').close()
        with open(self.path_stats, "w", encoding="utf8") as file:
            file.write('Edge Type' + '\t' + \
                       'Node1 Type' + '\t' + \
                       'Node2 Type' + '\t' + \
                       'Nr edges' + '\t' + \
                       'Nr edges no mapping' + '\t' + \
                       'Nr edges below cutoff' + '\t' + \
                       'Edges coverage' + '\t' + \
                       'Duplicated edges' + '\t' + \
                       'Nr edges return direction' + '\t' + \
                       'Nr edges after mapping (final nr)' + '\t' + \
                       'Nr nodes1 no mapping' + '\t' + \
                       'Nr nodes2 no mapping' + '\t' + \
                       'Nr nodes1' + '\t' + \
                       'Nr nodes2' + '\t' + \
                       'nodes1 coverage' + '\t' + \
                       'nodes2 coverage' +
                       '\n')

    def meta_edges_to_graph(self, edge_metadata_list, tn=None):
        edges_dic = {}
        nodes_dic = {}
        for d in tqdm(edge_metadata_list):
            nodes1, nodes2, edges = self.create_nodes_and_edges(d, tn)
            if str(d.edgeType) in edges_dic:
                edges_dic[str(d.edgeType)].update(edges)
            else:
                edges_dic[str(d.edgeType)] = edges
            if str(d.node1_type) in nodes_dic:
                nodes_dic[str(d.node1_type)].update(nodes1)
            else:
                nodes_dic[str(d.node1_type)] = nodes1
            if str(d.node2_type) in nodes_dic:
                nodes_dic[str(d.node2_type)].update(nodes2)
            else:
                nodes_dic[str(d.node2_type)] = nodes2
        return nodes_dic, edges_dic

    def create_nodes_and_edges(self, edge_metadata, tn=None):
        if not os.path.isfile(edge_metadata.edges_file_path):
            message = 'File does not exist: %s ! Edgetype %s will not be created' % (
            edge_metadata.edges_file_path, str(edge_metadata.edgeType))
            if globalConfig.INTERACTIVE_MODE:
                if globConst.GUI_MODE:
                    from openbiolink.gui import gui
                    gui.askForExit(message)
                else:
                    Cli.ask_for_exit(message)
            else:
                logging.error(message)
            return set(), set(), set()

        # --- mapping ---
        mapping1 = utils.db_mapping_file_to_dic(edge_metadata.mapping1_file, edge_metadata.map1_sourceindex,
                                                edge_metadata.map1_targetindex)
        mapping2 = utils.db_mapping_file_to_dic(edge_metadata.mapping2_file, edge_metadata.map2_sourceindex,
                                                edge_metadata.map2_targetindex)
        altid_mapping1 = utils.db_mapping_file_to_dic(edge_metadata.altid_mapping1_file,
                                                      edge_metadata.altid_map1_sourceindex,
                                                      edge_metadata.altid_map1_targetindex)
        altid_mapping2 = utils.db_mapping_file_to_dic(edge_metadata.altid_mapping2_file,
                                                      edge_metadata.altid_map2_sourceindex,
                                                      edge_metadata.altid_map2_targetindex)

        for mapping in [edge_metadata.mapping1_file, edge_metadata.mapping2_file, edge_metadata.altid_mapping1_file,
                        edge_metadata.altid_mapping2_file]:
            if mapping is not None:
                infile_folder = os.path.join(globConst.WORKING_DIR, gcConst.IN_FILE_FOLDER_NAME)
                mapping_path = os.path.join(infile_folder, mapping)
                if not os.path.isfile(mapping_path):
                    message = 'File does not exist: %s ! Edgetype %s will not be created' % (
                        edge_metadata.edges_file_path, str(edge_metadata.edgeType))
                    if globalConfig.INTERACTIVE_MODE:
                        if globConst.GUI_MODE:
                            from openbiolink.gui import gui
                            gui.askForExit(message)
                        else:
                            Cli.ask_for_exit(message)
                    else:
                        logging.error(message)
                    return set(), set(), set()

        # --- edges ---
        nodes1 = set()
        nodes2 = set()
        edges = set()
        ids1_no_mapping = set()
        ids2_no_mapping = set()
        ids1 = set()
        ids2 = set()
        nr_edges = 0
        nr_edges_return_dir = 0
        nr_edges_after_mapping = 0
        nr_edges_incl_dup = 0
        nr_edges_below_cutoff = 0
        nr_edges_no_mapping = 0

        no_cutoff_defined = edge_metadata.cutoff_num is None and edge_metadata.cutoff_txt is None

        with open(edge_metadata.edges_file_path, "r", encoding="utf8") as edge_content:

            reader = csv.reader(edge_content, delimiter=";")

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

                # apply mapping
                if (edge_metadata.mapping1_file is not None and raw_id1 in mapping1):
                    edge_id1 = mapping1.get(raw_id1)
                elif (edge_metadata.mapping1_file is None):
                    edge_id1 = [raw_id1]
                if (edge_metadata.mapping2_file is not None and raw_id2 in mapping2):
                    edge_id2 = mapping2.get(raw_id2)
                elif (edge_metadata.mapping2_file is None):
                    edge_id2 = [raw_id2]

                # if mapped successfully
                if edge_id1 is not None and edge_id2 is not None:
                    for id1 in edge_id1:
                        # apply alt_id mapping 1
                        if (edge_metadata.altid_mapping1_file is not None and id1 in altid_mapping1):
                            id1 = altid_mapping1[id1][0]  # there should only be one
                        for id2 in edge_id2:
                            # apply alt_id mapping 2
                            if (edge_metadata.altid_mapping2_file is not None and id2 in altid_mapping2):
                                id2 = altid_mapping2[id2][0]  # there should only be one
                            # check for quality cutoff
                            within_num_cutoff = edge_metadata.cutoff_num is not None and float(
                                qscore) > edge_metadata.cutoff_num
                            within_text_cutoff = edge_metadata.cutoff_txt is not None and qscore not in edge_metadata.cutoff_txt
                            if no_cutoff_defined or within_num_cutoff or within_text_cutoff:
                                bimeg_id1 = edge_metadata.node1_type.name + '_' + id1
                                bimeg_id2 = edge_metadata.node2_type.name + '_' + id2
                                edges.add(Edge(bimeg_id1, edge_metadata.edgeType, bimeg_id2, None, qscore))
                                # add an edge in the other direction when edge is undirectional and graph is directional
                                if (not edge_metadata.is_directional) and graphProp.DIRECTED:
                                    edges.add(Edge(bimeg_id2, edge_metadata.edgeType, bimeg_id1, None, qscore))
                                    nr_edges_incl_dup += 1
                                    nr_edges_return_dir += 1
                                nodes1.add(Node(bimeg_id1, edge_metadata.node1_type))
                                nodes2.add(Node(bimeg_id2, edge_metadata.node2_type))

                                nr_edges_incl_dup += 1
                            else:
                                nr_edges_below_cutoff += 1

                # if not mapped successfully
                else:
                    nr_edges_no_mapping += 1
                    if (edge_id1 is None and edge_metadata.mapping1_file is not None):
                        ids1_no_mapping.add(raw_id1)
                    if (edge_id2 is None and edge_metadata.mapping2_file is not None):
                        ids2_no_mapping.add(raw_id2)
                nr_edges += 1

        nr_edges_after_mapping = len(edges)

        if not no_cutoff_defined and nr_edges_below_cutoff == 0:
            logging.warning(
                "No edges of type %s were cut off by quality cutoff, maybe the metric has changed?" % edge_metadata.edgeType.name)
        if nr_edges_after_mapping == 0:
            logging.warning("No edges of type %s are left after mapping and cutoff!" % edge_metadata.edgeType.name)

        # print statistics
        stats_dic = {
            'edge_type': edge_metadata.edgeType,
            'node1_type': edge_metadata.node1_type,
            'node2_type': edge_metadata.node2_type,
            'nr_edges': nr_edges,
            'nr_edges_below_cutoff': nr_edges_below_cutoff,
            'nr_edges_no_mapping': nr_edges_no_mapping,
            'nr_edges_after_mapping': nr_edges_after_mapping,
            'nr_edges_incl_dup': nr_edges_incl_dup,
            'nr_edges_return_dir': nr_edges_return_dir,
            'ids1_no_mapping': ids1_no_mapping,
            'ids2_no_mapping': ids2_no_mapping,
            'ids1': ids1,
            'ids2': ids2
        }
        self.print_graph_stats(stats_dic, tn)

        return nodes1, nodes2, edges

    def print_graph_stats(self, stats_dic, tn):
        edgeType = stats_dic['edge_type']
        if tn:
            path_no_mappings = self.tn_path_no_mappings
            path_stats = self.tn_path_stats
        else:
            path_no_mappings = self.path_no_mappings
            path_stats = self.path_stats
        with open(path_no_mappings, 'a') as out_file:
            for id in stats_dic['ids1_no_mapping']:
                out_file.write('%s\t%s\n' % (id, edgeType))
            for id in stats_dic['ids2_no_mapping']:
                out_file.write('%s\t%s\n' % (id, edgeType))
            out_file.close()

        stats_string = '\nEdge Type: ' + str(edgeType) + '\n' + \
                       'Node1 Type: ' + str(stats_dic['node1_type']) + '\n' + \
                       'Node2 Type: ' + str(stats_dic['node2_type']) + '\n' + \
                       'Nr edges: ' + str(stats_dic['nr_edges']) + '\n' + \
                       'Nr edges no mapping: ' + str(stats_dic['nr_edges_no_mapping']) + '\n' + \
                       'Nr edges below cutoff: ' + str(stats_dic['nr_edges_below_cutoff']) + '\n' + \
                       'Edges coverage: ' + str(1 - (stats_dic['nr_edges_no_mapping'] / stats_dic['nr_edges'])) + '\n' + \
                       'Duplicated edges: ' + str(
            stats_dic['nr_edges_incl_dup'] - stats_dic['nr_edges_after_mapping']) + '\n' + \
                       'Nr edges after mapping (final nr): ' + str(stats_dic['nr_edges_after_mapping']) + '\n' + \
                       'Nr nodes1 no mapping: ' + str(len(stats_dic['ids1_no_mapping'])) + '\n' + \
                       'Nr nodes2 no mapping: ' + str(len(stats_dic['ids2_no_mapping'])) + '\n' + \
                       'Nr nodes1: ' + str(len(stats_dic['ids1'])) + '\n' + \
                       'Nr nodes2: ' + str(len(stats_dic['ids2'])) + '\n' + \
                       'nodes1 coverage: ' + str(
            1 - (len(stats_dic['ids1_no_mapping']) / len(stats_dic['ids1']))) + '\n' + \
                       'nodes2 coverage: ' + str(
            1 - (len(stats_dic['ids2_no_mapping']) / len(stats_dic['ids2']))) + '\n' + \
                       '######################################################################################\n'

        stats_string = str(edgeType) + '\t' + \
                       str(stats_dic['node1_type']) + '\t' + \
                       str(stats_dic['node2_type']) + '\t' + \
                       str(stats_dic['nr_edges']) + '\t' + \
                       str(stats_dic['nr_edges_no_mapping']) + '\t' + \
                       str(stats_dic['nr_edges_below_cutoff']) + '\t' + \
                       str(1 - (stats_dic['nr_edges_no_mapping'] / stats_dic['nr_edges'])) + '\t' + \
                       str(stats_dic['nr_edges_incl_dup'] - stats_dic['nr_edges_after_mapping']) + '\t' + \
                       str(stats_dic['nr_edges_return_dir']) + '\t' + \
                       str(stats_dic['nr_edges_after_mapping']) + '\t' + \
                       str(len(stats_dic['ids1_no_mapping'])) + '\t' + \
                       str(len(stats_dic['ids2_no_mapping'])) + '\t' + \
                       str(len(stats_dic['ids1'])) + '\t' + \
                       str(len(stats_dic['ids2'])) + '\t' + \
                       str(1 - (len(stats_dic['ids1_no_mapping']) / len(stats_dic['ids1']))) + '\t' + \
                       str(1 - (len(stats_dic['ids2_no_mapping']) / len(stats_dic['ids2']))) + \
                       '\n'
        with open(path_stats, 'a') as out_file:
            out_file.write(stats_string)
