from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.nodeType import NodeType


class InMetaEdgeString(InfileMetadata):
    CSV_NAME = "DB_STRING_gene_gene.csv"
    USE_COLS = ['string1', 'string2', 'qscore']
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    NODE1_TYPE = NodeType.GENE
    NODE2_TYPE = NodeType.GENE
    EDGE_TYPE = EdgeType.GENE_GENE
    INFILE_TYPE = InfileType.IN_EDGE_STRING

    MAPPING_SEP = None

    def __init__(self):
        super().__init__(csv_name=InMetaEdgeString.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaEdgeString.INFILE_TYPE)
