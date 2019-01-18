from unittest import TestCase


class TestEdgeMetadataSubclasses(TestCase):

    def check_edge_variables(self,cls):
        self.assertTrue(hasattr(cls, "LQ_CUTOFF"))
        self.assertTrue(hasattr(cls, "MQ_CUTOFF"))
        self.assertTrue(hasattr(cls, "HQ_CUTOFF"))
        self.assertTrue(hasattr(cls, "LQ_CUTOFF_TEXT"))
        self.assertTrue(hasattr(cls, "MQ_CUTOFF_TEXT"))
        self.assertTrue(hasattr(cls, "HQ_CUTOFF_TEXT"))