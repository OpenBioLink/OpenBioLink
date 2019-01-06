from graph_creation.metadata_db_file.dbMetadata import DbMetadata

class DbMetadataOnto (DbMetadata):

    def __init__(self, url, ofile_name, dbType, onto_mapping=None):
        super().__init__(url, ofile_name, dbType)
        if onto_mapping is None:
            onto_mapping = []
        self.onto_mapping = onto_mapping


