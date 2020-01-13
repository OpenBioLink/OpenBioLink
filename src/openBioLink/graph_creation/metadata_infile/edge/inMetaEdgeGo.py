from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.nodeType import NodeType


class InMetaEdgeGo(InfileMetadata):
    CSV_NAME = "DB_GO_annotations.csv"
    USE_COLS = ['DOI', 'GO_ID', 'evidence_code']
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    NODE1_TYPE = NodeType.GENE
    NODE2_TYPE = NodeType.GO
    EDGE_TYPE = EdgeType.GENE_GO
    INFILE_TYPE = InfileType.IN_EDGE_GO
    MAPPING_SEP = None

    def __init__(self):
        super().__init__(csv_name=InMetaEdgeGo.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaEdgeGo.INFILE_TYPE)
