from graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from graph_creation.Types.dbType import DbType


class DbMetaEdgeStitch(DbMetadataEdge):
    URL = "http://stitch.embl.de/download/protein_chemical.links.v5.0/9606.protein_chemical.links.v5.0.tsv.gz"
    OFILE_NAME = "STITCH_gene_drug.tsv.gz"
    COLS = ['chemID', 'stringID', 'qscore']
    FILTER_COLS = ['stringID', 'chemID', 'qscore']  # todo why does this not work when other order -.-
    HEADER = 1
    DB_TYPE = DbType.DB_EDGE_STITCH

    def __init__(self):
        super().__init__(url=DbMetaEdgeStitch.URL,
                         ofile_name=DbMetaEdgeStitch.OFILE_NAME ,
                         dbType=DbMetaEdgeStitch.DB_TYPE)