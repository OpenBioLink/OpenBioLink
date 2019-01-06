from edgeType import EdgeType
from graph_creation.infileType import InfileType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata
from nodeType import NodeType


class InMetaEdgeHpa(InfileMetadata):
    CSV_NAME = "DB_HPA_gene_anatomy.csv"
    USE_COLS = ['geneID', 'anatomy', 'expressionValue']
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    NODE1_TYPE = NodeType.GENE
    NODE2_TYPE = NodeType.ANATOMY
    EDGE_TYPE = EdgeType.GENE_ANATOMY
    INFILE_TYPE = InfileType.IN_EDGE_HPA


    MAPPING_SEP = None
    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaEdgeHpa.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaEdgeHpa.INFILE_TYPE)
