from edgeType import EdgeType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata
from graph_creation.Types.ontoType import OntoType
from nodeType import NodeType


class InMetaOntoDoIsA(InfileMetadata):

    CSV_NAME = "DB_ONTO_DO_IS_A_ontology.csv"
    USE_COLS = ['ID', 'IS_A']
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = None
    NODE1_TYPE = NodeType.DIS
    NODE2_TYPE = NodeType.DIS
    EDGE_TYPE = EdgeType.IS_A
    MAPPING_SEP = ';'
    INFILE_TYPE = InfileType.IN_ONTO_DO_IS_A

    ONTO_TYPE = OntoType.DIS

    def __init__(self, folder_path):
        super().__init__(csv_name=self.CSV_NAME,
                         folder_path=folder_path,
                         infileType=self.INFILE_TYPE)
