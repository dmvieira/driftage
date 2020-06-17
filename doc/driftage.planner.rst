Planner
========================
Observes for new predictions and based on them choose if the drift is really valid. If it's a real drift, 
should be send to Executor. A custom Predictor can be done for that too, like a voting one or more 
time consuming algorithms from `Scikit-Learn <https://scikit-learn.org/stable/>`_, 
`TensorFlow <https://www.tensorflow.org/>`_, `PyTorch <https://pytorch.org/>`_, or others.

Planner Predictor
------------------

.. automodule:: driftage.planner.predictor
   :members:
   :undoc-members:
