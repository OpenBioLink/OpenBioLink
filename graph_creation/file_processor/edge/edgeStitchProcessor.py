from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.Types.readerType import ReaderType
from graph_creation.Types.infileType import InfileType
from graph_creation.metadata_infile.edge.inMetaEdgeStitch import InMetaEdgeStitch


class EdgeStitchProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaEdgeStitch.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_EDGE_STITCH,
                         infileType=InfileType.IN_EDGE_STITCH, mapping_sep=InMetaEdgeStitch.MAPPING_SEP)


    def individual_postprocessing(self, data):
        data = data[data.chemID.str.startswith('CIDs')]
        self.stitch_to_pubchem_id(data,self.use_cols.index('chemID'))
        return data