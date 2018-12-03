from db.sourceDB import SourceDB

class SourceOntoDB (SourceDB):

    def __init__(self, url, ofile_name, csv_name, use_cols):
        super().__init__(url, ofile_name, csv_name, use_cols)

