from openbiolink.graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from openbiolink.graph_creation.types.dbType import DbType


class DbMetaEdgeTnHpoDis(DbMetadataEdge):
    NAME = 'Edge - HPO - Disease Phenotype (Negative)'

    URL = "http://compbio.charite.de/jenkins/job/hpo.annotations/lastStableBuild/artifact/misc/negative_phenotype_annotation.tab"
    OFILE_NAME = "HPO_TN_disease_phenotype.tab"
    COLS = ['DB', 'DOI', 'DBname', 'qulifier', 'HPO_ID', 'DB_ref',
            'evidence_code', 'onsetMod', 'freq', 'sex',
            'mod', 'aspect', 'date', 'assigned_by']
    FILTER_COLS = ['DB_ref', 'HPO_ID', 'evidence_code']
    HEADER = 0
    DB_TYPE = DbType.DB_EDGE_TN_HPO_DIS

    def __init__(self):
        super().__init__(url=DbMetaEdgeTnHpoDis.URL,
                         ofile_name=DbMetaEdgeTnHpoDis.OFILE_NAME,
                         dbType=DbMetaEdgeTnHpoDis.DB_TYPE)
