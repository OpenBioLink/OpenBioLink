from ...types.infileType import InfileType
from ...metadata_infile.infileMetadata import InfileMetadata


class InMetaMapDisGeNet(InfileMetadata):

    CSV_NAME = "DB_DisGeNet_mapping_disease_umls_do.csv"
    USE_COLS = ['umlsID', 'code']  # voc gets deleted while individual preprocessing
    SOURCE_COL = 0
    TARGET_COL = 1
    MAPPING_SEP = None
    INFILE_TYPE = InfileType.IN_MAP_DISGENET

    def __init__(self):
        super().__init__(csv_name=InMetaMapDisGeNet.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaMapDisGeNet.INFILE_TYPE)
