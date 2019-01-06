import os
import urllib
import urllib.request
from graph_creation.dbType import DbType

class DbMetadata:

    def __init__(self, url, ofile_name, dbType):
        self.url = url
        self.ofile_name = ofile_name
        self.dbType = dbType