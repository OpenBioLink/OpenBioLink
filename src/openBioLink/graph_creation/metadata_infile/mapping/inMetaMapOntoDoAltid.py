from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType


class InMetaMapOntoDoAltid(InfileMetadata):
    CSV_NAME = "DB_ONTO_mapping_DO_alt_id.csv"
    USE_COLS = ['ID', 'ALT_ID']
    SOURCE_COL = 1
    TARGET_COL = 0
    MAPPING_SEP = ';'  # ';' sep is created while parsing
    INFILE_TYPE = InfileType.IN_MAP_ONTO_DO_ALT_ID

    def __init__(self):
        super().__init__(csv_name=InMetaMapOntoDoAltid.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaMapOntoDoAltid.INFILE_TYPE)
