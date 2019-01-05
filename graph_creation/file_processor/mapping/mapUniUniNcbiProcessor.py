from graph_creation.file_processor.fileProcessor import FileProcessor
from graph_creation.dbType import DbType
from graph_creation.infileType import InfileType
import graph_creation.constants.in_file.mapping.inMapUniUniNcbiConstant as constant



class MapUniUniNcbiProcessor(FileProcessor):

    def __init__(self):
        super().__init__(constant.USE_COLS, dbType=DbType.DB_MAP_UNIPROT, infileType=InfileType.IN_MAP_UNI_UNI_NCBI, mapping_sep=constant.MAPPING_SEP)
