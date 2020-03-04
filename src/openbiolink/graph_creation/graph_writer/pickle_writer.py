"""A utility for outputting graphs as pickle files.

To test, run ``openbiolink generate --no-download --no-input --output-format pickle --qual hq``.
"""

import os
import pickle
from typing import Mapping

from openbiolink.edge import Edge
from openbiolink.graph_creation.graph_writer.base import GraphWriter

__all__ = [
    "GraphPickleWriter",
]


class GraphPickleWriter(GraphWriter):
    format_key = 'PICKLE'

    def write(self, *, tp_nodes, tp_edges: Mapping[str, Edge], tp_namespaces, tn_nodes, tn_edges, tn_namespaces):
        """Write the graph as pickles."""
        with open(os.path.join(self.graph_dir_path, "tp_nodes.pkl"), "wb") as file:
            pickle.dump(tp_nodes, file, protocol=pickle.HIGHEST_PROTOCOL)
        with open(os.path.join(self.graph_dir_path, "tp_edges.pkl"), "wb") as file:
            pickle.dump(tp_edges, file, protocol=pickle.HIGHEST_PROTOCOL)
        with open(os.path.join(self.graph_dir_path, "tp_namespaces.pkl"), "wb") as file:
            pickle.dump(tp_namespaces, file, protocol=pickle.HIGHEST_PROTOCOL)
        with open(os.path.join(self.graph_dir_path, "tn_nodes.pkl"), "wb") as file:
            pickle.dump(tn_nodes, file, protocol=pickle.HIGHEST_PROTOCOL)
        with open(os.path.join(self.graph_dir_path, "tn_edges.pkl"), "wb") as file:
            pickle.dump(tn_edges, file, protocol=pickle.HIGHEST_PROTOCOL)
        with open(os.path.join(self.graph_dir_path, "tn_namespaces.pkl"), "wb") as file:
            pickle.dump(tn_namespaces, file, protocol=pickle.HIGHEST_PROTOCOL)
