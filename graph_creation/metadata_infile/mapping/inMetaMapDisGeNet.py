from graph_creation.infileType import InfileType
from graph_creation.mappingType import MappingType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata


class InMetaMapDisGeNet(InfileMetadata):

    CSV_NAME = "DB_DisGeNet_mapping_disease_umls_do.csv"
    USE_COLS = ['umlsID', 'code']  # voc gets deleted while individual preprocessing
    SOURCE_COL = 0
    TARGET_COL = 1
    MAPPING_SEP = None
    INFILE_TYPE = InfileType.IN_MAP_DISGENET
    MAP_TYPE = MappingType.UMLS_DO

    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaMapDisGeNet.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaMapDisGeNet.INFILE_TYPE)
