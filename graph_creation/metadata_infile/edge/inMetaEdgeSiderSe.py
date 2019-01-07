from edgeType import EdgeType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata
from nodeType import NodeType


class InMetaEdgeSiderSe(InfileMetadata):
    CSV_NAME = "DB_SIDER_se.csv"
    USE_COLS = ['stitchID_flat', 'umlsID']
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = None
    NODE1_TYPE = NodeType.DRUG
    NODE2_TYPE = NodeType.PHENOTYPE
    EDGE_TYPE = EdgeType.DRUG_PHENOTYPE
    INFILE_TYPE = InfileType.IN_EDGE_SIDER_SE


    MAPPING_SEP = None

    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaEdgeSiderSe.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaEdgeSiderSe.INFILE_TYPE)
