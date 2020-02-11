from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.namespace import *
from openbiolink.nodeType import NodeType


class InMetaEdgeSiderInd(InfileMetadata):
    CSV_NAME = "DB_SIDER_dis_drug.csv"
    USE_COLS = ["umlsID", "stichID", "method"]
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    SOURCE = "SIDER"
    NODE1_TYPE = NodeType.DIS
    NODE1_NAMESPACE = Namespace(Namespaces.NONE)
    NODE2_TYPE = NodeType.DRUG
    NODE2_NAMESPACE = Namespace(Namespaces.NONE)
    EDGE_TYPE = EdgeType.DIS_DRUG
    INFILE_TYPE = InfileType.IN_EDGE_SIDER_IND

    MAPPING_SEP = None

    def __init__(self):
        super().__init__(
            csv_name=InMetaEdgeSiderInd.CSV_NAME, cols=self.USE_COLS, infileType=InMetaEdgeSiderInd.INFILE_TYPE
        )
