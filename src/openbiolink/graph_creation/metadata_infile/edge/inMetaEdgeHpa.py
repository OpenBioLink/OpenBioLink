from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.namespace import *
from openbiolink.nodeType import NodeType


class InMetaEdgeHpa(InfileMetadata):
    CSV_NAME = "DB_HPA_gene_anatomy.csv"
    USE_COLS = ["geneID", "anatomy", "expressionValue"]
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    SOURCE = "HPA"
    NODE1_TYPE = NodeType.GENE
    NODE1_NAMESPACE = Namespace(Namespaces.NONE)
    NODE2_TYPE = NodeType.ANATOMY
    NODE2_NAMESPACE = Namespace(Namespaces.NONE)
    EDGE_TYPE = EdgeType.GENE_EXPRESSED_ANATOMY
    INFILE_TYPE = InfileType.IN_EDGE_HPA

    MAPPING_SEP = None

    def __init__(self):
        super().__init__(csv_name=InMetaEdgeHpa.CSV_NAME, cols=self.USE_COLS, infileType=InMetaEdgeHpa.INFILE_TYPE)
