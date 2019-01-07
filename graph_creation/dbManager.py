import csv
import gzip
import os
import sys
import urllib.request
import zipfile

import pandas
from graph_creation.metadata_db_file.edge.dbMetadataEdge import DbMetadataEdge
from graph_creation.metadata_db_file.mapping.dbMetadataMapping import DbMetadataMapping
from graph_creation.metadata_db_file.onto.dbMetadataOnto import DbMetadataOnto

from graph_creation.metadata_edge.edgeMetadata import EdgeMetadata
from graph_creation.file_reader.parser.oboParser import OboParser
from graph_creation.file_reader.parser.postgresDumpParser import PostgresDumpParser as dcp
from edge import Edge
from edgeType import EdgeType
from node import Node
from nodeType import NodeType


class DbManager(object):
    """This class is responsible for downloading original (source) database files,
    converting them into 'uniform' csv files (only containing relevant columns),
     and converting those csv files into a graph and nodes file"""

    # ----- user input --------
    # which metadata_db_file they like to include
    dbList = []

    def __init__(self, folder_path):
        """Folder path (working dircetory) as well as all files needed shall be defined here. If new files are added,
        additional changes might be necessary in download -,  parser -  etc methods"""

        self.folder_path = folder_path
        self.oFiles_path = os.path.join(self.folder_path, 'oFiles')
        self.dbFiles_path = os.path.join(self.folder_path, 'dbFiles')
        if not os.path.exists(self.oFiles_path):
            os.makedirs(self.oFiles_path)
        if not os.path.exists(self.dbFiles_path):
            os.makedirs(self.dbFiles_path)

        self.edges_file_prefix = "edges"
        self.nodes_file_prefix = "nodes"


        # _________________________________________________________________________
        # |
        # |                         SOURCE FILES
        # |_________________________________________________________________________

        # ---- Nodes ----
        #TODO

        # ---- Ontologies and onto mappings----
        # each quadruple consists of (1) beginning of the line, (2) split character,(3) index of split element being the id, (4) the name of dict entry (must be same as in use_fields)
        self.source_onto_go = DbMetadataOnto(url="http://purl.obolibrary.org/obo/go/go-basic.obo",
                                             ofile_name="GO_ontology.obo",
                                             csv_name="DB_ONTO_GO_ontology.csv",
                                             use_fields=['ID', 'IS_A'],
                                             quadruple_list=[('id', ' ', 1, 'ID'),
                                      ('alt_id', ' ', 1, 'ID'),
                                      ('is_a', ' ', 1, 'IS_A')])
        self.source_onto_do = DbMetadataOnto(url="https://raw.githubusercontent.com/DiseaseOntology/HumanDiseaseOntology/master/src/ontology/doid.obo",
                                             ofile_name="DO_ontology.obo",
                                             csv_name="DB_ONTO_DO_ontology.csv",
                                             use_fields=['ID', 'IS_A'],
                                             quadruple_list=[('id', ' ', 1, 'ID'),
                                       ('alt_id', ' ', 1, 'ID'),
                                       ('is_a', ' ', 1, 'IS_A')])
        self.source_onto_hpo = DbMetadataOnto(url="https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo",
                                              ofile_name="HPO_ontology.obo",
                                              csv_name="DB_ONTO_HPO_ontology.csv",
                                              use_fields=['ID', 'IS_A'],
                                              quadruple_list=[('id', ' ', 1, 'ID'),
                                       ('alt_id', ' ', 1, 'ID'),
                                       ('is_a', ' ', 1, 'IS_A')])

        # ---- Onto Mappings ----
        # id quadruples should be defined at ontology section

        self.source_onto_mapping_hpo_umls = DbMetadataOntoMapping(url=None,       #todo self??
                                                                ofile_name="HPO_ontology.obo",
                                                                csv_name="DB_ONTO_mapping_HPO_UMLS.csv",
                                                                use_fields=['ID', 'UMLS'])

        self.source_onto_hpo.onto_mapping.append(self.source_onto_mapping_hpo_umls)
        self.source_onto_hpo.quadruple_list.append(('xref: UMLS:', ':', 2, 'UMLS'))

        self.source_onto_mapping_do_umls = DbMetadataOntoMapping(url=None,
                                                               ofile_name="DO_ontology.obo",
                                                               csv_name="DB_ONTO_mapping_DO_UMLS.csv",
                                                               use_fields=['ID', 'UMLS'])
        self.source_onto_do.onto_mapping.append(self.source_onto_mapping_do_umls)
        self.source_onto_do.quadruple_list.append(('xref: UMLS_CUI:', ':', 2, 'UMLS'))

        self.source_onto_mapping_do_omim = DbMetadataOntoMapping(url=None,
                                                               ofile_name="DO_ontology.obo",
                                                               csv_name="DB_ONTO_mapping_DO_OMIM.csv",
                                                               use_fields=['ID', 'OMIM'])
        self.source_onto_do.onto_mapping.append(self.source_onto_mapping_do_omim)
        self.source_onto_do.quadruple_list.append(('xref: OMIM:', ' ', 1, 'OMIM'))


        self.source_onto_list = [self.source_onto_go,
                                 self.source_onto_do,
                                 self.source_onto_hpo
                                ]

        # ---- Edges ----

        self.source_edge_gene_gene = DbMetadataEdge( url="https://stringdb-static.org/download/protein.links.v10.5/9606.protein.links.v10.5.txt.gz",
                                     ofile_name="STRING_gene_gene.txt.gz",
                                     csv_name= "DB_STRING_gene_gene.csv",
                                     cols=['string1', 'string2', 'qscore'],
                                     use_cols = ['string1', 'string2', 'qscore'],
                                     nr_lines_header=1)
        self.source_edge_gene_go = DbMetadataEdge(url="http://geneontology.org/gene-associations/goa_human.gaf.gz",
                                     ofile_name="GO_annotations.gaf.gz",
                                     csv_name="DB_GO_annotations.csv",
                                     cols=['DB', 'DOI', 'qulifier', 'none13', 'GO_ID', 'DB_ref', 'evidence_code',
                                           'with_from', 'taxon', 'date','assigned_by', 'ann_ext', 'ann_prop',
                                           'none14', 'none15', 'none16', 'none17'],
                                     use_cols = ['DOI', 'GO_ID', 'evidence_code'],
                                     nr_lines_header=30)
        self.source_edge_gene_dis = DbMetadataEdge(url="http://www.disgenet.org/ds/DisGeNET/results/curated_gene_disease_associations.tsv.gz",
                                     ofile_name="DisGeNet_gene_disease.tsv.gz",
                                     csv_name="DB_DisGeNet_gene_disease.csv",
                                     cols=['geneID', 'geneSym', 'umlsID', 'disName', 'score', 'NofPmids',
                                           'NofSnps', 'source'],
                                     use_cols=['geneID', 'umlsID', 'score'],
                                     nr_lines_header=1)
        self.source_edge_gene_drug = DbMetadataEdge( url="http://stitch.embl.de/download/protein_chemical.links.v5.0/9606.protein_chemical.links.v5.0.tsv.gz",
                                     ofile_name= "STITCH_gene_drug.tsv.gz",
                                     csv_name="DB_STITCH_gene_drug.csv",
                                     cols=['chemID', 'stringID', 'qscore'],
                                     use_cols = ['stringID', 'chemID', 'qscore'],
                                     nr_lines_header=1)
        #self.source_edge_gene_drug_action = DbMetadataEdge(
        #    url="http://stitch.embl.de/download/protein_chemical.links.v5.0/9606.protein_chemical.links.v5.0.tsv.gz",
        #    ofile_name="STITCH_gene_drug_actions.tsv.gz",
        #    csv_name="DB_STITCH_gene_drug_actions.csv",
        #    cols=['item_a', 'item_b', 'mode', 'action','a_is_acting', 'score'], #TODO ms action?
        #    use_cols=['item_a', 'item_b', 'mode','a_is_acting', 'score'],
        #    nr_lines_header=1)
        self.source_edge_gene_pheno = DbMetadataEdge( url="http://compbio.charite.de/jenkins/job/hpo.annotations.monthly/lastSuccessfulBuild/artifact/annotation/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt",
                                     ofile_name="HPO_gene_phenotype.tsv",
                                     csv_name="DB_HPO_gene_phenotype.csv",
                                     cols=['geneID', 'geneSymb', 'hpoName', 'hpoID'],
                                     use_cols = ['geneID', 'hpoID'],
                                     nr_lines_header=1)
        self.source_edge_gene_path = DbMetadataEdge ( url="http://ctdbase.org/reports/CTD_genes_pathways.tsv.gz",
                                     ofile_name="CDT_gene_pathway.tsv.gz",
                                     csv_name="DB_CDT_gene_pathway.csv",
                                     cols=['geneSymb', 'geneID', 'pathName', 'pathID'],
                                     use_cols = ['geneID', 'pathID'],
                                     nr_lines_header=29)
        self.source_edge_gene_anatomy = DbMetadataEdge ( url="https://www.proteinatlas.org/download/rna_tissue.tsv.zip",  #TODO GTEx
                                     ofile_name="HPA_gene_anatomy.tsv.zip",
                                     csv_name="DB_HPA_gene_anatomy.csv",
                                     cols=['geneID', 'geneName', 'anatomy', 'expressionValue', 'Unit'],
                                     use_cols=['geneID', 'anatomy', 'expressionValue'],
                                     nr_lines_header=1)
        self.source_edge_dis_drug = DbMetadataEdge(url="http://unmtid-shinyapps.net/download/drugcentral.dump.08262018.sql.gz",
                                                   ofile_name="sql_dump.sql.gz",
                                                   csv_name="DB_DrugCentral_dis_drug.csv",cols=[],use_cols=[],nr_lines_header=None)
        # FIXME continue here!!!

        self.source_edge_dis_drug = DbMetadataEdge(url="http://sideeffects.embl.de/media/download/meddra_all_indications.tsv.gz",
                                     ofile_name="SIDER_dis_drug.tsv.gz",
                                     csv_name="DB_SIDER_dis_drug.csv",
                                     cols=['stichID', 'umlsID', 'method', 'umlsName', 'medDRAumlsType',
                                           'medDRAumlsID', 'medDRAumlsName'],
                                     use_cols=['umlsID', 'stichID', 'method'],
                                     nr_lines_header=0)
        self.source_edge_dis_pheno = DbMetadataEdge(url="http://compbio.charite.de/jenkins/job/hpo.annotations/lastStableBuild/" \
                                          "artifact/misc/phenotype_annotation_hpoteam.tab",
                                      ofile_name="HPO_disease_phenotype.tab",
                                      csv_name="DB_HPO_disease_phenotype.csv",
                                      cols=['DB', 'DOI', 'DBname', 'qulifier', 'HPO_ID', 'DB_ref',
                                            'evidence_code', 'onsetMod', 'freq', 'sex',
                                            'mod', 'aspect', 'date', 'assigned_by'],
                                      use_cols = ['DB_ref', 'HPO_ID', 'evidence_code'],
                                      nr_lines_header=0)
        self.source_edge_drug_pheno = DbMetadataEdge(url="http://sideeffects.embl.de/media/download/meddra_all_se.tsv.gz",
                                      ofile_name="SIDER_se.tsv.gz",
                                      csv_name="DB_SIDER_se.csv",
                                      cols=['stitchID_flat', 'stitchID_stereo', 'umlsID', 'medDRAumlsType', 'medDRAumlsID', 'SEname'],
                                      use_cols=['stitchID_flat', 'umlsID'],
                                      nr_lines_header=0)

        self.source_edge_list = [self.source_edge_gene_gene,
                                 self.source_edge_gene_go,
                                 self.source_edge_gene_dis,
                                 self.source_edge_gene_drug,
                                 self.source_edge_gene_path,
                                 self.source_edge_gene_pheno,
                                 self.source_edge_gene_anatomy,
                                 self.source_edge_dis_drug,
                                 self.source_edge_dis_pheno,
                                 self.source_edge_drug_pheno
                                 ]

        # ---- Mappings ----

        self.source_mapping_string_ncbi_string =    DbMetadataMapping(url= "https://string-metadata_db_file.org/mapping_files/entrez_mappings/entrez_gene_id.vs.string.v10.28042015.tsv" ,
                                                                    ofile_name="String_mapping_gene_ncbi_string.tsv",
                                                                    csv_name="DB_String_mapping_gene_ncbi_string.csv",
                                                                    cols=['ncbiID', 'stringID'],
                                                                    use_cols=['ncbiID', 'stringID'],
                                                                    nr_lines_header=1)
        self.source_mapping_uniprot_uniprot_ncbi =  DbMetadataMapping(url= "ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/by_organism/HUMAN_9606_idmapping_selected.tab.gz",
                                                                    ofile_name="Uniprot_mapping_gene.tab.gz",
                                                                    csv_name="DB_Uniprot_mapping_gene_uniprot_ncbi.csv",
                                                                    cols=['UniProtKB-AC', 'UniProtKB-ID', 'GeneID', 'RefSeq', 'GI', 'PDB', 'GO', 'UniRef100', 'UniRef90','UniRef50', 'UniParc', 'PIR', 'NCBI-taxon', 'MIM', 'UniGene', 'PubMed', 'EMBL', 'EMBL-CDS', 'Ensembl','Ensembl_TRS', 'Ensembl_PRO', 'Additional PubMed'],
                                                                    use_cols=['UniProtKB-AC', 'GeneID'],
                                                                    nr_lines_header=0,
                                                                    dtypes={'UniProtKB-AC': str, 'GeneID': str},
                                                                    mapping_sep=';')
        self.source_mapping_uniprot_ensembl_ncbi =  DbMetadataMapping(url= None,
                                                                    ofile_name="Uniprot_mapping_gene.tab.gz",
                                                                    csv_name="DB_Uniprot_mapping_gene_ensembl_ncbi.csv",
                                                                    cols=['UniProtKB-AC', 'UniProtKB-ID', 'GeneID',
                                                                          'RefSeq', 'GI', 'PDB', 'GO', 'UniRef100',
                                                                          'UniRef90', 'UniRef50', 'UniParc', 'PIR',
                                                                          'NCBI-taxon', 'MIM', 'UniGene', 'PubMed',
                                                                          'EMBL', 'EMBL-CDS', 'Ensembl', 'Ensembl_TRS',
                                                                          'Ensembl_PRO', 'Additional PubMed'],
                                                                    use_cols=['Ensembl', 'GeneID'],
                                                                    nr_lines_header=0,
                                                                    dtypes={'Ensembl': str, 'GeneID': str},
                                                                    mapping_sep=';')
        self.source_mapping_disgenet_umls_do =      DbMetadataMapping(url= "http://www.disgenet.org/ds/DisGeNET/results/disease_mappings.tsv.gz",
                                                                    ofile_name="DisGeNet_mapping_disease_umls_do.tab.gz",
                                                                    csv_name="DB_DisGeNet_mapping_disease_umls_do.csv",
                                                                    cols=['umlsID', 'name', 'voc', 'code', 'vocName'],
                                                                    use_cols=['umlsID', 'voc', 'code'],
                                                                    nr_lines_header=1)

        self.source_mapping_list = [self.source_mapping_string_ncbi_string,
                                    self.source_mapping_uniprot_uniprot_ncbi,
                                    self.source_mapping_uniprot_ensembl_ncbi,
                                    self.source_mapping_disgenet_umls_do
                                    ]



        # _________________________________________________________________________
        # |
        # |                         DB FILES
        # |________________________________________________________________________

        # ---- Ontologies ----
        self.dbFile_go = EdgeMetadata(edges_file_path=os.path.join (self.dbFiles_path, self.source_onto_go.csv_name),
                                      colindex1=0, colindex2=1, edgeType=EdgeType.IS_A,
                                      node1_type=NodeType.GO, node2_type=NodeType.GO)
        self.dbFile_do = EdgeMetadata(edges_file_path=os.path.join(self.dbFiles_path, self.source_onto_do.csv_name),
                                      colindex1=0, colindex2=1, edgeType=EdgeType.IS_A,
                                      node1_type=NodeType.DIS, node2_type=NodeType.DIS)
        self.dbFile_hpo = EdgeMetadata(edges_file_path= os.path.join(self.dbFiles_path, self.source_onto_hpo.csv_name),
                                       colindex1=0, colindex2=1, edgeType=EdgeType.IS_A,
                                       node1_type=NodeType.PHENOTYPE, node2_type=NodeType.PHENOTYPE)

        # --- Edges ---
        # --- gene - gene ---
        edges_file_path = os.path.join(self.dbFiles_path, self.source_edge_gene_gene.csv_name)
        mapping_file1 = os.path.join(self.dbFiles_path, self.source_mapping_string_ncbi_string.csv_name)
        self.dbFile_gene_gene = EdgeMetadata(edges_file_path=edges_file_path,
                                             colindex1=0, colindex2=1, edgeType=EdgeType.GENE_GENE,
                                             node1_type=NodeType.GENE, node2_type=NodeType.GENE,
                                             colindex_qscore=2, cutoff_num=700,
                                             mapping1_file=mapping_file1, map1_sourceindex=1, map1_targetindex=0,
                                             mapping2_file=mapping_file1, map2_sourceindex=1, map2_targetindex=0)
        # --- gene - go ---
        edges_file_path = os.path.join(self.dbFiles_path, self.source_edge_gene_go.csv_name)
        mapping_file1 = os.path.join(self.dbFiles_path, self.source_mapping_uniprot_uniprot_ncbi.csv_name)
        self.dbFile_gene_go = EdgeMetadata(edges_file_path=edges_file_path,
                                           colindex1=0, colindex2=1, edgeType=EdgeType.GENE_GO,
                                           node1_type=NodeType.GENE, node2_type=NodeType.GO,
                                           colindex_qscore=2, cutoff_txt=['IEA'],
                                           mapping1_file=mapping_file1, map1_sourceindex=0, map1_targetindex=1)
        #  --- gene - dis ---
        edges_file_path = os.path.join(self.dbFiles_path, self.source_edge_gene_dis.csv_name)
        mapping_file2 = os.path.join(self.dbFiles_path, self.source_mapping_disgenet_umls_do.csv_name)
        self.dbFile_gene_dis = EdgeMetadata(edges_file_path=edges_file_path, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_DIS,
                                            node1_type=NodeType.GENE, node2_type=NodeType.DIS, colindex_qscore=2, cutoff_num=0.7,  # from 0 to 1
                                            mapping2_file=mapping_file2, map2_sourceindex=0, map2_targetindex=2,
                                            db2_index=1, db2_name='DO') #fixme create unique mapping file

        #  --- gene - drug ---
        edges_file_path = os.path.join(self.dbFiles_path, self.source_edge_gene_drug.csv_name)
        mapping_file1 = os.path.join(self.dbFiles_path, self.source_mapping_string_ncbi_string.csv_name)
        self.dbFile_gene_drug = EdgeMetadata(edges_file_path=edges_file_path, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_DRUG,
                                             node1_type=NodeType.GENE, node2_type=NodeType.DRUG,
                                             colindex_qscore=2, cutoff_num=700,
                                             mapping1_file=mapping_file1, map1_sourceindex=1, map1_targetindex=0)

        # --- gene - phenotype ---
        edges_file_path = os.path.join(self.dbFiles_path, self.source_edge_gene_pheno.csv_name)
        self.dbFile_gene_pheno = EdgeMetadata(edges_file_path=edges_file_path, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_PHENOTYPE,
                                              node1_type=NodeType.GENE, node2_type=NodeType.PHENOTYPE)

        # --- gene - pathway ---
        edges_file_path = os.path.join(self.dbFiles_path, self.source_edge_gene_path.csv_name)
        self.dbFile_gene_pathway = EdgeMetadata(edges_file_path=edges_file_path, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_PATHWAY,
                                                node1_type=NodeType.GENE, node2_type=NodeType.PATHWAY)
        # --- gene - anatomy ---
        edges_file_path = os.path.join(self.dbFiles_path, self.source_edge_gene_anatomy.csv_name)
        mapping_file1 = os.path.join(self.dbFiles_path, self.source_mapping_uniprot_ensembl_ncbi.csv_name)
        self.dbFile_gene_anatomy = EdgeMetadata(edges_file_path=edges_file_path, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_EXPRESSED_ANATOMY,
                                                node1_type=NodeType.GENE, node2_type=NodeType.ANATOMY,
                                                colindex_qscore=2,  # todo ms expression score
                                                mapping1_file=mapping_file1, map1_sourceindex=0, map1_targetindex=1)
        # --- dis - phenotype ---
        edges_file_path = os.path.join(self.dbFiles_path, self.source_edge_dis_pheno.csv_name)
        mapping_file1 = os.path.join(self.dbFiles_path, self.source_onto_mapping_do_omim.csv_name)
        self.dbFile_dis_pheno = EdgeMetadata(edges_file_path=edges_file_path, colindex1=0, colindex2=1, edgeType=EdgeType.DIS_PHENOTYPE,
                                             node1_type=NodeType.DIS, node2_type=NodeType.PHENOTYPE,
                                             colindex_qscore=2,  # todo check licenses / if IEA ok
                                             mapping1_file=mapping_file1, map1_sourceindex=1, map1_targetindex=0)
        # --- dis - drug ---
        edges_file_path = os.path.join(self.dbFiles_path, self.source_edge_dis_drug.csv_name)
        mapping_file1 = os.path.join(self.dbFiles_path, self.source_onto_mapping_do_umls.csv_name)
        self.dbFile_dis_drug = EdgeMetadata(edges_file_path=edges_file_path, colindex1=0, colindex2=1, edgeType=EdgeType.DIS_DRUG,
                                            node1_type=NodeType.DIS, node2_type=NodeType.DRUG,
                                            colindex_qscore=2,  # todo read sider paper
                                            mapping1_file=mapping_file1, map1_sourceindex=1, map1_targetindex=0)


        # --- drug - phenotype ---
        edges_file_path = os.path.join(self.dbFiles_path, self.source_edge_drug_pheno.csv_name)
        mapping_file2 = os.path.join(self.dbFiles_path, self.source_onto_mapping_hpo_umls.csv_name)
        self.dbFile_drug_pheno = EdgeMetadata(edges_file_path=edges_file_path,
                                              colindex1=0, colindex2=1, edgeType=EdgeType.DRUG_PHENOTYPE,
                                              node1_type=NodeType.DRUG, node2_type=NodeType.PHENOTYPE,
                                              mapping2_file=mapping_file2, map2_sourceindex=1, map2_targetindex=0)

        self.dbFile_list = [self.dbFile_go,
                            self.dbFile_do,
                            self.dbFile_hpo,
                            self.dbFile_gene_gene,
                            self.dbFile_gene_go,
                            self.dbFile_gene_dis,
                            self.dbFile_gene_drug,
                            self.dbFile_gene_pheno,
                            self.dbFile_gene_pathway,
                            self.dbFile_gene_anatomy,
                            self.dbFile_dis_pheno,
                            self.dbFile_dis_drug,
                            self.dbFile_drug_pheno
                            ]

    # ##################################################################################################################################################

    # ----- DOWNLOAD RECOURCES --------
    def download_resources(self):
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        ignore_existing_files = False

        for onto in self.source_onto_list:
            if onto.url is not None:
                file_path = os.path.join(self.oFiles_path, onto.ofile_name)
                if not ignore_existing_files:
                    ignore_existing_files = self.check_if_file_exisits(file_path)
                urllib.request.urlretrieve(onto.url, file_path )

        for edge in self.source_edge_list:
            if edge.url is not None:
                file_path = os.path.join(self.oFiles_path, edge.ofile_name)
                if not ignore_existing_files:
                    ignore_existing_files = self.check_if_file_exisits(file_path)
                urllib.request.urlretrieve(edge.url, file_path )

        for mapping in self.source_mapping_list:
            if mapping.url is not None:
                file_path = os.path.join(self.oFiles_path, mapping.ofile_name)
                if not ignore_existing_files:
                    ignore_existing_files = self.check_if_file_exisits(file_path)
                urllib.request.urlretrieve(mapping.url, file_path)


    def check_if_file_exisits(self, file_path):
        if os.path.isfile(file_path):
            user_input = input(
                'The file ' + file_path + ' already exists. Do you want to continue [y], cancel [n] or continue for all files [a]?')
            if user_input == 'n':
                sys.exit()
            elif user_input == 'a':
                return True
        return False


    # ----- CREATE DB FILES --------
    def create_db_files(self):
        # ontologies and onto mappings
        oboParser = OboParser()
        for o in self.source_onto_list:
            in_path = os.path.join(self.oFiles_path, o.ofile_name)
            df = oboParser.obo_to_df(in_path, o.quadruple_list)
            self.create_db_file_from_df(os.path.join(self.dbFiles_path,o.csv_name), o.use_cols, df, ';')    # ';' sep is created while parsing
            if o.onto_mapping:
                for m in o.onto_mapping:
                    self.create_db_file_from_df(os.path.join(self.dbFiles_path,m.csv_name), m.use_cols, df, ';')

        # edges
        for e in self.source_edge_list:
            self.create_db_file(os.path.join(self.oFiles_path,e.ofile_name),
                                os.path.join(self.dbFiles_path,e.csv_name), e.cols, e.use_cols, e.nr_lines_header)

        # mapping
        for m in self.source_mapping_list:
            self.create_db_file(os.path.join(self.oFiles_path,m.ofile_name),
                                os.path.join(self.dbFiles_path,m.csv_name), m.cols, m.use_cols, m.nr_lines_header, m.mapping_sep, m.dtypes)

        self.individual_preprocessing_for_db_files()


    def create_db_file(self, in_path, out_path, col_names, use_cols, skiprows, mapping_sep=None, dtype=None):
        data = self.read_in_file_as_df(in_path, col_names, use_cols, skiprows, dtype)
        self.create_db_file_from_df(out_path, use_cols, data, mapping_sep)


    def read_in_file_as_df(self, in_path, col_names, use_cols, skiprows, dtype=None):
        """txt files must be whitespace separated; tsv, tab and gaf files must be tab separated;
        all other files must me comma separated; can decode gz and zip compression; in zip files, only the first
        file is taken into account"""

        path_parts = in_path.split('.')
        if (path_parts[-1] == "gz"):
            in_file = gzip.open(in_path, "rt", encoding="utf8")
        elif (path_parts[-1] == "zip"):
            zf = zipfile.ZipFile(in_path)
            in_file = zf.open(zf.namelist()[0])
        else:
            in_file = open(in_path)

        if (path_parts[1] == "txt"):
            sep = " "
        elif (path_parts[1] == "tsv" or path_parts[1] == "gaf" or path_parts[1] == "tab"):
            sep = "\t"
        elif (path_parts[1] == "sql"):
            data = dcp.table_to_df(in_file, "omop_relationship")
            in_file.close()
            return data
        else:
            sep = ","

        data = pandas.read_csv(in_file, sep=sep, names=col_names, usecols=use_cols, skiprows=skiprows, dtype=dtype)
        in_file.close()
        return data


    def create_db_file_from_df(self, out_path, use_cols, data, mapping_sep= None):
        if mapping_sep is not None:
            data = self.flat_df(data, use_cols, mapping_sep)
        #data = data[data[data.columns[1]] != ''] #todo good?
        data[use_cols].to_csv(out_path, sep=';', index=False,header=False)


    def flat_df(self, data, use_cols, mapping_sep =None):
        """creates a 'flat' df, i.e. no NAN columns and one relationship per row (a -> b,c) becomes (a -> b ; a -> c)"""
        drop_list = sorted(set(list(data))-set(use_cols))
        data = data.drop(drop_list, axis=1)
        data = data.dropna()
        if mapping_sep is not None:
            #todo performance
            temp = data[data[use_cols[0]].str.contains(mapping_sep)]
            for index, line in temp.iterrows():
                for alt in line[0].split(mapping_sep):
                    data = data.append(pandas.DataFrame([[alt.lstrip(), line[1]]], columns=use_cols))
            data = data[~data[use_cols[0]].str.contains(mapping_sep)]
            temp = data[data[use_cols[1]].str.contains(mapping_sep)]
            for index, line in temp.iterrows():
                for alt in line[1].split(mapping_sep):
                    data = data.append(pandas.DataFrame([[line[0], alt.lstrip()]], columns=use_cols))
            data = data[~data[use_cols[1]].str.contains(mapping_sep)]
        return data


    def individual_preprocessing_for_db_files(self):
        """individual further preprocessing steps should be handled here only"""

        # making ids unique in DisGeNet mapping file for DO and OMIM (metadata_db_file:id)
        if self.source_mapping_disgenet_umls_do in self.source_mapping_list:
            in_file = open(os.path.join(self.dbFiles_path, self.source_mapping_disgenet_umls_do.csv_name))
            cols = self.source_mapping_disgenet_umls_do.use_cols
            data = pandas.read_csv(in_file, sep=';', names=cols, dtype={cols[1]: str, cols[2]: str})
            in_file.close()
            data.loc[data[cols[1]] == 'OMIM', cols[2]] = 'OMIM:' + data[data[cols[1]] == 'OMIM'][cols[2]]
            data.loc[data[cols[1]] == 'DO', cols[2]] = 'DO:' + data[data[cols[1]] == 'DO'][cols[2]]
            out_file = open(os.path.join(self.dbFiles_path, self.source_mapping_disgenet_umls_do.csv_name), 'w')
            data[self.source_mapping_disgenet_umls_do.use_cols].to_csv(out_file, sep=';', index=False, header=False)
            out_file.close()

        # converting stitch id to pubchem
        if self.source_edge_gene_drug in self.source_edge_list:
            self.stitch_to_pubchem_id(self.source_edge_gene_drug, 1)  # todo performance
        #if self.source_edge_dis_drug in self.source_edge_list:         #todo check
        #    self.stitch_to_pubchem_id(self.source_edge_dis_drug, 1)
        if self.source_edge_drug_pheno in self.source_edge_list:
            self.stitch_to_pubchem_id(self.source_edge_drug_pheno, 0)


    def stitch_to_pubchem_id(self, source_obj, id_col):
        """converts stitch id to pubchem id (removing the first 4 characters, i.e. CID1, CID0, CISm or CIDs;
        then remove leading zeros"""
        in_file = open(os.path.join(self.dbFiles_path, source_obj.csv_name))
        cols = source_obj.use_cols
        data = pandas.read_csv(in_file, sep=';', names=cols, dtype={cols[id_col]: str})
        in_file.close()
        data[cols[id_col]] = data[cols[id_col]].str[4:].str.lstrip("0")
        out_file = open(os.path.join(self.dbFiles_path, source_obj.csv_name), 'w')
        data.to_csv(out_file, sep=';', index=False, header=False)
        out_file.close()


    # ----- CREATE GRAPH --------
    def create_graph(self):
        open(os.path.join(self.folder_path, 'ids_no_mapping.tsv'), 'w').close()
        open(os.path.join(self.folder_path, 'stats.txt'), 'w').close()

        edges_dic = {}
        nodes_dic = {}
        for d in self.dbFile_list:
            nodes1, nodes2, edges = self.create_nodes_and_edges(d)
            edges_dic[str(d.edgeType)] = edges
            if str(d.node1_type) in nodes_dic :
                nodes_dic[str(d.node1_type)].update(nodes1)
            else:
                nodes_dic[str(d.node1_type)] = nodes1
            if str(d.node2_type) in nodes_dic :
                nodes_dic[str(d.node2_type)].update(nodes2)
            else:
                nodes_dic[str(d.node2_type)] = nodes2
        self.output_graph(nodes_dic, edges_dic, '\t')
        return


    def output_graph(self, nodes_dic: dict, edges_dic : dict, one_file_sep = ';', multi_file_sep = None):
        # one file
        if one_file_sep is not None:
            with open(os.path.join(self.folder_path, self.nodes_file_prefix + '.csv'), 'w') as out_file:
                writer = csv.writer(out_file, delimiter=one_file_sep, lineterminator='\n')
                for key, value in nodes_dic.items():
                    for node in value:
                        writer.writerow(list(node))
                out_file.close()
            with open(os.path.join(self.folder_path, self.edges_file_prefix + '.csv'), 'w') as out_file:
                writer = csv.writer(out_file, delimiter=one_file_sep, lineterminator='\n')
                for key, value in edges_dic.items():
                    for edge in value:
                        writer.writerow(list(edge))
                out_file.close()
        # separate files
        if multi_file_sep is not None:
            for key, value in nodes_dic.items():
                with open(os.path.join(self.folder_path, self.nodes_file_prefix + '_' + key +  '.csv'), 'w') as out_file:
                    writer = csv.writer(out_file, delimiter=multi_file_sep, lineterminator='\n')
                    for node in value:
                        writer.writerow(list(node))
                out_file.close()
            for key, value in edges_dic.items():
                with open(os.path.join(self.folder_path, self.edges_file_prefix + '_' + key + '.csv'), 'w') as out_file:
                    writer = csv.writer(out_file, delimiter=multi_file_sep, lineterminator='\n')
                    for edge in value:
                        writer.writerow(list(edge))
                out_file.close()
        #adjacency matrix
        key, value = nodes_dic
        d = {x: i for i, x in enumerate(value)} #fixme continue here


    def create_nodes_and_edges (self, dbFile):
        # --- mapping ---
        mapping1 = self.db_mapping_file_to_dic(dbFile.mapping1_file, dbFile.map1_sourceindex, dbFile.map1_targetindex, dbFile.db1_index, dbFile.db1_name)
        mapping2 = self.db_mapping_file_to_dic(dbFile.mapping2_file, dbFile.map2_sourceindex, dbFile.map2_targetindex, dbFile.db2_index, dbFile.db2_name)

        # --- edges ---
        with open(dbFile.edges_file_path, "r", encoding="utf8") as edge_content:
            nodes1 = set()
            nodes2 = set()
            edges = set()
            ids1_no_mapping = set()
            ids2_no_mapping = set()
            ids1 = set()
            ids2 = set()
            nr_edges=0
            nr_edges_after_mapping = 0
            nr_edges_with_dup = 0
            nr_edges_below_cutoff = 0
            nr_edges_no_mapping = 0

            reader = csv.reader(edge_content, delimiter = ";")

            for row in reader:
                raw_id1 = row[dbFile.colindex1]
                raw_id2 = row[dbFile.colindex2]
                if dbFile.colindex_qscore is not None:
                    qscore = row[dbFile.colindex_qscore]
                else:
                    qscore = None
                edge_id1 = None
                edge_id2 = None
                ids1.add(raw_id1)
                ids2.add(raw_id2)

                if (dbFile.mapping1_file is not None and raw_id1 in mapping1):
                    edge_id1 = mapping1.get(raw_id1)
                if (dbFile.mapping2_file is not None and raw_id2 in mapping2):
                    edge_id2 = mapping2.get(raw_id2)

                if ((edge_id1 is not None and edge_id2 is not None) or
                    (edge_id1 is not None and dbFile.mapping2_file is None) or
                    (edge_id2 is not None and dbFile.mapping1_file is None) or
                    (dbFile.mapping1_file is None and dbFile.mapping2_file is None)):
                    if (edge_id1 is None):
                        edge_id1 = [raw_id1]
                    if (edge_id2 is None):
                        edge_id2 = [raw_id2]
                    for id1 in edge_id1:
                        for id2 in edge_id2:
                            if (dbFile.cutoff_num is None and dbFile.cutoff_txt is None) or \
                                     (dbFile.cutoff_num is not None and float(qscore) > dbFile.cutoff_num) or \
                                     (dbFile.cutoff_txt is not None and qscore not in dbFile.cutoff_txt):
                                edges.add(Edge(id1, dbFile.edgeType, id2, None, qscore))
                                nodes1.add(Node(id1, dbFile.node1_type))
                                nodes2.add(Node(id2, dbFile.node2_type))
                                nr_edges_with_dup +=1
                            else:
                                nr_edges_below_cutoff+=1
                else:
                    nr_edges_no_mapping += 1
                    if (edge_id1 is None and dbFile.mapping1_file is not None):
                        ids1_no_mapping.add(raw_id1 )
                    if (edge_id2 is None and dbFile.mapping2_file is not None):
                        ids2_no_mapping.add(raw_id2)
                nr_edges += 1

        nr_edges_after_mapping =len(edges)
        edge_content.close()

        # print statistics
        edgeType = dbFile.edgeType
        with open(os.path.join(self.folder_path, 'ids_no_mapping.tsv'), 'a') as out_file:
            for id in ids1_no_mapping:
                out_file.write('%s\t%s\n' %(id, edgeType))
            for id in ids2_no_mapping:
                out_file.write('%s\t%s\n' % (id, edgeType))
            out_file.close()

        out_string = 'Edge Type: ' + str(edgeType) + '\n' + \
                     'Nr edges: ' + str(nr_edges) + '\n' + \
                     'Nr edges no mapping: ' + str(nr_edges_no_mapping) + '\n' + \
                     'Nr edges below cutoff: ' + str(nr_edges_below_cutoff) + '\n' + \
                     'Edges coverage: ' + str(1-(nr_edges_no_mapping/ nr_edges)) + '\n' + \
                     'Duplicated edges: ' + str(nr_edges_with_dup-nr_edges_after_mapping) + '\n' + \
                     'Nr edges after mapping (final nr): ' + str(nr_edges_after_mapping) + '\n' + \
                     'Nr nodes1 no mapping: ' + str(len(ids1_no_mapping)) + '\n' + \
                     'Nr nodes2 no mapping: ' + str(len(ids2_no_mapping)) + '\n' + \
                     'Nr nodes1: ' + str(len(ids1)) + '\n' + \
                     'Nr nodes2: ' + str(len(ids2)) + '\n' + \
                     'nodes1 coverage: ' + str(1-(len(ids1_no_mapping)/ len(ids1))) + '\n' + \
                     'nodes2 coverage: ' + str(1-(len(ids2_no_mapping)/ len(ids2))) + '\n' + \
                     '######################################################################################'
        print(out_string)
        with open(os.path.join(self.folder_path, 'stats.txt'), 'a') as out_file:
            out_file.write(out_string)

        return nodes1, nodes2, edges


    def db_mapping_file_to_dic(self, mapping_file, map_sourceindex, map_targetindex, db_index, db_name):
        """creates a dic out of a metadata_db_file mapping file (source_id to list of target_ids)"""
        if (mapping_file is not None):
            mapping = {}
            with open(mapping_file, mode="r") as mapping_content1:
                reader = csv.reader(mapping_content1, delimiter=";")

                for row in reader:
                    if (db_index is None or row[db_index]==db_name):
                        if row[map_sourceindex] in mapping:
                            mapping[row[map_sourceindex]].append(row[map_targetindex])
                        else:
                            mapping[row[map_sourceindex]] = [row[map_targetindex]]
                mapping_content1.close()
            return mapping
