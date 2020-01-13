from openbiolink.graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from openbiolink.graph_creation.types.dbType import DbType


class DbMetaEdgeStringAction(DbMetadataEdge):
    NAME = 'Edge - STRING - Gene Gene (Action)'

    # current link can be extracted from https://stringdb-static.org/cgi/download.pl?sessionId=FuXJ9a0fkSMB&species_text=Homo+sapiens
    URL = "https://stringdb-static.org/download/protein.actions.v11.0/9606.protein.actions.v11.0.txt.gz"
    OFILE_NAME = "STRING_gene_gene_actions.tsv.gz"  # tab separated txt file
    COLS = ['item_id_a', 'item_id_b', 'mode', 'action', 'is_directional', 'a_is_acting', 'score']
    FILTER_COLS = ['item_id_a', 'item_id_b', 'mode', 'action', 'is_directional', 'a_is_acting', 'score']
    HEADER = 1
    DB_TYPE = DbType.DB_EDGE_STRING_ACTION

    def __init__(self):
        super().__init__(url=self.URL,
                         ofile_name=self.OFILE_NAME,
                         dbType=self.DB_TYPE)
