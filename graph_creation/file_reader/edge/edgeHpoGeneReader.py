from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.Types.readerType import ReaderType
from graph_creation.metadata_db_file.edge.dbMetaEdgeHpoGene import DbMetaEdgeHpoGene
import graph_creation.globalConstant as g
import os


class EdgeHpoGeneReader(CsvReader):

    def __init__(self):
        self.dbMetaClass = DbMetaEdgeHpoGene
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, self.dbMetaClass.OFILE_NAME),
        sep = None,
            cols=self.dbMetaClass.COLS,
            use_cols=self.dbMetaClass.FILTER_COLS,
            nr_lines_header=self.dbMetaClass.HEADER,
        dtypes = None,
            readerType= ReaderType.READER_EDGE_HPO_GENE
        )

