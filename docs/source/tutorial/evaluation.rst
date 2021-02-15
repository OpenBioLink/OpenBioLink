Evaluation
==========
To evaluate a trained model on a OpenBioLink dataset a subclass of :class:`~openbiolink.evaluation.evaluation.Evaluator` has to be created that implements the :meth:`~openbiolink.evaluation.evaluation.Evaluator.score_batch` function and initializes the Evaluator.

Initializing
------------

The :class:`~openbiolink.evaluation.evaluation.Evaluator` class uses an instantiation of :class:`~openbiolink.evaluation.dataLoader.DataLoader`, which is used to download the specified version of the OpenBioLink dataset. Furthermore it maps the string labels of entities and relations to integer identifiers, either by passing the paths to dictionary files or, if no such files are provided, by creating a mapping from scratch.

Implementing :meth:`~openbiolink.evaluation.evaluation.Evaluator.score_batch`
-----------------------------------------------------------------------------

The function :meth:`~openbiolink.evaluation.evaluation.Evaluator.score_batch` is used by :class:`~openbiolink.evaluation.evaluation.Evaluator` to retrieve the scores of a set of test triples. It gets called with a tensor containing the batch test triples and should return a tuple :code:`(pos_score_head, neg_score_head, pos_score_tail, neg_score_tail)`.

:code:`pos_score_head` and :code:`pos_score_tail` should contain the positive scores for the head and tail of all triples in the batch respectively. Therefore both tensors should be of size (batch_size,) where :code:`pos_score_head[i]` should be the score for predicting the head of triple :code:`batch[i,:]` and :code:`pos_score_tail[i]` should be the score for predicting the tail of triple :code:`batch[i,:]` (Note: In many embedding models :code:`pos_score_head == pos_score_tail`).

:code:`neg_score_head` and :code:`neg_score_tail` should contain the scores of for corrupted triples of triples in the batch. OpenBioLink is evaluated by corrupting the head/tail of a triple with all possible entities in the dataset. Consider $\mathcal{K} = (\mathcal{E},\mathcal{R},\mathcal{T})$ where $\mathcal{E}$ is the set of unique entities, $\mathcal{R}$ is the set of unique relations, and $\mathcal{T}$ are the triples in the dataset. Then the corrupted tail triples for a positive triple $(h, r, t)$ are $(h, r, e)$ for $e \in \mathcal{E}$ and the corrupted head triples are $(e, r, t)$ for $e \in \mathcal{E}$. A 1-d tensor containing all possible entities can be retrieved from :code:`self.entities` on the Evaluator. The length of this tensor is also stored in :code:`self.num_neg`. The shape of the tensors :code:`neg_score_head` and :code:`neg_score_tail` therefore should be (batch_size, num_neg), where :code:`neg_score_head[i,j]` is the score of the triple :code:`batch[i]` which head got corrupted with the entity j.

The following two examples show how to evaluate a model trained with `DGL-KE <https://github.com/awslabs/dgl-ke>`__ and a rule-based approach called `SAFRAN <https://github.com/OpenBioLink/SAFRAN>`__.

Calling :meth:`~openbiolink.evaluation.evaluation.Evaluator.evaluate`
---------------------------------------------------------------------

After the creation of a custom class that implements :class:`~openbiolink.evaluation.evaluation.Evaluator`, your approach can be evaluated by calling :meth:`~openbiolink.evaluation.evaluation.Evaluator.evaluate` with the desired batch_size and the amount of processors to use for evaluation.

The attribute :code:`filtering` should only be set to false, if you are evaluating a filtered top-k file (see example SAFRAN)

Example DGL-KE
---------------

.. code-block:: python

   """
       Import dependencies, such as the DGL-KE ScoreInfer class and the OpenBioLink DataLoader and Evaluator."""
   import torch
   import os
   import numpy as np
   
   from openbiolink.evaluation.dataLoader import DataLoader
   from openbiolink.evaluation.evaluation import Evaluator
   
   from dglke.models.infer import ScoreInfer
   from dglke.utils import load_model_config
   
   """As we do not create a DGLGraph Object, DGL-KE needs an auxilary class that stores the embeddings of the positive edges"""
   class FakeEdge(object):
       def __init__(self, head_emb, rel_emb, tail_emb):
           self._hobj = {}
           self._robj = {}
           self._tobj = {}
           self._hobj['emb'] = head_emb
           self._robj['emb'] = rel_emb
           self._tobj['emb'] = tail_emb
   
       @property
       def src(self):
           return self._hobj
   
       @property
       def dst(self):
           return self._tobj
   
       @property
       def data(self):
           return self._robj
   
   
   class DglkeEvaluator(Evaluator):
   
       def __init__(self, dataset_name, model_path, entity_to_id_path, relation_to_id_path):
           dl = DataLoader(dataset_name, entity_to_id_path=entity_to_id_path, relation_to_id_path=relation_to_id_path)
           super().__init__(dl)
           
           config = load_model_config(os.path.join(model_path, 'config.json'))
           model = ScoreInfer(-1, config, model_path)
           model.load_model()
           self.model = model.model
   
           self.entity_emb = self.model.entity_emb(self.entities.long())
           self.entity_emb.share_memory_()
           self.relation_emb = self.model.relation_emb(self.relations.long())
           self.relation_emb.share_memory_()
   
       def score_batch(self, batch):
           head_neg_score = self.model.score_func.create_neg(True)
           tail_neg_score = self.model.score_func.create_neg(False)
           head_neg_prepare = self.model.score_func.create_neg_prepare(True)
           tail_neg_prepare = self.model.score_func.create_neg_prepare(False)
   
           pos_head_emb = self.entity_emb[batch[:, 0], :]
           pos_tail_emb = self.entity_emb[batch[:, 2], :]
           pos_rel = batch[:, 1].long()
           pos_rel_emb = self.model.relation_emb(pos_rel)
   
           edata = FakeEdge(pos_head_emb, pos_rel_emb, pos_tail_emb)
           pos_score = self.model.score_func.edge_func(edata)['score']
   
           neg_head, tail = head_neg_prepare(pos_rel, 1, self.entity_emb, pos_tail_emb, -1, False)
           neg_scores_head = head_neg_score(neg_head, pos_rel_emb, tail,
                                            1, len(batch), self.num_neg)
   
           head, neg_tail = tail_neg_prepare(pos_rel, 1, pos_head_emb, self.entity_emb, -1, False)
           neg_scores_tail = tail_neg_score(head, pos_rel_emb, neg_tail,
                                            1, len(batch), self.num_neg)
   
           return pos_score, neg_scores_head.squeeze(0), pos_score, neg_scores_tail.squeeze(0)
   
   
   if __name__ == "__main__":
       torch.manual_seed(145)
       np.random.seed(145)
   
       model_path = r"G:\ckpts\TransE_l2_FB15k_0"
       entity_to_id_path = r"G:\triples\entities.tsv"
       relation_to_id_path = r"G:\triples\relations.tsv"
   
       evaluator = DglkeEvaluator("HQ_DIR", model_path, entity_to_id_path, relation_to_id_path)
       result = evaluator.evaluate(100, -1)
       print(result)

Example SAFRAN
---------------

SAFRAN is a rule-based approach, that creates a filtered top-k text file in the form of 

.. code-block:: text

   DOID:14320 DIS_DRUG PUBCHEM.COMPOUND:122282
   Heads: DOID:14320	0.9824	DOID:4964	0.9713	DOID:594	0.7095	DOID:10763	0.6424	DOID:8986	0.6423	DOID:1596	0.5923	DOID:10825	0.4874	DOID:1825	0.3771	DOID:750	0.3608	DOID:1470	0.3416	
   Tails: PUBCHEM.COMPOUND:10240	0.6357	PUBCHEM.COMPOUND:122282	0.5567	PUBCHEM.COMPOUND:4585	0.4798	PUBCHEM.COMPOUND:2160	0.4310	PUBCHEM.COMPOUND:3696	0.3965	PUBCHEM.COMPOUND:2726	0.2493	PUBCHEM.COMPOUND:3559	0.2251	PUBCHEM.COMPOUND:2995	0.2008	PUBCHEM.COMPOUND:2520	0.0172	PUBCHEM.COMPOUND:3386	0.0142	
   DOID:14320 DIS_DRUG PUBCHEM.COMPOUND:2771
   Heads: DOID:10933	0.9822	DOID:594	0.9551	DOID:14320	0.8485	DOID:11257	0.7170	DOID:2055	0.4382	DOID:2030	0.4334	DOID:0060891	0.3585	DOID:0060895	0.2242	DOID:9970	0.1990	DOID:0060896	0.0977	
   Tails: PUBCHEM.COMPOUND:10240	0.8967	PUBCHEM.COMPOUND:4585	0.7613	PUBCHEM.COMPOUND:2160	0.7521	PUBCHEM.COMPOUND:3696	0.7000	PUBCHEM.COMPOUND:2726	0.6095	PUBCHEM.COMPOUND:3559	0.5914	PUBCHEM.COMPOUND:2995	0.4491	PUBCHEM.COMPOUND:2520	0.4050	PUBCHEM.COMPOUND:3386	0.3957	PUBCHEM.COMPOUND:5002	0.1693	
   DOID:14320 DIS_DRUG PUBCHEM.COMPOUND:2712
   Heads: DOID:240	0.8082	DOID:13603	0.7477	DOID:12030	0.7133	DOID:4353	0.7011	DOID:2089	0.6067	DOID:13141	0.5286	DOID:9741	0.3540	DOID:10808	0.3119	DOID:14320	0.2678	DOID:4964	0.0284	
   Tails: PUBCHEM.COMPOUND:2712	0.9847	PUBCHEM.COMPOUND:10240	0.7101	PUBCHEM.COMPOUND:4585	0.6751	PUBCHEM.COMPOUND:2160	0.6031	PUBCHEM.COMPOUND:3696	0.5430

To evaluate such a filtered top-k file, a custom class is needed that reads the file on initialization and implements the :meth:`~openbiolink.evaluation.evaluation.Evaluator.score_batch` function of the Evaluator. As the file contains filtered top-k predictions, the prediction of all negative entities and the filtering can be omitted.

.. code-block:: python

   import torch
   from openbiolink.evaluation.dataLoader import DataLoader
   from openbiolink.evaluation.evaluation import Evaluator
   
   
   class SafranEvaluator(Evaluator):
   
       def __init__(self, dataset_name, evaluation_file_path):
           dl = DataLoader(dataset_name)
           super().__init__(dl)
   
           with open(evaluation_file_path) as infile:
               content = infile.readlines()
           content = [x.strip() for x in content]
   
           self.predictions = dict()
   
           for i in range(0, len(content), 3):
               head, rel, tail = content[i].split(" ")
   
               head = self.dl.entity_to_id[head]
               rel = self.dl.relation_to_id[rel]
               tail = self.dl.entity_to_id[tail]
   
               pos_head = 0.0
               neg_head = []
               head_predictions = content[i+1]
               if(head_predictions == "Heads:"):
                   continue
               else:
                   head_predictions = head_predictions[len("Heads: "):].split("\t")
                   for j in range(0, len(head_predictions), 2):
                       head_prediction = self.dl.entity_to_id[head_predictions[j]]
                       confidence = float(head_predictions[j+1])
                       if head == head_prediction:
                           # Correct prediction
                           pos_head = confidence
                       else:
                           # False prediction
                           neg_head.append((head_prediction, confidence))
   
               pos_tail = 0.0
               neg_tail = []
               tail_predictions = content[i+2]
               if tail_predictions == "Tails:":
                   continue
               else:
                   tail_predictions = tail_predictions[len("Tails: "):].split("\t")
                   for j in range(0, len(tail_predictions), 2):
                       tail_prediction = self.dl.entity_to_id[tail_predictions[j]]
                       confidence = float(tail_predictions[j+1])
                       if tail == tail_prediction:
                           # Correct prediction
                           pos_tail = confidence
                       else:
                           # False prediction
                           neg_tail.append((tail_prediction, confidence))
               self.predictions[f"{str(head)};{str(rel)};{str(tail)}"] = (pos_head, neg_head, pos_tail, neg_tail)
   
   
   
       def score_batch(self, batch):
           pos_score_head = torch.zeros((len(batch),), dtype=torch.float)
           neg_score_head = torch.zeros((100, self.num_neg), dtype=torch.float)
           pos_score_tail = torch.zeros((len(batch),), dtype=torch.float)
           neg_score_tail = torch.zeros((100, self.num_neg), dtype=torch.float)
   
           for i in range(batch.shape[0]):
               head, rel, tail = batch[i,:]
               key = f"{str(head.item())};{str(rel.item())};{str(tail.item())}"
   
               if key in self.predictions:
                   (pos_head, neg_heads, pos_tail, neg_tails) = self.predictions[key]
                   pos_score_head[i] = pos_head
                   for neg_head, confidence in neg_heads:
                       neg_score_head[i, neg_head] = confidence
   
                   pos_score_tail[i] = pos_tail
                   for neg_tail, confidence in neg_tails:
                       neg_score_tail[i, neg_tail] = confidence
               else:
                   pass
   
   
           return pos_score_head, neg_score_head, pos_score_tail, neg_score_tail
   
   
   if __name__ == "__main__":
   
       evaluation_file_path = r"G:\prediction.txt"
   
       evaluator = SafranEvaluator("HQ_DIR", evaluation_file_path)
       result = evaluator.evaluate(100, 1, filtering=False)
       print(result)
