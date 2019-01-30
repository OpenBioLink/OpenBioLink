from edgeType import EdgeType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata
from nodeType import NodeType


class InMetaEdgeStringExpression(InfileMetadata):
    CSV_NAME = "DB_STRING_gene_expression_gene.csv"
    USE_COLS = ['item_id_a', 'item_id_b', 'score']
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    NODE1_TYPE = NodeType.GENE
    NODE2_TYPE = NodeType.GENE
    EDGE_TYPE = EdgeType.GENE_EXPRESSION_GENE
    INFILE_TYPE = InfileType.IN_EDGE_STRING_EXPRESSION


    MAPPING_SEP = None

    def __init__(self, folder_path):
        super().__init__(csv_name=self.CSV_NAME,
                         folder_path=folder_path,
                         infileType=self.INFILE_TYPE)
