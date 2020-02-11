from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.namespace import *
from openbiolink.nodeType import NodeType


class InMetaEdgeStitch(InfileMetadata):
    CSV_NAME = "DB_STITCH_gene_drug.csv"
    USE_COLS = ["stringID", "chemID", "qscore"]
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    SOURCE = "STITCH"
    NODE1_TYPE = NodeType.GENE
    NODE1_NAMESPACE = Namespace(Namespaces.ENSEMBL, False, mapping={"9606.": ""})
    NODE2_TYPE = NodeType.DRUG
    NODE2_NAMESPACE = Namespace(Namespaces.PUBCHEM, False)
    EDGE_TYPE = EdgeType.GENE_DRUG
    INFILE_TYPE = InfileType.IN_EDGE_STITCH

    MAPPING_SEP = None

    def __init__(self):
        super().__init__(
            csv_name=InMetaEdgeStitch.CSV_NAME, cols=self.USE_COLS, infileType=InMetaEdgeStitch.INFILE_TYPE
        )
