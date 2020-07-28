Planner
========================
Observes the situation for possible new predictions and based on them chooses whether the drift is actually valid. If it's a real drift, 
it should be sent to the Executor. A custom Predictor can be done for that too, like a voting one or a more 
time-consuming algorithm from `Scikit-Learn <https://scikit-learn.org/stable/>`_, 
`TensorFlow <https://www.tensorflow.org/>`_, `PyTorch <https://pytorch.org/>`_, or others.

Planner Predictor
------------------

.. automodule:: driftage.planner.predictor
   :members:
   :undoc-members:
