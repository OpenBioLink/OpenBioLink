import unittest

from src.openbiolink import utils
from src.openbiolink.graph_creation.types.dbType import DbType
from src.openbiolink.graph_creation.file_reader import *
from src.openbiolink.graph_creation.metadata_db_file import *


class TestDbMetaSubclasses(unittest.TestCase):
    def test_general_variables(self):
        leaf_classes = utils.get_leaf_subclasses(DbMetadata)
        for subclass in leaf_classes:
            with self.subTest(subclass=subclass):
                with self.subTest():
                    self.assertTrue(hasattr(subclass, "URL"))
                with self.subTest():
                    self.assertTrue(hasattr(subclass, "OFILE_NAME"))
                with self.subTest():
                    self.assertTrue(hasattr(subclass, "DB_TYPE"))

    def test_csv_variables(self):
        leaf_classes_csv_reader = utils.get_leaf_subclasses(CsvReader)
        csv_subclasses = set()
        for csv_reader_subclass in leaf_classes_csv_reader:
            csv_subclasses.add(csv_reader_subclass.DB_META_CLASS)
        for subclass in csv_subclasses:
            with self.subTest(subclass=subclass):
                self.assertTrue(hasattr(subclass, "COLS"))
                self.assertTrue(hasattr(subclass, "FILTER_COLS"))
                self.assertTrue(hasattr(subclass, "HEADER"))

    def test_obo_variables(self):
        leaf_classes_obo_reader = utils.get_leaf_subclasses(OboReader)
        obo_subclasses = set()
        for obo_reader_subclass in leaf_classes_obo_reader:
            obo_subclasses.add(obo_reader_subclass.DB_META_CLASS)
        for subclass in obo_subclasses:
            with self.subTest(subclass=subclass):
                self.assertTrue(hasattr(subclass, "QUADRUPLES"))

    # TODO test for sql ??

    def test_db_types(self):
        self.assertTrue(DbMetaEdgeBgeeExpr.DB_TYPE == DbType.DB_EDGE_BGEE)
        self.assertTrue(DbMetaEdgeBgeeDiffExpr.DB_TYPE == DbType.DB_EDGE_BGEE_DIFF)
        self.assertTrue(DbMetaEdgeCtdPath.DB_TYPE == DbType.DB_EDGE_CDT_PATH)
        self.assertTrue(DbMetaEdgeDisGeNet.DB_TYPE == DbType.DB_EDGE_DISGENET)
        self.assertTrue(DbMetaEdgeDrugCentral.DB_TYPE == DbType.DB_EDGE_DRUGCENTRAL)
        self.assertTrue(DbMetaEdgeString.DB_TYPE == DbType.DB_EDGE_STRING)
        self.assertTrue(DbMetaEdgeStitch.DB_TYPE == DbType.DB_EDGE_STITCH)
        self.assertTrue(DbMetaEdgeSiderSe.DB_TYPE == DbType.DB_EDGE_SIDER_SE)
        self.assertTrue(DbMetaEdgeHpoGene.DB_TYPE == DbType.DB_EDGE_HPO_GENE)
        self.assertTrue(DbMetaEdgeHpoDis.DB_TYPE == DbType.DB_EDGE_HPO_DIS)
        self.assertTrue(DbMetaEdgeTnHpoDis.DB_TYPE == DbType.DB_EDGE_TN_HPO_DIS)
        self.assertTrue(DbMetaEdgeGo.DB_TYPE == DbType.DB_EDGE_GO)

        self.assertTrue(DbMetaOntoDo.DB_TYPE == DbType.DB_ONTO_DO)
        self.assertTrue(DbMetaOntoGo.DB_TYPE == DbType.DB_ONTO_GO)
        self.assertTrue(DbMetaOntoHpo.DB_TYPE == DbType.DB_ONTO_HPO)

        self.assertTrue(DbMetaMapString.DB_TYPE == DbType.DB_MAP_STRING)
        self.assertTrue(DbMetaMapDisGeNet.DB_TYPE == DbType.DB_MAP_DISGENET)
        self.assertTrue(DbMetaMapUniprot.DB_TYPE == DbType.DB_MAP_UNIPROT)
