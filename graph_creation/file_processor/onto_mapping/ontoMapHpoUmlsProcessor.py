from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
import graph_creation.constants.in_file.mapping.inMapOntoHpoUmlsConstant as constant


class OntoMapHpoUmlsProcessor(FileProcessor):

    def __init__(self):
        self.use_cols =   constant.USE_COLS
        super().__init__(self.use_cols, dbType=DbType.DB_ONTO_HPO, infileType=InfileType.IN_MAP_ONTO_HPO_UMLS, mapping_sep= constant.MAPPING_SEP)