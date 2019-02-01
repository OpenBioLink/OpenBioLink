import os
from unittest import TestCase

import graph_creation.globalConstant as glob
from graph_creation.graphCreator import GraphCreator
from graph_creation.metadata_db_file import *


class TestGraphCreator(TestCase):

    def test_graph_creation(self):

        manual_db_file_metadata = []

        #EDGES --------------------------------------------------
        dbMetaEdgeBgeeDiffExpr = DbMetaEdgeBgeeDiffExpr
        dbMetaEdgeBgeeDiffExpr.OFILE_NAME = 'BGEE_overexpr.tsv'
        manual_db_file_metadata.append(dbMetaEdgeBgeeDiffExpr)

        dbMetaEdgeBgeeExpr = DbMetaEdgeBgeeExpr
        dbMetaEdgeBgeeExpr.OFILE_NAME = 'BGEE_expr_calls.tsv'
        manual_db_file_metadata.append(dbMetaEdgeBgeeExpr)

        dbMetaEdgeCdtPath = DbMetaEdgeCtdPath
        dbMetaEdgeCdtPath.OFILE_NAME = 'CDT_gene_pathway.tsv'
        manual_db_file_metadata.append(dbMetaEdgeCdtPath)

        dbMetaEdgeDisGeNet = DbMetaEdgeDisGeNet
        dbMetaEdgeDisGeNet.OFILE_NAME = 'DisGeNet_gene_disease.tsv'
        manual_db_file_metadata.append(dbMetaEdgeDisGeNet)

        dbMetaEdgeDrugCentral = DbMetaEdgeDrugCentral
        dbMetaEdgeDrugCentral.OFILE_NAME = 'drugcentral_dump.sql'
        manual_db_file_metadata.append(dbMetaEdgeDrugCentral)

        dbMetaEdgeGo = DbMetaEdgeGo
        dbMetaEdgeGo.OFILE_NAME = 'GO_annotations.gaf'
        manual_db_file_metadata.append(dbMetaEdgeGo)

        dbMetaEdgeHpoDis = DbMetaEdgeHpoDis
        dbMetaEdgeHpoDis.OFILE_NAME = 'HPO_disease_phenotype.tab'
        manual_db_file_metadata.append(dbMetaEdgeHpoDis)

        dbMetaEdgeHpoGene = DbMetaEdgeHpoGene
        dbMetaEdgeHpoGene.OFILE_NAME = 'HPO_gene_phenotype.tsv'
        manual_db_file_metadata.append(dbMetaEdgeHpoGene)

        dbMetaEdgeSiderSe = DbMetaEdgeSiderSe
        dbMetaEdgeSiderSe.OFILE_NAME = 'SIDER_se.tsv'
        manual_db_file_metadata.append(dbMetaEdgeSiderSe)

        dbMetaEdgeStitch = DbMetaEdgeStitch
        dbMetaEdgeStitch.OFILE_NAME = 'STITCH_gene_drug.tsv'
        manual_db_file_metadata.append(dbMetaEdgeStitch)

        dbMetaEdgeString = DbMetaEdgeString
        dbMetaEdgeString.OFILE_NAME = 'STRING_gene_gene.txt'
        manual_db_file_metadata.append(dbMetaEdgeString)

        dbMetaEdgeStitchAction = DbMetaEdgeStitchAction
        dbMetaEdgeStitchAction.OFILE_NAME = 'STITCH_gene_drug_actions.tsv'
        manual_db_file_metadata.append(dbMetaEdgeStitchAction)

        dbMetaEdgeStringAction = DbMetaEdgeStringAction
        dbMetaEdgeStringAction.OFILE_NAME = 'STRING_gene_gene_actions.tsv'
        manual_db_file_metadata.append(dbMetaEdgeStringAction)

        #MAPPINGS --------------------------------------------------
        dbMetaMapDisGeNet = DbMetaMapDisGeNet
        dbMetaMapDisGeNet.OFILE_NAME = 'DisGeNet_mapping_disease_umls_do.tab'
        manual_db_file_metadata.append(dbMetaMapDisGeNet)

        dbMetaMapString = DbMetaMapString
        dbMetaMapString.OFILE_NAME = 'String_mapping_gene_ncbi_string.tsv'
        manual_db_file_metadata.append(dbMetaMapString)

        dbMetaMapUnipro = DbMetaMapUniprot
        dbMetaMapUnipro.OFILE_NAME = 'Uniprot_mapping_gene.tab'
        manual_db_file_metadata.append(dbMetaMapUnipro)

        #ONTO --------------------------------------------------
        dbMetaOntoDo = DbMetaOntoDo
        dbMetaOntoDo.OFILE_NAME = 'DO_ontology.obo'
        manual_db_file_metadata.append(dbMetaOntoDo)

        dbMetaOntoGo = DbMetaOntoGo
        dbMetaOntoGo.OFILE_NAME = 'GO_ontology.obo'
        manual_db_file_metadata.append(dbMetaOntoGo)

        dbMetaOntoHpo = DbMetaOntoHpo
        dbMetaOntoHpo.OFILE_NAME = 'HPO_ontology.obo'
        manual_db_file_metadata.append(dbMetaOntoHpo)

        dbMetaOntoUberon = DbMetaOntoUberon
        dbMetaOntoUberon.OFILE_NAME = 'UBERON_ontology.obo'
        manual_db_file_metadata.append(dbMetaOntoUberon)

        test_folder = os.path.dirname(os.path.realpath(__file__))
        test_data_folder = os.path.join(test_folder, 'test_data')

        # global variables
        glob.QUALITY = None
        glob.INTERACTIVE_MODE = False
        glob.SKIP_EXISTING_FILES = False

        directed_tuple =  True, 'TR_DIR_'
        undirected_tuple =  False, 'TR_NOT_'
        cases = [directed_tuple, undirected_tuple]

        for case in cases:
            graph_is_directed, true_ref_file_prefix = case
            with self.subTest():

                glob.DIRECTED = graph_is_directed

                graph_creator = GraphCreator("test_data", manual_db_file_metadata)
                graph_creator.create_input_files()
                graph_creator.create_graph()


                true_ref_files = [f for f in os.listdir(test_data_folder) if f.startswith(true_ref_file_prefix)]# os.path.isfile(f) ]
                for ref_file_name in true_ref_files:
                    with self.subTest(ref_file_name):
                        all_lines_in_comp_file = True
                        with open(os.path.join(test_data_folder,ref_file_name)) as f:
                            ref_file = f.read()
                        with open(os.path.join(test_data_folder,ref_file_name[7:])) as f:
                            comp_file = f.read()
                        comp_dict = {}
                        j = 0
                        for row in comp_file:
                            comp_dict[j] = row
                            j += 1
                        i = 0
                        for row in ref_file:
                            if row not in comp_dict.values():
                                all_lines_in_comp_file = False
                            i += 1

                        assert (j == i)
                        assert (all_lines_in_comp_file)



