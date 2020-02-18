"""A utility for outputting graphs as BEL documents.

To test, run ``openbiolink generate --no-download --no-input --output-format BEL --qual hq``.
"""
import logging
import os
from typing import Mapping, Optional, Set

from tqdm import tqdm

from openbiolink import Edge, EdgeType, Node, NodeType
from openbiolink.graph_creation.graph_writer.base import GraphWriter

__all__ = [
    "GraphBELWriter",
]

logger = logging.getLogger(__name__)


class GraphBELWriter(GraphWriter):

    def __init__(self, directory: Optional[str] = None, nodelink_gz: bool = True):
        super().__init__(directory=directory)
        self.nodelink_gz = nodelink_gz

    def write(
        self,
        *,
        tp_nodes: Mapping[str, Set[Node]],
        tp_edges: Mapping[str, Set[Edge]],
        tn_nodes: Mapping[str, Set[Node]],
        tn_edges: Mapping[str, Set[Edge]],
        **kwargs,
    ) -> None:
        """Write the graph as gzipped BEL graphs."""
        from pybel import to_nodelink_gz

        for nodes, edges, name in ((tp_nodes, tp_edges, "positive"), (tn_nodes, tn_edges, "negative")):
            graph = convert(nodes=nodes, edges=edges, name=name)
            graph_path = os.path.join(self.graph_dir_path, f"{name}.bel.nodelink.json.gz")
            to_nodelink_gz(graph, graph_path)


def _get_type_to_dsl():
    import pybel.dsl

    return {
        NodeType.ANATOMY: pybel.dsl.Population,
        NodeType.GENE: pybel.dsl.Protein,
        NodeType.GO: pybel.dsl.BiologicalProcess,
        NodeType.DIS: pybel.dsl.Pathology,
        NodeType.DRUG: pybel.dsl.Abundance,
        NodeType.PHENOTYPE: pybel.dsl.Pathology,
        NodeType.PATHWAY: pybel.dsl.BiologicalProcess,
    }


def _get_type_to_adder():
    from pybel import BELGraph

    _type_to_adder = {
        EdgeType.DRUG_BINDINH_GENE: BELGraph.add_directly_inhibits,
        EdgeType.GENE_GENE: BELGraph.add_association,
        EdgeType.GENE_OVEREXPRESSED_ANATOMY: BELGraph.add_positive_correlation,
        EdgeType.GENE_GO: BELGraph.add_part_of,
        EdgeType.GENE_INHIBITION_GENE: BELGraph.add_inhibits,
        EdgeType.GENE_EXPRESSED_ANATOMY: BELGraph.add_association,
        EdgeType.DRUG_ACTIVATION_GENE: BELGraph.add_activates,
        EdgeType.DRUG_PREDBIND_GENE: None,
        EdgeType.GENE_PHENOTYPE: BELGraph.add_association,
        EdgeType.GENE_PTMOD_GENE: None,
        EdgeType.GENE_EXPRESSION_GENE: BELGraph.add_correlation,
        EdgeType.GENE_REACTION_GENE: None,
        EdgeType.DIS_PHENOTYPE: BELGraph.add_association,
        EdgeType.DRUG_INHIBITION_GENE: BELGraph.add_inhibits,
        EdgeType.DRUG_PHENOTYPE: BELGraph.add_association,
        EdgeType.DRUG_BINDING_GENE: BELGraph.add_binds,
        EdgeType.DRUG_REACTION_GENE: None,
        EdgeType.GENE_ACTIVATION_GENE: BELGraph.add_activates,
        EdgeType.GENE_BINDINH_GENE: BELGraph.add_directly_activates,
        EdgeType.GENE_DRUG: BELGraph.add_association,
        EdgeType.GENE_BINDING_GENE: BELGraph.add_binds,
        EdgeType.GENE_CATALYSIS_GENE: None,
        EdgeType.DRUG_CATALYSIS_GENE: None,
        EdgeType.DRUG_EXPRESSION_GENE: BELGraph.add_positive_correlation,
        EdgeType.GENE_PATHWAY: BELGraph.add_part_of,
        EdgeType.DIS_DRUG: BELGraph.add_association,
        EdgeType.GENE_UNDEREXPRESSED_ANATOMY: BELGraph.add_negative_correlation,
        EdgeType.GENE_DIS: BELGraph.add_association,
        EdgeType.GENE_BINDACT_GENE: BELGraph.add_directly_activates,
        EdgeType.DRUG_BINDACT_GENE: BELGraph.add_directly_activates,
        EdgeType.PART_OF: BELGraph.add_part_of,
        EdgeType.IS_A: BELGraph.add_is_a,
    }
    return {k.name: v for k, v in _type_to_adder.items()}


UNQUALIFIED_EDGE_TYPES = {
    edge_type.name for edge_type in (EdgeType.GENE_GO, EdgeType.GENE_PATHWAY, EdgeType.PART_OF, EdgeType.IS_A)
}


def convert(*, nodes: Mapping[str, Set[Node]], edges: Mapping[str, Set[Edge]], **graph_kwargs):
    """Convert a set of edges to a BEL graph."""
    from pybel import BELGraph, BaseEntity

    type_to_dsl = _get_type_to_dsl()
    type_to_adder = _get_type_to_adder()
    id_to_node: Mapping[str, Node] = {node.id: node for type_nodes in nodes.values() for node in type_nodes}

    def _get_node(node_id: str) -> BaseEntity:
        node = id_to_node[node_id]
        dsl = type_to_dsl[node.type]
        return dsl(namespace=node.namespace.namespace.value, identifier=node_id, name=node.name)

    graph = BELGraph(**graph_kwargs)

    for edge_type, edge_type_edges in tqdm(edges.items()):
        adder = type_to_adder[edge_type]
        if adder is None:
            logger.warning("%s is not yet supported", edge_type)
            continue
        if edge_type in UNQUALIFIED_EDGE_TYPES:
            for edge in tqdm(edge_type_edges, desc=edge_type, leave=False):
                adder(graph, u=_get_node(edge.id1), v=_get_node(edge.id2))
        else:
            for edge in tqdm(edge_type_edges, desc=edge_type, leave=False):
                annotations = dict()
                if edge.source:
                    annotations["source"] = edge.source
                if edge.sourcedb:
                    annotations["source_db"] = edge.sourcedb
                if edge.qScore:
                    annotations["q"] = edge.qScore
                adder(
                    graph,
                    u=_get_node(edge.id1),
                    v=_get_node(edge.id2),
                    citation="",
                    evidence="",
                    annotations=annotations,
                )

    return graph