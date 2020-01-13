from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType


class InMetaMapUniUniNcbi(InfileMetadata):
    CSV_NAME = "DB_Uniprot_mapping_gene_uniprot_ncbi.csv"
    USE_COLS = ['UniProtKB-AC', 'GeneID']
    SOURCE_COL = 0
    TARGET_COL = 1
    MAPPING_SEP = ";"
    INFILE_TYPE = InfileType.IN_MAP_UNI_UNI_NCBI

    def __init__(self):
        super().__init__(csv_name=InMetaMapUniUniNcbi.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaMapUniUniNcbi.INFILE_TYPE)
