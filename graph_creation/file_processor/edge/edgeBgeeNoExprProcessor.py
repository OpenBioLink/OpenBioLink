from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeBgeeNoExpr import InMetaEdgeBgeeNoExpr


class EdgeBgeeNoExprProcessor(FileProcessor):

    def __init__(self):
        self.MetaInfileClass = InMetaEdgeBgeeNoExpr
        self.use_cols =   self.MetaInfileClass.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_BGEE,
                         infileType=InfileType.IN_EDGE_BGEE_NO_EXPR, mapping_sep= self.MetaInfileClass.MAPPING_SEP)

    def individual_preprocessing(self, data):
        data = data[data.expression == 'absent']
        return data