from openbiolink.graph_creation.metadata_db_file.dbMetadata import DbMetadata


class DbMetadataOnto(DbMetadata):

    def __init__(self, url, ofile_name, dbType):
        super().__init__(url, ofile_name, dbType)
