from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
from graph_creation.metadata_infile.onto.inMetaOntoHpo import InMetaOntoHpo



class OntoHpoProcessor(FileProcessor):

    def __init__(self):
        self.use_cols = InMetaOntoHpo.USE_COLS
        super().__init__(self.use_cols, dbType=DbType.DB_ONTO_HPO,
                         infileType=InfileType.IN_ONTO_HPO, mapping_sep=InMetaOntoHpo.MAPPING_SEP)