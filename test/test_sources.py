import unittest
import urllib.request as request

from src.openbiolink import utils
from src.openbiolink.graph_creation.metadata_db_file import DbMetadata


class TestSources(unittest.TestCase):
    def test_valid_urls(self):
        db_metadata_classes = utils.get_leaf_subclasses(DbMetadata)
        opener = request.build_opener()
        opener.addheaders = [("User-agent", "Mozilla/5.0")]
        request.install_opener(opener)
        for cls in db_metadata_classes:
            with self.subTest(cls):
                url = cls.URL
                # if url.startswith('ftp'):
                self.assertTrue(utils.url_exists(url))
                # else:
                # assert(request.urlopen(cls.URL).status==200)
