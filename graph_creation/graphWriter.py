import csv
import os
import graph_creation.globalConstant as glob


class GraphWriter ():

    @staticmethod
    def output_graph(nodes_dic: dict, edges_dic : dict, one_file_sep = None, multi_file_sep = None, prefix= None, without_onto=None):
        if without_onto is None:
            without_onto = False
        if prefix is None:
            prefix=''

        if one_file_sep is None and multi_file_sep is None:
            one_file_sep = ','
        # one file
        if one_file_sep is not None:
            GraphWriter.output_graph_in_single_file(prefix, one_file_sep, nodes_dic, edges_dic)
        # separate files
        if multi_file_sep is not None:
            GraphWriter.output_graph_in_multi_files(prefix, multi_file_sep, nodes_dic, edges_dic)
        if without_onto:
            GraphWriter.output_graph_wo_onto(prefix, one_file_sep, edges_dic)


        #adjacency matrix
        #key, value = nodes_dic
        #d = {x: i for i, x in enumerate(value)} #fixme continue here

    @staticmethod
    def output_graph_in_single_file(prefix, file_sep, nodes_dic, edges_dic):
        with open(os.path.join(glob.FILE_PATH, prefix + glob.NODES_FILE_PREFIX + '.csv'), 'w') as out_file:
            writer = csv.writer(out_file, delimiter=file_sep, lineterminator='\n')
            for key, value in nodes_dic.items():
                for node in value:
                    writer.writerow(list(node))
        with open(os.path.join(glob.FILE_PATH, prefix + glob.EDGES_FILE_PREFIX + '.csv'), 'w') as out_file:
            writer = csv.writer(out_file, delimiter=file_sep, lineterminator='\n')
            for key, value in edges_dic.items():
                for edge in value:
                    writer.writerow(list(edge))


    @staticmethod
    def output_graph_in_multi_files(prefix, file_sep, nodes_dic, edges_dic):
        for key, value in nodes_dic.items():
            with open(os.path.join(glob.FILE_PATH, prefix + glob.NODES_FILE_PREFIX + '_' + key + '.csv'),
                      'w') as out_file:
                writer = csv.writer(out_file, delimiter=file_sep, lineterminator='\n')
                for node in value:
                    writer.writerow(list(node))
        for key, value in edges_dic.items():
            with open(os.path.join(glob.FILE_PATH, prefix + glob.EDGES_FILE_PREFIX + '_' + key + '.csv'),
                      'w') as out_file:
                writer = csv.writer(out_file, delimiter=file_sep, lineterminator='\n')
                for edge in value:
                    writer.writerow(list(edge))

    @staticmethod
    def output_graph_wo_onto(prefix, file_sep, edges_dic):
        del edges_dic['IS_A']
        with open(os.path.join(glob.FILE_PATH, prefix + glob.EDGES_FILE_PREFIX + '.csv'), 'w') as out_file:
            writer = csv.writer(out_file, delimiter=file_sep, lineterminator='\n')
            for key, value in edges_dic.items():
                for edge in value:
                    writer.writerow(list(edge))