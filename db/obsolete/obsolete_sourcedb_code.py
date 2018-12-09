# __________________________________________________________________
# ################## HOEHNDORF MAPPINGS #############################
# __________________________________________________________________

# ----- insert into __init__(self, folder_path)

#       self.source_mapping_hoehndorf_omim_do =     SourceMappingDB(url= "https://raw.githubusercontent.com/bio-ontology-research-group/multi-drug-embedding/master/data/omim2doid.dict" ,
#                                                                   ofile_name="Hoehndorf_mapping_omim_do.txt",
#                                                                   csv_name="DB_Hoehndorf_mapping_omim_do.csv",
#                                                                   cols=None,
#                                                                   use_cols=None,
#                                                                   nr_lines_header=None)
#       self.source_mapping_hoehndorf_umls_do =     SourceMappingDB(url= "https://raw.githubusercontent.com/bio-ontology-research-group/multi-drug-embedding/master/data/umls2doid.txt",
#                                                                   ofile_name="Hoehndorf_mapping_umls_do.tsv",
#                                                                   csv_name="DB_Hoehndorf_mapping_umls_do.csv",
#                                                                   cols=['doID', 'umlsID', 'umlsName'],
#                                                                   use_cols=['umlsID', 'doID'],
#                                                                   nr_lines_header=0)
#       self.source_mapping_hoehndorf_umls_hpo =    SourceMappingDB(url= "https://raw.githubusercontent.com/bio-ontology-research-group/multi-drug-embedding/master/data/umls2hpo.txt" ,
#                                                                           ofile_name="Hoehndorf_mapping_umls_hpo.tsv",
#                                                                           csv_name="DB_Hoehndorf_mapping_umls_hpo.csv",
#                                                                           cols=['hpoID', 'umlsID', 'umlsName'],
#                                                                           use_cols=['umlsID', 'hpoID'],
#                                                                           nr_lines_header=0)
# do not insert omim_do into mapping list

# ----- insert into download_resources(self)

# urllib.request.urlretrieve(self.source_mapping_hoehndorf_omim_do.url,  os.path.join(self.oFiles_path, self.source_mapping_hoehndorf_omim_do.ofile_name ))


# ----- insert into create_db_files(self)

#        with open(os.path.join(self.oFiles_path, self.source_mapping_hoehndorf_omim_do.ofile_name)) as infile:
#            data = json.load(infile)
#            infile.close()
#
#        with open(os.path.join(self.folder_path, self.source_mapping_hoehndorf_omim_do.csv_name), 'w') as out_file:
#            writer = csv.writer(out_file, delimiter=";", lineterminator="\n")
#            key_translate ={}
#            for k,v in data.items():
#                #key_translate[k] = k.replace('OMIM:', '').replace('PS', '') #todo ms PS?
#                data[k] = v.replace('_', ':')
#            for old, new in key_translate.items():
#                data[new] = data.pop(old)
#            out_data = zip(data.keys(),data.values())
#            writer.writerows(out_data)
#            out_file.close()


# __________________________________________________________________
# ################## BioPortal Mappings #############################
# __________________________________________________________________

# ----- insert into __init__(self, folder_path)

#        self.api_key = '541ff25a-641f-4963-b774-81df7d39e956'
#        extract_do_id_lambda = lambda a: a.split('_')[1]
#        extract_orpha_id_lambda = lambda a: a.split('_')[1]
#        extract_omim_id_lambda = lambda a:  a.split('/')[-1] if (a.split('/')[-1].find('MTHU') == -1) else None
#        self.source_biomapping_do_omim = SourceBioMappingDB(url='http://data.bioontology.org/mappings?ontologies=OMIM,DOID',
#                                                            ofile_name='BioPortal_mapping_do_omim.json',
#                                                            csv_name='DB_BioPortal_mapping_do_omim.csv',
#                                                            use_cols= ['DOID', 'OMIM'],
#                                                            id1_prefix='DOID:',
#                                                            id2_prefix='OMIM:',
#                                                            id1_lambda=extract_do_id_lambda,
#                                                            id2_lambda=extract_omim_id_lambda)
#        self.source_biomapping_do_orpha = SourceBioMappingDB(url='http://data.bioontology.org/mappings?ontologies=ORDO,DOID',
#                                                             ofile_name='BioPortal_mapping_do_orpha.json',
#                                                             csv_name='DB_BioPortal_mapping_do_orpha.csv',
#                                                             use_cols=['DOID', 'ORPHA'],
#                                                             id1_prefix='DOID:',
#                                                             id2_prefix='ORPHA:',
#                                                             id1_lambda=extract_do_id_lambda,
#                                                             id2_lambda=extract_orpha_id_lambda)
#
#        self.source_biomapping_list = [self.source_biomapping_do_omim,
#                                       self.source_biomapping_do_orpha]

# ----- insert into download_resources(self)
#
#        for b in self.source_biomapping_list:
#            BioPortalMappingParser.url_to_json(b.url, os.path.join(self.oFiles_path, b.ofile_name), self.api_key)
#
# ----- insert into create_db_files(self)
#
#       for b in self.source_biomapping_list:
#           BioPortalMappingParser.create_db_file(os.path.join(self.oFiles_path, b.ofile_name), b.id1_prefix, b.id2_prefix,
#                                                 b.use_cols, b.id1_lambda, b.id2_lambda,
#                                                 os.path.join(self.folder_path, b.csv_name))
