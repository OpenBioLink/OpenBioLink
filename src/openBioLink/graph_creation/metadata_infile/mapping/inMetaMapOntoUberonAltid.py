from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType


class InMetaMapOntoUberonAltid(InfileMetadata):
    CSV_NAME = "DB_ONTO_mapping_UBERON_alt_id.csv"
    USE_COLS = ['ID', 'ALT_ID']
    SOURCE_COL = 1
    TARGET_COL = 0
    MAPPING_SEP = ';'  # ';' sep is created while parsing
    INFILE_TYPE = InfileType.IN_MAP_ONTO_UBERON_ALT_ID

    def __init__(self):
        super().__init__(csv_name=self.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=self.INFILE_TYPE)
