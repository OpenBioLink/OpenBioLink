import csv
import os

import graph_creation.globalConstant as glob
from edge import Edge
from graph_creation.Types.qualityType import QualityType
from node import Node
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

        self.db_file_metadata = [x() for x in self.get_leaf_subclasses(DbMetadata)]
        self.file_readers = [x() for x in self.get_leaf_subclasses(FileReader)]
        self.file_processors = [x() for x in self.get_leaf_subclasses(FileProcessor)]
        self.infile_metadata = [x(glob.IN_FILE_PATH) for x in self.get_leaf_subclasses(InfileMetadata)]
        self.edge_metadata = [x(quality) for x in self.get_leaf_subclasses(EdgeMetadata)]

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
        if not os.path.exists(glob.O_FILE_PATH):
            os.makedirs(glob.O_FILE_PATH)
        for db_file in self.db_file_metadata:
            FileDownloader.download(db_file.url, os.path.join(glob.O_FILE_PATH, db_file.ofile_name))


    def create_input_files(self):
        if not os.path.exists(glob.IN_FILE_PATH):
            os.makedirs(glob.IN_FILE_PATH)
        for reader in self.file_readers:
            if reader.readerType in self.file_processor_db_map:             #todo thorw error or so if not? "there is no processor for this db type"
                in_data = reader.read_file()
                for processor in self.file_processor_db_map[reader.readerType]:
                    out_data = processor.process(in_data)
                    FileWriter.wirte_to_file(out_data, os.path.join(glob.IN_FILE_PATH, (self.in_file_metadata_map[processor.infileType]).csv_name))

    
    def create_graph(self, ):
        open(os.path.join(glob.FILE_PATH, 'ids_no_mapping.tsv'), 'w').close()
        open(os.path.join(glob.FILE_PATH, 'stats.txt'), 'w').close()

        edges_dic = {}
        nodes_dic = {}
        for d in self.edge_metadata:
            nodes1, nodes2, edges = self.create_nodes_and_edges(d)
            edges_dic[str(d.edgeType)] = edges
            if str(d.node1_type) in nodes_dic :
                nodes_dic[str(d.node1_type)].update(nodes1)
            else:
                nodes_dic[str(d.node1_type)] = nodes1
            if str(d.node2_type) in nodes_dic :
                nodes_dic[str(d.node2_type)].update(nodes2)
            else:
                nodes_dic[str(d.node2_type)] = nodes2
        self.output_graph(nodes_dic, edges_dic, '\t')


    def output_graph(self, nodes_dic: dict, edges_dic : dict, one_file_sep = ';', multi_file_sep = None):
        # one file
        if one_file_sep is not None:
            with open(os.path.join(glob.FILE_PATH, glob.NODES_FILE_PREFIX + '.csv'), 'w') as out_file:
                writer = csv.writer(out_file, delimiter=one_file_sep, lineterminator='\n')
                for key, value in nodes_dic.items():
                    for node in value:
                        writer.writerow(list(node))
                out_file.close()
            with open(os.path.join(glob.FILE_PATH, glob.EDGES_FILE_PREFIX + '.csv'), 'w') as out_file:
                writer = csv.writer(out_file, delimiter=one_file_sep, lineterminator='\n')
                for key, value in edges_dic.items():
                    for edge in value:
                        writer.writerow(list(edge))
                out_file.close()
        # separate files
        if multi_file_sep is not None:
            for key, value in nodes_dic.items():
                with open(os.path.join(glob.FILE_PATH, glob.NODES_FILE_PREFIX + '_' + key +  '.csv'), 'w') as out_file:
                    writer = csv.writer(out_file, delimiter=multi_file_sep, lineterminator='\n')
                    for node in value:
                        writer.writerow(list(node))
                out_file.close()
            for key, value in edges_dic.items():
                with open(os.path.join(glob.FILE_PATH, glob.EDGES_FILE_PREFIX + '_' + key + '.csv'), 'w') as out_file:
                    writer = csv.writer(out_file, delimiter=multi_file_sep, lineterminator='\n')
                    for edge in value:
                        writer.writerow(list(edge))
                out_file.close()
        #adjacency matrix
        #key, value = nodes_dic
        #d = {x: i for i, x in enumerate(value)} #fixme continue here


    def create_nodes_and_edges (self, dbFile):
        # --- mapping ---
        mapping1 = self.db_mapping_file_to_dic(dbFile.mapping1_file, dbFile.map1_sourceindex, dbFile.map1_targetindex)
        mapping2 = self.db_mapping_file_to_dic(dbFile.mapping2_file, dbFile.map2_sourceindex, dbFile.map2_targetindex)

        # --- edges ---
        with open(dbFile.edges_file_path, "r", encoding="utf8") as edge_content:
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
                raw_id1 = row[dbFile.colindex1]
                raw_id2 = row[dbFile.colindex2]
                if dbFile.colindex_qscore is not None:
                    qscore = row[dbFile.colindex_qscore]
                else:
                    qscore = None
                edge_id1 = None
                edge_id2 = None
                ids1.add(raw_id1)
                ids2.add(raw_id2)

                if (dbFile.mapping1_file is not None and raw_id1 in mapping1):
                    edge_id1 = mapping1.get(raw_id1)
                if (dbFile.mapping2_file is not None and raw_id2 in mapping2):
                    edge_id2 = mapping2.get(raw_id2)

                if ((edge_id1 is not None and edge_id2 is not None) or
                    (edge_id1 is not None and dbFile.mapping2_file is None) or
                    (edge_id2 is not None and dbFile.mapping1_file is None) or
                    (dbFile.mapping1_file is None and dbFile.mapping2_file is None)):
                    if (edge_id1 is None):
                        edge_id1 = [raw_id1]
                    if (edge_id2 is None):
                        edge_id2 = [raw_id2]
                    for id1 in edge_id1:
                        for id2 in edge_id2:
                            if (dbFile.cutoff_num is None and dbFile.cutoff_txt is None) or \
                                     (dbFile.cutoff_num is not None and float(qscore) > dbFile.cutoff_num) or \
                                     (dbFile.cutoff_txt is not None and qscore not in dbFile.cutoff_txt):
                                edges.add(Edge(id1, dbFile.edgeType, id2, None, qscore))
                                nodes1.add(Node(id1, dbFile.node1_type))
                                nodes2.add(Node(id2, dbFile.node2_type))
                                nr_edges_with_dup +=1
                            else:
                                nr_edges_below_cutoff+=1
                else:
                    nr_edges_no_mapping += 1
                    if (edge_id1 is None and dbFile.mapping1_file is not None):
                        ids1_no_mapping.add(raw_id1 )
                    if (edge_id2 is None and dbFile.mapping2_file is not None):
                        ids2_no_mapping.add(raw_id2)
                nr_edges += 1

        nr_edges_after_mapping =len(edges)
        edge_content.close()

        # print statistics
        edgeType = dbFile.edgeType
        with open(os.path.join(glob.FILE_PATH, 'ids_no_mapping.tsv'), 'a') as out_file:
            for id in ids1_no_mapping:
                out_file.write('%s\t%s\n' %(id, edgeType))
            for id in ids2_no_mapping:
                out_file.write('%s\t%s\n' % (id, edgeType))
            out_file.close()

        out_string = 'Edge Type: ' + str(edgeType) + '\n' + \
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
                     '######################################################################################'
        print(out_string)
        with open(os.path.join(glob.FILE_PATH, 'stats.txt'), 'a') as out_file:
            out_file.write(out_string)

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


    def get_all_subclasses(self, cls):
        return set(cls.__subclasses__()).union([x for c in cls.__subclasses__() for x in self.get_all_subclasses(c)])


    def get_leaf_subclasses(self, cls, classSet=None):
        if classSet is None:
            classSet = set()
        if len(cls.__subclasses__()) == 0:
            classSet.add(cls)
        else:
            classSet.union(x for c in cls.__subclasses__() for x in self.get_leaf_subclasses(c, classSet))
        return classSet