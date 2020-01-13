from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.nodeType import NodeType


class InMetaEdgeCdtPath(InfileMetadata):
    CSV_NAME = "DB_CDT_gene_pathway.csv"
    USE_COLS = ['geneID', 'pathID']
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = None
    NODE1_TYPE = NodeType.GENE
    NODE2_TYPE = NodeType.PATHWAY
    EDGE_TYPE = EdgeType.GENE_PATHWAY
    INFILE_TYPE = InfileType.IN_EDGE_CDT_PATH
    MAPPING_SEP = None

    def __init__(self):
        super().__init__(csv_name=InMetaEdgeCdtPath.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaEdgeCdtPath.INFILE_TYPE)
