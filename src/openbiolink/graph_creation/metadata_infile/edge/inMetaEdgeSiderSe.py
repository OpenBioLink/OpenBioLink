from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.namespace import *
from openbiolink.nodeType import NodeType


class InMetaEdgeSiderSe(InfileMetadata):
    CSV_NAME = "DB_SIDER_se.csv"
    USE_COLS = ["stitchID_stereo", "umlsID"]
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = None
    SOURCE = "SIDER"
    NODE1_TYPE = NodeType.DRUG
    NODE1_NAMESPACE = Namespace(Namespaces.PUBCHEM, False)
    NODE2_TYPE = NodeType.PHENOTYPE
    NODE2_NAMESPACE = Namespace(Namespaces.UMLS, False)
    EDGE_TYPE = EdgeType.DRUG_PHENOTYPE
    INFILE_TYPE = InfileType.IN_EDGE_SIDER_SE

    MAPPING_SEP = None

    def __init__(self):
        super().__init__(
            csv_name=InMetaEdgeSiderSe.CSV_NAME, cols=self.USE_COLS, infileType=InMetaEdgeSiderSe.INFILE_TYPE
        )
