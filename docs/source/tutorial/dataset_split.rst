Dataset split
=============

Commands
--------

To split the default graph using the random scheme, use:

.. code-block:: sh

   openbiolink split rand --edges graph_files/edges.csv --tn-edges graph_files/TN_edges.csv --nodes graph_files/nodes.csv

For a list of arguments, use:

.. code-block:: sh

   openbiolink split rand --help

Splitting can also be done by time with 

.. code-block:: sh

   openbiolink split time


File description
----------------

.. list-table::
   :header-rows: 1

   * - Default file name
     - Description
     - Column descriptions
   * - train_sample.csv
     - All positive samples from the training set
     - Node 1 ID, Edge type, Node 2 ID, Quality score, TP/TN, Source
   * - test_sample.csv
     - All positive samples from the test set
     - Node 1 ID, Edge type, Node 2 ID, Quality score, TP/TN, Source
   * - val_sample.csv
     - All positive samples from the validation set
     - Node 1 ID, Edge type, Node 2 ID, Quality score, TP/TN, Source
   * - negative_train_sample.csv
     - All negative samples from the training set
     - Node 1 ID, Edge type, Node 2 ID, Quality score, TP/TN, Source
   * - negative_test_sample.csv
     - All negative samples from the test set
     - Node 1 ID, Edge type, Node 2 ID, Quality score, TP/TN, Source
   * - negative_val_sample.csv
     - All negative samples from the validation set
     - Node 1 ID, Edge type, Node 2 ID, Quality score, TP/TN, Source
   * - train_val_nodes.csv
     - All nodes present in the training and validation set combined
     - Node ID, Node type
   * - test_nodes.csv
     - All nodes present in the test set
     - Node ID, Node typ
   * - removed_test_nodes.csv
     - All nodes which got removed from the test set, due to not being present in the trainingset
     - Node ID
   * - removed_val_nodes.csv
     - All nodes which got removed from the validation set, due to not being present in the trainingset
     - Node ID

Random split
------------

In the random split setting, first, negative sampling is performed. Afterwards, the whole dataset (containing positive and negative examples) is split randomly according to the defined ratio. Finally, post-processing steps are performed to facilitate training and to avoid information leakage.

Time-slice split
----------------

In the time-slice split setting, for both of the provided time slices, first, negative sampling is performed. Afterwards, the first time slice (t-1 graph) is used as training sample, while the difference between the first and the second time slice serves as the test set. Finally, post-processing steps are performed to facilitate training and to avoid information leakage.

Generally, the time slice setting is trickier to implement than the random split strategy, as it requires more manual evaluation and knowledge of the data. One of the most difficult factors is the change of the source databases over time. For example, a database might change its quality score, or even its ID-format. Also, the number of relationships stored might increase sharply due to new mapping files being used. This might also result in ‘vanishing edges’, where edges that were present in the t-1 graph are no longer existent in the current graph. Although the OpenBioLink toolbox tries to assist the user with different kinds of warnings to identify such difficulties in the data, it is unfortunately not possible to automatically detect nor solve all these problems, making some manual pre- and post-processing of the data inevitable.

Post-processing
---------------

**To facilitate model application**

*   Edges that contain nodes that are not present in the training set are dropped from the test set. This facilitates use of embedding-based models that usually cannot make predictions for nodes that have not been embedded during training.

**Avoiding train-test information leakage and trivial predictions in the test set**

*   **Removal of reverse edges** If the graph is directed, reverse edges are removed from the training set. The reason for this is that if the original edge a-b was undirected, both directions a→b and a←b are materialized in the directed graph. If one of these directed edges would be present in the training set and one in the test set, the prediction would be trivial. Therefore, in these cases, the reverse edges from the training set are removed. (Note that edges are removed from the training set instead of the test set because this is advantagous for maintaining the train-test-set ratio)
*   **Removal of super-properties** Some types of edges have sub-property characteristics, meaning that relationship x indicates a generic interaction between two entities (e.g. _protein_interaction_protein_), while relationship y further describes this relationship in more detail (e.g., _protein_activation_protein_). This means that the presence of x between two nodes does not imply the existence of a relation y between those same entities, but the presence of y necessarily implies the existence of x. These kinds of relationships could cause information leakage in the datasets, therefore super-relations of relations present in the training set are removed from the test set.

