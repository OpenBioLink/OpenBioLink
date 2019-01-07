from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.mapping.inMetaMapDrugCentralPubchem import InMetaMapDrugCentralPubchem



class MapDrugCentralPubchemProcessor(FileProcessor):

    def __init__(self):
        self.inMetaClass = InMetaMapDrugCentralPubchem
        self.use_cols = self.inMetaClass.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_MAP_DRUGCENTRAL_PUBCHEM,
                         infileType=InfileType.IN_MAP_DRUGCENTRAL_PUBCHEM, mapping_sep=self.inMetaClass.MAPPING_SEP)

    def individual_preprocessing(self, data):
        data = data[data.id_type == 'PUBCHEM_CID']
        return data