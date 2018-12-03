import urllib.request
import os
import csv
import gzip
import zipfile
import json
import pandas
from edge import Edge
from edgeTypes import EdgeType
from db.oboParser import OboParser
from db.sourceOntoDB import SourceOntoDB
from db.sourceEdgeDB import SourceEdgeDB
from db.sourceMappingDB import SourceMappingDB

class DbManager(object):
    # ----- user input --------
    # which db they like to include
    dbList = []

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.oFiles_path = os.path.join(self.folder_path, 'oFiles')
        if not os.path.exists(self.oFiles_path):
            os.makedirs(self.oFiles_path)

        # ---- Nodes ----
        # self.node_ncbi_url = "ftp://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz"
        # self.node_go_url = "http://snapshot.geneontology.org/ontology/go-basic.obo" # TODO DOPPELT!
        # self.node_do_url = "https://raw.githubusercontent.com/DiseaseOntology/HumanDiseaseOntology/master/src/ontology/HumanDO.obo"
        # # node_pubchem_url TODO
        # self.node_hpo_url = "https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo" # TODO DOPPELT!
        # # node_keeg_url TODO
        # # node_reactome_url TODO
        # # node_uberon_url TODO
        # # -- file names --
        # self.node_ncbi_path = "ncbi_nodes.gz"
        # self.node_go_path = "GO_nodes.obo"
        # self.node_do_path = "DO_nodes.obo"
        # self.node_hpo_path = "HPO_nodes.obo"

        # ---- Ontologies ----

        self.source_onto_go = SourceOntoDB( url="http://purl.obolibrary.org/obo/go/go-basic.obo",
                                    ofile_name="GO_ontology.obo",
                                    csv_name="DB_ONTO_GO_ontology.csv",
                                    use_cols=['ID', 'IS_A'])
        self.source_onto_do = SourceOntoDB(url="https://raw.githubusercontent.com/DiseaseOntology/HumanDiseaseOntology/master/src/ontology/doid.obo",
                                    ofile_name="DO_ontology.obo",
                                    csv_name="DB_ONTO_DO_ontology.csv",
                                    use_cols=['ID', 'IS_A'])
        self.source_onto_hpo = SourceOntoDB(url="https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo",
                                    ofile_name="HPO_ontology.obo",
                                    csv_name="DB_ONTO_HPO_ontology.csv",
                                    use_cols=['ID', 'IS_A'])

        self.source_onto_list = [self.source_onto_go, self.source_onto_do, self.source_onto_hpo]

        self.url_onto_go = "http://purl.obolibrary.org/obo/go/go-basic.obo"
        self.url_onto_do = "https://raw.githubusercontent.com/DiseaseOntology/HumanDiseaseOntology/master/src/ontology/doid.obo"
        self.url_onto_hpo = "https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo"
        # onto_uberon_url
        # -- file names --
        self.path_onto_go = "GO_ontology.obo"
        self.path_onto_do = "DO_ontology.obo"
        self.path_onto_hpo = "HPO_ontology.obo"

        # ---- Edges ----

        self.source_edge_gene_gene = SourceEdgeDB( url="https://stringdb-static.org/download/protein.links.v10.5/9606.protein.links.v10.5.txt.gz",
                                     ofile_name="STRING_gene_gene.txt.gz",
                                     csv_name= "DB_STRING_gene_gene.csv",
                                     cols=['string1', 'string2', 'qscore'],
                                     use_cols = ['string1', 'string2', 'qscore'],
                                     nr_lines_header=1 )
        self.source_edge_gene_go = SourceEdgeDB(url="http://geneontology.org/gene-associations/goa_human.gaf.gz",
                                     ofile_name="GO_annotations.gaf.gz",
                                     csv_name="DB_GO_annotations.csv",
                                     cols=['DB', 'DOI', 'qulifier', 'none13', 'GO_ID', 'DB_ref', 'evidence_code',
                                           'with_from', 'taxon', 'date','assigned_by', 'ann_ext', 'ann_prop',
                                           'none14', 'none15', 'none16', 'none17'],
                                     use_cols = ['DOI', 'GO_ID', 'evidence_code'],
                                     nr_lines_header=30)
        self.source_edge_gene_dis = SourceEdgeDB(url="http://www.disgenet.org/ds/DisGeNET/results/curated_gene_disease_associations.tsv.gz",
                                     ofile_name="DisGeNet_gene_disease.tsv.gz",
                                     csv_name="DB_DisGeNet_gene_disease.csv",
                                     cols=['geneID', 'geneSym', 'umlsID', 'disName', 'score', 'NofPmids',
                                           'NofSnps', 'source'],
                                     use_cols=['geneID', 'umlsID', 'score'],
                                     nr_lines_header=1)
        self.source_edge_gene_drug = SourceEdgeDB( url="http://stitch.embl.de/download/protein_chemical.links.v5.0/9606.protein_chemical.links.v5.0.tsv.gz",
                                     ofile_name= "STITCH_gene_drug.tsv.gz",
                                     csv_name="DB_STITCH_gene_drug.csv",
                                     cols=['chemID', 'stringID', 'qscore'],
                                     use_cols = ['stringID', 'chemID', 'qscore'],
                                     nr_lines_header=1)
        self.source_edge_gene_pheno = SourceEdgeDB( url="http://compbio.charite.de/jenkins/job/hpo.annotations.monthly/lastSuccessfulBuild/artifact/annotation/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt",
                                     ofile_name="HPO_gene_phenotype.tsv",
                                     csv_name="DB_HPO_gene_phenotype.csv",
                                     cols=['geneID', 'geneSymb', 'hpoName', 'hpoID'],
                                     use_cols = ['geneID', 'hpoID'],
                                     nr_lines_header=1)
        self.source_edge_gene_path = SourceEdgeDB ( url="http://ctdbase.org/reports/CTD_genes_pathways.tsv.gz",
                                     ofile_name="CDT_gene_pathway.tsv.gz",
                                     csv_name="DB_CDT_gene_pathway.csv",
                                     cols=['geneID', 'geneSymb', 'hpoName', 'hpoID'],
                                     use_cols = ['geneID', 'hpoID'],
                                     nr_lines_header=29)
        self.source_edge_gene_anatomy = SourceEdgeDB ( url="https://www.proteinatlas.org/download/rna_tissue.tsv.zip",  #TODO GTEx
                                     ofile_name="HPA_gene_anatomy.tsv.zip",
                                     csv_name="DB_HPA_gene_anatomy.csv",
                                     cols=['geneID', 'geneName', 'anatomy', 'expressionValue', 'Unit'],
                                     use_cols=['geneID', 'anatomy', 'expressionValue'],
                                     nr_lines_header=1)
        self.source_edge_dis_drug = SourceEdgeDB(url="http://sideeffects.embl.de/media/download/meddra_all_indications.tsv.gz",
                                     ofile_name="SIDER_dis_drug.tsv.gz",
                                     csv_name="DB_SIDER_dis_drug.csv",
                                     cols=['stichID', 'umlsID', 'method', 'umlsName', 'medDRAumlsType',
                                           'medDRAumlsID', 'medDRAumlsName'],
                                     use_cols=['umlsID', 'stichID', 'method'],
                                     nr_lines_header=0)
        self.source_edge_dis_pheno = SourceEdgeDB(url="http://compbio.charite.de/jenkins/job/hpo.annotations/lastStableBuild/" \
                                      "artifact/misc/phenotype_annotation_hpoteam.tab",
                                      ofile_name="HPO_disease_phenotype.tab",
                                      csv_name="DB_HPO_disease_phenotype.csv",
                                      cols=['DB', 'DOI', 'DBname', 'qulifier', 'HPO_ID', 'DB_ref',
                                            'evidence_code', 'onsetMod', 'freq', 'sex',
                                            'mod', 'aspect', 'date', 'assigned_by'],
                                      use_cols = ['DOI', 'HPO_ID', 'evidence_code', 'DB'],
                                      nr_lines_header=0)
        self.source_edge_drug_pheno = SourceEdgeDB(url="http://sideeffects.embl.de/media/download/meddra_all_se.tsv.gz",
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
                                 self.source_edge_drug_pheno]

        # ---- Mappings ----

        self.source_mapping_string_ncbi_string =    SourceMappingDB(url= "https://string-db.org/mapping_files/entrez_mappings/entrez_gene_id.vs.string.v10.28042015.tsv" ,
                                                                    ofile_name="String_mapping_gene_ncbi_string.tsv",
                                                                    csv_name="DB_String_mapping_gene_ncbi_string.csv",
                                                                    cols=['ncbiID', 'stringID'],
                                                                    use_cols=['ncbiID', 'stringID'],
                                                                    nr_lines_header=1)
        self.source_mapping_uniprot_uniprot_ncbi =  SourceMappingDB(url= "ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/by_organism/HUMAN_9606_idmapping_selected.tab.gz",
                                                                    ofile_name="Uniprot_mapping_gene.tab.gz",
                                                                    csv_name="DB_Uniprot_mapping_gene_uniprot_ncbi.csv",
                                                                    cols=['UniProtKB-AC', 'UniProtKB-ID', 'GeneID', 'RefSeq', 'GI', 'PDB', 'GO', 'UniRef100', 'UniRef90','UniRef50', 'UniParc', 'PIR', 'NCBI-taxon', 'MIM', 'UniGene', 'PubMed', 'EMBL', 'EMBL-CDS', 'Ensembl','Ensembl_TRS', 'Ensembl_PRO', 'Additional PubMed'],
                                                                    use_cols=['UniProtKB-AC', 'GeneID'],  # todo AC or ID for uniprot,
                                                                    nr_lines_header=0,
                                                                    dtypes={'UniProtKB-AC': str, 'GeneID': str},
                                                                    mapping_sep=';')
        self.source_mapping_uniprot_ensembl_ncbi =  SourceMappingDB(url= None,
                                                                    ofile_name="Uniprot_mapping_gene.tab.gz",
                                                                    csv_name="DB_Uniprot_mapping_gene_ensembl_ncbi.csv",
                                                                    cols=['UniProtKB-AC', 'UniProtKB-ID', 'GeneID',
                                                                          'RefSeq', 'GI', 'PDB', 'GO', 'UniRef100',
                                                                          'UniRef90', 'UniRef50', 'UniParc', 'PIR',
                                                                          'NCBI-taxon', 'MIM', 'UniGene', 'PubMed',
                                                                          'EMBL', 'EMBL-CDS', 'Ensembl', 'Ensembl_TRS',
                                                                          'Ensembl_PRO', 'Additional PubMed'],
                                                                    use_cols=['Ensembl', 'GeneID'],  # todo AC or ID for uniprot,
                                                                    nr_lines_header=0,
                                                                    dtypes={'Ensembl': str, 'GeneID': str},
                                                                    mapping_sep=';')
        self.source_mapping_disgenet_umls_do =      SourceMappingDB(url= "http://www.disgenet.org/ds/DisGeNET/results/disease_mappings.tsv.gz",
                                                                    ofile_name="DisGeNet_mapping_disease_umls_do.tab.gz",
                                                                    csv_name="DB_DisGeNet_mapping_disease_umls_do.csv",
                                                                    cols=['umlsID', 'name', 'voc', 'code', 'vocName'],
                                                                    use_cols=['umlsID', 'voc', 'code'],
                                                                    nr_lines_header=1)
        self.source_mapping_hoehndorf_omim_do =     SourceMappingDB(url= "https://raw.githubusercontent.com/bio-ontology-research-group/multi-drug-embedding/master/data/omim2doid.dict" ,
                                                                    ofile_name="Hoehndorf_mapping_omim_do.txt",
                                                                    csv_name="DB_Hoehndorf_mapping_omim_do.csv",
                                                                    cols=None,
                                                                    use_cols=None,
                                                                    nr_lines_header=None)
        self.source_mapping_hoehndorf_umls_do =     SourceMappingDB(url= "https://raw.githubusercontent.com/bio-ontology-research-group/multi-drug-embedding/master/data/umls2doid.txt",
                                                                    ofile_name="Hoehndorf_mapping_umls_do.tsv",
                                                                    csv_name="DB_Hoehndorf_mapping_umls_do.csv",
                                                                    cols=['doID', 'umlsID', 'umlsName'],
                                                                    use_cols=['umlsID', 'doID'],
                                                                    nr_lines_header=0)
        self.source_mapping_hoehndorf_umls_hpo =    SourceMappingDB(url= "https://raw.githubusercontent.com/bio-ontology-research-group/multi-drug-embedding/master/data/umls2hpo.txt" ,
                                                                    ofile_name="Hoehndorf_mapping_umls_hpo.tsv",
                                                                    csv_name="DB_Hoehndorf_mapping_umls_hpo.csv",
                                                                    cols=['hpoID', 'umlsID', 'umlsName'],
                                                                    use_cols=['umlsID', 'hpoID'],
                                                                    nr_lines_header=0)

        self.source_mapping_list = [self.source_mapping_string_ncbi_string,
                                    self.source_mapping_uniprot_uniprot_ncbi,
                                    self.source_mapping_uniprot_ensembl_ncbi,
                                    self.source_mapping_disgenet_umls_do,       #TODO w/o omim
                                    self.source_mapping_hoehndorf_umls_do,
                                    self.source_mapping_hoehndorf_umls_hpo]


        # TODO mapping stitch to pubchem



    # ##################################################################################################################################################

    def download_resources(self):
        # TODO check if files already present
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)

        for onto in self.source_onto_list:
            if onto.url is not None:
                urllib.request.urlretrieve(onto.url, os.path.join(self.oFiles_path, onto.ofile_name))

        for edge in self.source_edge_list:
            if edge.url is not None:
                urllib.request.urlretrieve(edge.url, os.path.join(self.oFiles_path, edge.ofile_name))

        for mapping in self.source_mapping_list:
            if mapping.url is not None:
                urllib.request.urlretrieve(mapping.url, os.path.join(self.oFiles_path, mapping.ofile_name))

        urllib.request.urlretrieve(self.source_mapping_hoehndorf_omim_do.url,  os.path.join(self.oFiles_path, self.source_mapping_hoehndorf_omim_do.ofile_name ))


    def create_db_files(self):
        # ###### ontologies ####### #todo edges
#        # --GO --
#        in_path = os.path.join(self.oFiles_path, self.source_onto_go.ofile_name)
#        do_list = OboParser.parse_go_obo_from_file(in_path)
#        df = pandas.DataFrame.from_records([s.to_dict() for s in do_list])
#        # onto edges
#        self.create_db_file_from_onto(self.source_onto_go.csv_name, self.source_onto_go.use_cols, df)
#
#        # -- HPO --
#        in_path = os.path.join(self.oFiles_path, self.source_onto_hpo.ofile_name)
#        hpo_list = OboParser.parse_hpo_obo_from_file(in_path)
#        df = pandas.DataFrame.from_records([s.to_dict() for s in hpo_list])
#        # onto edges
#        self.create_db_file_from_onto(self.source_onto_hpo.csv_name, self.source_onto_hpo.use_cols, df)
#        # mapping edges
#        self.create_db_file_from_onto('DB_ONTO_mapping_HPO_UMLS.csv', ['ID', 'UMLS'],df)
#
#        # -- DO --
#        in_path = os.path.join(self.oFiles_path, self.source_onto_do.ofile_name)
#        do_list = OboParser.parse_do_obo_from_file(in_path)
#        df = pandas.DataFrame.from_records([s.to_dict() for s in do_list])
#        # onto edges
#        self.create_db_file_from_onto(self.source_onto_hpo.csv_name, self.source_onto_hpo.use_cols, df)
#        # mapping edges
#        self.create_db_file_from_onto('DB_ONTO_mapping_DO_UMLS.csv', ['ID', 'UMLS'],df)
#        self.create_db_file_from_onto('DB_ONTO_mapping_DO_OMIM.csv', ['ID', 'OMIM'],df)


        # ##### edges #####
        #for e in self.source_edge_list:
        #    self.create_db_file(e.ofile_name, e.csv_name, e.cols, e.use_cols, e.nr_lines_header)

        self.create_db_file(self.source_edge_dis_pheno.ofile_name, self.source_edge_dis_pheno.csv_name, self.source_edge_dis_pheno.cols, self.source_edge_dis_pheno.use_cols, self.source_edge_dis_pheno.nr_lines_header)
        # making ids unique in HPO file (db:id)
        in_file = open(os.path.join(self.folder_path, self.source_edge_dis_pheno.csv_name))
        cols = self.source_edge_dis_pheno.use_cols
        data = pandas.read_csv(in_file, sep=';', names=cols, dtype={cols[0]:str, cols[3]:str})
        in_file.close()
        data[cols[0]] = data[cols[3]] + ':' + data[cols[0]]
        data = data.drop(cols[3], axis=1)
        del self.source_edge_dis_pheno.use_cols[3]
        out_file = open(os.path.join(self.folder_path, self.source_edge_dis_pheno.csv_name), 'w')
        data[self.source_edge_dis_pheno.use_cols].to_csv(out_file, sep=';', index=False, header=False)
        out_file.close()

        # ###### mapping ######
        for m in self.source_mapping_list:
            self.create_db_file(m.ofile_name, m.csv_name,m.cols, m.use_cols, m.nr_lines_header, m.mapping_sep, m.dtypes)

        #TODO mapping stitch to pubchem

        # --- dis - phenotype ---
        with open(os.path.join(self.oFiles_path, self.source_mapping_hoehndorf_omim_do.ofile_name)) as infile:
            data = json.load(infile)
            infile.close()
        with open(os.path.join(self.folder_path, self.source_mapping_hoehndorf_omim_do.csv_name), 'w') as out_file:
            writer = csv.writer(out_file, delimiter=";", lineterminator="\n")
            key_translate ={}
            for k,v in data.items():
                #key_translate[k] = k.replace('OMIM:', '').replace('PS', '') #todo PS?
                data[k] = v.replace('_', ':')
            for old, new in key_translate.items():
                data[new] = data.pop(old)
            out_data = zip(data.keys(),data.values())
            writer.writerows(out_data)
            out_file.close()
        return


    def create_db_file_from_onto(self, outname, use_cols, df):
        data = self.flat_df(df, use_cols, ';')
        data = data[data[data.columns[1]] != '']
        data[use_cols].to_csv(os.path.join(self.folder_path, outname), sep=';', index=False,
                                        header=False)


    def create_db_file(self, in_name, out_name, col_names, use_cols, skiprows, mapping_sep =None, dtype=None):
        in_path = os.path.join(self.oFiles_path, in_name)
        data = self.read_in_file_as_df(in_path, col_names, use_cols, skiprows, dtype)
        out_path = os.path.join(self.folder_path,out_name)
        if mapping_sep is not None:
            data = self.flat_df(data, use_cols, mapping_sep)
        data[use_cols].to_csv(out_path, sep=';', index=False, header=False)


    def read_in_file_as_df(self, in_path, col_names, use_cols, skiprows, dtype=None):
        path_parts = in_path.split('.')
        if (path_parts[1] == "txt"):
            sep = " "
        elif (path_parts[1] == "tsv" or path_parts[1] == "gaf" or path_parts[1] == "tab"):
            sep = "\t"
        else:
            sep = ","
        if (path_parts[-1] == "gz"):
            in_file = gzip.open(in_path, "rt", encoding="utf8")
        elif (path_parts[-1] == "zip"):
            zf = zipfile.ZipFile(in_path)
            in_file = zf.open(zf.namelist()[0])
        else:
            in_file = open(in_path)

        data = pandas.read_csv(in_file, sep=sep, names=col_names, usecols=use_cols, skiprows=skiprows, dtype=dtype)
        in_file.close()
        return data


    def flat_df(self, data, use_cols, mapping_sep =None):
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


    def create_graph(self):
#        # todo create empty edge file
#
#        # ##### ONTOLOGIES #########
#        # --- GO ---
#        edge_file = os.path.join(self.folder_path, self.source_onto_go.csv_name)
#        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.IS_A)
#        # --- DO ---
#        edge_file = os.path.join(self.folder_path, self.source_onto_do.csv_name)
#        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.IS_A)
#        # --- HPO ---
#        edge_file = os.path.join(self.folder_path, self.source_onto_hpo.csv_name)
#        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.IS_A)
#
#       # ##### EDGES ###########
#        #todo maybe also classes
#       # --- gene - gene ---
#        edge_file = os.path.join(self.folder_path, self.source_edge_gene_gene.csv_name)         #todo cutoff rule
#        mapping_file1 = os.path.join(self.folder_path, self.source_mapping_string_ncbi_string.csv_name)
#        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType = EdgeType.GENE_GENE, colindex_qscore=2,
#                      mapping1_file=mapping_file1, map1_sourceindex=1, map1_targetindex=0, db1_index=None, db1_name=None,
#                      mapping2_file=mapping_file1, map2_sourceindex=1, map2_targetindex=0, db2_index=None, db2_name=None)
#
#       # --- gene - go ---
#        edge_file = os.path.join(self.folder_path, self.source_edge_gene_go.csv_name)
#        mapping_file1 = os.path.join(self.folder_path, self.source_mapping_uniprot_uniprot_ncbi.csv_name)
#        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_GO, colindex_qscore=2,
#                          mapping1_file=mapping_file1, map1_sourceindex=0, map1_targetindex=1)
#
#       #  --- gene - dis ---
#        edge_file = os.path.join(self.folder_path, self.source_edge_gene_dis.csv_name)
#        mapping_file2 = os.path.join(self.folder_path, self.source_mapping_disgenet_umls_do.csv_name)
#        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_DIS, colindex_qscore=2,
#                          mapping1_file=None, map1_sourceindex=None, map1_targetindex=None, db1_index=None,db1_name=None,
#                          mapping2_file=mapping_file2, map2_sourceindex=0, map2_targetindex=2, db2_index=1, db2_name='DO')
#
#       #  --- gene - drug ---
#        edge_file = os.path.join(self.folder_path, self.source_edge_gene_drug.csv_name)
#        mapping_file1 = os.path.join(self.folder_path, self.source_mapping_string_ncbi_string.csv_name) #todo map stitch to pubchem
#        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_DRUG, colindex_qscore=2,
#                          mapping1_file=mapping_file1, map1_sourceindex=1, map1_targetindex=0, db1_index=None,
#                          db1_name=None,
#                          mapping2_file=None, map2_sourceindex=None, map2_targetindex=None, db2_index=None,
#                          db2_name=None)
#
#        # --- gene - phenotype ---
#        edge_file = os.path.join(self.folder_path, self.source_edge_gene_pheno.csv_name)
#        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_PHENOTYPE, colindex_qscore=None)
#
#        # --- gene - pathway ---
#        edge_file = os.path.join(self.folder_path, self.source_edge_gene_path.csv_name)
#        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_PATHWAY)
#
#        # --- gene - anatomy ---
#        edge_file = os.path.join(self.folder_path, self.source_edge_gene_anatomy.csv_name)
#        mapping_file1 = os.path.join(self.folder_path, self.source_mapping_uniprot_ensembl_ncbi.csv_name)
#        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_ANATOMY, colindex_qscore=2,
#                          mapping1_file=mapping_file1, map1_sourceindex=0, map1_targetindex=1, db1_index=None,
#                          db1_name=None
#                          )

        # --- dis - phenotype ---
        edge_file = os.path.join(self.folder_path, self.source_edge_dis_pheno.csv_name)
        mapping_file1 = os.path.join(self.folder_path, self.source_mapping_hoehndorf_omim_do.csv_name)
        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.DIS_PHENOTYPE,
                          colindex_qscore=2,
                          mapping1_file=mapping_file1, map1_sourceindex=0, map1_targetindex=1, db1_index=None,
                          db1_name=None,
                          mapping2_file=None, map2_sourceindex=None, map2_targetindex=None, db2_index=None,
                          db2_name=None)

#        # --- dis - drug ---
#        edge_file = os.path.join(self.folder_path, self.source_edge_dis_drug.csv_name)
#        mapping_file1 = os.path.join(self.folder_path, self.source_mapping_hoehndorf_umls_do.csv_name)  # todo map stitch to pubchem
#        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.DIS_DRUG,
#                          colindex_qscore=2,
#                          mapping1_file=mapping_file1, map1_sourceindex=0, map1_targetindex=1, db1_index=None,
#                          db1_name=None,
#                          mapping2_file=None, map2_sourceindex=None, map2_targetindex=None, db2_index=None,
#                          db2_name=None)
#
#        # --- drug - phenotype ---
#        edge_file = os.path.join(self.folder_path, self.source_edge_drug_pheno.csv_name)
#        mapping_file2 = os.path.join(self.folder_path, self.source_mapping_hoehndorf_umls_hpo.csv_name)        # todo map stitch to pubchem
#        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.DRUG_PHENOTYPE, colindex_qscore=None,
#                         mapping1_file=None, map1_sourceindex=None, map1_targetindex=None, db1_index=None, db1_name=None,
#                         mapping2_file=mapping_file2, map2_sourceindex=0, map2_targetindex=1, db2_index=None, db2_name=None)
        return


    def create_edges (self, edges_file, colindex1, colindex2, edgeType, colindex_qscore=None, cutoff_num= None, cutoff_txt = None,
                      mapping1_file = None, map1_sourceindex = None, map1_targetindex = None, db1_index = None, db1_name= None,
                      mapping2_file = None, map2_sourceindex = None, map2_targetindex = None, db2_index = None, db2_name= None):
        # --- mapping ---
        if (mapping1_file is not None):
            mapping1 = {}
            with open(mapping1_file, mode="r") as mapping_content1:
                reader = csv.reader(mapping_content1, delimiter=";")

                for row in reader:
                    if (db1_index is None or row[db1_index]==db1_name):
                        if row[map1_sourceindex] in mapping1:
                            mapping1[row[map1_sourceindex]].append(row[map1_targetindex])
                        else:
                            mapping1[row[map1_sourceindex]] = [row[map1_targetindex]]
                mapping_content1.close()
        if (mapping2_file is not None):
            mapping2 = {}
            with open(mapping2_file, mode="r") as mapping_content2:
                reader = csv.reader(mapping_content2, delimiter=";")
                for row in reader:
                    if (db2_index is None or row[db2_index]==db2_name):
                        if row[map2_sourceindex] in mapping2:
                            mapping2[row[map2_sourceindex]].append(row[map2_targetindex])
                        else:
                            mapping2[row[map2_sourceindex]] = [row[map2_targetindex]]
                mapping_content2.close()

        # --- edges ---
        with open(edges_file, "rt", encoding="utf8") as edge_content:
            edges = []
            ids1_no_mapping = set()
            ids2_no_mapping = set()
            nr_id1 = set()
            nr_id2 = set()
            nr_edges=0
            nr_edges_after_mapping = 0
            nr_edges_no_mapping = 0

            reader = csv.reader(edge_content, delimiter = ";")

            for row in reader:
                raw_id1 = row[colindex1]
                raw_id2 = row[colindex2]
                if colindex_qscore is not None:
                    qscore = row[colindex_qscore]
                else:
                    qscore = None
                edge_id1 = None
                edge_id2 = None
                nr_id1.add(raw_id1)
                nr_id2.add(raw_id2)

                if (mapping1_file is not None and raw_id1 in mapping1):
                    edge_id1 = mapping1.get(raw_id1)
                if (mapping2_file is not None and raw_id2 in mapping2):
                    edge_id2 = mapping2.get(raw_id2)

                if ((edge_id1 is not None and edge_id2 is not None) or
                    (edge_id1 is not None and mapping2_file is None) or
                    (edge_id2 is not None and mapping1_file is None) or
                    (mapping1_file is None and mapping2_file is None)):
                    if (edge_id1 is None):
                        edge_id1 = [raw_id1]
                    if (edge_id2 is None):
                        edge_id2 = [raw_id2]
                    for id1 in edge_id1:
                        for id2 in edge_id2:
                            #todo here cutoff
                            edge = Edge(id1, edgeType, id2, None, qscore)
                            edges.append(edge)
                            nr_edges_after_mapping += 1
                else:
                    nr_edges_no_mapping += 1
                    if (edge_id1 is None and mapping1_file is not None):
                        ids1_no_mapping.add(raw_id1 )
                    if (edge_id2 is None and mapping2_file is not None):
                        ids2_no_mapping.add(raw_id2)
                nr_edges += 1

            edge_content.close()


        # write output
        with open(os.path.join(self.folder_path, 'ONTO_edges.tsv'), 'a') as out_file: #todo change here
            writer = csv.writer(out_file, delimiter='\t', lineterminator='\n')
            for edge in edges:
                writer.writerow(list(edge))
            out_file.close()
        with open(os.path.join(self.folder_path, 'ids_no_mapping.tsv'), 'a') as out_file:
            for id in ids1_no_mapping:
                out_file.write('%s\t%s\n' %(id, edgeType))
            for id in ids2_no_mapping:
                out_file.write('%s\t%s\n' % (id, edgeType))
            out_file.close()

        # TODO write nodes
        # maybe load all relevant edges/nodes to set and substract from local id file -> write

        print('Nr edges '  + str(edgeType) + ': ' + str(nr_edges))
        print('Nr edges no mapping for ' + str(edgeType) + ': ' + str(nr_edges_no_mapping))
        print('Edges coverage ' + str(edgeType) + ': ' + str(1-(nr_edges_no_mapping/ nr_edges)))
        print('Nr edges after mapping (final nr) ' + str(edgeType) + ': ' + str(nr_edges_after_mapping))
        print('Nr nodes1 no mapping for ' + str(edgeType) + ': ' + str(len(ids1_no_mapping)))
        print('Nr nodes2 no mapping for ' + str(edgeType) + ': ' + str(len(ids2_no_mapping)))

        print('Nr nodes1  ' + str(edgeType) + ': ' + str(len(nr_id1)))
        print('Nr nodes2  ' + str(edgeType) + ': ' + str(len(nr_id2)))

        print('nodes1 coverage ' + str(edgeType) + ': ' + str(1-(len(ids1_no_mapping)/ len(nr_id1))))
        print('nodes2 coverage ' + str(edgeType) + ': ' + str(1-(len(ids2_no_mapping)/ len(nr_id2))))
        print('######################################################################################')
        return
