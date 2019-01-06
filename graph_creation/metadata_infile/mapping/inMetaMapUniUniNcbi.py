from graph_creation.infileType import InfileType
from graph_creation.mappingType import MappingType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata


class InMetaMapUniUniNcbi(InfileMetadata):

    CSV_NAME = "DB_Uniprot_mapping_gene_uniprot_ncbi.csv"
    USE_COLS = ['UniProtKB-AC', 'GeneID']
    SOURCE_COL = 0
    TARGET_COL = 1
    MAPPING_SEP = ";"
    MAP_TYPE = MappingType.UNIPRO_NCBI
    INFILE_TYPE = InfileType.IN_MAP_UNI_UNI_NCBI


    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaMapUniUniNcbi.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaMapUniUniNcbi.INFILE_TYPE)
