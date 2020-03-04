import csv
import os
from typing import Mapping

from openbiolink.graph_creation import graphCreationConfig as gcConst
from openbiolink.graph_creation.graph_writer.base import OpenBioLinkGraphWriter


class GraphTSVWriter(OpenBioLinkGraphWriter):
    format_key = 'TSV'

    def output_graph(
        self, nodes: Mapping = None, edges: Mapping = None, prefix=None, node_edge_list=True,
    ):
        if prefix is None:
            prefix = ""

        # separate files
        if self.multi_file:
            self._output_graph_in_multi_files(prefix=prefix, nodes=nodes, edges=edges)
        # one file
        else:
            self._output_graph_in_single_file(prefix=prefix, nodes=nodes, edges=edges)

        # lists of all nodes and metaedges
        if node_edge_list:
            self.write_node_and_edge_list(prefix, nodes.keys(), edges.keys())

        # niceToHave (8) adjacency matrix
        # key, value = nodes_dic
        # d = {x: i for i, x in enumerate(value)}
        # niceToHave (8) outputformat for graph DB

    def _output_graph_in_single_file(self, *, prefix, nodes, edges):
        if nodes is not None:
            sorted_nodes = self.sort_nodes(nodes)
            with open(os.path.join(self.graph_dir_path, prefix + gcConst.NODES_FILE_PREFIX + ".csv"), "w") as out_file:
                writer = csv.writer(out_file, delimiter=self.file_sep, lineterminator="\n")
                for node in sorted_nodes:
                    writer.writerow([node.resolved_id, node.type])
        if edges is not None:
            with open(os.path.join(self.graph_dir_path, prefix + gcConst.EDGES_FILE_PREFIX + ".csv"), "w") as out_file:
                sorted_edges = self.sort_edges(edges)
                writer = csv.writer(out_file, delimiter=self.file_sep, lineterminator="\n")
                for edge in sorted_edges:
                    writer.writerow(edge.to_list(self.print_qscore))

    def _output_graph_in_multi_files(self, *, prefix, nodes, edges):
        # write nodes
        for key, value in nodes.items():
            nodes_path = os.path.join(self.graph_dir_path, f"{prefix}{gcConst.NODES_FILE_PREFIX}_{key}.csv")
            with open(nodes_path, "w") as out_file:
                writer = csv.writer(out_file, delimiter=self.file_sep, lineterminator="\n")
                for node in value:
                    writer.writerow(list(node))

        # write edges
        for key, value in edges.items():
            edges_path = os.path.join(self.graph_dir_path, f"{prefix}{gcConst.EDGES_FILE_PREFIX}_{key}.csv")
            with open(edges_path, "w") as out_file:
                writer = csv.writer(out_file, delimiter=self.file_sep, lineterminator="\n")
                for edge in value:
                    writer.writerow(edge.to_list(self.print_qscore))
