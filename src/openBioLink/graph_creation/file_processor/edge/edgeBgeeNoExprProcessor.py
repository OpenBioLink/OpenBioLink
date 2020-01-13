from openbiolink.graph_creation.file_processor.fileProcessor import FileProcessor
from openbiolink.graph_creation.metadata_infile.edge.inMetaEdgeBgeeNoExpr import InMetaEdgeBgeeNoExpr
from openbiolink.graph_creation.types.infileType import InfileType
from openbiolink.graph_creation.types.readerType import ReaderType


class EdgeBgeeNoExprProcessor(FileProcessor):
    IN_META_CLASS = InMetaEdgeBgeeNoExpr

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_BGEE,
                         infileType=InfileType.IN_EDGE_BGEE_NO_EXPR, mapping_sep=self.IN_META_CLASS.MAPPING_SEP)

    def individual_preprocessing(self, data):
        data = data[data.expression == 'absent']
        return data
