import unittest
import utils
import pandas


class TestUtils(unittest.TestCase):

    # ----- get_leaf_subclasses -------
    def test_get_leaf_subclasses_no_subclasses(self):
        # given
        class A:
            pass
        # when
        leaf_classes = utils.get_leaf_subclasses(A)
        # then
        self.assertEqual(set(leaf_classes), {A})

    def test_get_leaf_subclasses_one_lvl(self):
        # given
        class A:
            pass
        class B (A):
            pass
        # when
        leaf_classes = utils.get_leaf_subclasses(A)
        # then
        self.assertEqual(set(leaf_classes), {B})

    def test_get_leaf_subclasses_two_lvl(self):
        # given
        class A:
            pass
        class B (A):
            pass
        class C (B):
            pass
        # when
        leaf_classes = utils.get_leaf_subclasses(A)
        # then
        self.assertEqual(set(leaf_classes), {C})

    def test_get_leaf_subclasses_diff_lvls(self):
        # given
        class A:
            pass
        class B (A):
            pass
        class C (B):
            pass
        class D (A):
            pass
        # when
        leaf_classes = utils.get_leaf_subclasses(A)
        # then
        self.assertEqual(set(leaf_classes), {C,D})

    def test_get_leaf_subclasses_None(self):
        # given
        # when
        leaf_classes = utils.get_leaf_subclasses(None)
        # then
        self.assertEqual(None, None)


    # ----- make_undir -------
    def test_make_undir_all_undir(self):
        # given
        df = pandas.DataFrame({'id1': list('abc'), 'id2': list('xyz')})
        # then
        self.assertTrue(df.equals(utils.make_undir(df)))

    def test_make_undir_all_dir(self):
        # given
        df = pandas.DataFrame({'id1': list('abcd'), 'id2': list('badc')})
        undir = pandas.DataFrame({'id1': list('ac'), 'id2': list('bd')})
        # then
        self.assertTrue(undir.equals(utils.make_undir(df)))

    def test_make_undir_mixed(self):
        # given
        df = pandas.DataFrame({'id1': list('abc'), 'id2': list('cxa')})
        undir = pandas.DataFrame({'id1': list('ab'), 'id2': list('cx')})
        # then
        self.assertTrue(undir.equals(utils.make_undir(df)))


    def test_db_mapping_file_to_dic(self):
        #given
            #file with content
            # x	foo	a
            # y	bar	a; b
            # z	baz
            # q		c
        file_path = 'test_mapping_file.tsv'
        dic =  {'x': ['a'], 'y': ['a; b'], 'q': ['c']}
        #then
        self.assertEqual(utils.db_mapping_file_to_dic(file_path, 0, 2, '\t'),dic )



    def test_cls_list_to_dic(self):
        self.fail()


    def test_file_exists(self):
        self.fail()


    def test_get_diff(self):
        self.fail()


    def test_remove_reverse_edges(self):
        #given
        remove = pandas.DataFrame({'id1':[0,1,2,3], 'edgeType': list('xxxx'), 'id2' : list('abcd'),  'value': list('xxxx')})
        remain = pandas.DataFrame({'id1':['a','b','c',11], 'edgeType': list('xyxx'), 'id2' : [0, 1,2,13],  'value': list('xxyx')})
        result = pandas.DataFrame({'id1':['b','c',11], 'edgeType': list('yxx'), 'id2' : [ 1,2,13],  'value': list('xyx')}, index=[1,2,3])
        #then
        self.assertTrue(result.equals(utils.remove_reverse_edges(remove_set=remove, remain_set=remain)))



    def test_calc_corrupted_triples(self):
        self.fail()


    def test_get_corrupted_examples(self):
        self.fail()


    def test_group_corrupted_examples(self):
        self.fail()