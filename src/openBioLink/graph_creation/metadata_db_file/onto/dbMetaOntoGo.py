from openbiolink.graph_creation.metadata_db_file.onto.dbMetadataOnto import DbMetadataOnto
from openbiolink.graph_creation.types.dbType import DbType


class DbMetaOntoGo(DbMetadataOnto):
    NAME = 'Onto - GO - is_a,part_of'
    URL = "http://purl.obolibrary.org/obo/go/go-basic.obo"
    OFILE_NAME = "GO_ontology.obo"
    QUADRUPLES = [('id', ' ', 1, 'ID'),
                  ('alt_id', ' ', 1, 'ALT_ID'),
                  ('is_a', ' ', 1, 'IS_A'),
                  ('relationship: part_of', ' ', 2, 'PART_OF')]
    DB_TYPE = DbType.DB_ONTO_GO

    def __init__(self):
        super().__init__(url=DbMetaOntoGo.URL,
                         ofile_name=DbMetaOntoGo.OFILE_NAME,
                         dbType=DbMetaOntoGo.DB_TYPE)
