from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
import graph_creation.constants.in_file.onto.inOntoDoConstant as constant



class OntoDoProcessor(FileProcessor):

    def __init__(self):
        self.use_cols =   constant.USE_COLS
        super().__init__(self.use_cols, dbType=DbType.DB_ONTO_DO, infileType=InfileType.IN_ONTO_DO, mapping_sep=constant.MAPPING_SEP)