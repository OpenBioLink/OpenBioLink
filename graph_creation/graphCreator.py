import csv
import inspect
import os
import sys
from functools import reduce

from tqdm import tqdm

import graph_creation.globalConstant as glob
import graph_creation.utils as utils
from edge import Edge
from graph_creation.graphWriter import GraphWriter
from graph_creation.metadata_edge.tnEdgeMetadata import TnEdgeMetadata
from node import Node
from .file_downloader.fileDownloader import *
from .file_processor.fileProcessor import *
from .file_reader.fileReader import *
from .file_writer.fileWriter import *
from .metadata_db_file import *
from .metadata_edge import *
from .metadata_infile import *
from .userInteractor import UserInteractor


class GraphCreator():
    def __init__(self, folder_path, use_db_metadata_classes = None, use_edge_metadata_classes = None):
        glob.FILE_PATH = folder_path
        glob.O_FILE_PATH = os.path.join(folder_path, 'o_files')
        glob.IN_FILE_PATH = os.path.join(folder_path, 'in_files')

        if not os.path.exists(glob.FILE_PATH):
            os.makedirs(glob.FILE_PATH)

        self.db_file_metadata = [x() for x in utils.get_leaf_subclasses(DbMetadata)]
        self.file_readers = [x() for x in utils.get_leaf_subclasses(FileReader)]
        self.file_processors = [x() for x in utils.get_leaf_subclasses(FileProcessor)]
        self.infile_metadata = [x(glob.IN_FILE_PATH) for x in utils.get_leaf_subclasses(InfileMetadata)]
        self.edge_metadata = [x(glob.QUALITY) for x in utils.get_leaf_subclasses(EdgeMetadata)]
        self.tn_edge_metadata = [x(glob.QUALITY) for x in utils.get_leaf_subclasses(TnEdgeMetadata)]

        self.dbType_reader_map = self.cls_list_to_dic(self.file_readers, 'dbType')
        self.readerType_processor_map = self.cls_list_to_dic(self.file_processors, 'readerType')
        self.infileType_inMetadata_map = {x.infileType: x for x in self.infile_metadata}


        if not glob.DIRECTED:
        # remove onto
            if use_edge_metadata_classes is None:
                use_edge_metadata_classes = [x(glob.QUALITY) for x in utils.get_leaf_subclasses(EdgeMetadata)]
            use_edge_metadata_classes = [x for x in use_edge_metadata_classes if not hasattr(x.EdgesMetaClass, "ONTO_TYPE")] #fixme should be top down

        # only use the desired sources
        if use_db_metadata_classes is not None:
            self.init_custom_sources_bottom_up(use_db_metadata_classes)
        if use_edge_metadata_classes is not None:
            self.init_custom_sources_top_down(use_edge_metadata_classes)



    def download_db_files(self):
        skip = None
        for_all = False
        if not glob.INTERACTIVE_MODE:
            skip =glob.SKIP_EXISTING_FILES
            for_all = True
        if not os.path.exists(glob.O_FILE_PATH):
            os.makedirs(glob.O_FILE_PATH)
        for db_file in tqdm(self.db_file_metadata):
            o_file_path = os.path.join(glob.O_FILE_PATH, db_file.ofile_name)
            if not for_all:
                skip, for_all = UserInteractor.check_if_file_exisits(o_file_path)
            if not (skip and os.path.isfile(o_file_path)):
                FileDownloader.download(db_file.url, o_file_path)


    def create_input_files(self):
        skip = None
        for_all = False
        if not glob.INTERACTIVE_MODE:
            skip =glob.SKIP_EXISTING_FILES
            for_all = True
        if not os.path.exists(glob.IN_FILE_PATH):
            os.makedirs(glob.IN_FILE_PATH)
        for reader in tqdm(self.file_readers):
            if reader.readerType in self.readerType_processor_map:

                #check beforehand if read in content is processed as parsing can be time consuming
                all_files_exist = True
                for processor in self.readerType_processor_map[reader.readerType]:
                    if not os.path.isfile(os.path.join(glob.IN_FILE_PATH, (self.infileType_inMetadata_map[processor.infileType]).csv_name)):
                        all_files_exist = False
                if all_files_exist and not for_all and self.readerType_processor_map[reader.readerType]:
                    first_processor = self.readerType_processor_map[reader.readerType][0]
                    first_processor_out_path = os.path.join(glob.IN_FILE_PATH, (self.infileType_inMetadata_map[first_processor.infileType]).csv_name)
                    skip, for_all = UserInteractor.check_if_file_exisits(first_processor_out_path)
                if not (skip and all_files_exist): #fixme test skip

                    #execute processors
                    in_data = reader.read_file()
                    #fixme  ResourceWarning: Enable tracemalloc to get the object allocation traceback
                    for processor in self.readerType_processor_map[reader.readerType]:
                        out_file_path = os.path.join(glob.IN_FILE_PATH, (self.infileType_inMetadata_map[processor.infileType]).csv_name)
                        if not for_all:
                            skip, for_all = UserInteractor.check_if_file_exisits(out_file_path)
                        if not (skip and os.path.isfile(out_file_path)):
                            out_data = processor.process(in_data)
                            FileWriter.wirte_to_file(out_data, out_file_path)
            else:
                print ('\nWARNING: There is no processor for the Reader '+ str(reader.readerType))

    
    def create_graph(self):
        #create and empty stat files
        tn_path_no_mappings = os.path.join(glob.FILE_PATH, glob.TN_ID_NO_MAPPING_FILE_NAME)
        tn_path_stats = os.path.join(glob.FILE_PATH, glob.TN_STATS_FILE_NAME)
        path_no_mappings = os.path.join(glob.FILE_PATH, glob.ID_NO_MAPPING_FILE_NAME)
        path_stats = os.path.join(glob.FILE_PATH, glob.STATS_FILE_NAME)
        open(tn_path_no_mappings, 'w').close()
        open(tn_path_stats, 'w').close()
        open(path_no_mappings, 'w').close()
        open(path_stats, 'w').close()
        #create graph
        nodes_dic, edges_dic = self.meta_edges_to_graph(self.edge_metadata)
        GraphWriter.output_graph(nodes_dic, edges_dic, one_file_sep='\t')
        #create TN edges
        tn_nodes_dic, tn_edges_dic = self.meta_edges_to_graph(self.tn_edge_metadata, tn = True)
        GraphWriter.output_graph(tn_nodes_dic, tn_edges_dic, multi_file_sep='\t', prefix='TN_')


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
        mapping1 = self.db_mapping_file_to_dic(edge_metadata.mapping1_file, edge_metadata.map1_sourceindex, edge_metadata.map1_targetindex)
        mapping2 = self.db_mapping_file_to_dic(edge_metadata.mapping2_file, edge_metadata.map2_sourceindex, edge_metadata.map2_targetindex)
        altid_mapping1 = self.db_mapping_file_to_dic(edge_metadata.altid_mapping1_file, edge_metadata.altid_map1_sourceindex, edge_metadata.altid_map1_targetindex)
        altid_mapping2 = self.db_mapping_file_to_dic(edge_metadata.altid_mapping2_file, edge_metadata.altid_map2_sourceindex, edge_metadata.altid_map2_targetindex)

        # --- edges ---
        nodes1 = set()
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
                                edges.add(Edge(id1, edge_metadata.edgeType, id2, None, qscore))
                                # add an edge in the other direction when edge is undirectional and graph is directional
                                if not edge_metadata.is_directional and glob.DIRECTED:
                                    edges.add(Edge(id2, edge_metadata.edgeType, id1, None, qscore)) #todo test
                                nodes1.add(Node(id1, edge_metadata.node1_type))
                                nodes2.add(Node(id2, edge_metadata.node2_type))

                                nr_edges_with_dup += 1
                            else:
                                nr_edges_below_cutoff += 1

                #if not mapped successfully
                else:
                    nr_edges_no_mapping += 1
                    if (edge_id1 is None and edge_metadata.mapping1_file is not None):
                        ids1_no_mapping.add(raw_id1 )
                    if (edge_id2 is None and edge_metadata.mapping2_file is not None):
                        ids2_no_mapping.add(raw_id2)
                nr_edges += 1

        nr_edges_after_mapping = len(edges)

        # print statistics
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


    def cls_list_to_dic(self, clsList, keyAttr, condition = None):
        if condition is None:
            condition = lambda a:True
        dic = {}
        for cls in clsList:
            if condition(cls):
                key = self.rgetattr(cls, keyAttr)
                if key in dic:
                    dic[key].append(cls)
                elif key is not None:
                    dic[key]= [cls]
        return dic


    def init_custom_sources_bottom_up(self, use_db_metdata_classes):
        self.db_file_metadata = []

        # remove dbMetadata from list
        # make sure to use instances of classes
        for x in use_db_metdata_classes:
            if inspect.isclass(x):
                self.db_file_metadata.append(x())
            else:
                self.db_file_metadata.append(x)
        keep_dbType = [x.dbType for x in self.db_file_metadata]

        # remove readers from map
        #self.file_readers = [x for x in self.file_readers if x.dbType in keep_dbType]
        keep_readerType = []
        new_dbType_reader_map = {}
        for key in self.dbType_reader_map.keys():
            if key in keep_dbType:
                new_dbType_reader_map[key] = self.dbType_reader_map[key]
                keep_readerType.extend([x.readerType for x in self.dbType_reader_map[key]])
            else:
                print('removed reader: ' + str(key))
        self.dbType_reader_map = new_dbType_reader_map

        # remove processors from map
        keep_infileType = []
        new_readerType_processor_map = {}
        for key in self.readerType_processor_map.keys():
            if key in keep_readerType:
                new_readerType_processor_map[key] = self.readerType_processor_map[key]
                keep_infileType.extend([x.infileType for x in self.readerType_processor_map[key]])
            else:
                print('removed processor: ' + str(key))
        self.readerType_processor_map = new_readerType_processor_map

        # remove inMetadata from map
        keep_infile = []
        new_infileType_inMetadata_map = {}
        for key in self.infileType_inMetadata_map.keys():
            if key in keep_infileType:
                new_infileType_inMetadata_map[key] = self.infileType_inMetadata_map[key]
                keep_infile.extend([type(self.infileType_inMetadata_map[key])])
            else:
                print('removed inMetadata: ' + str(key))
        self.infileType_inMetadata_map = new_infileType_inMetadata_map

        print('keep infile: ' + str(keep_infile))

        # remove from lists
        self.file_readers = [x for sublist in self.dbType_reader_map.values() for x in sublist]
        self.file_processors = [x for sublist in self.readerType_processor_map.values() for x in sublist]
        self.infile_metadata = list(self.infileType_inMetadata_map.values())
        temp_edge_metadata = [x(glob.QUALITY) for x in utils.get_leaf_subclasses(EdgeMetadata)]
        temp_tn_edge_metadata = [x(glob.QUALITY) for x in utils.get_leaf_subclasses(TnEdgeMetadata)]
        self.edge_metadata = [x for x in temp_edge_metadata if x.EdgesMetaClass in keep_infile]
        self.tn_edge_metadata = [x for x in temp_tn_edge_metadata if x.EdgesMetaClass in keep_infile]

        # check for upstream dependencies
        infileType_processor_map = {x.infileType: x for x in self.file_processors}
        readerType_reader_map = {x.readerType: x for x in self.file_readers}

        for metaEdge in self.edge_metadata:
            deleted_upstream_dependency = False
            mappings = [metaEdge.Map1MetaClass, metaEdge.Map2MetaClass, metaEdge.MapAltId1MetaClass, metaEdge.MapAltId2MetaClass]
            for mapping in mappings:
                if mapping is not None:
                    infileType = mapping.INFILE_TYPE
                    if infileType not in self.infileType_inMetadata_map.keys():
                        deleted_upstream_dependency = True
                        break
                    readerType = infileType_processor_map[infileType].readerType
                    if readerType not in self.readerType_processor_map:
                        deleted_upstream_dependency = True
                        break
                    dbType = readerType_reader_map[readerType].dbType
                    if dbType not in self.dbType_reader_map:
                        deleted_upstream_dependency = True
                        break
            if deleted_upstream_dependency:
                sys.exit('ERROR: the db source of a mapping in ' + metaEdge.__class__.__name__ + ' was deleted. Please use another mapping and try again.')


    def init_custom_sources_top_down(self, use_edge_metdata_classes):

        #remove all edge_metadata
        print ('Edge Metadata removed: ' + str([x.__class__.__name__ for x in self.edge_metadata if x.EdgesMetaClass not in [y.EdgesMetaClass for y in use_edge_metdata_classes]]))
        self.edge_metadata = []

        for x in use_edge_metdata_classes:
            if inspect.isclass(x):
                self.edge_metadata.append(x())
            else:
                self.edge_metadata.append(x)

        # remove inMetadata
        infileType_edgeMetadata_map = self.cls_list_to_dic(self.edge_metadata, 'EdgesMetaClass.INFILE_TYPE')
        infileType_edgeMetadata_map.update(self.cls_list_to_dic(self.edge_metadata,'Map1MetaClass.INFILE_TYPE', lambda a: a.Map1MetaClass is not None ))
        infileType_edgeMetadata_map.update(self.cls_list_to_dic(self.edge_metadata,'Map2MetaClass.INFILE_TYPE', lambda a: a.Map2MetaClass is not None ))
        infileType_edgeMetadata_map.update(self.cls_list_to_dic(self.edge_metadata,'MapAltId1MetaClass.INFILE_TYPE', lambda a: a.MapAltId1MetaClass is not None ))
        infileType_edgeMetadata_map.update(self.cls_list_to_dic(self.edge_metadata,'MapAltId2MetaClass.INFILE_TYPE', lambda a: a.MapAltId2MetaClass is not None ))

        infileType_edgeMetadata_map.update(self.cls_list_to_dic(self.tn_edge_metadata, 'EdgesMetaClass.INFILE_TYPE'))
        infileType_edgeMetadata_map.update(self.cls_list_to_dic(self.tn_edge_metadata,'Map1MetaClass.INFILE_TYPE', lambda a: a.Map1MetaClass is not None ))
        infileType_edgeMetadata_map.update(self.cls_list_to_dic(self.tn_edge_metadata,'Map2MetaClass.INFILE_TYPE', lambda a: a.Map2MetaClass is not None ))
        infileType_edgeMetadata_map.update(self.cls_list_to_dic(self.tn_edge_metadata,'MapAltId1MetaClass.INFILE_TYPE', lambda a: a.MapAltId1MetaClass is not None ))
        infileType_edgeMetadata_map.update(self.cls_list_to_dic(self.tn_edge_metadata,'MapAltId2MetaClass.INFILE_TYPE', lambda a: a.MapAltId2MetaClass is not None ))

        keep_infileTypes = list(infileType_edgeMetadata_map.keys())
        print('Infile Metadata removed: ' + str([x.__class__.__name__ for x in self.infile_metadata if x.infileType not in keep_infileTypes]))
        self.infile_metadata = [x for x in self.infile_metadata if x.infileType in keep_infileTypes]
        self.infileType_inMetadata_map = {x.infileType: x for x in self.infile_metadata}

        # remove processors
        print('Processors removed: ' + str([x.__class__.__name__ for x in self.file_processors if x.infileType not in keep_infileTypes]))
        self.file_processors = [x for x in self.file_processors if x.infileType in keep_infileTypes]
        self.readerType_processor_map = self.cls_list_to_dic(self.file_processors, 'readerType')

        #remove readers
        keep_readerType = list(self.readerType_processor_map.keys())
        print('Readers removed: ' + str([x.__class__.__name__ for x in self.file_readers if x.readerType not in keep_readerType]))
        self.file_readers = [x for x in self.file_readers if x.readerType in keep_readerType]
        self.dbType_reader_map = self.cls_list_to_dic(self.file_readers, 'dbType')

        #remove db_metadata
        keep_dbType = list(self.dbType_reader_map.keys())
        print('DB_source removed: ' + str([x.__class__.__name__ for x in self.db_file_metadata if x.dbType not in keep_dbType]))

        self.db_file_metadata = [x for x in self.db_file_metadata if x.dbType in keep_dbType]


    # source: https://gist.github.com/wonderbeyond/d293e7a2af1de4873f2d757edd580288#file-rgetattr-py
    def rgetattr(self,obj, attr, *args):
        def _getattr(obj, attr):
            return getattr(obj, attr, *args)
        return reduce(_getattr, [obj] + attr.split('.'))
