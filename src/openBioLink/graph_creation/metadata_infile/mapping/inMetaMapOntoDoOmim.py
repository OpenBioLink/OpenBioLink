from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType


class InMetaMapOntoDoOmim(InfileMetadata):
    CSV_NAME = "DB_ONTO_mapping_DO_OMIM.csv"
    USE_COLS = ['ID', 'OMIM']
    SOURCE_COL = 1
    TARGET_COL = 0
    MAPPING_SEP = ';'  # ';' sep is created while parsing
    INFILE_TYPE = InfileType.IN_MAP_ONTO_DO_OMIM

    def __init__(self):
        super().__init__(csv_name=InMetaMapOntoDoOmim.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaMapOntoDoOmim.INFILE_TYPE)
