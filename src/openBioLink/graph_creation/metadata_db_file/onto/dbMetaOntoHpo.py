from openbiolink.graph_creation.metadata_db_file.onto.dbMetadataOnto import DbMetadataOnto
from openbiolink.graph_creation.types.dbType import DbType


class DbMetaOntoHpo(DbMetadataOnto):
    NAME = 'Onto - HPO - is_a, mapping(umls->hpo)'
    URL = "https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo"
    OFILE_NAME = "HPO_ontology.obo"
    QUADRUPLES = [('id', ' ', 1, 'ID'),
                  ('alt_id', ' ', 1, 'ALT_ID'),
                  ('is_a', ' ', 1, 'IS_A'),
                  ('xref: UMLS:', ':', 2, 'UMLS')]  # mapping to UMLS
    DB_TYPE = DbType.DB_ONTO_HPO

    def __init__(self):
        super().__init__(url=DbMetaOntoHpo.URL,
                         ofile_name=DbMetaOntoHpo.OFILE_NAME,
                         dbType=DbMetaOntoHpo.DB_TYPE)
