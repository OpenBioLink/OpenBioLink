from openbiolink.graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from openbiolink.graph_creation.types.dbType import DbType


class DbMetaEdgeGo(DbMetadataEdge):
    NAME = 'Edge - GO - GO Annotations'
    URL = "http://geneontology.org/gene-associations/goa_human.gaf.gz"
    OFILE_NAME = "GO_annotations.gaf.gz"
    COLS = ['DB', 'DOI', 'DB_symbol', 'qulifier', 'GO_ID', 'DB_ref', 'evidence_code',
            'with_from', 'aspect', 'DB_obj_name', 'DB_obj_syn', 'DB_obj_type', 'taxon', 'date', 'assigned_by',
            'ann_ext', 'ann_prop']
    FILTER_COLS = ['DOI', 'GO_ID', 'evidence_code']
    HEADER = 30
    DB_TYPE = DbType.DB_EDGE_GO

    def __init__(self):
        super().__init__(url=DbMetaEdgeGo.URL,
                         ofile_name=DbMetaEdgeGo.OFILE_NAME,
                         dbType=DbMetaEdgeGo.DB_TYPE)
