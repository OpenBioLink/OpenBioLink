# OpenBioLink

OpenBioLink is a resource and evaluation framework for evaluating link prediction models on heterogeneous biomedical graph data. It contains benchmark datasets as well as the underlying scrips to create them and to evaluate a costume model on them.

[Paper preprint on arXiv](https://arxiv.org/abs/1912.04616)

[Supplementary data](https://github.com/OpenBioLink/OpenBioLink/raw/master/paper/supplementary%20data.pdf)

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


To also be able to analyze the effect of the data quality as well as the directionality of the 
evaluation graph other settings of OpenBioLink2020 are provided, in directed and undirected setting,
with and without quality cutoff.

* [OpenBioLink2020: directed, high quality](https://samwald.info/res/OpenBioLink_2020/HQ_DIR.zip) (default dataset)
* [OpenBioLink2020: undirected, high quality](https://samwald.info/res/OpenBioLink_2020/HQ_UNDIR.zip)
* [OpenBioLink2020: directed, no quality cutoff](https://samwald.info/res/OpenBioLink_2020/ALL_DIR.zip)
* [OpenBioLink2020: undirected, no quality cutoff](https://samwald.info/res/OpenBioLink_2020/ALL_UNDIR.zip)

 
## Manual

The OpenBioLink framework consists of three parts, called actions
 1) graph creation
 2) train-test split creation
 3) training and evaluation

With the graph creation and the train-test set action, costumed data sets can be created to suit individual needs.
The last action serves as interface to train and evaluate link prediction models.

#### Calling via GUI
By calling the program without any parameters, the gui is started, 
providing a handy interface to define parameters needed. In the last step, 
the corresponding command line options are displayed.

#### Calling via command line
From folder src
```python -m openbiolink.openBioLink -p WORKING_DIR_PATH [-action] [--options] ...```

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
    --out_format [Format] [Sep]       Format of graph output, takes 2 arguments: list of file formats 
                                      [s= single file, m=multiple files] and list of separators 
                                      (e.g. t=tab, n=newline, or any other character) (default= s t)
    --no_qscore     The output files will contain no scores
    --dbs [Cls]     custom source databases selection to be used, full class name, options --> see doc
    --mes [Cls]     custom meta edges selection to be used, full class name, options --> see doc
````
**Action: Train- Test Split Generation**
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

