from ...types.dbType import DbType
from ...file_reader.oboReader import OboReader
from ...types.readerType import ReaderType
from ...metadata_db_file.onto.dbMetaOntoHpo import DbMetaOntoHpo
from ... import graphCreationConfig as g
import os


class OntoHpoReader(OboReader):
    DB_META_CLASS = DbMetaOntoHpo

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, self.DB_META_CLASS.OFILE_NAME),
            quadruple_list= self.DB_META_CLASS.QUADRUPLES,
            readerType= ReaderType.READER_ONTO_HPO,
        dbType = DbType.DB_ONTO_HPO
        )

