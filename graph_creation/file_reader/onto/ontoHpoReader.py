from graph_creation.file_reader.oboReader import OboReader
from graph_creation.Types.readerType import ReaderType
from graph_creation.metadata_db_file.onto.dbMetaOntoHpo import DbMetaOntoHpo
import graph_creation.globalConstant as g
import os


class OntoHpoReader(OboReader):
    def __init__(self):
        self.dbMetaClass = DbMetaOntoHpo

        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, self.dbMetaClass.OFILE_NAME),
            quadruple_list= self.dbMetaClass.QUADRUPLES,
            readerType= ReaderType.READER_ONTO_HPO
        )

