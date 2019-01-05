from graph_creation.file_reader.fileReader import FileReader
from graph_creation.file_reader.parser.postgresDumpParser import PostgresDumpParser as dcp

class SqlReader(FileReader):

    def __init__(self, in_path, table_name, dbType):
        self.in_path = in_path
        self.table_name = table_name
        self.dbType = dbType

    def read_file(self):
        file = FileReader.open_file(self.in_path)
        df = dcp.table_to_df(file, self.table_name)
        return df
