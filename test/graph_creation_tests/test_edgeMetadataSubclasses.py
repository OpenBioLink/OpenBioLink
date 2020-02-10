from unittest import TestCase

from src.openbiolink import utils
from src.openbiolink.graph_creation.metadata_edge.tnEdgeRegularMetadata import *


class TestEdgeMetadataSubclasses(TestCase):
    def test_edge_variables(self):
        leaf_classes = utils.get_leaf_subclasses(EdgeMetadata)
        for cls in leaf_classes:
            with self.subTest(subclass=cls):
                self.assertTrue(hasattr(cls, "EDGE_INMETA_CLASS"))
            # self.assertTrue(hasattr(cls, "LQ_CUTOFF"))
            # self.assertTrue(hasattr(cls, "MQ_CUTOFF"))
            # self.assertTrue(hasattr(cls, "HQ_CUTOFF"))
            # self.assertTrue(hasattr(cls, "LQ_CUTOFF_TEXT"))
            # self.assertTrue(hasattr(cls, "MQ_CUTOFF_TEXT"))
            # self.assertTrue(hasattr(cls, "HQ_CUTOFF_TEXT"))
