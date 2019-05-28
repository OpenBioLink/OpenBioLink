from ...types.infileType import InfileType

from ...metadata_infile.infileMetadata import InfileMetadata


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


    def __init__(self):
        super().__init__(csv_name=InMetaMapDrugCentralPubchem.CSV_NAME,
                         cols=self.USE_COLS,
                         infileType=InMetaMapDrugCentralPubchem.INFILE_TYPE)
