About
=============

The amount of data and the change in behavior happens very fast in this 
interconnected world. These repeated changes and the amount of data make 
machine learning algorithms loose accuracy because they don't know about 
these new patterns. This change in the pattern of data is known as 
`Concept Drift <https://en.wikipedia.org/wiki/Concept_drift>`_ and 
there are already many approaches for treating these drifts. 
Usually these treatments are costly to implement because they require knowledge 
of drift detection algorithms, software engineering and needs maintence for new drifts. 

The propose of Driftage is build a framework using multi-agent systems to simplify 
the implementation of concept drift detectors.

:doc:`Driftage <index>` is a modular framework where:

:doc:`Monitor <driftage.monitor>`
---------------------------------
Captures data integrated to any framework you want: `Spark <https://spark.apache.org/>`_, `Flink <https://ci.apache.org/projects/flink/flink-docs-stable/>`_, or even a Python function.

:doc:`Analyser <driftage.analyser>`
-----------------------------------
Analyse data collected by Monitor using a customized Predictor for Concept Drift detection. 
Fast classifiers from `Scikit-Multiflow <https://scikit-multiflow.github.io/>`_ or 
`Facebook Prophet <https://facebook.github.io/prophet/>`_ are great projects for that.

:doc:`Planner <driftage.planner>`
---------------------------------
Observes for new predictions and based on them choose if the drift is really valid. If it's a real drift, 
should be send to Executor. A custom Predictor can be done for that too, like a voting one or more 
time consuming algorithms from `Scikit-Learn <https://scikit-learn.org/stable/>`_, 
`TensorFlow <https://www.tensorflow.org/>`_, `PyTorch <https://pytorch.org/>`_, or others.

:doc:`Executor <driftage.executor>`
-----------------------------------
Receives from Planner new Drifts and send to a custom Sink. It can be a `Apache Kafka <https://kafka.apache.org/>`_, `RabbitMQ <https://www.rabbitmq.com/>`_, API, and so on...

:doc:`Knowledge Base <driftage.kb>`
-----------------------------------
Store data collected and predicted by :doc:`driftage.analyser` can be queried by 
:doc:`driftage.analyser` for retraining or :doc:`driftage.planner` for predictions.