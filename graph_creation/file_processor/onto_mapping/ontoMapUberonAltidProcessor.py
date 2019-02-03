from graph_creation.Types.infileType import InfileType
from graph_creation.Types.readerType import ReaderType
from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.metadata_infile.mapping.inMetaMapOntoDoAltid import InMetaMapOntoDoAltid
from graph_creation.metadata_infile.mapping.inMetaMapOntoUberonAltid import InMetaMapOntoUberonAltid


class OntoMapUberonAltidProcessor(FileProcessor):

    META_INFILE_CLASS = InMetaMapOntoUberonAltid

    def __init__(self):
        self.use_cols =  self.META_INFILE_CLASS.USE_COLS
        super().__init__(self.use_cols, readerType=ReaderType.READER_ONTO_UBERON,
                         infileType=InfileType.IN_MAP_ONTO_UBERON_ALT_ID, mapping_sep=self.META_INFILE_CLASS.MAPPING_SEP)