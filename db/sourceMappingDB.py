from db.sourceDB import SourceDB

class SourceMappingDB (SourceDB):

    def __init__(self, url, ofile_name, csv_name, cols, use_cols , nr_lines_header, mapping_sep =None, dtypes=None):
        super().__init__(url, ofile_name, csv_name, use_cols)
        self.nr_lines_header = nr_lines_header
        self.cols = cols
        self.mapping_sep = mapping_sep
        self.dtypes = dtypes
