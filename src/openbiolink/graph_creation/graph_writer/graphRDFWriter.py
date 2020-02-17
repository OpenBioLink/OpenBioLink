import os

from openbiolink.graph_creation import graphCreationConfig as gcConst
from openbiolink.graph_creation.graph_writer.base import OpenBioLinkGraphWriter


class GraphRDFWriter(OpenBioLinkGraphWriter):
    identifiersURL = "https://identifiers.org/"

    def output_graph(
        self,
        nodes_dic: dict = None,
        edges_dic: dict = None,
        file_sep=None,
        multi_file=None,
        prefix=None,
        print_qscore=True,
        node_edge_list=True,
    ):
        if not prefix:
            prefix = ""

        if file_sep is None:
            file_sep = ","

        # separate files
        if multi_file:
            self.output_graph_in_multi_files(prefix, file_sep, nodes_dic, edges_dic, qscore=print_qscore)
        # one file
        else:
            self.output_graph_in_single_file(
                prefix=prefix, file_sep=file_sep, nodes_dic=nodes_dic, edges_dic=edges_dic, qscore=print_qscore
            )

        # lists of all nodes and metaedges
        if node_edge_list:
            self.write_node_and_edge_list(prefix, nodes_dic.keys(), edges_dic.keys())

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
