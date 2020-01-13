from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.nodeType import NodeType


class InMetaEdgeBgeeOverExpr(InfileMetadata):
    CSV_NAME = "DB_Bgee_gene_anatomy_overexpr.csv"
    USE_COLS = ['gene_id', 'anatomical_entity', 'call_quality']
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    NODE1_TYPE = NodeType.GENE
    NODE2_TYPE = NodeType.ANATOMY
    EDGE_TYPE = EdgeType.GENE_OVEREXPRESSED_ANATOMY
    INFILE_TYPE = InfileType.IN_EDGE_BGEE_OVEREXPR
    MAPPING_SEP = None

    def __init__(self):
        super().__init__(csv_name=InMetaEdgeBgeeOverExpr.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaEdgeBgeeOverExpr.INFILE_TYPE)
