from graph_creation.infileType import InfileType
from graph_creation.mappingType import MappingType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata


class InMetaMapOntoDoOmim(InfileMetadata):

    CSV_NAME = "DB_ONTO_mapping_DO_OMIM.csv"
    USE_COLS = ['ID', 'OMIM']
    SOURCE_COL = 1
    TARGET_COL = 0
    MAPPING_SEP = ';'  # ';' sep is created while parsing
    INFILE_TYPE = InfileType.IN_MAP_ONTO_DO_OMIM

    MAP_TYPE = MappingType.OMIM_DO

    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaMapOntoDoOmim.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaMapOntoDoOmim.INFILE_TYPE)
