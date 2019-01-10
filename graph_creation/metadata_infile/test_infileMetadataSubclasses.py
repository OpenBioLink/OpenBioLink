from unittest import TestCase

from graph_creation.metadata_db_file import DbMetadata
from graph_creation.metadata_infile import *


class TestInfileMetadataSubclasses(TestCase):

    def check_general_variables(self,cls):
        self.assertTrue(hasattr(cls, 'CSV_NAME'))
        self.assertTrue(hasattr(cls, 'USE_COLS'))
        self.assertTrue(hasattr(cls, 'INFILE_TYPE'))
        self.assertTrue(hasattr(cls, 'INFILE_TYPE'))
        #warning
        self.assertTrue(hasattr(cls, 'MAPPING_SEP'))

    def check_edge_variables(self, cls):
        self.assertTrue(hasattr(cls, 'NODE1_COL'))
        self.assertTrue(hasattr(cls, 'NODE2_COL'))
        self.assertTrue(hasattr(cls, 'NODE1_TYPE'))
        self.assertTrue(hasattr(cls, 'NODE2_TYPE'))
        self.assertTrue(hasattr(cls, 'EDGE_TYPE'))
        self.assertTrue(hasattr(cls, 'USE_COLS'))
        #warning
        self.assertTrue(hasattr(cls, 'QSCORE_COL'))

    def check_onto_variables(self, cls):
        self.check_edge_variables(cls)
        self.assertTrue(cls, 'ONTO_TYPE')

    def check_mapping_variables(self,cls):
        self.assertTrue(hasattr(cls, 'SOURCE_COL'))
        self.assertTrue(hasattr(cls, 'TARGET_COL'))
        self.assertTrue(hasattr(cls, 'MAP_TYPE'))


