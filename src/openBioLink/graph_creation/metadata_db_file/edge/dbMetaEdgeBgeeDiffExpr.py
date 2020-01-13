from openbiolink.graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from openbiolink.graph_creation.types.dbType import DbType


class DbMetaEdgeBgeeDiffExpr(DbMetadataEdge):
    NAME = 'Edge - Bgee - differential expression (over-/under-expressed)'
    URL = "ftp://ftp.bgee.org/bgee_v13/download/calls/diff_expr_calls/Homo_sapiens_diffexpr-anatomy-simple.tsv.zip"
    OFILE_NAME = "BGEE_overexpr.tsv.zip"
    COLS = ['gene_id', 'gene_name', 'anatomical_entity', 'anatomical_entity_name',
            'developmental_stage', 'developmental_stage_name', 'differential_expr', 'call_quality']
    FILTER_COLS = ['gene_id', 'anatomical_entity', 'differential_expr', 'call_quality']
    HEADER = 1
    DB_TYPE = DbType.DB_EDGE_BGEE_DIFF

    def __init__(self):
        super().__init__(url=DbMetaEdgeBgeeDiffExpr.URL,
                         ofile_name=DbMetaEdgeBgeeDiffExpr.OFILE_NAME,
                         dbType=DbMetaEdgeBgeeDiffExpr.DB_TYPE)
