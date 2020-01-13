from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType


class InMetaMapUniEnsNcbi(InfileMetadata):
    CSV_NAME = "DB_Uniprot_mapping_gene_ensembl_ncbi.csv"
    USE_COLS = ['Ensembl', 'GeneID']
    SOURCE_COL = 0
    TARGET_COL = 1
    MAPPING_SEP = ";"
    INFILE_TYPE = InfileType.IN_MAP_UNI_ENS_NCBI

    def __init__(self):
        super().__init__(csv_name=InMetaMapUniEnsNcbi.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaMapUniEnsNcbi.INFILE_TYPE)
