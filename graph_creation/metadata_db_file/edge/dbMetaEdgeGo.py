from graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from graph_creation.Types.dbType import DbType


class DbMetaEdgeGo(DbMetadataEdge):
    URL = "http://geneontology.org/gene-associations/goa_human.gaf.gz"
    OFILE_NAME = "GO_annotations.gaf.gz"
    COLS = ['DB', 'DOI', 'qulifier', 'none13', 'GO_ID', 'DB_ref', 'evidence_code',
            'with_from', 'taxon', 'date', 'assigned_by', 'ann_ext', 'ann_prop',
            'none14', 'none15', 'none16', 'none17']
    FILTER_COLS = ['DOI', 'GO_ID', 'evidence_code']
    HEADER = 30
    DB_TYPE = DbType.DB_EDGE_GO


    def __init__(self):
        super().__init__(url= DbMetaEdgeGo.URL,
                         ofile_name=DbMetaEdgeGo.OFILE_NAME,
                         dbType=DbMetaEdgeGo.DB_TYPE)