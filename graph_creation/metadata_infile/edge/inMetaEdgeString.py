from edgeType import EdgeType
from graph_creation.infileType import InfileType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata
from nodeType import NodeType


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
    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaEdgeString.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaEdgeString.INFILE_TYPE)
