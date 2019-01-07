from graph_creation.Types.infileType import InfileType
from graph_creation.Types.mappingType import MappingType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata


class InMetaMapString(InfileMetadata):

    CSV_NAME = "DB_String_mapping_gene_ncbi_string.csv"
    USE_COLS = ['ncbiID', 'stringID']
    SOURCE_COL = 1
    TARGET_COL = 0
    MAPPING_SEP = None
    INFILE_TYPE = InfileType.IN_MAP_STRING
    MAP_TYPE = MappingType.STRING_NCBI

    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaMapString.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaMapString.INFILE_TYPE)
