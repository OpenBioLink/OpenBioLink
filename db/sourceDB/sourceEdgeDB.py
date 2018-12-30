from db.sourceDB import SourceDB

class SourceEdgeDB (SourceDB):

    def __init__(self, url, ofile_name, csv_name, cols, use_cols , nr_lines_header):
        super().__init__(url, ofile_name, csv_name, use_cols)
        self.nr_lines_header = nr_lines_header
        self.cols = cols
