from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType


class InMetaMapOntoHpoUmls(InfileMetadata):
    CSV_NAME = "DB_ONTO_mapping_HPO_UMLS.csv"
    USE_COLS = ['ID', 'UMLS']
    SOURCE_COL = 1
    TARGET_COL = 0
    MAPPING_SEP = ';'
    INFILE_TYPE = InfileType.IN_MAP_ONTO_HPO_UMLS

    def __init__(self):
        super().__init__(csv_name=InMetaMapOntoHpoUmls.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaMapOntoHpoUmls.INFILE_TYPE)
