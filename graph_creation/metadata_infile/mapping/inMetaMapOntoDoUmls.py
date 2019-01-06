from graph_creation.infileType import InfileType
from graph_creation.mappingType import MappingType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata


class InMetaMapOntoDoUmls(InfileMetadata):

    CSV_NAME = "DB_ONTO_mapping_DO_UMLS.csv"
    USE_COLS = ['ID', 'UMLS']
    SOURCE_COL = 1
    TARGET_COL = 0
    MAPPING_SEP = ';'
    INFILE_TYPE = InfileType.IN_MAP_ONTO_DO_UMLS

    MAP_TYPE = MappingType.UMLS_DO

    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaMapOntoDoUmls.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaMapOntoDoUmls.INFILE_TYPE)
