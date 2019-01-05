URL         = "https://raw.githubusercontent.com/DiseaseOntology/HumanDiseaseOntology/master/src/ontology/doid.obo"
OFILE_NAME  = "DO_ontology.obo"
QUADRUPLES  = [('id', ' ', 1, 'ID'),
                            ('alt_id', ' ', 1, 'ID'),
                            ('is_a', ' ', 1, 'IS_A'),
                            ('xref: UMLS_CUI:', ':', 2, 'UMLS'),    # mapping umls
                            ('xref: OMIM:', ' ', 1, 'OMIM')]        # mapping omim

