from db.sourceDB import SourceDB

class SourceOntoDB (SourceDB):

    def __init__(self, url, ofile_name, csv_name, use_fields, quadruple_list, onto_mapping=None):
        super().__init__(url, ofile_name, csv_name, use_fields)
        # each quadruple consists of (1) beginning of the line, (2) split character,(3) index of split element being the id, (4) the name of dict entry (must be same as in use_fields)
        if onto_mapping is None:
            onto_mapping = []
        self.quadruple_list = quadruple_list
        self.onto_mapping = onto_mapping

