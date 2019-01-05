from graph_creation.file_reader.fileReader import FileReader
import pandas

class CsvReader (FileReader):
    def __init__(self, in_path, dbType, sep = None, cols = None, use_cols = None, nr_lines_header = 0,  dtypes=None):
        self.in_path = in_path
        if sep is None:
            self.sep = CsvReader.get_sep(self.in_path)
        else:
            self.sep = sep
        self.cols = cols
        self.use_cols = use_cols
        self.nr_lines_header = nr_lines_header
        self.dtype = dtypes
        self.dbType = dbType

    @staticmethod
    def get_sep(in_path):
        path_parts = in_path.split('.')
        if (path_parts[1] == "txt"):
            sep = " "
        elif (path_parts[1] == "tsv" or path_parts[1] == "gaf" or path_parts[1] == "tab") :
            sep = "\t"
        else:
            sep = ","
        return sep

    def read_file(self):
        in_file = FileReader.open_file(self.in_path)
        data = pandas.read_csv(in_file, sep=self.sep, names=self.cols, usecols=self.use_cols, skiprows=self.nr_lines_header, dtype=self.dtype)
        return data
