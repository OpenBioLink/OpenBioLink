import logging
import sys

import numpy as np

from openbiolink import globalConfig
from openbiolink import globalConfig as globConst
from openbiolink.cli import Cli
from openbiolink.graph_creation.file_reader.fileReader import FileReader
from openbiolink.graph_creation.file_reader.parser.oboParser import OboParser


class OboReader(FileReader):

    def __init__(self, in_path, readerType, dbType, quadruple_list=None):
        ''' quadruple_list should contain all quadruples incl. mappings
        each quadruple consists of
        (1) beginning of the line,
        (2) split character,
        (3) index of split element being the id,
        (4) the name of dict entry (must be same as in use_fields)'''

        super().__init__(in_path, readerType, dbType)
        if quadruple_list is None:
            self.quadruple_list = [('id', ' ', 1, 'ID'),
                                   ('alt_id', ' ', 1, 'ALT_ID'),
                                   ('is_a', ' ', 1, 'IS_A'),
                                   ('xref: UMLS:', ':', 2, 'UMLS'),
                                   ('xref: OMIM:', ' ', 1, 'OMIM')]
        else:
            self.quadruple_list = quadruple_list

    def read_file(self):
        oboParser = OboParser()
        with FileReader.open_file(self.in_path) as file:
            df = oboParser.obo_to_df(file, self.quadruple_list)
            df_cols = df.columns
            defined_cols = [x[3] for x in self.quadruple_list]
            if len(df_cols) != len(defined_cols):

                no_occurences = [x for x in defined_cols if x not in df_cols]
                info_string = 'Reader %s should parse %s but there are no occurrences in file %s. ' % (
                str(self.readerType), str(no_occurences), self.in_path)
                if globalConfig.INTERACTIVE_MODE:
                    ask_continue_string = info_string + 'Continue if you do not need these edges in your graph'
                    if globConst.GUI_MODE:
                        from openbiolink.gui import gui
                        gui.askForExit(ask_continue_string)
                    else:
                        Cli.ask_for_exit(ask_continue_string)
                    for col in no_occurences:
                        df[col] = np.nan
                else:
                    logging.error(info_string)
                    sys.exit(info_string)

            return df
