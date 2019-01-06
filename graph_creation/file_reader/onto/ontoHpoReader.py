from graph_creation.file_reader.oboReader import OboReader
from graph_creation.dbType import DbType
from graph_creation.metadata_db_file.onto.dbMetaOntoHpo import DbMetaOntoHpo
import graph_creation.globalConstant as g
import os


class OntoHpoReader(OboReader):
    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, DbMetaOntoHpo.OFILE_NAME),
            quadruple_list= DbMetaOntoHpo.QUADRUPLES,
            dbType= DbType.DB_ONTO_HPO
        )

