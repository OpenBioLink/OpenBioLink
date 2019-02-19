from edgeType import EdgeType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata
from graph_creation.Types.ontoType import OntoType
from nodeType import NodeType


class InMetaOntoGoPartOf(InfileMetadata):

    CSV_NAME = "DB_ONTO_GO_PART_OF_ontology.csv"
    USE_COLS = ['ID', 'PART_OF']
    NODE1_COL = 0
    NODE2_COL = 1
    QSCORE_COL = None
    NODE1_TYPE = NodeType.GO
    NODE2_TYPE = NodeType.GO
    EDGE_TYPE = EdgeType.PART_OF
    MAPPING_SEP = ';'
    INFILE_TYPE = InfileType.IN_ONTO_GO_PART_OF
    ONTO_TYPE = OntoType.GO


    def __init__(self, folder_path):
        super().__init__(csv_name=self.CSV_NAME,
                         folder_path=folder_path,
                         infileType=self.INFILE_TYPE)
