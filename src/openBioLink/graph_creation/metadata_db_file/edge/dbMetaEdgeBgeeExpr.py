from openbiolink.graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from openbiolink.graph_creation.types.dbType import DbType


class DbMetaEdgeBgeeExpr(DbMetadataEdge):
    NAME = 'Edge - Bgee - presence/absence of expression'
    URL = "ftp://ftp.bgee.org/current/download/calls/expr_calls/Homo_sapiens_expr_simple.tsv.gz"
    OFILE_NAME = "BGEE_expr_calls.tsv.gz"

    COLS = ['gene_id', 'gene_name', 'anatomical_entity', 'anatomical_entity_name',
            'expression', 'call_quality', 'expression_rank']
    FILTER_COLS = ['gene_id', 'anatomical_entity', 'expression', 'call_quality']
    HEADER = 1
    DB_TYPE = DbType.DB_EDGE_BGEE

    def __init__(self):
        super().__init__(url=DbMetaEdgeBgeeExpr.URL,
                         ofile_name=DbMetaEdgeBgeeExpr.OFILE_NAME,
                         dbType=DbMetaEdgeBgeeExpr.DB_TYPE)
