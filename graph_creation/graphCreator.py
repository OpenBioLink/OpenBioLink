import csv
import os
import sys
from tqdm import tqdm

import graph_creation.globalConstant as glob
from edge import Edge
from graph_creation.Types.qualityType import QualityType
from graph_creation.graphWriter import GraphWriter
from graph_creation.metadata_edge.tnEdgeMetadata import TnEdgeMetadata
from node import Node
from graph_creation.utils import get_leaf_subclasses
from .file_downloader.fileDownloader import *
from .file_processor.fileProcessor import *
from .file_reader.fileReader import *
from .file_writer.fileWriter import *
from .metadata_db_file import *
from .metadata_edge import *
from .metadata_infile import *


class GraphCreator():
    def __init__(self, folder_path):
        glob.FILE_PATH = folder_path
        glob.O_FILE_PATH = os.path.join(folder_path, 'o_files')
        glob.IN_FILE_PATH = os.path.join(folder_path, 'in_files')
        quality = QualityType.HQ

        if not os.path.exists(glob.FILE_PATH):
            os.makedirs(glob.FILE_PATH)

        self.db_file_metadata = [x() for x in get_leaf_subclasses(DbMetadata)]
        self.file_readers = [x() for x in get_leaf_subclasses(FileReader)]
        self.file_processors = [x() for x in get_leaf_subclasses(FileProcessor)]
        self.infile_metadata = [x(glob.IN_FILE_PATH) for x in get_leaf_subclasses(InfileMetadata)]
        self.edge_metadata = [x(quality) for x in get_leaf_subclasses(EdgeMetadata)]
        self.tn_edge_metadata = [x(quality) for x in get_leaf_subclasses(TnEdgeMetadata)]

        #self.db_file_map = {x.dbType: x for x in self.db_file_metadata }
        #self.file_reader_map = {x.dbType: x for x in self.file_readers }
        self.file_processor_db_map={}
        for x in self.file_processors:
            if x.readerType in self.file_processor_db_map:
                self.file_processor_db_map[x.readerType].append(x)
            else:
                self.file_processor_db_map[x.readerType]= [x]

        #self.file_processor_in_map = {x.infileType: x for x in self.file_processors}
        self.in_file_metadata_map = {x.infileType: x for x in self.infile_metadata}


    def download_db_files(self):
        skip = None
        for_all = False
        if not os.path.exists(glob.O_FILE_PATH):
            os.makedirs(glob.O_FILE_PATH)
        for db_file in tqdm(self.db_file_metadata):
            o_file_path = os.path.join(glob.O_FILE_PATH, db_file.ofile_name)
            if not for_all:
                skip, for_all = self.check_if_file_exisits(o_file_path)
            if not skip:
                FileDownloader.download(db_file.url, o_file_path)


    def create_input_files(self):
        skip = None
        for_all = False
        if not os.path.exists(glob.IN_FILE_PATH):
            os.makedirs(glob.IN_FILE_PATH)
        for reader in tqdm(self.file_readers):
            if reader.readerType in self.file_processor_db_map:

                #check beforehand if read in content is processed as parsing can be time consuming
                all_files_exist = True
                for processor in self.file_processor_db_map[reader.readerType]:
                    if not os.path.isfile(os.path.join(glob.IN_FILE_PATH, (self.in_file_metadata_map[processor.infileType]).csv_name)):
                        all_files_exist = False
                if all_files_exist and not for_all and self.file_processor_db_map[reader.readerType]:
                    first_processor = self.file_processor_db_map[reader.readerType][0]
                    first_processor_out_path = os.path.join(glob.IN_FILE_PATH, (self.in_file_metadata_map[first_processor.infileType]).csv_name)
                    skip, for_all = self.check_if_file_exisits(first_processor_out_path)
                if not (skip and all_files_exist):

                    in_data = reader.read_file()
                    for processor in tqdm(self.file_processor_db_map[reader.readerType]):
                        out_file_path = os.path.join(glob.IN_FILE_PATH, (self.in_file_metadata_map[processor.infileType]).csv_name)
                        if not for_all:
                            skip, for_all = self.check_if_file_exisits(out_file_path)
                        if not (skip and os.path.isfile(out_file_path)):
                            out_data = processor.process(in_data)
                            FileWriter.wirte_to_file(out_data, out_file_path)

            else:
                print ('\nWARNING: There is no processor for the Reader '+ str(reader.readerType))

    
    def create_graph(self):
        nodes_dic, edges_dic = self.meta_edges_to_graph(self.edge_metadata)
        GraphWriter.output_graph(nodes_dic, edges_dic, one_file_sep='\t')
        tn_nodes_dic, tn_edges_dic = self.meta_edges_to_graph(self.tn_edge_metadata, tn = True)
        GraphWriter.output_graph(tn_nodes_dic, tn_edges_dic, multi_file_sep='\t', prefix='TN_')


    def meta_edges_to_graph(self, edge_metadata_list, tn = None):
        edges_dic = {}
        nodes_dic = {}
        for d in tqdm(edge_metadata_list):
            nodes1, nodes2, edges = self.create_nodes_and_edges(d, tn)
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
            print('\nFile does not exist: ' + edge_metadata.edges_file_path)
            sys.exit() #todo also fo mapping files
        # --- mapping ---
        mapping1 = self.db_mapping_file_to_dic(edge_metadata.mapping1_file, edge_metadata.map1_sourceindex, edge_metadata.map1_targetindex)
        mapping2 = self.db_mapping_file_to_dic(edge_metadata.mapping2_file, edge_metadata.map2_sourceindex, edge_metadata.map2_targetindex)

        # --- edges ---

        with open(edge_metadata.edges_file_path, "r", encoding="utf8") as edge_content:
            nodes1 = set()
            nodes2 = set()
            edges = set()
            ids1_no_mapping = set()
            ids2_no_mapping = set()
            ids1 = set()
            ids2 = set()
            nr_edges=0
            nr_edges_after_mapping = 0
            nr_edges_with_dup = 0
            nr_edges_below_cutoff = 0
            nr_edges_no_mapping = 0

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

                if (edge_metadata.mapping1_file is not None and raw_id1 in mapping1):
                    edge_id1 = mapping1.get(raw_id1)
                if (edge_metadata.mapping2_file is not None and raw_id2 in mapping2):
                    edge_id2 = mapping2.get(raw_id2)

                if ((edge_id1 is not None and edge_id2 is not None) or
                    (edge_id1 is not None and edge_metadata.mapping2_file is None) or
                    (edge_id2 is not None and edge_metadata.mapping1_file is None) or
                    (edge_metadata.mapping1_file is None and edge_metadata.mapping2_file is None)):
                    if (edge_id1 is None):
                        edge_id1 = [raw_id1]
                    if (edge_id2 is None):
                        edge_id2 = [raw_id2]
                    for id1 in edge_id1:
                        for id2 in edge_id2:
                            if (edge_metadata.cutoff_num is None and edge_metadata.cutoff_txt is None) or \
                                     (edge_metadata.cutoff_num is not None and float(qscore) > edge_metadata.cutoff_num) or \
                                     (edge_metadata.cutoff_txt is not None and qscore not in edge_metadata.cutoff_txt):
                                edges.add(Edge(id1, edge_metadata.edgeType, id2, None, qscore))
                                nodes1.add(Node(id1, edge_metadata.node1_type))
                                nodes2.add(Node(id2, edge_metadata.node2_type))
                                nr_edges_with_dup +=1
                            else:
                                nr_edges_below_cutoff+=1
                else:
                    nr_edges_no_mapping += 1
                    if (edge_id1 is None and edge_metadata.mapping1_file is not None):
                        ids1_no_mapping.add(raw_id1 )
                    if (edge_id2 is None and edge_metadata.mapping2_file is not None):
                        ids2_no_mapping.add(raw_id2)
                nr_edges += 1

        nr_edges_after_mapping =len(edges)
        edge_content.close()

        # print statistics
        edgeType = edge_metadata.edgeType
        if tn:
            path_no_mappings = os.path.join(glob.FILE_PATH, 'tn_ids_no_mapping.tsv')
            path_stats = os.path.join(glob.FILE_PATH, 'tn_stats.txt')
        else:
            path_no_mappings = os.path.join(glob.FILE_PATH, 'ids_no_mapping.tsv')
            path_stats = os.path.join(glob.FILE_PATH, 'stats.txt')
        if not os.path.isfile(path_no_mappings):
            open(path_no_mappings, 'w').close()
        if not os.path.isfile(path_stats):
            open(path_stats, 'w').close()
        with open(path_no_mappings, 'a') as out_file:
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


    def db_mapping_file_to_dic(self, mapping_file, map_sourceindex, map_targetindex):
        """creates a dic out of a metadata_db_file mapping file (source_id to list of target_ids)"""
        if (mapping_file is not None):
            mapping = {}
            with open(mapping_file, mode="r") as mapping_content1:
                reader = csv.reader(mapping_content1, delimiter=";")

                for row in reader:
                    if row[map_sourceindex] in mapping:
                        mapping[row[map_sourceindex]].append(row[map_targetindex])
                    else:
                        mapping[row[map_sourceindex]] = [row[map_targetindex]]
                mapping_content1.close()
            return mapping

    def check_if_file_exisits(self, file_path): #todo naming
        skip = None
        for_all = False
        if os.path.isfile(file_path):
            user_input = input(
                '\nThe file ' + file_path + ' already exists. \n'
                                          'Do you want to \n'
                                          ' [y] continue anyways\n'
                                          ' [c] continue anyways for all files\n'
                                          ' [n] skip this file\n'
                                          ' [s] skip all existing files\n'
                                          ' [x] chancel \n')
            if user_input == 'x':
                sys.exit()
            elif user_input == 'c':
                skip = False
                for_all = True
            elif user_input == 'n':
                skip = True
            elif user_input == 's':
                skip = True
                for_all = True
        return skip, for_all