from openbiolink.graph_creation.file_processor.fileProcessor import FileProcessor
from openbiolink.graph_creation.metadata_infile.edge.inMetaEdgeDrugCentral import InMetaEdgeDrugCentral
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.graph_creation.types.readerType import ReaderType


class EdgeDrugCentralIndProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeDrugCentral

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_DRUGCENTRAL_IND,
                         infileType=InfileType.IN_EDGE_DRUGCENTRAL_IND, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)

    def individual_preprocessing(self, data):
        data = data[data.relationship_name == 'indication']
        return data
