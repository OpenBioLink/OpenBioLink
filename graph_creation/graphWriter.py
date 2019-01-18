import csv
import os
import graph_creation.globalConstant as glob


class GraphWriter ():

    @staticmethod
    def output_graph(nodes_dic: dict, edges_dic : dict, one_file_sep = None, multi_file_sep = None, prefix= None):
        if prefix is None:
            prefix=''
        if one_file_sep is None and multi_file_sep is None:
            one_file_sep = ','
        # one file
        if one_file_sep is not None:
            with open(os.path.join(glob.FILE_PATH, prefix + glob.NODES_FILE_PREFIX + '.csv'), 'w') as out_file:
                writer = csv.writer(out_file, delimiter=one_file_sep, lineterminator='\n')
                for key, value in nodes_dic.items():
                    for node in value:
                        writer.writerow(list(node))
                out_file.close()
            with open(os.path.join(glob.FILE_PATH, prefix + glob.EDGES_FILE_PREFIX + '.csv'), 'w') as out_file:
                writer = csv.writer(out_file, delimiter=one_file_sep, lineterminator='\n')
                for key, value in edges_dic.items():
                    for edge in value:
                        writer.writerow(list(edge))
                out_file.close()
        # separate files
        if multi_file_sep is not None:
            for key, value in nodes_dic.items():
                with open(os.path.join(glob.FILE_PATH, prefix + glob.NODES_FILE_PREFIX + '_' + key +  '.csv'), 'a') as out_file:
                    writer = csv.writer(out_file, delimiter=multi_file_sep, lineterminator='\n')
                    for node in value:
                        writer.writerow(list(node))
                out_file.close()
            for key, value in edges_dic.items():
                with open(os.path.join(glob.FILE_PATH, prefix + glob.EDGES_FILE_PREFIX + '_' + key + '.csv'), 'w') as out_file:
                    writer = csv.writer(out_file, delimiter=multi_file_sep, lineterminator='\n')
                    for edge in value:
                        writer.writerow(list(edge))
                out_file.close()
        #adjacency matrix
        #key, value = nodes_dic
        #d = {x: i for i, x in enumerate(value)} #fixme continue here
