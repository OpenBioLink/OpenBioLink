from graph_creation.infileType import InfileType
from graph_creation.mappingType import MappingType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata


class InMetaMapUniEnsNcbi(InfileMetadata):

    CSV_NAME = "DB_Uniprot_mapping_gene_ensembl_ncbi.csv"
    USE_COLS = ['Ensembl', 'GeneID']
    SOURCE_COL = 0
    TARGET_COL = 1
    MAPPING_SEP = ";"
    INFILE_TYPE = InfileType.IN_MAP_UNI_ENS_NCBI

    MAP_TYPE = MappingType.ENSEMBL_NCBI

    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaMapUniEnsNcbi.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaMapUniEnsNcbi.INFILE_TYPE)
