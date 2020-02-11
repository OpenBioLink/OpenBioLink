import json
import os

import openbiolink.graphProperties as graphProp
from openbiolink import globalConfig as globConst
from openbiolink.graph_creation import graphCreationConfig as gcConst


class GraphRDFWriter:
    identifiersURL = "https://identifiers.org/"

    def __init__(self):
        self.graph_dir_path = os.path.join(globConst.WORKING_DIR, gcConst.GRAPH_FILES_FOLDER_NAME)
        os.makedirs(self.graph_dir_path, exist_ok=True)

    def output_graph_props(self):
        graph_prop_list = [item for item in dir(graphProp) if not item.startswith("__")]
        graph_prop_dict = {var: getattr(graphProp, var) for var in graph_prop_list}
        with open(os.path.join(self.graph_dir_path, "graph_props.json"), "w") as json_file:
            for k, v in graph_prop_dict.items():
                if not type(v) == str:
                    graph_prop_dict[k] = str(v)
            json.dump(graph_prop_dict, json_file, indent=4)

    @staticmethod
    def output_graph(
        nodes_dic: dict = None,
        edges_dic: dict = None,
        one_file_sep=None,
        multi_file_sep=None,
        prefix=None,
        print_qscore=True,
        node_edge_list=True,
    ):
        if not prefix:
            prefix = ""

        if one_file_sep is None and multi_file_sep is None:
            one_file_sep = ","
        # one file
        if one_file_sep is not None:
            GraphRDFWriter().output_graph_in_single_file(
                prefix=prefix, file_sep=one_file_sep, nodes_dic=nodes_dic, edges_dic=edges_dic, qscore=print_qscore
            )
        # separate files
        if multi_file_sep is not None:
            GraphRDFWriter().output_graph_in_multi_files(
                prefix, multi_file_sep, nodes_dic, edges_dic, qscore=print_qscore
            )
        # lists of all nodes and metaedges
        if node_edge_list:
            GraphRDFWriter().write_node_and_edge_list(prefix, nodes_dic.keys(), edges_dic.keys())

        # niceToHave (8) adjacency matrix
        # key, value = nodes_dic
        # d = {x: i for i, x in enumerate(value)}
        # niceToHave (8) outputformat for graph DB

    def output_graph_in_single_file(self, prefix, file_sep, nodes_dic, edges_dic, qscore):
        if nodes_dic is not None:
            with open(os.path.join(self.graph_dir_path, prefix + gcConst.NODES_FILE_PREFIX + ".N3"), "w") as out_file:
                for key, value in nodes_dic.items():
                    for node in value:
                        out_file.write("<" + self.identifiersURL + node.id + "> a #" + str(node.type) + " .\n")
        if edges_dic is not None:
            with open(os.path.join(self.graph_dir_path, prefix + gcConst.EDGES_FILE_PREFIX + ".N3"), "w") as out_file:
                for key, value in edges_dic.items():
                    for edge in value:
                        if qscore:
                            out_file.write(
                                "<"
                                + self.identifiersURL
                                + edge.id1
                                + "> <#"
                                + str(edge.type)
                                + "> <"
                                + self.identifiersURL
                                + edge.id2
                                + "> . #quality:"
                                + str(edge.qScore)
                                + " source:"
                                + edge.sourcedb
                                + "\n"
                            )
                        else:
                            out_file.write(
                                "<"
                                + self.identifiersURL
                                + edge.id1
                                + "> <#"
                                + str(edge.type)
                                + "> <"
                                + self.identifiersURL
                                + edge.id2
                                + "> . #source:"
                                + edge.sourcedb
                                + "\n"
                            )

    def output_graph_in_multi_files(self, prefix, file_sep, nodes_dic, edges_dic, qscore):
        # write nodes
        for key, value in nodes_dic.items():
            with open(
                os.path.join(self.graph_dir_path, prefix + gcConst.NODES_FILE_PREFIX + "_" + key + ".N3"), "w"
            ) as out_file:
                for node in value:
                    out_file.write("<" + self.identifiersURL + node.id + "> a #" + str(node.type) + " .\n")
        # write edges
        for key, value in edges_dic.items():
            with open(
                os.path.join(self.graph_dir_path, prefix + gcConst.EDGES_FILE_PREFIX + "_" + key + ".N3"), "w"
            ) as out_file:
                for edge in value:
                    if qscore:
                        out_file.write(
                            "<"
                            + self.identifiersURL
                            + edge.id1
                            + "> <#"
                            + str(edge.type)
                            + "> <"
                            + self.identifiersURL
                            + edge.id2
                            + "> . #quality:"
                            + str(edge.qScore)
                            + " source:"
                            + edge.sourcedb
                            + "\n"
                        )
                    else:
                        out_file.write(
                            "<"
                            + self.identifiersURL
                            + edge.id1
                            + "> <#"
                            + self.identifiersURL
                            + str(edge.type)
                            + "> <"
                            + self.identifiersURL
                            + edge.id2
                            + "> . #source:"
                            + edge.sourcedb
                            + "\n"
                        )

    def write_node_and_edge_list(self, prefix, nodes_list, edges_list):
        with open(os.path.join(self.graph_dir_path, prefix + "nodes_list.csv"), "w") as out_file:
            out_file.writelines(list("\n".join(nodes_list)))

        with open(os.path.join(self.graph_dir_path, prefix + "edges_list.csv"), "w") as out_file:
            out_file.writelines(list("\n".join(edges_list)))