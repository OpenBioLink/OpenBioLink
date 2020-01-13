from openbiolink.graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from openbiolink.graph_creation.types.dbType import DbType


class DbMetaEdgeStitchAction(DbMetadataEdge):
    NAME = 'Edge - STITCH - Gene Drug (Action)'
    URL = "http://stitch.embl.de/download/actions.v5.0/9606.actions.v5.0.tsv.gz"
    OFILE_NAME = "STITCH_gene_drug_actions.tsv.gz"
    COLS = ['item_id_a', 'item_id_b', 'mode', 'action', 'a_is_acting', 'score']
    FILTER_COLS = ['item_id_a', 'item_id_b', 'mode', 'action', 'score']
    HEADER = 1
    DB_TYPE = DbType.DB_EDGE_STITCH_ACTION

    def __init__(self):
        super().__init__(url=DbMetaEdgeStitchAction.URL,
                         ofile_name=DbMetaEdgeStitchAction.OFILE_NAME,
                         dbType=DbMetaEdgeStitchAction.DB_TYPE)
