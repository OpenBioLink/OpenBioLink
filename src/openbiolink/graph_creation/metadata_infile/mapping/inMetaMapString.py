from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.namespace import *


class InMetaMapString(InfileMetadata):
    CSV_NAME = "DB_String_mapping_gene_ncbi_string.csv"
    USE_COLS = ["ncbiID", "stringID"]
    SOURCE_COL = 1
    TARGET_COL = 0
    TARGET_NAMESPACE = Namespace(Namespaces.NCBI, False)
    MAPPING_SEP = "|"
    INFILE_TYPE = InfileType.IN_MAP_STRING

    def __init__(self):
        super().__init__(csv_name=InMetaMapString.CSV_NAME, cols=self.USE_COLS, infileType=InMetaMapString.INFILE_TYPE)
