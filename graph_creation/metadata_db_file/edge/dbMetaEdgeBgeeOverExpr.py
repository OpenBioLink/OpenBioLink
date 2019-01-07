from graph_creation.Types.dbType import DbType
from graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge


class DbMetaEdgeBgeeOverExpr(DbMetadataEdge):
        URL = "ftp://ftp.bgee.org/bgee_v13/download/calls/diff_expr_calls/Homo_sapiens_diffexpr-anatomy-simple.tsv.zip"
        OFILE_NAME = "BGEE_overexpr.tsv.zip"
        COLS = ['gene_id', 'gene_name', 'anatomical_entity', 'anatomical_entity_name',
                'developmental_stage', 'developmental_stage_name', 'differential_expr', 'call_quality']
        FILTER_COLS = ['gene_id', 'anatomical_entity', 'differential_expr','call_quality' ]
        HEADER = 1
        DB_TYPE = DbType.DB_EDGE_BGEE_OVER

        def __init__(self):
            super().__init__(url=DbMetaEdgeBgeeOverExpr.URL,
                             ofile_name=DbMetaEdgeBgeeOverExpr.OFILE_NAME,
                             dbType=DbMetaEdgeBgeeOverExpr.DB_TYPE)
