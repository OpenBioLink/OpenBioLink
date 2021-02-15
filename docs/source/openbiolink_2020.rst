OpenBioLink2020
=================

The `OpenBioLink2020 Dataset <https://zenodo.org/record/3834052/files/HQ_DIR.zip?download=1>`_ is a highly challenging benchmark dataset containing over 5 million positive and negative edges. The test set does not contain trivially predictable, inverse edges from the training set and does contain all different edge types, to provide a more realistic edge prediction scenario.

`OpenBioLink2020: directed, high quality <https://zenodo.org/record/3834052/files/HQ_DIR.zip?download=1>`_ is the default dataset that should be used for benchmarking purposes. To allow anayzing the effect of data quality as well as the directionality of the evaluation graph, four variants of OpenBioLink2020 are provided -- in directed and undirected setting, with and without quality cutoff. 

Additionally, each graph is available in `RDF N3 <https://en.wikipedia.org/wiki/Notation3>`_ format (without train-validation-test splits). 

Download
--------

All datasets are hosted on `zenodo <https://zenodo.org/record/3834052>`_.

*   `OpenBioLink2020: directed, high quality <https://zenodo.org/record/3834052files/HQ_DIR.zip?download=1>`_ // `RDF <https://zenodo.org/record/3834052/files/RDF_HQ_DIR.zip>`_ (default dataset for benchmarking)
*   `OpenBioLink2020: undirected, high quality <https://zenodo.org/record/3834052files/HQ_UNDIR.zip?download=1>`_ // `RDF <https://zenodo.org/record/3834052/files/RDF_HQ_UNDIR.zip>`_
*   `OpenBioLink2020: directed, no quality cutoff <https://zenodo.org/record/3834052files/ALL_DIR.zip?download=1>`_ // `RDF <https://zenodo.org/record/3834052/files/RDF_ALL_DIR.zip>`_
*   `OpenBioLink2020: undirected, no quality cutoff <https://zenodo.org/record/3834052files/ALL_UNDIR.zip?download=1>`_ // `RDF <https://zenodo.org/record/3834052/files/RDF_ALL_UNDIR.zip>`_

Leaderboard
-----------

+---------------------+-------------+------------+------------------------------------------------------------------+------------------------------------------------------------------------------------------------+
| Model               | Hits @ 10   | Hits @ 1   | Paper                                                            | Code                                                                                           |
+=====================+=============+============+==================================================================+================================================================================================+
| TransE (Baseline)   | 0.0749      | 0.0125     | `Paper preprint on arXiv <https://arxiv.org/abs/1912.04616>`__   | `Code <https://github.com/OpenBioLink/OpenBioLink/tree/master/src/openBioLink/evaluation>`__   |
+---------------------+-------------+------------+------------------------------------------------------------------+------------------------------------------------------------------------------------------------+
| TransR (Baseline)   | 0.0639      | 0.0096     | `Paper preprint on arXiv <https://arxiv.org/abs/1912.04616>`__   | `Code <https://github.com/OpenBioLink/OpenBioLink/tree/master/src/openBioLink/evaluation>`__   |
+---------------------+-------------+------------+------------------------------------------------------------------+------------------------------------------------------------------------------------------------+
| RotatE              | 0.522       | 0.156      |                                                                  | `Code <https://github.com/awslabs/dgl-ke>`__                                                   |
+---------------------+-------------+------------+------------------------------------------------------------------+------------------------------------------------------------------------------------------------+
| ComplEx             | 0.525       | 0.166      |                                                                  | `Code <https://github.com/awslabs/dgl-ke>`__                                                   |
+---------------------+-------------+------------+------------------------------------------------------------------+------------------------------------------------------------------------------------------------+
| DistMult            | 0.534       | 0.184      |                                                                  | `Code <https://github.com/awslabs/dgl-ke>`__                                                   |
+---------------------+-------------+------------+------------------------------------------------------------------+------------------------------------------------------------------------------------------------+
| TransR              | 0.592       | 0.369      |                                                                  | `Code <https://github.com/awslabs/dgl-ke>`__                                                   |
+---------------------+-------------+------------+------------------------------------------------------------------+------------------------------------------------------------------------------------------------+
| RESCAL              | 0.615       | 0.407      |                                                                  | `Code <https://github.com/awslabs/dgl-ke>`__                                                   |
+---------------------+-------------+------------+------------------------------------------------------------------+------------------------------------------------------------------------------------------------+

If you want to see your results added to the Leaderboard please create a new issue.

Summary
-------

+---------------------------------+--------------+-------------+-------------+------------+-------------+
| Dataset                         | Train        | Test        | Valid       | Entities   | Relations   |
+=================================+==============+=============+=============+============+=============+
| directed, high quality          | 8.503.580    | 401.901     | 397.066     | 184.732    | 28          |
+---------------------------------+--------------+-------------+-------------+------------+-------------+
| undirected, high quality        | 7.559.921    | 372.877     | 357.297     | 184.722    | 28          |
+---------------------------------+--------------+-------------+-------------+------------+-------------+
| directed, no quality cutoff     | 51.636.927   | 2.079.139   | 2.474.921   | 486.998    | 32          |
+---------------------------------+--------------+-------------+-------------+------------+-------------+
| undirected, no quality cutoff   | 41.383.093   | 2.010.662   | 1.932.436   | 486.998    | 32          |
+---------------------------------+--------------+-------------+-------------+------------+-------------+

