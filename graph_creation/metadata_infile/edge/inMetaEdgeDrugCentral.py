from edgeType import EdgeType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata
from nodeType import NodeType


class InMetaEdgeDrugCentral(InfileMetadata):
    CSV_NAME = "DB_DrugCentral_drug_indication_dis.csv"

    USE_COLS = [
        "struct_id",
        "umls_cui",
    ]
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = None
    NODE1_TYPE = NodeType.DRUG
    NODE2_TYPE = NodeType.DIS
    EDGE_TYPE = EdgeType.DIS_DRUG
    INFILE_TYPE = InfileType.IN_EDGE_DRUGCENTRAL_IND
    MAPPING_SEP = None

    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaEdgeDrugCentral.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaEdgeDrugCentral.INFILE_TYPE)
