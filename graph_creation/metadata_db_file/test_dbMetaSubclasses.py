import unittest

from graph_creation.Types.dbType import DbType
from graph_creation.metadata_db_file import *


class TestDbMetaSubclasses(unittest.TestCase):


    def test_general_variables(self):
        leaf_classes = self.get_leaf_subclasses(DbMetadata)
        for subclass in leaf_classes:
            with self.subTest(subclass = subclass):
                with self.subTest():
                    self.assertTrue(hasattr(subclass, 'URL'))
                with self.subTest():
                    self.assertTrue(hasattr(subclass, 'OFILE_NAME'))
                with self.subTest():
                    self.assertTrue(hasattr(subclass, 'DB_TYPE'))

    def check_csv_variables(self, cls): # TODO hwo to get scv dbs
        self.assertTrue(hasattr(cls, 'COLS'))
        self.assertTrue(hasattr(cls, 'FILTER_COLS'))
        self.assertTrue(hasattr(cls, 'HEADER'))

    def check_obo_variables(self, cls): # TODO how to get sql dbs
        self.assertTrue(hasattr(cls, 'QUADRUPLES'))

    def test_db_types(self):
        self.assertTrue(DbMetaEdgeBgeeExpr.DB_TYPE ==  DbType.DB_EDGE_BGEE)
        self.assertTrue(DbMetaEdgeBgeeOverExpr.DB_TYPE ==  DbType.DB_EDGE_BGEE_OVER)
        self.assertTrue(DbMetaEdgeCtdPath.DB_TYPE ==  DbType.DB_EDGE_CDT_PATH)
        self.assertTrue(DbMetaEdgeDisGeNet.DB_TYPE ==  DbType.DB_EDGE_DISGENET)
        self.assertTrue(DbMetaEdgeDrugCentral.DB_TYPE ==  DbType.DB_EDGE_DRUGCENTRAL)
        self.assertTrue(DbMetaEdgeString.DB_TYPE ==  DbType.DB_EDGE_STRING)
        self.assertTrue(DbMetaEdgeStitch.DB_TYPE ==  DbType.DB_EDGE_STITCH)
        self.assertTrue(DbMetaEdgeSiderSe.DB_TYPE ==  DbType.DB_EDGE_SIDER_SE)
        self.assertTrue(DbMetaEdgeHpoGene.DB_TYPE ==  DbType.DB_EDGE_HPO_GENE)
        self.assertTrue(DbMetaEdgeHpoDis.DB_TYPE ==  DbType.DB_EDGE_HPO_DIS)
        self.assertTrue(DbMetaEdgeGo.DB_TYPE ==  DbType.DB_EDGE_GO)

        self.assertTrue(DbMetaOntoDo.DB_TYPE ==  DbType.DB_ONTO_DO)
        self.assertTrue(DbMetaOntoGo.DB_TYPE ==  DbType.DB_ONTO_GO)
        self.assertTrue(DbMetaOntoHpo.DB_TYPE ==  DbType.DB_ONTO_HPO)

        self.assertTrue(DbMetaMapString ==  DbType.DB_MAP_STRING)
        self.assertTrue(DbMetaMapDisGeNet.DB_TYPE ==  DbType.DB_MAP_DISGENET)
        self.assertTrue(DbMetaMapUniprot.DB_TYPE ==  DbType.DB_MAP_UNIPROT)



    def get_leaf_subclasses(self, cls, classSet=None):
        if classSet is None:
            classSet = set()
        if len(cls.__subclasses__()) == 0:
            classSet.add(cls)
        else:
            classSet.union(x for c in cls.__subclasses__() for x in self.get_leaf_subclasses(c, classSet))
        return classSet

