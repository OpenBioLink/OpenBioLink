from graph_creation.file_reader.fileReader import FileReader
from graph_creation.file_reader.parser.oboParser import OboParser

class OboReader(FileReader):

    def __init__(self, in_path,dbType, quadruple_list = None):
        ''' quadruple_list should contain all quadruples incl. mappings
        each quadruple consists of
        (1) beginning of the line,
        (2) split character,
        (3) index of split element being the id,
        (4) the name of dict entry (must be same as in use_fields)'''

        self.in_path = in_path
        if quadruple_list is None:
            self.quadruple_list = [('id', ' ', 1, 'ID'),
                              ('alt_id', ' ', 1, 'ID'),
                              ('is_a', ' ', 1, 'IS_A'),
                                   ('xref: UMLS:', ':', 2, 'UMLS'),
                                   ('xref: OMIM:', ' ', 1, 'OMIM')]
        else:
            self.quadruple_list = quadruple_list
        self.dbType = dbType

    def read_file(self):
        oboParser = OboParser()
        file = FileReader.open_file(self.in_path)
        df = oboParser.obo_to_df(file, self.quadruple_list)
        return df
