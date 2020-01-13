from openbiolink.graph_creation.file_processor.fileProcessor import FileProcessor
from openbiolink.graph_creation.metadata_infile.mapping.inMetaMapDrugCentralPubchem import InMetaMapDrugCentralPubchem
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.graph_creation.types.readerType import ReaderType


class MapDrugCentralPubchemProcessor(FileProcessor):
    IN_META_CLASS = InMetaMapDrugCentralPubchem

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_MAP_DRUGCENTRAL_PUBCHEM,
                         infileType=InfileType.IN_MAP_DRUGCENTRAL_PUBCHEM, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)

    def individual_preprocessing(self, data):
        data = data[data.id_type == 'PUBCHEM_CID']
        return data
