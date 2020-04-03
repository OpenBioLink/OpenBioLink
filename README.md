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
 
[OpenBioLink2020: directed, high quality](https://samwald.info/res/OpenBioLink_2020_final/HQ_DIR.zip) is the default dataset that should be used for benchmarking purposes. To allow anayzing the effect of data quality as well as the directionality of the 
evaluation graph, four variants of OpenBioLink2020 are provided -- in directed and undirected setting,
with and without quality cutoff. 

Additionally, each graph is available in [RDF N3](https://en.wikipedia.org/wiki/Notation3) format (without train-validation-test splits). 

### OpenBioLink 2020 datasets

* __[OpenBioLink2020: directed, high quality](https://samwald.info/res/OpenBioLink_2020_final/HQ_DIR.zip) // [RDF](https://samwald.info/res/OpenBioLink_2020_final/RDF_HQ_DIR.zip) (default dataset for benchmarking)__
* [OpenBioLink2020: undirected, high quality](https://samwald.info/res/OpenBioLink_2020_final/HQ_UNDIR.zip) // [RDF](https://samwald.info/res/OpenBioLink_2020_final/RDF_HQ_UNDIR.zip)
* [OpenBioLink2020: directed, no quality cutoff](https://samwald.info/res/OpenBioLink_2020_final/ALL_DIR.zip) // [RDF](https://samwald.info/res/OpenBioLink_2020_final/RDF_ALL_DIR.zip)
* [OpenBioLink2020: undirected, no quality cutoff](https://samwald.info/res/OpenBioLink_2020_final/ALL_UNDIR.zip) // [RDF](https://samwald.info/res/OpenBioLink_2020_final/RDF_ALL_UNDIR.zip)

<details>
  <summary>Previous versions of the Benchmark (click to expand)</summary>
    
### OpenBioLink 2020 alpha-release
    
* [OpenBioLink2020: directed, high quality](https://samwald.info/res/OpenBioLink_2020/HQ_DIR.zip) (default dataset)
* [OpenBioLink2020: undirected, high quality](https://samwald.info/res/OpenBioLink_2020/HQ_UNDIR.zip)
* [OpenBioLink2020: directed, no quality cutoff](https://samwald.info/res/OpenBioLink_2020/ALL_DIR.zip)
* [OpenBioLink2020: undirected, no quality cutoff](https://samwald.info/res/OpenBioLink_2020/ALL_UNDIR.zip)
</details>

Please note that the OpenBioLink benchmark files contain data derived from external ressources. Licensing terms of these external resources are detailed [below](#Source-databases-and-their-licenses). 

 ## OpenBioLink 2020 Leaderboard    
 
 | model | hits@10 | hits@1 |  paper | code |
|-------|---------|--------|-------|------|
|   TransE (Baseline)   |    0.0749     |   0.0125     | [Paper preprint on arXiv](https://arxiv.org/abs/1912.04616)      | [Code](https://github.com/OpenBioLink/OpenBioLink/tree/master/src/openBioLink/evaluation)     |
|   TransR (Baseline)   |    0.0639     |   0.0096     | [Paper preprint on arXiv](https://arxiv.org/abs/1912.04616)      | [Code](https://github.com/OpenBioLink/OpenBioLink/tree/master/src/openBioLink/evaluation)     |

Please contact us if you want to see your results added to the Leaderboard.
 
## Manual

The OpenBioLink framework consists of three parts, called 'actions':
 1) graph creation
 2) train-test split creation
 3) training and evaluation

With the graph creation and the train-test set action, customized datasets can be created to suit individual needs.
The third action serves as an interface for training and evaluating link prediction models.

For HOW-TO's please check also the [wiki](https://github.com/OpenBioLink/OpenBioLink/wiki/Table-of-Contents)

#### Calling via GUI
By calling the program without any parameters, the GUI is started, 
providing an interface to define required parameters. In the last step, 
the corresponding command line options are displayed.

#### Calling via command line
From folder src
```sh
openbiolink -p WORKING_DIR_PATH [-action] [--options] ...
```

**Action: Graph Creation**

To generate the default graph (with all edges of all qualifies) in the current directory, use:

```sh
openbiolink generate
```

For a list of arguments, use:

```sh
openbiolink generate --help
```

**Action: Train-Test Split Generation**

To split the default graph using the random scheme, use:

```sh
openbiolink split rand --edges graph_files/edges.csv --tn-edges graph_files/TN_edges.csv --nodes graph_files/nodes.csv
```

For a list of arguments, use:

```sh
openbiolink split rand --help
```

Splitting can also be done by time with 

```sh
openbiolink split time
```

More documentation will be provided later.

**Action: Training and Evaluation**

To train on the split default graph, use:

```shell script
openbiolink train -m TransE_Pykeen -t train_test_data/train_sample.csv -s train_test_data/test_sample.csv
```

For a list of arguments, use:

```sh
openbiolink train --help
```

## File description

### Graph Generation

#### TSV Writer

| Default File Name | Description | Columns |
|----------------------|--------------|-----------------|
| ALL_nodes.csv | All nodes present in the graph |Node Id, Node type|
| edges.csv | All true positive edges | Node 1 ID, Edge type, Node 2 ID, Quality score, Source |
| edges_list.csv | List of edge types present in edges.csv | Edge type |
|nodes.csv| All nodes present in edges.csv | Node ID, Node type |
|nodes_list.csv| List of node types present in nodes.csv | Node type |
|TN_edges.csv| All true negative edges | Node 1 ID, Edge type, Node 2 ID, Quality score, Source |
|TN_edges_list.csv| List of edge types present in TN_edges.csv | Edge type |
|TN_nodes.csv| All nodes present in TN_edges.csv | Node ID, Node type |
|TN_nodes_list.csv| List of node types present in TN_nodes.csv | Node type |
|ids_no_mapping.tsv| ID's of nodes that could not be mapped to other ontology systems | Node ID, Node type |
|tn_ids_no_mapping.tsv| ID's of nodes that could not be mapped to other ontology systems | Node ID, Node type 
|stats.txt| Statistics about edges.csv and nodes.csv | (See column headers of file) |
|tn_stats.txt| Statistics about TN_edges.csv and TN_nodes.csv | (See column headers of file) |

#### Biological Expression Language (BEL) Writer

The Biological Expression Language (BEL) is a domain specific language that enables the expression of
biological relationships in a machine-readable format. It is supported by the [PyBEL](https://github.com/pybel/pybel)
software ecosystem.

| Default File Name | Description             |
|-------------------|-------------------------|
| positive.bel.gz   | All true positive edges in [BEL Script](https://language.bel.bio/language/structure/) format (gzipped) for usage in PyBEL or other BEL-aware applications) |   
| positive.bel.nodelink.json.gz | All true positive edges in [Nodelink JSON](https://pybel.readthedocs.io/en/latest/reference/io.html#pybel.from_nodelink_gz) format (gzipped) for direct usage with [PyBEL](https://pybel.readthedocs.io) |   
| negative.bel.gz   | All true negative edges in BEL Script format (gzipped) |
| negative.bel.nodelink.json.gz | All true negative edges in Nodelink JSON format (gzipped) |

Example opening BEL Script using [`pybel.from_bel_script()`](https://pybel.readthedocs.io/en/latest/reference/io.html#pybel.from_bel_script):

```python
import gzip
from pybel import from_bel_script
with gzip.open('positive.bel.gz') as file:
    graph = from_bel_script(file)
```

Example opening Nodelink JSON using [`pybel.from_nodelink_gz()`](https://pybel.readthedocs.io/en/latest/reference/io.html#pybel.from_nodelink_gz):

```python
from pybel import from_nodelink_gz
graph = from_nodelink_gz('positive.bel.nodelink.json.gz')
```

### Train-test split creation

| Default file name | Description | Column descriptions |
|----------------------|--------------|-----------------|
| train_sample.csv| All samples from the training set | Node 1 ID, Edge type, Node 2 ID, Quality score, TP/TN, Source |
| test_sample.csv| All samples from the test set | Node 1 ID, Edge type, Node 2 ID, Quality score, TP/TN, Source |
| val_sample.csv| All samples from the validation set | Node 1 ID, Edge type, Node 2 ID, Quality score, TP/TN, Source |
| train_val_nodes.csv | All nodes present in the training and validation set combined | Node ID, Node type |
| test_nodes.csv | All nodes present in the test set | Node ID, Node typ |
| removed_test_nodes.csv | All nodes which got removed from the test set, due to not being present in the trainingset | Node ID |
| removed_val_nodes.csv | All nodes which got removed from the validation set, due to not being present in the trainingset | Node ID |

### CURIE's

All node ID's in the graph are CURIES, meaning entities can be easily looked up online by concatenating https://identifiers.org/ with the ID, f.e.:

|CURIE|Identifiers.org|
|--|--|
|GO:0006915|https://identifiers.org/GO:0006915|
|REACTOME:R-HSA-201451|https://identifiers.org/REACTOME:R-HSA-201451|

Detailed information of how the Identifiers are resolved can be found here https://registry.identifiers.org/



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
 
 # True Negative edges
As randomly sampled negative edges can produce noise or trivial examples, true negative edges (i.e., relationships that were explicitly mentioned to not exist) were used wherever possible. 
Specifically, for disease_drug and disease_phenotype edges, true negative examples were extracted from the data source directly, as they were explicitly stated. For gene-anatomy relationships, over-expression and under-expression data was used as contradicting data. For other relationship-types, e.g., gene_activation_gene and drug_inhibition_gene, this indirect true negative sample creation could not be applied, as the relationship does not hold all information necessary (the same substance can have both activating and inhibiting effects, e.g. depending on dosage).

 



# Source databases and their licenses

| Source type                    | Source name                                  | License                                     | True neg.   | Score	  |
|--------------------------------|----------------------------------------------|---------------------------------------------|-------------|---------|
| edge (gene-gene)               | [STRING](https://string-db.org/)             | CC BY                                       | No	        | Yes     |
| edge (gene-go)                 | [GO](http://geneontology.org/)               | CC BY                                       | No	        | Yes     |
| edge (gene-disease)            | [DisGeNet](https://www.disgenet.org/)        | CC BY-NC-CA                                 | No	        | Yes     |
| edge (gene-phenotype)          | [HPO](https://hpo.jax.org/app/)              | Custom: [HPO](https://hpo.jax.org/app/license)      | No	        | No     |
| edge (gene-anatomy)            | [Bgee](https://bgee.org/)                    | CC 0                                        | Yes	        | Yes     |
| edge (gene-drug)               | [STITCH](http://stitch.embl.de/)             | CC BY                                       | No	        | Yes     |
| edge (gene-pathway)            | [CTD](http://ctdbase.org/)                   | Custom: [CTD](http://ctdbase.org/about/legal.jsp)   | No	        | No     |
| edge (disease-phenotype)       | [HPO](https://hpo.jax.org/app/)              | Custom: [HPO](https://hpo.jax.org/app/license)      | Yes	        | No     |
| edge (disease-drug)            | [DrugCentral](http://drugcentral.org/)       | CC BY-SA                                    | Yes	        | No     |
| edge (drug-phenotype)          | [SIDER](http://sideeffects.embl.de/)         | CC BY-NC-CA                                 | No	        | No     |
| ontology (genes)               | [GO](http://geneontology.org/)               | CC BY                                       | 	        |      |
| ontology (diseases)            | [DO](http://disease-ontology.org/)           | CC 0                                        | 	        |      |
| ontology (phenotype)           | [HPO](https://hpo.jax.org/app/)              | Custom: [HPO](https://hpo.jax.org/app/license)      | 	        |      |
| ontology (anatomy)             | [UBERON](http://uberon.github.io/about.html) | CC BY                                       |   	        |        |
| mapping (UMLS-DO)              | [DisGeNet](https://www.disgenet.org/)        | CC BY-NC-CA                                 |   	        |         |
| mapping (STRING-NCBI)          | [STRING](https://string-db.org/)             | CC BY                                       |   	        |         |
| mapping (ENSEMBL/UNIPROT-NCBI) | [UniProt](https://www.uniprot.org/)          | CC BY                                       |   	        |         |
| id (genes)                     | [NCBI](https://www.ncbi.nlm.nih.gov/gene)    | Public Domain                               |   	        |         |
| id (go)                        | [GO](http://geneontology.org/)               | CC BY                                       |   	        |         |
| id (anatomy)                   | [UBERON](http://uberon.github.io/about.html) | CC BY                                       |   	        |         |
| id (disease)                   | [DO](http://disease-ontology.org/)           | CC 0                                        |   	        |         |
| id (drug)                      | [PubChem](https://pubchem.ncbi.nlm.nih.gov/) | Public Domain                               |   	        |         |
| id (phenotype)                 | [HPO](https://hpo.jax.org/app/)              | Custom: [HPO](https://hpo.jax.org/app/license)      |   	        |         |
| id (pathway)                   | [REACTOME](https://reactome.org/)            | CC BY                                       |   	        |         |
| id (pathway)                   | [KEGG](https://www.genome.jp/kegg/)          | Custom: [KEGG](https://www.kegg.jp/kegg/legal.html) |   

*(True neg.: whether the data contains true negative relations; Score: whether the data contains evidence quality scores for filtering relations)*

The OpenBioLink benchmark files integrate data or identifiers from these sources. The provenance of data items is captured in the benchmark files, and licensing terms of source databases apply to these data items. Please mind these licensing terms when utilizing or redistributing the benchmark files or derivatives thereof.

All original data in the benchmark files created by the OpenBioLink project (not covered by the licenses of external data sources)  are released as [CC 0](https://creativecommons.org/publicdomain/zero/1.0/). 

We offer the benchmark files as-is and make no representations or warranties of any kind concerning the benchmark files, express, implied, statutory or otherwise, including without limitation warranties of title, merchantability, fitness for a particular purpose, non infringement, or the absence of latent or other defects, accuracy, or the present or absence of errors, whether or not discoverable, all to the greatest extent permissible under applicable law.

# Evaluating your own Model

Currently, models provided in pykeen can be tested in the framework. To add your own models, please perform the following steps:
1) implement the model interface ``src/openbiolink/evaluation/models/model.py`` 
1) add your model to the modeltypes ``src/openbiolink/evaluation/models/modelTypes.py``
 

