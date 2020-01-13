from openbiolink.graph_creation.metadata_db_file.dbMetadata import DbMetadata


class DbMetadataMapping(DbMetadata):

    def __init__(self, url, ofile_name, dbType, dtypes=None):
        super().__init__(url, ofile_name, dbType)
        self.dtypes = dtypes
