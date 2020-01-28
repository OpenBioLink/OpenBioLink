from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.nodeType import NodeType


class InMetaEdgeDrugCentralContraInd(InfileMetadata):
    CSV_NAME = "DB_DrugCentral_drug_contra_indication_dis.csv"

    USE_COLS = [
        "struct_id",
        "umls_cui",
    ]
    NODE1_COL = 1
    NODE2_COL = 0
    QSCORE_COL = None
    NODE1_TYPE = NodeType.DIS
    NODE2_TYPE = NodeType.DRUG
    EDGE_TYPE = EdgeType.DIS_DRUG
    INFILE_TYPE = InfileType.IN_EDGE_DRUGCENTRAL_CONTRA_IND
    MAPPING_SEP = None

    def __init__(self):
        super().__init__(csv_name=InMetaEdgeDrugCentralContraInd.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaEdgeDrugCentralContraInd.INFILE_TYPE)
