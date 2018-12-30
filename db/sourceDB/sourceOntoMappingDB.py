from db.sourceDB import SourceDB


class SourceOntoMappingDB (SourceDB):

    def __init__(self, url, ofile_name, csv_name, use_fields):

        super().__init__(url, ofile_name, csv_name, use_fields)
