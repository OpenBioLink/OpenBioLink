# OpenBioLink

OpenBioLink is a resource and evaluation framework for evaluating link prediction models on heterogeneous biomedical graph data. It contains benchmark datasets as well as tools for creating custom benchmarks and training and evaluating models.

[Paper preprint on arXiv](https://arxiv.org/abs/1912.04616)

[Supplementary data](https://github.com/OpenBioLink/OpenBioLink/raw/master/paper/supplementary%20data.pdf)

The OpenBioLink benchmark aims to meet the following criteria:
* Openly available
* Large-scale
* Wide coverage of current biomedical knowledge and entity types
* Standardized, balanced train-test split
* Open-source code for benchmark dataset generation 
* Open-source code for evaluation (independent of model) 
* Integrating and differentiating multiple types of biological entities and relations (i.e., formalized as a heterogeneous graph)
* Minimized information leakage between train and test sets (e.g., avoid inclusion of trivially inferable 
    relations in the test set)
* Coverage of true negative relations, where available
* Differentiating high-quality data from noisy, low-quality data
* Differentiating benchmarks for directed and undirected graphs in order to be applicable to a wide variety of link prediction methods
* Clearly defined release cycle with versions of the benchmark and public leaderboard

## Installation

### Pip
1) Install a pytorch version suitable for your system https://pytorch.org/
1) ```pip install openbiolink```

### Source
1) clone the git repository or download the project
1) Create a new python3.7, or python3.6 virtual environment  *(note: under Windows, only python3.6 will work)*
e.g.:
```python3 -m venv my_venv```
1) activate the virtual environment
    * windows: ``my_venv\Scrips\activate``
    * linux/mac: ``source my_venv/bin/activate``
1) Install a pytorch version suitable for your system https://pytorch.org/
1) Install the requirements stated in requirements.txt e.g.  ```pip install -r requirements.txt```

## Benchmark Dataset
 The [OpenBioLink2020 Dataset](https://samwald.info/res/OpenBioLink_2020/HQ_DIR.zip) is a highly challenging
 benchmark dataset containing over 5 million positive and negative edges.
 The test set does not contain trivially predictable, inverse edges from the training set 
 and does contain all different edge types, to provide a more realistic edge prediction
 scenario.
 
 ### Leaderboard    
 
 | model | hits@10 | hits@1 |  paper | code |
|-------|---------|--------|-------|------|
|   TransE (Baseline)   |    0.0749     |   0.0125     | (under review)      | [Code](https://github.com/OpenBioLink/OpenBioLink/tree/master/src/openBioLink/evaluation)     |
|   TransR (Baseline)   |    0.0639     |   0.0096     | (under review)      | [Code](https://github.com/OpenBioLink/OpenBioLink/tree/master/src/openBioLink/evaluation)     |

Please contact us if you want to see your results added to the Leaderboard.


To allow anayzing the effect of data quality as well as the directionality of the 
evaluation graph, other variants of OpenBioLink2020 are provided, in directed and undirected setting,
with and without quality cutoff.

* [OpenBioLink2020: directed, high quality](https://samwald.info/res/OpenBioLink_2020/HQ_DIR.zip) (default dataset)
* [OpenBioLink2020: undirected, high quality](https://samwald.info/res/OpenBioLink_2020/HQ_UNDIR.zip)
* [OpenBioLink2020: directed, no quality cutoff](https://samwald.info/res/OpenBioLink_2020/ALL_DIR.zip)
* [OpenBioLink2020: undirected, no quality cutoff](https://samwald.info/res/OpenBioLink_2020/ALL_UNDIR.zip)

Please note that the OpenBioLink benchmark files contain data derived from external ressources. Licensing terms of these external resources are detailed [below](#Source-databases-and-their-licenses). 

 
## Manual

The OpenBioLink framework consists of three parts, called 'actions':
 1) graph creation
 2) train-test split creation
 3) training and evaluation

With the graph creation and the train-test set action, customized datasets can be created to suit individual needs.
The third action serves as an interface for training and evaluating link prediction models.

#### Calling via GUI
By calling the program without any parameters, the GUI is started, 
providing an interface to define required parameters. In the last step, 
the corresponding command line options are displayed.

#### Calling via command line
From folder src
```bash
openbiolink -p WORKING_DIR_PATH [-action] [--options] ...
```

**Action: Graph Creation**
````
-g:    
    --undir         Output-Graph should be undirectional (default = directional)
    --qual          quality cutoff of the output-graph, options = [hq, mq, lq], (default = None -> all entries are used)
    --no_interact   Disables interactive mode - existing files will be replaced (default = interactive)
    --skip          Existing files will be skipped - in combination with --no_interact (default = replace)
    --no_dl         No download is being performed (e.g. when local data is used)
    --no_in         No input_files are created (e.g. when local data is used)
    --no_create     No graph is created (e.g. when only in-files should be created)
    --out_format [TSV|RDF-N3] [Format] [Sep]       Format of graph output, takes 3 arguments: 
                                                   - The format of the graph files (Currently TSV or RDF-N3 are supported)
                                                   - A list of file formats [s= single file, m=multiple files] 
                                                   - A list of separators (only needed if TSV, e.g. t=tab, n=newline, or any other character)
                                                   (default= TSV s t)
    --no_qscore     The output files will contain no scores
    --dbs [Cls]     custom source databases selection to be used, full class name, options --> see doc
    --mes [Cls]     custom meta edges selection to be used, full class name, options --> see doc
````
**Action: Train-Test Split Generation**
 ````
-s
    --edges Path        Path to edges.csv file (required with action -s
    --tn_edges Path     Path to true_negatives_edges.csv file (required with action -s)
    --nodes Path        Path to nodes.csv file (required with action -s)
    --tts_sep [Sep]     Separator of edge, tn-edge and nodes file (e.g. t=tab, n=newline, 
                        or any other character) (default=t)
    --mode rand|time    Mode of train-test-set split, options=[rand, time], (default=rand)
    --test_frac F       Fraction of test set as float (default= 0.2)
    --crossval          Multiple train-validation-sets are generated
    --val F             fraction of validation set as float (default= 0.2) or number of folds as int
    --tmo_edges Path    Path to edges.csv file of t-minus-one graph (required for --mode time
    --tmo_tn_edges Path     Path to true_negatives_edges.csv file of t-minus-one graph (required for --mode time)
    --tmo_nodes Path        Path to nodes.csv file of t-minus-one graph (required for --mode time)
````
**Action: Training and Evaluation**
````
-e
    --model_cls Cls         class of the model to be trained/evaluated (required with -e)
    --config Path           Path to the models config file
    --no_train              No training is being performed, trained model id provided via --trained_model
    --trained_model Path    Path to trained model (required with --no_train)
    --no_eval               No evaluation is being performed, only training
    --test Path             Path to test set file (required with -e)
    --train Path            Path to trainings set file')
    --eval_nodes Path       Path to the nodes file (required for ranked triples if no corrupted triples 
                            file is provided and nodes cannot be taken from graph creation
    --metrics [Metric]      list of evaluation metrics
    --ks [K]                k's for hits@k metric (integer list)
````


# Train-test-split creation

## Random split
 In the random split setting, first, negative sampling is performed. Afterwards, the whole dataset (containing positive 
 and negative examples) is split randomly according to the defined ratio. Finally, post-processing steps are performed to
 facilitate training and to avoid information leakage.
 
 ## Time-slice split
 In the time-slice split setting, for both of the provided time slices, first, negative sampling is performed. Afterwards,
 the first time slice (t-1 graph) is used as training sample, while the difference between the first and the second time 
 slice serves as the test set. Finally, post-processing steps are performed to
 facilitate training and to avoid information leakage.
 
 Generally, the time slice setting is trickier to implement than the random split strategy, as it requires more manual evaluation and 
 knowledge of the data. One of the most difficult factors is the change of the source databases over time. For example, 
 a database might change its quality score, or even its ID-format. Also, the number of relationships stored might increase 
 sharply due to new mapping files being used. This might also result in ‘vanishing edges’, where edges that were present
 in the t-1 graph are no longer existent in the current graph. Although the OpenBioLink toolbox tries to assist the user with 
 different kinds of warnings to identify such difficulties in the data, it is unfortunately not possible to automatically detect nor solve all these problems, making some manual pre- and post-processing of the data inevitable.
 

## Negative sampling
First, the distribution of edges of different types is calculated to know how many samples are needed from each edge type. 
For now, this distribution corresponds to the original distribution (uniform distribution could a future extension).
Then, subsamples are either – where possible – taken from existing true negative edges or are created using type-based sampling.
 
In type-based sampling, head and tail node are randomly sampled from a reduced pool of all nodes, which only 
includes nodes with types that are compatible with the corresponding head- or tail-role of the given relation type.
E.g., for the relation type GENE_DRUG, one random node of type GENE is selected as head node and one
random node of type DRUG is selected as tail.

In most cases where true negative edges exist, however, their number is smaller than the number of positive examples. 
In these cases, all true negative samples are used for the negative set, which is then extended by samples created by type-based 
sampling.
 
 
 ## Train-test-set post-processing
 **To facilitate model application**
 * Edges that contain nodes that are not present in the training set are dropped from the test set. This facilitates use of embedding-based models that usually cannot make predictions for nodes that have not been embedded during training.

**Avoiding train-test information leakage and trivial predictions in the test set**
 * **Removal of reverse edges** If the graph is directed, reverse edges are removed from the training set. 
The reason for this is that if the original edge a-b was undirected, both directions a→b and a←b are materialized in the directed graph. 
 If one of these directed edges would be present in the training set and one in the test set, the prediction would be trivial.
 Therefore, in these cases, the reverse edges from the training set are removed. (Note that edges are removed from the training set instead of the test set because this is advantagous for maintaining the train-test-set ratio)
 * **Removal of super-properties**
 Some types of edges have sub-property characteristics, meaning that relationship x indicates a generic interaction between two entities (e.g. _protein_interaction_protein_), 
 while relationship y further describes this relationship in more detail (e.g., _protein_activation_protein_). This means that the presence of x between two nodes does not imply 
 the existence of a relation y between those same entities, but the presence of y necessarily implies the existence of x. These kinds of relationships 
 could cause information leakage in the datasets, therefore super-relations of relations present in the training set are removed 
 from the test set.


# Source databases and their licenses

| Source type                    | Source name                                  | License                                             | True neg.   | Score	  | Namespace Node 1                                                               | Namespace node 2                                                               |
|--------------------------------|----------------------------------------------|-----------------------------------------------------|-------------|---------|--------------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| edge (gene-gene)               | [STRING](https://string-db.org/)             | CC BY                                               | No	        | Yes     | [ENSEMBL*](https://registry.identifiers.org/registry/ensembl)                  | [ENSEMBL*](https://registry.identifiers.org/registry/ensembl)                  |
| edge (gene-go)                 | [GO](http://geneontology.org/)               | CC BY                                               | No	        | Yes     | [ENSEMBL*](https://registry.identifiers.org/registry/ensembl)                  | [ENSEMBL*](https://registry.identifiers.org/registry/ensembl)                  |
| edge (gene-disease)            | [DisGeNet](https://www.disgenet.org/)        | CC BY-NC-CA                                         | No	        | Yes     | [UNIPROT](https://registry.identifiers.org/registry/uniprot)                   | [GO](https://registry.identifiers.org/registry/go)                             |
| edge (gene-phenotype)          | [HPO](https://hpo.jax.org/app/)              | Custom: [HPO](https://hpo.jax.org/app/license)      | No	        | No      | [NCBIGENE](https://registry.identifiers.org/registry/ncbigene)                 | [UMLS](https://registry.identifiers.org/registry/umls)                         |
| edge (gene-anatomy)            | [Bgee](https://bgee.org/)                    | CC 0                                                | Yes	        | Yes     | [NCBIGENE](https://registry.identifiers.org/registry/ncbigene)                 | [HP](https://registry.identifiers.org/registry/hp)                             |
| edge (gene-drug)               | [STITCH](http://stitch.embl.de/)             | CC BY                                               | No	        | Yes     | [ENSEMBL](https://registry.identifiers.org/registry/ensembl)                   | [UBERON](https://registry.identifiers.org/registry/uberon), [CL](https://registry.identifiers.org/registry/cl)                                      |
| edge (gene-pathway)            | [CTD](http://ctdbase.org/)                   | Custom: [CTD](http://ctdbase.org/about/legal.jsp)   | No	        | No      | [ENSEMBL*](https://registry.identifiers.org/registry/ensembl)                  | [PUBCHEM.COMPOUND](https://registry.identifiers.org/registry/pubchem.compound) |
| edge (disease-phenotype)       | [HPO](https://hpo.jax.org/app/)              | Custom: [HPO](https://hpo.jax.org/app/license)      | No	        | No      | [PUBCHEM.COMPOUND](https://registry.identifiers.org/registry/pubchem.compound) | [ENSEMBL*](https://registry.identifiers.org/registry/ensembl)                  |
| edge (disease-drug)            | [DrugCentral](http://drugcentral.org/)       | CC BY-SA                                            | Yes	        | No      | [NCBIGENE](https://registry.identifiers.org/registry/ncbigene)                 | [KEGG](https://registry.identifiers.org/registry/kegg), [REACTOME](https://registry.identifiers.org/registry/reactome)                              |
| edge (drug-phenotype)          | [SIDER](http://sideeffects.embl.de/)         | CC BY-NC-CA                                         | No	        | No      | [PUBMED](https://registry.identifiers.org/registry/pubmed), [MIM](https://registry.identifiers.org/registry/mim), DECIPHER  | [HP](https://registry.identifiers.org/registry/hp)                                                     |
| ontology (genes)               | [GO](http://geneontology.org/)               | CC BY                                               | 	          |         | [UMLS](https://registry.identifiers.org/registry/umls)                         | [PUBCHEM.COMPOUND](https://registry.identifiers.org/registry/pubchem.compound) |
| ontology (diseases)            | [DO](http://disease-ontology.org/)           | CC 0                                                | 	          |         | [PUBCHEM.COMPOUND](https://registry.identifiers.org/registry/pubchem.compound) | [UMLS](https://registry.identifiers.org/registry/umls)                         |
| ontology (phenotype)           | [HPO](https://hpo.jax.org/app/)              | Custom: [HPO](https://hpo.jax.org/app/license)      | 	          |         | [GO](https://registry.identifiers.org/registry/go)                             | [GO](https://registry.identifiers.org/registry/go)                             |
| ontology (anatomy)             | [UBERON](http://uberon.github.io/about.html) | CC BY                                               |   	        |         | [DOID](https://registry.identifiers.org/registry/doid), [UMLS](https://registry.identifiers.org/registry/umls), [PUBMED](https://registry.identifiers.org/registry/pubmed) | [DOID](https://registry.identifiers.org/registry/doid) |
| mapping (UMLS-DO)              | [DisGeNet](https://www.disgenet.org/)        | CC BY-NC-CA                                         |   	        |         | [HP](https://registry.identifiers.org/registry/hp)                             | [HP](https://registry.identifiers.org/registry/hp), [UMLS](https://registry.identifiers.org/registry/umls)                                         |
| mapping (STRING-NCBI)          | [STRING](https://string-db.org/)             | CC BY                                               |   	        |         | [UBERON](https://registry.identifiers.org/registry/uberon), [CL](https://registry.identifiers.org/registry/cl)  | [UBERON](https://registry.identifiers.org/registry/uberon), [CL](https://registry.identifiers.org/registry/cl)    |
| mapping (ENSEMBL/UNIPROT-NCBI) | [UniProt](https://www.uniprot.org/)          | CC BY                                               |   	        |         | [UMLS](https://registry.identifiers.org/registry/umls)                         | [DOID](https://registry.identifiers.org/registry/doid)                         |
| id (genes)                     | [NCBI](https://www.ncbi.nlm.nih.gov/gene)    | Public Domain                                       |   	        |         | [ENSEMBL*](https://registry.identifiers.org/registry/ensembl)                  | [NCBIGENE](https://registry.identifiers.org/registry/ncbigene)                 |
| id (go)                        | [GO](http://geneontology.org/)               | CC BY                                               |   	        |         | [ENSEMBL](https://registry.identifiers.org/registry/ensembl), [UNIPROT](https://registry.identifiers.org/registry/uniprot) | [NCBIGENE](https://registry.identifiers.org/registry/ncbigene)                                         |
| id (anatomy)                   | [UBERON](http://uberon.github.io/about.html) | CC BY                                               |   	        |         |
| id (disease)                   | [DO](http://disease-ontology.org/)           | CC 0                                                |   	        |         |
| id (drug)                      | [PubChem](https://pubchem.ncbi.nlm.nih.gov/) | Public Domain                                       |   	        |         |
| id (phenotype)                 | [HPO](https://hpo.jax.org/app/)              | Custom: [HPO](https://hpo.jax.org/app/license)      |   	        |         |
| id (pathway)                   | [REACTOME](https://reactome.org/)            | CC BY                                               |   	        |         |
| id (pathway)                   | [KEGG](https://www.genome.jp/kegg/)          | Custom: [KEGG](https://www.kegg.jp/kegg/legal.html) |   	        |         |

*(True neg.: whether the data contains true negative relations; Score: whether the data contains evidence quality scores for filtering relations)*
 <sub>* String IDs are a combination of NCBI taxonomy Id and ENSEMBL joined by a dot. In the resulting graph the NCBI taxonomy Id is stripped (is always 9606 for Homo Sapiens).</sub>

The OpenBioLink benchmark files integrate data or identifiers from these sources. The provenance of data items is captured in the benchmark files, and licensing terms of source databases apply to these data items. Please mind these licensing terms when utilizing or redistributing the benchmark files or derivatives thereof.

All original data in the benchmark files created by the OpenBioLink project (not covered by the licenses of external data sources)  are released as [CC 0](https://creativecommons.org/publicdomain/zero/1.0/). 

We offer the benchmark files as-is and make no representations or warranties of any kind concerning the benchmark files, express, implied, statutory or otherwise, including without limitation warranties of title, merchantability, fitness for a particular purpose, non infringement, or the absence of latent or other defects, accuracy, or the present or absence of errors, whether or not discoverable, all to the greatest extent permissible under applicable law.

All nodes in the graph are CURIES, meaning entities can be easily looked up online by concatenating https://identifiers.org/ with the ID of the entity, f.e.:

|CURIE|Identifiers.org|
|--|--|
|GO:0006915|https://identifiers.org/GO:0006915|
|REACTOME:R-HSA-201451|https://identifiers.org/REACTOME:R-HSA-201451|

Detailed information of how the Identifiers are resolved can be found here https://registry.identifiers.org/
We are aware of an issue where entities of the Human Phenotype Ontology are not resolved correctly [(Issue)](https://github.com/identifiers-org/identifiers-org.github.io/issues/81). There is a workaround of this problem by using the ols resource, f.e. https://identifiers.org/ols/HP:0000118

