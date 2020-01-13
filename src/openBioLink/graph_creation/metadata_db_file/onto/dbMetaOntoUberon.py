from openbiolink.graph_creation.metadata_db_file.onto.dbMetadataOnto import DbMetadataOnto
from openbiolink.graph_creation.types.dbType import DbType


class DbMetaOntoUberon(DbMetadataOnto):
    NAME = 'Onto - HPO - is_a, part_of'
    URL = "http://ontologies.berkeleybop.org/uberon/ext.obo"
    OFILE_NAME = "UBERON_ontology.obo"
    QUADRUPLES = [('id', ' ', 1, 'ID'),
                  ('alt_id', ' ', 1, 'ALT_ID'),
                  ('is_a', ' ', 1, 'IS_A'),
                  ('relationship: part_of', ' ', 2, 'PART_OF')]
    DB_TYPE = DbType.DB_ONTO_UBERON

    def __init__(self):
        super().__init__(url=self.URL,
                         ofile_name=self.OFILE_NAME,
                         dbType=self.DB_TYPE)
