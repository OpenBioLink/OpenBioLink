from graph_creation.file_reader.csvReader import CsvReader
from graph_creation.dbType import DbType
from graph_creation.metadata_db_file.edge.dbMetaEdgeHpoGene import DbMetaEdgeHpoGene
import graph_creation.globalConstant as g
import os


class EdgeHpoGeneReader(CsvReader):

    def __init__(self):
        super().__init__(
        in_path = os.path.join(g.O_FILE_PATH, DbMetaEdgeHpoGene.OFILE_NAME),
        sep = None,
            cols=DbMetaEdgeHpoGene.COLS,
            use_cols=DbMetaEdgeHpoGene.FILTER_COLS,
            nr_lines_header=DbMetaEdgeHpoGene.HEADER,
        dtypes = None,
            dbType= DbType.DB_EDGE_HPO_GENE
        )

