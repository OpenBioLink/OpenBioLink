from graph_creation.metadata_db_file.onto.dbMetadataOnto import DbMetadataOnto
from graph_creation.dbType import DbType


class DbMetaOntoDo (DbMetadataOnto):
    URL = "https://raw.githubusercontent.com/DiseaseOntology/HumanDiseaseOntology/master/src/ontology/doid.obo"
    OFILE_NAME = "DO_ontology.obo"
    QUADRUPLES = [('id', ' ', 1, 'ID'),
                  ('alt_id', ' ', 1, 'ID'),
                  ('is_a', ' ', 1, 'IS_A'),
                  ('xref: UMLS_CUI:', ':', 2, 'UMLS'),  # mapping umls
                  ('xref: OMIM:', ' ', 1, 'OMIM')]  # mapping omim
    DB_TYPE = DbType.DB_ONTO_DO
    def __init__(self):
        super().__init__(url=DbMetaOntoDo.URL,
                         ofile_name= DbMetaOntoDo.OFILE_NAME,
                         dbType=DbMetaOntoDo.DB_TYPE)