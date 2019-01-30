from graph_creation.Types.infileType import InfileType
from graph_creation.Types.mappingType import MappingType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata


class InMetaMapOntoDoAltid(InfileMetadata):

    CSV_NAME = "DB_ONTO_mapping_DO_alt_id.csv"
    USE_COLS = ['ID', 'ALT_ID']
    SOURCE_COL = 1
    TARGET_COL = 0
    MAPPING_SEP = ';'  # ';' sep is created while parsing
    INFILE_TYPE = InfileType.IN_MAP_ONTO_DO_ALT_ID

    MAP_TYPE = MappingType.ALT_DO_DO

    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaMapOntoDoAltid.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaMapOntoDoAltid.INFILE_TYPE)
