from openbiolink.graph_creation.metadata_infile.infileMetadata import InfileMetadata
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.namespace import *


class InMetaMapUniEnsNcbi(InfileMetadata):
    CSV_NAME = "DB_Uniprot_mapping_gene_ensembl_ncbi.csv"
    USE_COLS = ["Ensembl", "GeneID"]
    SOURCE_COL = 0
    TARGET_COL = 1
    TARGET_NAMESPACE = Namespace(Namespaces.NCBI, False)
    MAPPING_SEP = ";"
    INFILE_TYPE = InfileType.IN_MAP_UNI_ENS_NCBI

    def __init__(self):
        super().__init__(
            csv_name=InMetaMapUniEnsNcbi.CSV_NAME, cols=self.USE_COLS, infileType=InMetaMapUniEnsNcbi.INFILE_TYPE
        )
