from graph_creation.Types.infileType import InfileType
from graph_creation.Types.mappingType import MappingType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata


class InMetaMapOntoHpoUmls(InfileMetadata):

    CSV_NAME = "DB_ONTO_mapping_HPO_UMLS.csv"
    USE_COLS = ['ID', 'UMLS']
    SOURCE_COL = 1
    TARGET_COL = 0
    MAPPING_SEP = ';'
    INFILE_TYPE = InfileType.IN_MAP_ONTO_HPO_UMLS

    MAP_TYPE = MappingType.UMLS_HPO

    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaMapOntoHpoUmls.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaMapOntoHpoUmls.INFILE_TYPE)
