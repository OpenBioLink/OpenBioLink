from edgeType import EdgeType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata
from nodeType import NodeType


class InMetaEdgeStitchActivation(InfileMetadata):
    CSV_NAME = "DB_STITCH_drug_activation_gene.csv"
    USE_COLS = ['item_id_a', 'item_id_b', 'score']
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = 2
    NODE1_TYPE = NodeType.DRUG
    NODE2_TYPE = NodeType.GENE
    EDGE_TYPE = EdgeType.DRUG_ACTIVATION_GENE
    INFILE_TYPE = InfileType.IN_EDGE_STITCH_ACTIVATION


    MAPPING_SEP = None

    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaEdgeStitchActivation.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaEdgeStitchActivation.INFILE_TYPE)
