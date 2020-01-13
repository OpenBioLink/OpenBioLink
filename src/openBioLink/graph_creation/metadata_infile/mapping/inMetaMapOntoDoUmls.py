from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType


class InMetaMapOntoDoUmls(InfileMetadata):
    CSV_NAME = "DB_ONTO_mapping_DO_UMLS.csv"
    USE_COLS = ['ID', 'UMLS']
    SOURCE_COL = 1
    TARGET_COL = 0
    MAPPING_SEP = ';'
    INFILE_TYPE = InfileType.IN_MAP_ONTO_DO_UMLS

    def __init__(self):
        super().__init__(csv_name=InMetaMapOntoDoUmls.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaMapOntoDoUmls.INFILE_TYPE)
