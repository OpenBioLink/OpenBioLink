from graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from graph_creation.dbType import DbType


class DbMetaEdgeString(DbMetadataEdge):
    URL = "https://stringdb-static.org/download/protein.links.v10.5/9606.protein.links.v10.5.txt.gz"
    OFILE_NAME = "STRING_gene_gene.txt.gz"
    COLS = ['string1', 'string2', 'qscore']
    FILTER_COLS = ['string1', 'string2', 'qscore']
    HEADER = 1
    DB_TYPE = DbType.DB_EDGE_STRING

    def __init__(self):
        super().__init__(url=DbMetaEdgeString.URL,
                         ofile_name=DbMetaEdgeString.OFILE_NAME,
                         dbType=DbMetaEdgeString.DB_TYPE)