from graph_creation.Types.infileType import InfileType
from graph_creation.Types.mappingType import MappingType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata


class InMetaMapOntoGoAltid(InfileMetadata):

    CSV_NAME = "DB_ONTO_mapping_GO_alt_id.csv"
    USE_COLS = ['ID', 'ALT_ID']
    SOURCE_COL = 1
    TARGET_COL = 0
    MAPPING_SEP = ';'  # ';' sep is created while parsing
    INFILE_TYPE = InfileType.IN_MAP_ONTO_GO_ALT_ID

    MAP_TYPE = MappingType.ALT_GO_GO

    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaMapOntoGoAltid.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaMapOntoGoAltid.INFILE_TYPE)
