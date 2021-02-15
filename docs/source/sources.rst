
Sources/Licenses
===================================

.. list-table::
   :header-rows: 1

   * - Source type
     - Source name
     - License
     - True neg.
     - Score
   * - edge (gene-gene)
     - `STRING <https://string-db.org/>`_
     - CC BY
     - No
     - Yes
   * - edge (gene-go)
     - `GO <http://geneontology.org/>`_
     - CC BY
     - No
     - Yes
   * - edge (gene-disease)
     - `DisGeNet <https://www.disgenet.org/>`_
     - CC BY-NC-CA
     - No
     - Yes
   * - edge (gene-phenotype)
     - `HPO <https://hpo.jax.org/app/>`_
     - Custom: `HPO <https://hpo.jax.org/app/license>`_
     - No
     - No
   * - edge (gene-anatomy)
     - `Bgee <https://bgee.org/>`_
     - CC 0
     - Yes
     - Yes
   * - edge (gene-drug)
     - `STITCH <http://stitch.embl.de/>`_
     - CC BY
     - No
     - Yes
   * - edge (gene-pathway)
     - `CTD <http://ctdbase.org/>`_
     - Custom: `CTD <http://ctdbase.org/about/legal.jsp>`_
     - No
     - No
   * - edge (disease-phenotype)
     - `HPO <https://hpo.jax.org/app/>`_
     - Custom: `HPO <https://hpo.jax.org/app/license>`_
     - Yes
     - No
   * - edge (disease-drug)
     - `DrugCentral <http://drugcentral.org/>`_
     - CC BY-SA
     - Yes
     - No
   * - edge (drug-phenotype)
     - `SIDER <http://sideeffects.embl.de/>`_
     - CC BY-NC-CA
     - No
     - No
   * - ontology (genes)
     - `GO <http://geneontology.org/>`_
     - CC BY
     - 
     - 
   * - ontology (diseases)
     - `DO <http://disease-ontology.org/>`_
     - CC 0
     - 
     - 
   * - ontology (phenotype)
     - `HPO <https://hpo.jax.org/app/>`_
     - Custom: `HPO <https://hpo.jax.org/app/license>`_
     - 
     - 
   * - ontology (anatomy)
     - `UBERON <http://uberon.github.io/about.html>`_
     - CC BY
     - 
     - 
   * - mapping (UMLS-DO)
     - `DisGeNet <https://www.disgenet.org/>`_
     - CC BY-NC-CA
     - 
     - 
   * - mapping (STRING-NCBI)
     - `STRING <https://string-db.org/>`_
     - CC BY
     - 
     - 
   * - mapping (ENSEMBL/UNIPROT-NCBI)
     - `UniProt <https://www.uniprot.org/>`_
     - CC BY
     - 
     - 
   * - id (genes)
     - `NCBI <https://www.ncbi.nlm.nih.gov/gene>`_
     - Public Domain
     - 
     - 
   * - id (go)
     - `GO <http://geneontology.org/>`_
     - CC BY
     - 
     - 
   * - id (anatomy)
     - `UBERON <http://uberon.github.io/about.html>`_
     - CC BY
     - 
     - 
   * - id (disease)
     - `DO <http://disease-ontology.org/>`_
     - CC 0
     - 
     - 
   * - id (drug)
     - `PubChem <https://pubchem.ncbi.nlm.nih.gov/>`_
     - Public Domain
     - 
     - 
   * - id (phenotype)
     - `HPO <https://hpo.jax.org/app/>`_
     - Custom: `HPO <https://hpo.jax.org/app/license>`_
     - 
     - 
   * - id (pathway)
     - `REACTOME <https://reactome.org/>`_
     - CC BY
     - 
     - 
   * - id (pathway)
     - `KEGG <https://www.genome.jp/kegg/>`_
     - Custom: `KEGG <https://www.kegg.jp/kegg/legal.html>`_
     - 
     - 


*(True neg.: whether the data contains true negative relations; Score: whether the data contains evidence quality scores for filtering relations)*

The OpenBioLink benchmark files integrate data or identifiers from these sources. The provenance of data items is captured in the benchmark files, and licensing terms of source databases apply to these data items. Please mind these licensing terms when utilizing or redistributing the benchmark files or derivatives thereof.

All original data in the benchmark files created by the OpenBioLink project (not covered by the licenses of external data sources)  are released as `CC 0 <https://creativecommons.org/publicdomain/zero/1.0/>`_. 

We offer the benchmark files as-is and make no representations or warranties of any kind concerning the benchmark files, express, implied, statutory or otherwise, including without limitation warranties of title, merchantability, fitness for a particular purpose, non infringement, or the absence of latent or other defects, accuracy, or the present or absence of errors, whether or not discoverable, all to the greatest extent permissible under applicable law.
