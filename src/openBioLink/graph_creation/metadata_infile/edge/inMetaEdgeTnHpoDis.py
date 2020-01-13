from openbiolink.edgeType import EdgeType
from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.nodeType import NodeType


class InMetaEdgeTnHpoDis(InfileMetadata):
    CSV_NAME = "DB_Tn_HPO_disease_phenotype.csv"
    USE_COLS = ['DB_ref', 'HPO_ID', 'evidence_code']
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    NODE1_TYPE = NodeType.DIS
    NODE2_TYPE = NodeType.PHENOTYPE
    EDGE_TYPE = EdgeType.DIS_PHENOTYPE
    INFILE_TYPE = InfileType.IN_EDGE_TN_HPO_DIS

    MAPPING_SEP = None

    def __init__(self):
        super().__init__(csv_name=InMetaEdgeTnHpoDis.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaEdgeTnHpoDis.INFILE_TYPE)
