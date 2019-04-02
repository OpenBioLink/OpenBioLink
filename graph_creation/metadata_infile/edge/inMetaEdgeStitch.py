from edgeType import EdgeType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata
from nodeType import NodeType


class InMetaEdgeStitch(InfileMetadata):
    CSV_NAME = "DB_STITCH_gene_drug.csv"
    USE_COLS = ['stringID', 'chemID', 'qscore']
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    NODE1_TYPE = NodeType.GENE
    NODE2_TYPE = NodeType.DRUG
    EDGE_TYPE = EdgeType.GENE_DRUG
    INFILE_TYPE = InfileType.IN_EDGE_STITCH


    MAPPING_SEP = None

    def __init__(self):
        super().__init__(csv_name=InMetaEdgeStitch.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaEdgeStitch.INFILE_TYPE)
