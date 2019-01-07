from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeDrugCentral import InMetaEdgeDrugCentral



class EdgeDrugCentralIndProcessor(FileProcessor):

    def __init__(self):
        self.inMetaClass = InMetaEdgeDrugCentral
        self.use_cols = self.inMetaClass.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_DRUGCENTRAL_IND,
                         infileType=InfileType.IN_EDGE_DRUGCENTRAL_IND, mapping_sep=self.inMetaClass.MAPPING_SEP)

    def individual_preprocessing(self, data):
        data = data[data.relationship_name == 'indication']
        return data