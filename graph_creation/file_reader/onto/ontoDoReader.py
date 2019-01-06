from graph_creation.file_reader.oboReader import OboReader
from graph_creation.dbType import DbType
from graph_creation.metadata_db_file.onto.dbMetaOntoDo import DbMetaOntoDo
import graph_creation.globalConstant as g
import os

class OntoDoReader(OboReader):
    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, DbMetaOntoDo.OFILE_NAME),
            quadruple_list= DbMetaOntoDo.QUADRUPLES,
            dbType= DbType.DB_ONTO_DO
        )

