#OpenBioLink

OpenBioLink is a resource and evaluation framework for evaluating link prediction models on heterogenous biomedical graph data. It contains benchmark datasets as well as the underlying scrips to create them and to evaluate a costume model on them.

##Installation

Via pip
* Install a pytorch version suitable for your system
* ```pip install -r requirements.txt```

##Overview
The OpenBioLink framework consists of three parts (1) graph creation, (2) train-test split creation, (3) training and evaluation.

With the graph creation module and the train-test set module, costumed data sets can be created to suit individual needs. The last module serves as interface to train and evaluate link prediction models.

##Manual

By calling the program without any parameters, the gui is started, 
providing a handy interface to define parameters needed. In the last step, 
the corresponding command line options are displayed.

````python openbiolnk.py -p WorkingDirPath [-action] [--options] ...````

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

