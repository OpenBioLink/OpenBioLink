URL         = "ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/idmapping/by_organism/HUMAN_9606_idmapping_selected.tab.gz"
OFILE_NAME  = "Uniprot_mapping_gene.tab.gz"
COLS        = ['UniProtKB-AC', 'UniProtKB-ID', 'GeneID',
                  'RefSeq', 'GI', 'PDB', 'GO', 'UniRef100',
                  'UniRef90', 'UniRef50', 'UniParc', 'PIR',
                  'NCBI-taxon', 'MIM', 'UniGene', 'PubMed',
                  'EMBL', 'EMBL-CDS', 'Ensembl', 'Ensembl_TRS',
                  'Ensembl_PRO', 'Additional PubMed']
FILTER_COLS = ['Ensembl', 'GeneID', 'UniProtKB-AC']
HEADER      = 0
DTYPES      = {'Ensembl': str, 'GeneID': str, 'UniProtKB-AC': str}
