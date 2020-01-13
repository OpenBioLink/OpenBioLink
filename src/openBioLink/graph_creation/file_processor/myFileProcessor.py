# from openbiolink.graph_creation.types.infileType import InfileType
# from openbiolink.graph_creation.types.readerType import ReaderType
from openbiolink.graph_creation.file_processor.fileProcessor import FileProcessor


class MyFileProcessor(FileProcessor):
    """ to create a new file processor
    *) declare the corresponding META_EDGE_CLASS, readerType, as well as infileType
    *) add pre- or post-processing steps if necessary
    *) for clearer structure, move class to corresponding module (and import in corresponding init)
    prior steps necessary:
    *) create META_EDGE_CLASS
    *) add readerType
    *) add infileType
     """

    IN_META_CLASS = None  # meta infile here

    def __init__(self):
        self.use_cols = self.IN_META_CLASS.USE_COLS
        super().__init__(self.use_cols,
                         readerType=None,  # reader type here
                         infileType=None,  # infile type here
                         mapping_sep=self.IN_META_CLASS.MAPPING_SEP)

    # def individual_preprocessing(self, data):
    """ data processing before selection of used columns """
    #    return data

    # def individual_postprocessing(self, data):
    """ data processing after selection of used columns """
    #    return data
