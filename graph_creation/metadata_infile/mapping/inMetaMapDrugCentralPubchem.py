from graph_creation.Types.infileType import InfileType

from graph_creation.Types.mappingType import MappingType
from graph_creation.metadata_infile.infileMetadata import InfileMetadata


class InMetaMapDrugCentralPubchem(InfileMetadata):
    CSV_NAME = "DB_DrugCentral_mapping_drug_pubchem.csv"

    USE_COLS = [
        "identifier",
        "struct_id",
    ]
    SOURCE_COL = 1
    TARGET_COL = 0
    MAPPING_SEP = None
    INFILE_TYPE = InfileType.IN_MAP_DRUGCENTRAL_PUBCHEM
    MAP_TYPE = MappingType.DRUGCENTRAL_PUBCHEM


    def __init__(self, folder_path):
        super().__init__(csv_name=InMetaMapDrugCentralPubchem.CSV_NAME,
                         folder_path=folder_path,
                         infileType=InMetaMapDrugCentralPubchem.INFILE_TYPE)
