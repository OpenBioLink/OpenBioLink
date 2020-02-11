import os
import unittest
import src.openbiolink.utils as utils
import pandas
import numpy as np

from src.openbiolink.edgeType import EdgeType


class TestUtils(unittest.TestCase):

    # ----- get_leaf_subclasses -------
    def test_get_leaf_subclasses_no_subclasses(self):
        # given
        class A:
            pass

        cls = A
        # when
        result = utils.get_leaf_subclasses(cls)
        # then
        true_result = {A}
        self.assertEqual(true_result, result)

    def test_get_leaf_subclasses_one_lvl(self):
        # given
        class A:
            pass

        class B(A):
            pass

        cls = A
        # when
        result = utils.get_leaf_subclasses(cls)
        # then
        true_result = {B}
        self.assertEqual(true_result, result)

    def test_get_leaf_subclasses_two_lvl(self):
        # given
        class A:
            pass

        class B(A):
            pass

        class C(B):
            pass

        cls = A
        # when
        result = utils.get_leaf_subclasses(cls)
        # then
        true_result = {C}
        self.assertEqual(true_result, result)

    def test_get_leaf_subclasses_diff_lvls(self):
        # given
        class A:
            pass

        class B(A):
            pass

        class C(B):
            pass

        class D(A):
            pass

        cls = A
        # when
        result = utils.get_leaf_subclasses(cls)
        # then
        true_result = {C, D}

    def test_get_leaf_subclasses_None(self):
        # given
        cls = None
        # when
        result = utils.get_leaf_subclasses(cls)
        # then
        true_result = None
        self.assertEqual(true_result, result)

    # ----- make_undir -------
    def test_make_undir_all_undir(self):
        # given
        df = pandas.DataFrame({"id1": list("abc"), "id2": list("xyz")})
        # when
        result = utils.make_undir(df)
        # then
        true_result = df
        np.testing.assert_array_equal(true_result, result)

    def test_make_undir_all_dir(self):
        # given
        df = pandas.DataFrame({"id1": list("abcd"), "id2": list("badc")})
        # when
        result = utils.make_undir(df)
        # then
        true_result = pandas.DataFrame({"id1": list("ac"), "id2": list("bd")})
        np.testing.assert_array_equal(true_result, result)

    def test_make_undir_mixed(self):
        # given
        df = pandas.DataFrame({"id1": list("abc"), "id2": list("cxa")})
        # when
        result = utils.make_undir(df)
        # then
        true_result = pandas.DataFrame({"id1": list("ab"), "id2": list("cx")})
        np.testing.assert_array_equal(true_result, result)

    def test_db_mapping_file_to_dic(self):
        # given
        # file with content
        # x	foo	a
        # y	bar	a; b
        # z	baz
        # q		c
        path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(path, "test_mapping_file.tsv")
        # when
        result = utils.db_mapping_file_to_dic(file_path, 0, 2, "\t")
        # then
        true_result = {"x": ["a"], "y": ["a; b"], "q": ["c"]}
        self.assertEqual(true_result, result)

    def test_cls_list_to_dic(self):
        self.fail()

    def test_file_exists(self):
        self.fail()

    def test_get_diff(self):
        self.fail()

    # ----- remove_parent_duplicates_and_reverses -----

    def test_remove_parent_parent_in_remain(self):
        # given
        remove = pandas.DataFrame(
            {"id1": ["a"], "edgeType": [EdgeType.GENE_REACTION_GENE], "id2": ["0"], "qscore": "100", "value": [1]}
        )
        remain = pandas.DataFrame(
            {
                "id1": ["a", "b", "c"],
                "edgeType": [EdgeType.GENE_GENE, EdgeType.GENE_GENE, EdgeType.GENE_GENE],
                "id2": ["0", "1", "2"],
                "qscore": [120.0, 50, 20],
                "value": [1, 1, 0],
            }
        )
        # when
        result = utils.remove_parent_duplicates_and_reverses(remove_set=remove, remain_set=remain)
        # then
        true_result = pandas.DataFrame(
            {
                "id1": ["b", "c"],
                "edgeType": [EdgeType.GENE_GENE, EdgeType.GENE_GENE],
                "id2": ["1", "2"],
                "qscore": [50, 20],
                "value": [1, 0],
            }
        )
        np.testing.assert_array_equal(true_result.values, result.values)

    def test_remove_parent_parent_in_remove(self):
        # given
        remove = pandas.DataFrame(
            {"id1": ["a"], "edgeType": [EdgeType.GENE_GENE], "id2": ["0"], "qscore": "100", "value": list("x")}
        )
        remain = pandas.DataFrame(
            {
                "id1": ["a", "b", "c"],
                "edgeType": [EdgeType.GENE_REACTION_GENE, EdgeType.GENE_REACTION_GENE, EdgeType.GENE_REACTION_GENE],
                "id2": ["0", "1", "2"],
                "value": list("xxy"),
            }
        )
        # when
        result = utils.remove_parent_duplicates_and_reverses(remove_set=remove, remain_set=remain)
        # then
        true_result = pandas.DataFrame(
            {
                "id1": ["a", "b", "c"],
                "edgeType": [EdgeType.GENE_REACTION_GENE, EdgeType.GENE_REACTION_GENE, EdgeType.GENE_REACTION_GENE],
                "id2": ["0", "1", "2"],
                "qscore": [100.0, 50, 20],
                "value": list("xxy"),
            }
        )
        np.testing.assert_array_equal(true_result.values, result.values)

    def test_remove_parent_reverse_parent(self):
        # given
        remove = pandas.DataFrame(
            {"id1": ["a"], "edgeType": [EdgeType.GENE_REACTION_GENE], "id2": ["0"], "qscore": ["a"], "value": list("x")}
        )
        remain = pandas.DataFrame(
            {
                "id1": ["0", "b", "c"],
                "edgeType": [EdgeType.GENE_GENE, EdgeType.GENE_GENE, EdgeType.GENE_GENE],
                "id2": ["a", "1", "2"],
                "qscore": [100.0, 50, 20],
                "value": list("xxy"),
            }
        )
        # when
        result = utils.remove_parent_duplicates_and_reverses(remove_set=remove, remain_set=remain)
        # then
        true_result = pandas.DataFrame(
            {
                "id1": ["b", "c"],
                "edgeType": [EdgeType.GENE_GENE, EdgeType.GENE_GENE],
                "id2": ["1", "2"],
                "qscore": [50, 20],
                "value": list("xy"),
            }
        )
        np.testing.assert_array_equal(true_result.values, result.values)

    def test_remove_parent_child_and_parent_and_sibling_in_remain(self):
        # given
        remove = pandas.DataFrame(
            {"id1": ["a"], "edgeType": [EdgeType.GENE_REACTION_GENE], "id2": ["0"], "qscore": "100", "value": list("x")}
        )
        remain = pandas.DataFrame(
            {
                "id1": ["a", "a", "a"],
                "edgeType": [EdgeType.GENE_GENE, EdgeType.GENE_EXPRESSION_GENE, EdgeType.GENE_REACTION_GENE],
                "id2": ["0", "0", "0"],
                "qscore": [100.0, 50, 20],
                "value": list("xxx"),
            }
        )
        # when
        result = utils.remove_parent_duplicates_and_reverses(remove_set=remove, remain_set=remain)
        # then
        true_result = pandas.DataFrame(
            {
                "id1": ["a", "a"],
                "edgeType": [EdgeType.GENE_EXPRESSION_GENE, EdgeType.GENE_REACTION_GENE],
                "id2": ["0", "0"],
                "qscore": [50, 20],
                "value": list("xx"),
            }
        )
        np.testing.assert_array_equal(true_result.values, result.values)

    def test_remove_parent_empty_remove(self):
        # given
        remove = pandas.DataFrame()
        remain = pandas.DataFrame(
            {
                "id1": ["a", "a", "a"],
                "edgeType": [EdgeType.GENE_GENE, EdgeType.GENE_EXPRESSION_GENE, EdgeType.GENE_REACTION_GENE],
                "id2": ["0", "0", "0"],
                "qscore": [100.0, 50, 20],
                "value": list("xxx"),
            }
        )
        # when
        result = utils.remove_parent_duplicates_and_reverses(remove_set=remove, remain_set=remain)
        # then
        true_result = remain.copy()
        np.testing.assert_array_equal(true_result.values, result.values)

    # ----- remove_reverse_edges -------
    def test_remove_reverse_edges(self):
        # given
        remove = pandas.DataFrame(
            {"id1": [0, 1, 2, 3], "edgeType": list("xxxx"), "id2": list("abcd"), "value": list("xxxx")}
        )
        remain = pandas.DataFrame(
            {"id1": ["a", "b", "c", 11], "edgeType": list("xyxx"), "id2": [0, 1, 2, 13], "value": list("xxyx")}
        )
        # when
        result = utils.remove_reverse_edges(remove_set=remove, remain_set=remain)
        # then
        true_result = pandas.DataFrame(
            {"id1": ["b", "c", 11], "edgeType": list("yxx"), "id2": [1, 2, 13], "value": list("xyx")}, index=[1, 2, 3]
        )
        np.testing.assert_array_equal(true_result.values, result.values)

    def test_remove_reverse_edges_diff_indices(self):
        # given
        remove = pandas.DataFrame(
            {"id1": [0, 1, 2, 3], "edgeType": list("xxxx"), "id2": list("abcd"), "value": list("xxxx")}
        )
        remove.set_index(pandas.Index(list("asdf")), inplace=True)
        remain = pandas.DataFrame(
            {"id1": ["a", "b", "c", 11], "edgeType": list("xyxx"), "id2": [0, 1, 2, 13], "value": list("xxyx")}
        )
        remain.set_index(pandas.Index(list("wert")), inplace=True)
        # when
        result = utils.remove_reverse_edges(remove_set=remove, remain_set=remain)
        # then
        true_result = pandas.DataFrame(
            {"id1": ["b", "c", 11], "edgeType": list("yxx"), "id2": [1, 2, 13], "value": list("xyx")}, index=[1, 2, 3]
        ).set_index(pandas.Index(list("ert")))
        np.testing.assert_array_equal(true_result.values, result.values)

    def test_calc_corrupted_triples(self):
        self.fail()

    def test_get_corrupted_examples(self):
        self.fail()

    def test_group_corrupted_examples(self):
        self.fail()
