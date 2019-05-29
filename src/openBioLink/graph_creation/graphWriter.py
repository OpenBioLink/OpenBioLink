import csv
import os
from . import graphCreationConfig as gcConst
import globalConfig as globConst
import graphProperties as graphProp
import json


class GraphWriter ():

    def __init__(self):
        self.graph_dir_path = os.path.join(globConst.WORKING_DIR, gcConst.GRAPH_FILES_FOLDER_NAME)
        os.makedirs(self.graph_dir_path, exist_ok=True)

    def output_graph_props(self):
        graph_prop_list = [item for item in dir(graphProp) if not item.startswith("__")]
        graph_prop_dict = {var: getattr(graphProp, var) for var in graph_prop_list}
        with open(os.path.join(self.graph_dir_path,'graph_props.json'), 'w') as json_file:
            json.dump(graph_prop_dict, json_file, indent=4)

    @staticmethod
    def output_graph(nodes_dic: dict, edges_dic : dict, one_file_sep = None, multi_file_sep = None, prefix= None, print_qscore=True, node_edge_list = True):
        if not prefix:
            prefix=''

        if one_file_sep is None and multi_file_sep is None:
            one_file_sep = ','
        # one file
        if one_file_sep is not None:
            GraphWriter().output_graph_in_single_file(prefix=prefix, file_sep=one_file_sep, nodes_dic=nodes_dic, edges_dic=edges_dic, qscore=print_qscore)
        # separate files
        if multi_file_sep is not None:
            GraphWriter().output_graph_in_multi_files(prefix, multi_file_sep, nodes_dic, edges_dic, qscore=print_qscore)
        # lists of all nodes and metaedges
        if node_edge_list:
            GraphWriter().write_node_and_edge_list(prefix, nodes_dic.keys(), edges_dic.keys())


        #todo adjacency matrix
        #key, value = nodes_dic
        #d = {x: i for i, x in enumerate(value)}
    #todo outputformat for graph DB

    def output_graph_in_single_file(self, prefix, file_sep, nodes_dic, edges_dic, qscore):
        with open(os.path.join(self.graph_dir_path, prefix + gcConst.NODES_FILE_PREFIX + '.csv'), 'w') as out_file:
            writer = csv.writer(out_file, delimiter=file_sep, lineterminator='\n')
            for key, value in nodes_dic.items():
                for node in value:
                    writer.writerow(list(node))
        with open(os.path.join(self.graph_dir_path, prefix + gcConst.EDGES_FILE_PREFIX + '.csv'), 'w') as out_file:
            writer = csv.writer(out_file, delimiter=file_sep, lineterminator='\n')
            for key, value in edges_dic.items():
                for edge in value:
                    if qscore:
                        writer.writerow(list(edge))
                    else:
                        writer.writerow(edge.to_sub_rel_obj_list())


    def output_graph_in_multi_files(self, prefix, file_sep, nodes_dic, edges_dic, qscore):
        # write nodes
        for key, value in nodes_dic.items():
            with open(os.path.join(self.graph_dir_path, prefix + gcConst.NODES_FILE_PREFIX + '_' + key + '.csv'),
                      'w') as out_file:
                writer = csv.writer(out_file, delimiter=file_sep, lineterminator='\n')
                for node in value:
                    writer.writerow(list(node))
        # write edges
        for key, value in edges_dic.items():
            with open(os.path.join(self.graph_dir_path, prefix + gcConst.EDGES_FILE_PREFIX + '_' + key + '.csv'),
                      'w') as out_file:
                writer = csv.writer(out_file, delimiter=file_sep, lineterminator='\n')
                for edge in value:
                    if qscore:
                        writer.writerow(list(edge))
                    else:
                        writer.writerow(edge.to_sub_rel_obj_list())

    def write_node_and_edge_list(self, prefix, nodes_list, edges_list):
        with open(os.path.join(self.graph_dir_path, prefix + 'nodes_list.csv'), 'w') as out_file:
            out_file.writelines(list('\n'.join(nodes_list)))

        with open(os.path.join(self.graph_dir_path, prefix + 'edges_list.csv'), 'w') as out_file:
            out_file.writelines(list('\n'.join(edges_list)))

