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
        self.url_onto_go = "http://purl.obolibrary.org/obo/go/go-basic.obo"
        self.url_onto_do = "https://raw.githubusercontent.com/DiseaseOntology/HumanDiseaseOntology/master/src/ontology/doid.obo"
        self.url_onto_hpo = "https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.obo"
        # onto_uberon_url
        # -- file names --
        self.path_onto_go = "GO_ontology.obo"
        self.path_onto_do = "DO_ontology.obo"
        self.path_onto_hpo = "HPO_ontology.obo"

        # ---- Edges ----
        self.url_edge_gene_gene = "https://stringdb-static.org/download/protein.links.v10.5/9606.protein.links.v10.5.txt.gz"          # STRING
        self.url_edge_gene_process = "http://geneontology.org/gene-associations/goa_human.gaf.gz"            # GO
        self.url_edge_gene_dis = "http://www.disgenet.org/ds/DisGeNET/results/" \
                                 "curated_gene_disease_associations.tsv.gz"                                  # DisGenNet
        self.url_edge_gene_drug= "http://stitch.embl.de/download/protein_chemical.links.v5.0/9606.protein_chemical.links.v5.0.tsv.gz" # STITCH
        self.url_edge_gene_phenotype = "http://compbio.charite.de/jenkins/job/hpo.annotations.monthly/lastSuccessfulBuild" \
                                     "/artifact/annotation/ALL_SOURCES_ALL_FREQUENCIES_genes_to_phenotype.txt "    #HPO
        self.url_edge_gene_pathway = "http://ctdbase.org/reports/CTD_genes_pathways.tsv.gz"                    # CDT
        self.url_edge_gene_anatomy = "https://www.proteinatlas.org/download/rna_tissue.tsv.zip"                 #HPA        //TODO GTEx
        self.url_edge_dis_drug = "http://sideeffects.embl.de/media/download/meddra_all_indications.tsv.gz"     #SIDER
        self.url_edge_dis_phenotype = "http://compbio.charite.de/jenkins/job/hpo.annotations/lastStableBuild/" \
                                      "artifact/misc/phenotype_annotation_hpoteam.tab"                        # HPO
        self.url_edge_drug_phenotype = "http://sideeffects.embl.de/media/download/meddra_all_se.tsv.gz"

        # self.url_edge_drug_drug
        # -- file names --
        self.path_edge_gene_gene = "STRING_gene_gene.txt.gz"
        self.path_edge_gene_process = "GO_annotations.gaf.gz"
        self.path_edge_gene_dis = "DisGeNet_gene_disease.tsv.gz"
        self.path_edge_gene_drug = "STITCH_gene_drug.tsv.gz"
        self.path_edge_gene_phenotyp =  "HPO_gene_phenotype.tsv"
        self.path_edge_gene_pathway = "CDT_gene_pathway.tsv.gz"
        self.path_edge_gene_anatomy = "HPA_gene_anatomy.tsv.zip" # TODO GTEx
        self.path_edge_dis_drug = "SIDER_dis_drug.tsv.gz"
        self.path_edge_dis_phenotype = "HPO_disease_phenotype.tab"
        self.path_edge_drug_phenotype = "SIDER_se.tsv.gz"

        # ---- Mappings ----
        self.url_mapping_string_ncbi_string = "https://string-db.org/mapping_files/entrez_mappings/entrez_gene_id.vs.string.v10.28042015.tsv"
        self.url_mapping_uniprot_uniprot_ncbi = "ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/by_organism/HUMAN_9606_idmapping_selected.tab.gz"
        self.url_mapping_uniprot_ensembl_ncbi = "ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/by_organism/HUMAN_9606_idmapping_selected.tab.gz" #TODO overhead
        self.url_mapping_disgenet_umls_do = "http://www.disgenet.org/ds/DisGeNET/results/disease_mappings.tsv.gz"
        self.url_mapping_hoehndorf_omim_do = "https://raw.githubusercontent.com/bio-ontology-research-group/multi-drug-embedding/master/data/omim2doid.dict"
        self.url_mapping_hoehndorf_umls_do = "https://raw.githubusercontent.com/bio-ontology-research-group/multi-drug-embedding/master/data/umls2doid.txt"
        self.url_mapping_hoehndorf_umls_hpo = "https://raw.githubusercontent.com/bio-ontology-research-group/multi-drug-embedding/master/data/umls2hpo.txt"
        # -- file names --
        self.path_mapping_string_ncbi_string = "String_mapping_gene_ncbi_string.tsv"
        self.path_mapping_uniprot_uniprot_ncbi = "Uniprot_mapping_gene_uniprot_ncbi.tab.gz"
        self.path_mapping_uniprot_ensembl_ncbi = "Uniprot_mapping_gene_ensembl_ncbi.tab.gz"
        self.path_mapping_disgenet_umls_do = "DisGeNet_mapping_disease_umls_do.tsv.gz"
        self.path_mapping_hoehndorf_omim_do = "Hoehndorf_mapping_omim_do.txt"
        self.path_mapping_hoehndorf_umls_do = "Hoehndorf_mapping_umls_do.tsv"
        self.path_mapping_hoehndorf_umls_hpo = "Hoehndorf_mapping_umls_hpo.tsv"


    # ##################################################################################################################################################

    def download_resources(self):
        # TODO check if files already present
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)


        # ---- Ontologies ----
        urllib.request.urlretrieve(self.url_onto_go,    os.path.join(self.oFiles_path, self.path_onto_go))
        urllib.request.urlretrieve(self.url_onto_do,    os.path.join(self.oFiles_path, self.path_onto_do))
        urllib.request.urlretrieve(self.url_onto_hpo,   os.path.join(self.oFiles_path, self.path_onto_hpo))

        # ---- Edges ----
        urllib.request.urlretrieve(self.url_edge_gene_gene,     os.path.join(self.oFiles_path, self.path_edge_gene_gene ))
        urllib.request.urlretrieve(self.url_edge_gene_process,  os.path.join(self.oFiles_path, self.path_edge_gene_process ))
        urllib.request.urlretrieve(self.url_edge_gene_dis,      os.path.join(self.oFiles_path, self.path_edge_gene_dis ))
        urllib.request.urlretrieve(self.url_edge_gene_drug,     os.path.join(self.oFiles_path, self.path_edge_gene_drug ))
        urllib.request.urlretrieve(self.url_edge_gene_phenotype,os.path.join(self.oFiles_path, self.path_edge_gene_phenotyp))
        urllib.request.urlretrieve(self.url_edge_gene_pathway,  os.path.join(self.oFiles_path, self.path_edge_gene_pathway ))
        urllib.request.urlretrieve(self.url_edge_gene_anatomy,  os.path.join(self.oFiles_path, self.path_edge_gene_anatomy ))
        urllib.request.urlretrieve(self.url_edge_dis_drug,      os.path.join(self.oFiles_path, self.path_edge_dis_drug ))
        urllib.request.urlretrieve(self.url_edge_dis_phenotype, os.path.join(self.oFiles_path, self.path_edge_dis_phenotype))
        urllib.request.urlretrieve(self.url_edge_drug_phenotype, os.path.join(self.oFiles_path, self.path_edge_drug_phenotype))

        # ---- Mappings ----
        urllib.request.urlretrieve(self.url_mapping_string_ncbi_string,     os.path.join(self.oFiles_path, self.path_mapping_string_ncbi_string))
        urllib.request.urlretrieve(self.url_mapping_uniprot_uniprot_ncbi,   os.path.join(self.oFiles_path, self.path_mapping_uniprot_uniprot_ncbi))
        urllib.request.urlretrieve(self.url_mapping_uniprot_ensembl_ncbi,   os.path.join(self.oFiles_path, self.path_mapping_uniprot_ensembl_ncbi))
        urllib.request.urlretrieve(self.url_mapping_disgenet_umls_do,       os.path.join(self.oFiles_path, self.path_mapping_disgenet_umls_do))
        urllib.request.urlretrieve(self.url_mapping_hoehndorf_omim_do ,     os.path.join(self.oFiles_path, self.path_mapping_hoehndorf_omim_do ))
        urllib.request.urlretrieve(self.url_mapping_hoehndorf_umls_do ,     os.path.join(self.oFiles_path, self.path_mapping_hoehndorf_umls_do ))
        urllib.request.urlretrieve(self.url_mapping_hoehndorf_umls_hpo,     os.path.join(self.oFiles_path, self.path_mapping_hoehndorf_umls_hpo))


    def create_db_files(self):
        # ###### ontologies #######
        in_path = os.path.join(self.oFiles_path, self.path_onto_go)
        do_list = OboParser.parse_go_obo_from_file(in_path)
        df = pandas.DataFrame.from_records([s.to_dict() for s in do_list])
        # onto edges
        outname_onto = 'DB_ONTO_' + self.path_onto_go.split('.')[0] + ".csv"
        use_cols_onto = ['ID', 'IS_A']
        data_onto = self.flat_df(df, use_cols_onto, ';')
        data_onto = data_onto[data_onto['IS_A'] != '']
        data_onto[use_cols_onto].to_csv(os.path.join(self.folder_path, outname_onto), sep=';', index=False, header=False)

        # -- HPO --
        in_path = os.path.join(self.oFiles_path, self.path_onto_hpo)
        hpo_list = OboParser.parse_hpo_obo_from_file(in_path)
        df = pandas.DataFrame.from_records([s.to_dict() for s in hpo_list])
        # onto edges
        outname_onto = 'DB_ONTO_' + self.path_onto_hpo.split('.')[0] + ".csv"
        use_cols_onto = ['ID', 'IS_A']
        data_onto = self.flat_df(df, use_cols_onto, ';')
        data_onto = data_onto[data_onto['IS_A']!='']
        data_onto[use_cols_onto].to_csv(os.path.join(self.folder_path,outname_onto), sep=';', index=False, header=False)
        # mapping edges
        outname_umls = 'DB_UMLS_' + self.path_onto_hpo.split('.')[0] + ".csv"
        use_cols_umls = ['ID', 'UMLS']
        data_umls = self.flat_df(df, use_cols_umls, ';')
        data_umls = data_umls[data_umls['UMLS']!='']
        data_umls[use_cols_umls].to_csv(os.path.join(self.folder_path,outname_umls), sep=';', index=False, header=False)

        # -- DO --
        in_path = os.path.join(self.oFiles_path, self.path_onto_do)
        do_list = OboParser.parse_do_obo_from_file(in_path)
        df = pandas.DataFrame.from_records([s.to_dict() for s in do_list])
        # onto edges
        outname_onto = 'DB_ONTO_' + self.path_onto_do.split('.')[0] + ".csv"
        use_cols_onto = ['ID', 'IS_A']
        data_onto = self.flat_df(df, use_cols_onto, ';')
        data_onto = data_onto[data_onto['IS_A'] != '']
        data_onto[use_cols_onto].to_csv(os.path.join(self.folder_path,outname_onto), sep=';', index=False, header=False)
        # mapping edges
        outname_umls = 'DB_ONTO_' + self.path_onto_do.split('.')[0] + ".csv"
        use_cols_umls = ['ID', 'UMLS']
        data_umls = self.flat_df(df, use_cols_umls, ';')
        data_umls = data_umls[data_umls['UMLS'] != '']
        data_umls[use_cols_umls].to_csv(os.path.join(self.folder_path,outname_umls), sep=';', index=False, header=False)

           # ##### edges #####

        # --- gene - gene  ---
        cols = ['string1', 'string2', 'qscore']
        use_cols = ['string1', 'string2', 'qscore']
        self.create_db_file(self.path_edge_gene_gene, cols, use_cols, 1)

        # --- gene - GO ---
        cols = ['DB', 'DOI', 'qulifier', 'none13', 'GO_ID', 'DB_ref', 'evidence_code', 'with_from', 'taxon', 'date', 'assigned_by', 'ann_ext', 'ann_prop', 'none14', 'none15', 'none16', 'none17']
        use_cols = ['DOI', 'GO_ID', 'evidence_code']
        self.create_db_file( self.path_edge_gene_process, cols, use_cols, 30)

        # --- gene - dis ---
        cols = ['geneID', 'geneSym', 'umlsID', 'disName', 'score', 'NofPmids', 'NofSnps', 'source']
        use_cols = ['geneID', 'umlsID', 'score']
        self.create_db_file(self.path_edge_gene_dis, cols, use_cols, 1)

        # --- gene - drug ---
        cols = ['chemID', 'stringID', 'qscore']
        use_cols = ['stringID', 'chemID', 'qscore']
        self.create_db_file( self.path_edge_gene_drug, cols, use_cols, 1)

        # --- gene - phenotype ---
        cols = ['geneID', 'geneSymb', 'hpoName', 'hpoID']
        use_cols = ['geneID', 'hpoID']
        self.create_db_file(self.path_edge_gene_phenotyp, cols, use_cols, 1)

        # --- gene - pathway ---
        cols = ['geneSymb', 'geneID', 'pathwayName', 'pathwayID'] #TODO remove keeg / reac pre
        use_cols = ['geneID', 'pathwayID']
        self.create_db_file(self.path_edge_gene_pathway, cols, use_cols, 29, None, {'geneID': str, 'pathwayID': str})
        # --- gene - anatomy ---
        cols = ['geneID', 'geneName', 'anatomy', 'expressionValue', 'Unit']
        use_cols = ['geneID', 'anatomy', 'expressionValue']
        self.create_db_file(self.path_edge_gene_anatomy, cols, use_cols, 1)


        # --- dis - drug ---
        cols = ['stichID', 'umlsID', 'method', 'umlsName', 'medDRAumlsType', 'medDRAumlsID', 'medDRAumlsName']
        use_cols = ['umlsID', 'stichID', 'method']
        self.create_db_file( self.path_edge_dis_drug, cols, use_cols, 0)
        # --- dis - phenotype ---
        cols = ['DB', 'DOI', 'DBname', 'qulifier', 'HPO_ID', 'DB_ref', 'evidence_code', 'onsetMod', 'freq', 'sex', 'mod', 'aspect', 'date', 'assigned_by']
        use_cols = ['DOI', 'HPO_ID', 'evidence_code', 'DB' ]
        self.create_db_file( self.path_edge_dis_phenotype, cols, use_cols, 0) #todo order cols

        # --- drug - phenotype ---
        cols = ['stitchID_flat', 'stitchID_stereo', 'umlsID', 'medDRAumlsType', 'medDRAumlsID', 'SEname']
        use_cols = ['stitchID_flat', 'umlsID'] #TODO which stitch ID ?
        self.create_db_file( self.path_edge_drug_phenotype, cols, use_cols, 0)


        # ###### mapping ######

        # --- gene - gene / gene - drug ---
        cols = ['ncbiID', 'stringID']
        use_cols = ['ncbiID', 'stringID']
        self.create_db_file(self.path_mapping_string_ncbi_string, cols, use_cols, 1)

        # --- gene - go  ---
        cols = ['UniProtKB-AC' ,'UniProtKB-ID' ,'GeneID' ,'RefSeq' ,'GI' ,'PDB' ,'GO' ,'UniRef100' ,'UniRef90' ,
                'UniRef50' ,'UniParc' ,'PIR' ,'NCBI-taxon' ,'MIM' ,'UniGene' ,'PubMed' ,'EMBL' ,'EMBL-CDS' ,'Ensembl' ,
                'Ensembl_TRS' ,'Ensembl_PRO' ,'Additional PubMed']
        use_cols = ['UniProtKB-AC', 'GeneID'] # todo AC or ID for uniprot
        dtypes = {'UniProtKB-AC': str, 'GeneID': str}
        self.create_db_file(self.path_mapping_uniprot_uniprot_ncbi, cols, use_cols, 0,                            ';', dtypes)

        # --- gene - anatomy  ---
        cols = ['UniProtKB-AC', 'UniProtKB-ID', 'GeneID', 'RefSeq', 'GI', 'PDB', 'GO', 'UniRef100', 'UniRef90',
                'UniRef50', 'UniParc', 'PIR', 'NCBI-taxon', 'MIM', 'UniGene', 'PubMed', 'EMBL', 'EMBL-CDS', 'Ensembl',
                'Ensembl_TRS', 'Ensembl_PRO', 'Additional PubMed']
        use_cols = ['Ensembl', 'UniProtKB-AC']  # todo AC or ID for uniprot
        dtypes = {'UniProtKB-AC': str, 'Ensembl': str}
        self.create_db_file(self.path_mapping_uniprot_ensembl_ncbi, cols, use_cols, 0,
                            ';', dtypes)

        # --- gene - dis ---
        cols = ['umlsID', 'name', 'voc', 'code', 'vocName']
        use_cols = ['umlsID', 'voc', 'code']
        self.create_db_file(self.path_mapping_disgenet_umls_do, cols, use_cols, 1)
#
        # --- gene - drug / dis - drug ---
        cols = ['doID', 'umlsID', 'umlsName']
        use_cols = ['umlsID', 'doID']
        self.create_db_file(self.path_mapping_hoehndorf_umls_do, cols, use_cols, 0)
#
        #TODO mapping stitch to pubchem
#
        # --- dis - phenotype ---
        with open(os.path.join(self.oFiles_path, self.path_mapping_hoehndorf_omim_do)) as infile:
            data = json.load(infile)
            infile.close()
        with open(os.path.join(self.folder_path,('DB_' + self.path_mapping_hoehndorf_omim_do.split('.')[0] + ".csv")), 'w') as out_file:
            writer = csv.writer(out_file, delimiter=";", lineterminator="\n")
            key_translate ={}
            for k,v in data.items():
                key_translate[k] = k.replace('OMIM:', '').replace('PS', '')
                data[k] = v.replace('_', ':')
            for old, new in key_translate.items():
                data[new] = data.pop(old)
            out_data = zip(data.keys(),data.values())
            writer.writerows(out_data)
            out_file.close()
#
        # --- drug - phenotype ---
        cols = ['hpoID', 'umlsID', 'umlsName']
        use_cols = ['umlsID', 'hpoID']
        self.create_db_file(self.path_mapping_hoehndorf_umls_hpo, cols, use_cols, 0)
        return


    def create_db_file(self, in_name, col_names, use_cols, skiprows, mapping_sep =None, dtype=None):
        in_path = os.path.join(self.oFiles_path, in_name)
        data = self.read_in_file_as_df(in_path, col_names, use_cols, skiprows, mapping_sep, dtype)
        out_path = os.path.join(self.folder_path,('DB_' + in_name.split('.')[0] + ".csv"))
        if mapping_sep is not None:
            data = self.flat_df(data, use_cols, mapping_sep)
        data[use_cols].to_csv(out_path, sep=';', index=False, header=False)


    def read_in_file_as_df(self, in_path, col_names, use_cols, skiprows, mapping_sep =None, dtype=None):
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
        # ##### ONTOLOGIES #########

 #       # --- GO ---
#       edge_file = os.path.join(self.folder_path, ('DB_ONTO_' + self.path_onto_go.split('.')[0] + ".csv"))
#       self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.IS_A)
#       # --- DO ---
#       edge_file = os.path.join(self.folder_path, ('DB_ONTO_' + self.path_onto_do.split('.')[0] + ".csv"))
#       self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.IS_A)
#       # --- HPO ---
#       edge_file = os.path.join(self.folder_path, ('DB_ONTO_' + self.path_onto_hpo.split('.')[0] + ".csv"))
#       self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.IS_A)

       # ##### EDGES ###########

       # --- gene - gene ---
        edge_file = os.path.join(self.folder_path, ('DB_' + self.path_edge_gene_gene.split('.')[0])+ ".csv")         #todo cutoff rule
        mapping_file1 = os.path.join(self.folder_path, ('DB_' + self.path_mapping_string_ncbi_string.split('.')[0] + ".csv"))
        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType = EdgeType.GENE_GENE, colindex_qscore=2,
                      mapping1_file=mapping_file1, map1_sourceindex=1, map1_targetindex=0, db1_index=None, db1_name=None,
                      mapping2_file=mapping_file1, map2_sourceindex=1, map2_targetindex=0, db2_index=None, db2_name=None)


       # --- gene - go ---
        edge_file = os.path.join(self.folder_path, ('DB_' + self.path_edge_gene_process.split('.')[0] + ".csv"))
        mapping_file1 = os.path.join(self.folder_path, ('DB_' + self.path_mapping_uniprot_uniprot_ncbi.split('.')[0] + ".csv"))
        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_GO, colindex_qscore=2,
                          mapping1_file=mapping_file1, map1_sourceindex=0, map1_targetindex=1)
       # --- gene - dis ---
        edge_file = os.path.join(self.folder_path, ('DB_' + self.path_edge_gene_dis.split('.')[0] + ".csv"))
        mapping_file2 = os.path.join(self.folder_path, ('DB_' + self.path_mapping_disgenet_umls_do.split('.')[0] + ".csv"))
        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_DIS, colindex_qscore=2,
                          mapping1_file=None, map1_sourceindex=None, map1_targetindex=None, db1_index=None,db1_name=None,
                          mapping2_file=mapping_file2, map2_sourceindex=0, map2_targetindex=2, db2_index=1, db2_name='DO')
        # --- gene - drug ---
        edge_file = os.path.join(self.folder_path, ('DB_' + self.path_edge_gene_drug.split('.')[0] + ".csv"))
        mapping_file1 = os.path.join(self.folder_path, ( 'DB_' + self.path_mapping_string_ncbi_string.split('.')[0] + ".csv")) #todo map stitch to pubchem
        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_DRUG, colindex_qscore=2,
                          mapping1_file=mapping_file1, map1_sourceindex=1, map1_targetindex=0, db1_index=None,
                          db1_name=None,
                          mapping2_file=None, map2_sourceindex=None, map2_targetindex=None, db2_index=None,
                          db2_name=None)
        # --- gene - phenotype ---
        edge_file = os.path.join(self.folder_path, ('DB_' + self.path_edge_gene_phenotyp.split('.')[0] + ".csv"))
        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_PHENOTYPE, colindex_qscore=None)
        # --- gene - pathway ---
        edge_file = os.path.join(self.folder_path, ('DB_' + self.path_edge_gene_pathway.split('.')[0] + ".csv"))
        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_PATHWAY)
        # --- gene - anatomy ---
        edge_file = os.path.join(self.folder_path, ('DB_' + self.path_edge_gene_anatomy.split('.')[0] + ".csv"))
        mapping_file1 = os.path.join(self.folder_path, ('DB_' + self.path_mapping_uniprot_ensembl_ncbi.split('.')[0] + ".csv"))
        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.GENE_ANATOMY, colindex_qscore=2,
                          mapping1_file=mapping_file1, map1_sourceindex=0, map1_targetindex=1, db1_index=None,
                          db1_name=None
                          )
        #TODO DIS PEHNOTYPE
        # --- dis - phenotype --- #TODO try
        edge_file = os.path.join(self.folder_path, ('DB_' + self.path_edge_dis_phenotype.split('.')[0] + ".csv"))
  #      mapping_file1 = os.path.join(self.folder_path, (
  #      'DB_' + self.path_mapping_hoehndorf_umls_do.split('.')[0] + ".csv"))  # todo map stitch to pubchem
  #      self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.DIS_DRUG,
  #                        colindex_qscore=2,
  #                        mapping1_file=mapping_file1, map1_sourceindex=0, map1_targetindex=1, db1_index=None,
  #                        db1_name=None,
  #                        mapping2_file=None, map2_sourceindex=None, map2_targetindex=None, db2_index=None,
  #                        db2_name=None)

        # --- dis - drug --- #TODO try
        edge_file = os.path.join(self.folder_path, ('DB_' + self.path_edge_dis_drug.split('.')[0] + ".csv"))
        mapping_file1 = os.path.join(self.folder_path, ('DB_' + self.path_mapping_hoehndorf_umls_do.split('.')[0] + ".csv"))  # todo map stitch to pubchem
        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.DIS_DRUG,
                          colindex_qscore=2,
                          mapping1_file=mapping_file1, map1_sourceindex=0, map1_targetindex=1, db1_index=None,
                          db1_name=None,
                          mapping2_file=None, map2_sourceindex=None, map2_targetindex=None, db2_index=None,
                          db2_name=None)
        # --- drug - phenotype --- #TODO try
        edge_file = os.path.join(self.folder_path, ('DB_' + self.path_edge_drug_phenotype.split('.')[0] + ".csv"))
        mapping_file2 = os.path.join(self.folder_path, ('DB_' + self.path_mapping_hoehndorf_umls_hpo.split('.')[0] + ".csv"))        # todo map stitch to pubchem
        self.create_edges(edges_file=edge_file, colindex1=0, colindex2=1, edgeType=EdgeType.DRUG_PHENOTYPE, colindex_qscore=None,
                         mapping1_file=None, map1_sourceindex=None, map1_targetindex=None, db1_index=None, db1_name=None,
                         mapping2_file=mapping_file2, map2_sourceindex=0, map2_targetindex=1, db2_index=None, db2_name=None)
        return


    def create_edges (self, edges_file, colindex1, colindex2, edgeType, colindex_qscore=None, cutoff_num= None, cutoff_txt = None,
                      mapping1_file = None, map1_sourceindex = None, map1_targetindex = None, db1_index = None, db1_name= None,
                      mapping2_file = None, map2_sourceindex = None, map2_targetindex = None, db2_index = None, db2_name= None,):
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
        with open(os.path.join(self.folder_path, 'edges.tsv'), 'a') as out_file: #todo change here
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
