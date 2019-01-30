from graph_creation.Types.infileType import InfileType
from graph_creation.Types.mappingType import MappingType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata


class InMetaMapOntoHpoAltid(InfileMetadata):

    CSV_NAME = "DB_ONTO_mapping_HPO_alt_id.csv"
    USE_COLS = ['ID', 'ALT_ID']
    SOURCE_COL = 1
    TARGET_COL = 0
    MAPPING_SEP = ';'  # ';' sep is created while parsing
    INFILE_TYPE = InfileType.IN_MAP_ONTO_HPO_ALT_ID

    MAP_TYPE = MappingType.ALT_HPO_HPO

    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaMapOntoHpoAltid.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaMapOntoHpoAltid.INFILE_TYPE)
