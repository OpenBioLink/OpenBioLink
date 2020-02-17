import os
import unittest

import openbiolink.graphProperties as graphProp
from openbiolink import globalConfig
from openbiolink.graph_creation.graphCreation import Graph_Creation
from openbiolink.graph_creation.metadata_db_file import *


class TestGraphCreation(unittest.TestCase):
    def test_graph_creation(self):
        # creates test graph from test o_files and compares against true reference test graph
        # tests directed and undirected version of graph (and TN-graph)
        # well as the output into a single as well as in separate files
        # globalConfig = __import__('../../src/openbiolink/graphCreation.py')
        # graphProp = __import__('../../src/openbiolink/globalConfig.py')
        # graphProp = __import__('../../src/graph_creation/graphCreation.py')
        # graphProp = __import__('../../src/openbiolink/graphCreation.py')
        manual_db_file_metadata = []

        # EDGES --------------------------------------------------
        dbMetaEdgeBgeeDiffExpr = DbMetaEdgeBgeeDiffExpr
        dbMetaEdgeBgeeDiffExpr.OFILE_NAME = "BGEE_overexpr.tsv"
        manual_db_file_metadata.append(dbMetaEdgeBgeeDiffExpr)

        dbMetaEdgeBgeeExpr = DbMetaEdgeBgeeExpr
        dbMetaEdgeBgeeExpr.OFILE_NAME = "BGEE_expr_calls.tsv"
        manual_db_file_metadata.append(dbMetaEdgeBgeeExpr)

        dbMetaEdgeCdtPath = DbMetaEdgeCtdPath
        dbMetaEdgeCdtPath.OFILE_NAME = "CDT_gene_pathway.tsv"
        manual_db_file_metadata.append(dbMetaEdgeCdtPath)

        dbMetaEdgeDisGeNet = DbMetaEdgeDisGeNet
        dbMetaEdgeDisGeNet.OFILE_NAME = "DisGeNet_gene_disease.tsv"
        manual_db_file_metadata.append(dbMetaEdgeDisGeNet)

        dbMetaEdgeDrugCentral = DbMetaEdgeDrugCentral
        dbMetaEdgeDrugCentral.OFILE_NAME = "drugcentral_dump.sql"
        manual_db_file_metadata.append(dbMetaEdgeDrugCentral)

        dbMetaEdgeGo = DbMetaEdgeGo
        dbMetaEdgeGo.OFILE_NAME = "GO_annotations.gaf"
        manual_db_file_metadata.append(dbMetaEdgeGo)

        dbMetaEdgeHpoDis = DbMetaEdgeHpoDis
        dbMetaEdgeHpoDis.OFILE_NAME = "HPO_disease_phenotype.tab"
        manual_db_file_metadata.append(dbMetaEdgeHpoDis)

        dbMetaEdgeTnHpoDis = DbMetaEdgeTnHpoDis
        dbMetaEdgeTnHpoDis.OFILE_NAME = "HPO_TN_disease_phenotype.tab"
        manual_db_file_metadata.append(dbMetaEdgeTnHpoDis)

        dbMetaEdgeHpoGene = DbMetaEdgeHpoGene
        dbMetaEdgeHpoGene.OFILE_NAME = "HPO_gene_phenotype.tsv"
        manual_db_file_metadata.append(dbMetaEdgeHpoGene)

        dbMetaEdgeSiderSe = DbMetaEdgeSiderSe
        dbMetaEdgeSiderSe.OFILE_NAME = "SIDER_se.tsv"
        manual_db_file_metadata.append(dbMetaEdgeSiderSe)

        dbMetaEdgeStitch = DbMetaEdgeStitch
        dbMetaEdgeStitch.OFILE_NAME = "STITCH_gene_drug.tsv"
        manual_db_file_metadata.append(dbMetaEdgeStitch)

        dbMetaEdgeString = DbMetaEdgeString
        dbMetaEdgeString.OFILE_NAME = "STRING_gene_gene.txt"
        manual_db_file_metadata.append(dbMetaEdgeString)

        dbMetaEdgeStitchAction = DbMetaEdgeStitchAction
        dbMetaEdgeStitchAction.OFILE_NAME = "STITCH_gene_drug_actions.tsv"
        manual_db_file_metadata.append(dbMetaEdgeStitchAction)

        dbMetaEdgeStringAction = DbMetaEdgeStringAction
        dbMetaEdgeStringAction.OFILE_NAME = "STRING_gene_gene_actions.tsv"
        manual_db_file_metadata.append(dbMetaEdgeStringAction)

        # MAPPINGS --------------------------------------------------
        dbMetaMapDisGeNet = DbMetaMapDisGeNet
        dbMetaMapDisGeNet.OFILE_NAME = "DisGeNet_mapping_disease_umls_do.tab"
        manual_db_file_metadata.append(dbMetaMapDisGeNet)

        dbMetaMapString = DbMetaMapString
        dbMetaMapString.OFILE_NAME = "String_mapping_gene_ncbi_string.tsv"
        manual_db_file_metadata.append(dbMetaMapString)

        dbMetaMapUnipro = DbMetaMapUniprot
        dbMetaMapUnipro.OFILE_NAME = "Uniprot_mapping_gene.tab"
        manual_db_file_metadata.append(dbMetaMapUnipro)

        # ONTO --------------------------------------------------
        dbMetaOntoDo = DbMetaOntoDo
        dbMetaOntoDo.OFILE_NAME = "DO_ontology.obo"
        manual_db_file_metadata.append(dbMetaOntoDo)

        dbMetaOntoGo = DbMetaOntoGo
        dbMetaOntoGo.OFILE_NAME = "GO_ontology.obo"
        manual_db_file_metadata.append(dbMetaOntoGo)

        dbMetaOntoHpo = DbMetaOntoHpo
        dbMetaOntoHpo.OFILE_NAME = "HPO_ontology.obo"
        manual_db_file_metadata.append(dbMetaOntoHpo)

        dbMetaOntoUberon = DbMetaOntoUberon
        dbMetaOntoUberon.OFILE_NAME = "UBERON_ontology.obo"
        manual_db_file_metadata.append(dbMetaOntoUberon)

        current_folder = os.path.dirname(os.path.realpath(__file__))
        test_folder = os.path.abspath(os.path.join(current_folder, os.pardir))
        test_data_folder = os.path.join(test_folder, "test_data")
        output_data_folder = os.path.join(test_data_folder, "graph_files")
        true_ref_folder = os.path.join(test_data_folder, "TR_files")

        # global variables
        graphProp.QUALITY = None
        globalConfig.INTERACTIVE_MODE = False
        globalConfig.SKIP_EXISTING_FILES = False

        directed_tuple = True, "TR_DIR_"
        undirected_tuple = False, "TR_NOT_"
        cases = [directed_tuple, undirected_tuple]

        for case in cases:
            graph_is_directed, true_ref_file_prefix = case
            print("\n##########################################")
            print("GRAPH IS DIRECTED: " + str(graph_is_directed) + "\n")
            with self.subTest(graph_is_directed=graph_is_directed):
                graphProp.DIRECTED = graph_is_directed

                graph_creator = Graph_Creation(test_data_folder, manual_db_file_metadata)
                graph_creator.create_input_files()
                graph_creator.create_graph(one_file_sep="\t", multi_file_sep="\t")

                true_ref_files = [
                    f for f in os.listdir(true_ref_folder) if f.startswith(true_ref_file_prefix)
                ]  # os.path.isfile(f) ]
                missing_elements = []
                for ref_file_name in true_ref_files:
                    with self.subTest(ref_file_name=ref_file_name):
                        all_lines_in_comp_file = True
                        with open(os.path.join(true_ref_folder, ref_file_name)) as f:
                            ref_file = f.readlines()
                        with open(os.path.join(output_data_folder, ref_file_name[7:])) as f:
                            comp_file = f.readlines()
                        comp_dict = {}
                        j = 0
                        for row in comp_file:
                            comp_dict[j] = row
                            j += 1
                        i = 0
                        for row in ref_file:
                            if row not in comp_dict.values():
                                all_lines_in_comp_file = False
                                missing_elements.append(row)
                            i += 1

                        if not all_lines_in_comp_file:
                            print(ref_file_name)
                            print("missing elements:", missing_elements)

                        assert j == i
                        assert all_lines_in_comp_file
