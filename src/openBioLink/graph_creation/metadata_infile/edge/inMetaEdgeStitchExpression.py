from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.nodeType import NodeType


class InMetaEdgeStitchExpression(InfileMetadata):
    CSV_NAME = "DB_STITCH_drug_expression_gene.csv"
    USE_COLS = ['item_id_a', 'item_id_b', 'score']
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    NODE1_TYPE = NodeType.DRUG
    NODE2_TYPE = NodeType.GENE
    EDGE_TYPE = EdgeType.DRUG_EXPRESSION_GENE
    INFILE_TYPE = InfileType.IN_EDGE_STITCH_EXPRESSION

    MAPPING_SEP = None

    def __init__(self):
        super().__init__(csv_name=InMetaEdgeStitchExpression.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaEdgeStitchExpression.INFILE_TYPE)
