from edgeType import EdgeType
from graph_creation.infileType import InfileType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata
from nodeType import NodeType


class InMetaEdgeHpoDis(InfileMetadata):
    CSV_NAME = "DB_HPO_disease_phenotype.csv"
    USE_COLS = ['DB_ref', 'HPO_ID', 'evidence_code']
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    NODE1_TYPE = NodeType.DIS  # fixme false use_cols
    NODE2_TYPE = NodeType.PHENOTYPE
    EDGE_TYPE = EdgeType.DIS_PHENOTYPE
    INFILE_TYPE = InfileType.IN_EDGE_HPO_DIS


    MAPPING_SEP = None
    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaEdgeHpoDis.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaEdgeHpoDis.INFILE_TYPE)
