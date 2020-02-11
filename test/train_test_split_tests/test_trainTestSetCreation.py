from unittest import TestCase
import src.openbiolink.globalConfig as globalConst
from src.openbiolink.train_test_set_creation.trainTestSplitCreation import TrainTestSetCreation
import numpy as np
import pandas as pd
import random
import os


class TestTrainTestSetCreation(TestCase):

    # ------- remove_edges_with_nodes --------------------
    def test_remove_edges_with_nodes_none_removed(self):
        # given
        edges = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: ["xyz", "foo", "bar"],
                globalConst.EDGE_TYPE_COL_NAME: list("abc"),
                globalConst.NODE2_ID_COL_NAME: ["foo", "bar", "baz"],
            }
        )
        nodes = {5, 6, 7}
        # when
        result = TrainTestSetCreation.remove_edges_with_nodes(samples=edges, nodes=nodes)
        # then
        true_result = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: ["xyz", "foo", "bar"],
                globalConst.EDGE_TYPE_COL_NAME: list("abc"),
                globalConst.NODE2_ID_COL_NAME: ["foo", "bar", "baz"],
            }
        )
        np.array_equal(true_result.values, result.values)

    def test_remove_edges_with_nodes_removed_some(self):
        # given
        edges = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: ["xyz", "foo", "bar"],
                globalConst.EDGE_TYPE_COL_NAME: list("abc"),
                globalConst.NODE2_ID_COL_NAME: ["foo", "bar", "baz"],
            }
        )
        nodes = {"foo"}
        # when
        result = TrainTestSetCreation.remove_edges_with_nodes(samples=edges, nodes=nodes)
        # then
        true_result = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: ["bar"],
                globalConst.EDGE_TYPE_COL_NAME: list("c"),
                globalConst.NODE2_ID_COL_NAME: ["baz"],
            }
        )
        np.array_equal(true_result.values, result.values)

    def test_remove_edges_with_nodes_empty_node_set(self):
        # given
        edges = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: ["xyz", "foo", "bar"],
                globalConst.EDGE_TYPE_COL_NAME: list("abc"),
                globalConst.NODE2_ID_COL_NAME: ["foo", "bar", "baz"],
            }
        )
        nodes = set()
        # when
        result = TrainTestSetCreation.remove_edges_with_nodes(samples=edges, nodes=nodes)
        # then
        true_result = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: ["xyz", "foo", "bar"],
                globalConst.EDGE_TYPE_COL_NAME: list("abc"),
                globalConst.NODE2_ID_COL_NAME: ["foo", "bar", "baz"],
            }
        )
        np.array_equal(true_result.values, result.values)

    def test_remove_edges_with_nodes_remove_all(self):
        # given
        edges = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: ["xyz", "foo", "bar"],
                globalConst.EDGE_TYPE_COL_NAME: list("abc"),
                globalConst.NODE2_ID_COL_NAME: ["foo", "bar", "baz"],
            }
        )
        nodes = {"foo", "bar"}
        # when
        result = TrainTestSetCreation.remove_edges_with_nodes(samples=edges, nodes=nodes)
        # then
        true_result = pd.DataFrame(
            columns=[globalConst.NODE1_ID_COL_NAME, globalConst.EDGE_TYPE_COL_NAME, globalConst.NODE2_ID_COL_NAME]
        )
        np.array_equal(true_result.values, result.values)

    # ------- get_additional_nodes --------------------
    def test_get_additional_nodes_none(self):
        # given
        old_nodes_list = list("abc")
        new_nodes_list = list("abc")
        # when
        result = TrainTestSetCreation.get_additional_nodes(old_nodes_list=old_nodes_list, new_nodes_list=new_nodes_list)
        # then
        true_result = set()
        self.assertEqual(true_result, result)

    def test_get_additional_nodes_empty_new(self):
        # given
        old_nodes_list = list("abc")
        new_nodes_list = []
        # when
        result = TrainTestSetCreation.get_additional_nodes(old_nodes_list=old_nodes_list, new_nodes_list=new_nodes_list)
        # then
        true_result = set()
        self.assertEqual(true_result, result)

    def test_get_additional_nodes_empty_old(self):
        # given
        old_nodes_list = []
        new_nodes_list = list("abc")
        # when
        result = TrainTestSetCreation.get_additional_nodes(old_nodes_list=old_nodes_list, new_nodes_list=new_nodes_list)
        # then
        true_result = {"a", "b", "c"}
        self.assertEqual(true_result, result)

    def test_get_additional_nodes_some(self):
        # given
        old_nodes_list = list("ac")
        new_nodes_list = list("abcd")
        # when
        result = TrainTestSetCreation.get_additional_nodes(old_nodes_list=old_nodes_list, new_nodes_list=new_nodes_list)
        # then
        true_result = {"b", "d"}
        self.assertEqual(true_result, result)

    # ------- create_cross_val --------------------
    def test_create_cross_val_folds(self):
        random.seed(globalConst.RANDOM_STATE)

        # given
        edges = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: list("abc"),
                globalConst.EDGE_TYPE_COL_NAME: list("opq"),
                globalConst.NODE2_ID_COL_NAME: list("xyz"),
            }
        )
        n = 3
        # when
        result = TrainTestSetCreation.create_cross_val(df=edges, n_folds=n)
        # then
        first = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: list("a"),
                globalConst.EDGE_TYPE_COL_NAME: list("o"),
                globalConst.NODE2_ID_COL_NAME: list("x"),
            }
        )
        second = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: list("b"),
                globalConst.EDGE_TYPE_COL_NAME: list("p"),
                globalConst.NODE2_ID_COL_NAME: list("y"),
            }
        )
        third = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: list("c"),
                globalConst.EDGE_TYPE_COL_NAME: list("q"),
                globalConst.NODE2_ID_COL_NAME: list("z"),
            }
        )
        true_result = [(first.append(third), second), (second.append(third), first), (first.append(second), third)]
        for i in range(len(true_result)):
            np.array_equal(true_result[i], result[i])

    def test_create_cross_val_frac(self):
        random.seed(globalConst.RANDOM_STATE)

        # given
        edges = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: list("abc"),
                globalConst.EDGE_TYPE_COL_NAME: list("opq"),
                globalConst.NODE2_ID_COL_NAME: list("xyz"),
            }
        )
        n = 1 / 3
        # when
        result = TrainTestSetCreation.create_cross_val(df=edges, n_folds=n)
        # then
        first = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: list("a"),
                globalConst.EDGE_TYPE_COL_NAME: list("o"),
                globalConst.NODE2_ID_COL_NAME: list("x"),
            }
        )
        second = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: list("b"),
                globalConst.EDGE_TYPE_COL_NAME: list("p"),
                globalConst.NODE2_ID_COL_NAME: list("y"),
            }
        )
        third = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: list("c"),
                globalConst.EDGE_TYPE_COL_NAME: list("q"),
                globalConst.NODE2_ID_COL_NAME: list("z"),
            }
        )
        true_result = [(first.append(third), second), (second.append(third), first), (first.append(second), third)]
        for i in range(len(true_result)):
            np.array_equal(true_result[i], result[i])

    def test_create_cross_val_1_fold(self):
        random.seed(globalConst.RANDOM_STATE)

        # given
        edges = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: list("abc"),
                globalConst.EDGE_TYPE_COL_NAME: list("opq"),
                globalConst.NODE2_ID_COL_NAME: list("xyz"),
            }
        )
        n = 1

        # expect when
        self.assertRaises(Exception, lambda: TrainTestSetCreation.create_cross_val(df=edges, n_folds=n))

    def test_create_cross_val_0_fold(self):
        random.seed(globalConst.RANDOM_STATE)

        # given
        edges = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: list("abc"),
                globalConst.EDGE_TYPE_COL_NAME: list("opq"),
                globalConst.NODE2_ID_COL_NAME: list("xyz"),
            }
        )
        n = 0

        # expect when
        self.assertRaises(Exception, lambda: TrainTestSetCreation.create_cross_val(df=edges, n_folds=n))

    def test_create_cross_val_float_greater_1(self):
        random.seed(globalConst.RANDOM_STATE)

        # given
        edges = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: list("abc"),
                globalConst.EDGE_TYPE_COL_NAME: list("opq"),
                globalConst.NODE2_ID_COL_NAME: list("xyz"),
            }
        )
        n = 1.5

        # expect when
        self.assertRaises(Exception, lambda: TrainTestSetCreation.create_cross_val(df=edges, n_folds=n))

    # ------- time_slice_split --------------------
    def test_time_slice_split_additional_nodes(self):
        # tests:
        # *) removal of edges containing PATHWAY_KEGG:hsa04000 in test_set
        # given
        path = os.path.dirname(os.path.abspath(__file__))
        edges_path = os.path.join(path, "tmo_t_data/edges.csv")
        tn_edges_path = os.path.join(path, "tmo_t_data/TN_edges.csv")
        nodes_path = os.path.join(path, "tmo_t_data/nodes.csv")
        tmo_edges_path = os.path.join(path, "tmo_t_data/tmo_edges.csv")
        tmo_tn_edges_path = os.path.join(path, "tmo_t_data/tmo_TN_edges.csv")
        tmo_nodes_path = os.path.join(path, "tmo_t_data/tmo_nodes.csv")
        ttsc = TrainTestSetCreation(
            graph_path=edges_path,
            tn_graph_path=tn_edges_path,
            all_nodes_path=nodes_path,
            t_minus_one_graph_path=tmo_edges_path,
            t_minus_one_tn_graph_path=tmo_tn_edges_path,
            t_minus_one_nodes_path=tmo_nodes_path,
        )
        # when
        result_train_val_list, result_test = ttsc.time_slice_split()
        result_train, _ = result_train_val_list[0]
        # then
        true_result_test = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: [
                    "DRUG_55",
                    "DRUG_85",
                    "GENE_10",
                    "GENE_1",
                    "GENE_2",
                    "GENE_2",
                    "GENE_2",
                    "GENE_2",
                    "GO_GO:0000001",
                    "GO_GO:0000001",
                    "GO_GO:0000003",
                    "PHENOTYPE_HP:0000002",
                ],
                globalConst.EDGE_TYPE_COL_NAME: [
                    "DRUG_BINDING_GENE",
                    "DRUG_PHENOTYPE",
                    "GENE_BINDACT_GENE",
                    "GENE_DIS",
                    "GENE_EXPRESSED_ANATOMY",
                    "GENE_OVEREXPRESSED_ANATOMY",
                    "GENE_PATHWAY",
                    "GENE_PATHWAY",
                    "IS_A",
                    "IS_A",
                    "PART_OF",
                    "IS_A",
                ],
                globalConst.NODE2_ID_COL_NAME: [
                    "GENE_1",
                    "PHENOTYPE_HP:0000005",
                    "GENE_1",
                    "DIS_DOID:0000002",
                    "ANATOMY_UBERON:0000001",
                    "ANATOMY_UBERON:0000001",
                    "PATHWAY_KEGG:hsa04000",
                    "PATHWAY_REACT:R-HSA-1000008",
                    "GO_GO:0000002",
                    "GO_GO:0000003",
                    "GO_GO:0000006",
                    "PHENOTYPE_HP:0000005",
                ],
                globalConst.QSCORE_COL_NAME: [
                    "191",
                    "",
                    "309",
                    "0.24587142988000799",
                    "gold quality",
                    "high quality",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                ],
            }
        )
        with open(tmo_edges_path) as file:
            true_result_training = pd.read_csv(file, names=globalConst.COL_NAMES_EDGES)
        np.array_equal(true_result_test, result_test)
        np.array_equal(true_result_training, result_train)

    def test_time_slice_split_vanishing(self):
        # tests:
        # *) vanished edge: GENE_10	GENE_OVEREXPRESSED_ANATOMY	ANATOMY_UBERON:0000001	high quality	1
        # given
        path = os.path.dirname(os.path.abspath(__file__))
        edges_path = os.path.join(path, "tmo_t_data/vanishing_edges.csv")
        tn_edges_path = os.path.join(path, "tmo_t_data/TN_edges.csv")
        nodes_path = os.path.join(path, "tmo_t_data/nodes.csv")
        tmo_edges_path = os.path.join(path, "tmo_t_data/tmo_edges.csv")
        tmo_tn_edges_path = os.path.join(path, "tmo_t_data/tmo_TN_edges.csv")
        tmo_nodes_path = os.path.join(path, "tmo_t_data/tmo_nodes.csv")
        ttsc = TrainTestSetCreation(
            graph_path=edges_path,
            tn_graph_path=tn_edges_path,
            all_nodes_path=nodes_path,
            t_minus_one_graph_path=tmo_edges_path,
            t_minus_one_tn_graph_path=tmo_tn_edges_path,
            t_minus_one_nodes_path=tmo_nodes_path,
        )
        # when
        result_train_val_list, result_test = ttsc.time_slice_split()
        result_train, _ = result_train_val_list[0]
        # then
        true_result_test = pd.DataFrame(
            {
                globalConst.NODE1_ID_COL_NAME: [
                    "DRUG_55",
                    "DRUG_85",
                    "GENE_10",
                    "GENE_1",
                    "GENE_2",
                    "GENE_2",
                    "GENE_2",
                    "GENE_2",
                    "GO_GO:0000001",
                    "GO_GO:0000001",
                    "GO_GO:0000003",
                    "PHENOTYPE_HP:0000002",
                ],
                globalConst.EDGE_TYPE_COL_NAME: [
                    "DRUG_BINDING_GENE",
                    "DRUG_PHENOTYPE",
                    "GENE_BINDACT_GENE",
                    "GENE_DIS",
                    "GENE_EXPRESSED_ANATOMY",
                    "GENE_OVEREXPRESSED_ANATOMY",
                    "GENE_PATHWAY",
                    "GENE_PATHWAY",
                    "IS_A",
                    "IS_A",
                    "PART_OF",
                    "IS_A",
                ],
                globalConst.NODE2_ID_COL_NAME: [
                    "GENE_1",
                    "PHENOTYPE_HP:0000005",
                    "GENE_1",
                    "DIS_DOID:0000002",
                    "ANATOMY_UBERON:0000001",
                    "ANATOMY_UBERON:0000001",
                    "PATHWAY_KEGG:hsa04000",
                    "PATHWAY_REACT:R-HSA-1000008",
                    "GO_GO:0000002",
                    "GO_GO:0000003",
                    "GO_GO:0000006",
                    "PHENOTYPE_HP:0000005",
                ],
                globalConst.QSCORE_COL_NAME: [
                    "191",
                    "",
                    "309",
                    "0.24587142988000799",
                    "gold quality",
                    "high quality",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                ],
            }
        )
        with open(tmo_edges_path) as file:
            true_result_training = pd.read_csv(file, names=globalConst.COL_NAMES_EDGES)
        np.array_equal(true_result_test, result_test)
        np.array_equal(true_result_training, result_train)
