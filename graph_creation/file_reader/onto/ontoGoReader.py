from graph_creation.file_reader.oboReader import OboReader
from graph_creation.dbType import DbType
from graph_creation.metadata_db_file.onto.dbMetaOntoGo import DbMetaOntoGo
import graph_creation.globalConstant as g
import os

class OntoGoReader(OboReader):
    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, DbMetaOntoGo.OFILE_NAME),
            quadruple_list= DbMetaOntoGo.QUADRUPLES,
            dbType= DbType.DB_ONTO_GO
        )

