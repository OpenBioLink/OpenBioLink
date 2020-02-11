import inspect
from unittest import TestCase

from src.openbiolink import utils
from src.openbiolink.graph_creation.metadata_infile import *


class TestInfileMetadataSubclasses(TestCase):
    def test_general_variables(self):
        leaf_classes = utils.get_leaf_subclasses(InfileMetadata)
        for cls in leaf_classes:
            with self.subTest(cls=cls):
                self.assertTrue(hasattr(cls, "CSV_NAME"))
                self.assertTrue(hasattr(cls, "USE_COLS"))
                self.assertTrue(hasattr(cls, "INFILE_TYPE"))
        # warning
        # self.assertTrue(hasattr(cls, 'MAPPING_SEP'))

    def test_edge_variables(self):
        edge_module = edge
        clsmembers = inspect.getmembers(edge_module, inspect.isclass)
        for clsName, cls in clsmembers:
            with self.subTest(cls=cls):
                self.assertTrue(hasattr(cls, "NODE1_COL"))
                self.assertTrue(hasattr(cls, "NODE2_COL"))
                self.assertTrue(hasattr(cls, "NODE1_TYPE"))
                self.assertTrue(hasattr(cls, "NODE2_TYPE"))
                self.assertTrue(hasattr(cls, "EDGE_TYPE"))
                self.assertTrue(hasattr(cls, "USE_COLS"))
                # warning
                # self.assertTrue(hasattr(cls, 'QSCORE_COL'))

    # def test_onto_variables(self):
    #     onto_module = onto
    #     with self.subTest():
    #         self.test_edge_variables()
    #     clsmembers = inspect.getmembers(onto_module, inspect.isclass)
    #     for clsName, cls in clsmembers:
    #         with self.subTest(cls=cls):
    #              self.assertTrue(cls, 'ONTO_TYPE')

    def test_mapping_variables(self):
        mapping_module = mapping
        clsmembers = inspect.getmembers(mapping_module, inspect.isclass)
        for clsName, cls in clsmembers:
            with self.subTest(cls=cls):
                self.assertTrue(hasattr(cls, "SOURCE_COL"))
                self.assertTrue(hasattr(cls, "TARGET_COL"))
