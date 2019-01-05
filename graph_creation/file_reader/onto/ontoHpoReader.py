from graph_creation.file_reader.oboReader import OboReader
from graph_creation.dbType import DbType
import graph_creation.constants.db_file.onto.dbOntoHpoConstant as constant
import graph_creation.constants.globalConstant as g
import os


class OntoHpoReader(OboReader):
    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, constant.OFILE_NAME),
            quadruple_list= constant.QUADRUPLES,
            dbType= DbType.DB_ONTO_HPO
        )

