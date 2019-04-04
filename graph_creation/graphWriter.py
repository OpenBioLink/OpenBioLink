import csv
import os
import graph_creation.graphCreationConfig as glob


class GraphWriter ():

    @staticmethod
    def output_graph(nodes_dic: dict, edges_dic : dict, one_file_sep = None, multi_file_sep = None, prefix= None, weights=True, node_edge_list = True):
        if not prefix:
            prefix=''

        if one_file_sep is None and multi_file_sep is None:
            one_file_sep = ','
        # one file
        if one_file_sep is not None:
            GraphWriter.output_graph_in_single_file(prefix, one_file_sep, nodes_dic, edges_dic, weights=weights)
        # separate files
        if multi_file_sep is not None:
            GraphWriter.output_graph_in_multi_files(prefix, multi_file_sep, nodes_dic, edges_dic, weights=weights)
        # lists of all nodes and metaedges
        if node_edge_list:
            GraphWriter.write_node_and_edge_list(prefix, nodes_dic.keys(), edges_dic.keys())


        #todo adjacency matrix
        #key, value = nodes_dic
        #d = {x: i for i, x in enumerate(value)}
    #todo outputformat for graph DB

    @staticmethod
    def output_graph_in_single_file(prefix, file_sep, nodes_dic, edges_dic, weights):
        with open(os.path.join(glob.FILE_PATH, prefix + glob.NODES_FILE_PREFIX + '.csv'), 'w') as out_file:
            writer = csv.writer(out_file, delimiter=file_sep, lineterminator='\n')
            for key, value in nodes_dic.items():
                for node in value:
                    writer.writerow(list(node))
        with open(os.path.join(glob.FILE_PATH, prefix + glob.EDGES_FILE_PREFIX + '.csv'), 'w') as out_file:
            writer = csv.writer(out_file, delimiter=file_sep, lineterminator='\n')
            for key, value in edges_dic.items():
                for edge in value:
                    if weights:
                        writer.writerow(list(edge))
                    else:
                        writer.writerow(edge.to_sub_rel_obj_list())


    @staticmethod
    def output_graph_in_multi_files(prefix, file_sep, nodes_dic, edges_dic, weights):
        # write nodes
        for key, value in nodes_dic.items():
            with open(os.path.join(glob.FILE_PATH, prefix + glob.NODES_FILE_PREFIX + '_' + key + '.csv'),
                      'w') as out_file:
                writer = csv.writer(out_file, delimiter=file_sep, lineterminator='\n')
                for node in value:
                    writer.writerow(list(node))
        # write edges
        for key, value in edges_dic.items():
            with open(os.path.join(glob.FILE_PATH, prefix + glob.EDGES_FILE_PREFIX + '_' + key + '.csv'),
                      'w') as out_file:
                writer = csv.writer(out_file, delimiter=file_sep, lineterminator='\n')
                for edge in value:
                    if weights:
                        writer.writerow(list(edge))
                    else:
                        writer.writerow(edge.to_sub_rel_obj_list())

    @staticmethod
    def write_node_and_edge_list(prefix, nodes_list, edges_list):
        with open(os.path.join(glob.FILE_PATH, prefix + 'nodes_list.csv'), 'w') as out_file:
            out_file.writelines(list('\n'.join(nodes_list)))

        with open(os.path.join(glob.FILE_PATH, prefix + 'edges_list.csv'), 'w') as out_file:
            out_file.writelines(list('\n'.join(edges_list)))

