Examples
=============

An example was 
created as `a health monitor <https://github.com/dmvieira/driftage/tree/master/examples/health_monitor>`_ 
at the moment that a user is punching. The data 
`EMG Physical Action Data Set <https://archive.ics.uci.edu/ml/datasets/EMG+Physical+Action+Data+Set>`_ 
was collected from UCI Machine Learning.

There is a 
`Jupyter Notebook analysis <https://github.com/dmvieira/driftage/blob/master/examples/health_monitor/Data%20Analysis.ipynb>`_ 
that illustrates how different voltage signals are collected from the following muscles:

* R-Bic: right bicep (C1)
* R-Tri: right tricep (C2)
* L-Bic: left bicep (C3)
* L-Tri: left tricep (C4)
* R-Thi: right thigh (C5)
* R-Ham: right hamstring (C6)
* L-Thi: left thigh (C7)
* L-Ham: left hamstring (C8)

The analysis show how 
`ADWIN drift detection algorithm <https://scikit-multiflow.readthedocs.io/en/stable/api/generated/skmultiflow.drift_detection.ADWIN.html#skmultiflow.drift_detection.ADWIN>`_ 
adapts to each signal.

One example for each kind of agent was implemented:

* `Spark Monitor <https://github.com/dmvieira/driftage/tree/master/examples/health_monitor/monitor>`_: as a Monitor integrated with `Apache Spark <https://spark.apache.org/>`_ Structured Streaming to read csv punching signals from muscles.
* `ADWIN Analyser <https://github.com/dmvieira/driftage/tree/master/examples/health_monitor/analyser>`_: as an Analyser for each muscle signal using ADWIN from `Skmultiflow <https://scikit-multiflow.github.io/>`_ to detect drifts on muscle activity.
* `Voting Planner <https://github.com/dmvieira/driftage/tree/master/examples/health_monitor/planner>`_: as a Planner for voting with a threshold 3 >= X < 8. If X muscle signals are interpreted having drift in the threshold, than it alerts a drift to the Executor.
* `Csv Executor <https://github.com/dmvieira/driftage/tree/master/examples/health_monitor/executor>`_: as an Executor that validates if filesystem is ok and saves detected Concept Drift.

As Knowledge Base `TimescaleDB <https://www.timescale.com/>`_ was chosen because it is full compatible with 
SQLAlchemy used in :doc:`connection adapter <driftage.kb>` and handles time series data very well.

The full example can be executed using `Docker Compose <https://docs.docker.com/compose/install/>`_ following these 3 steps:

1. Cloning the repository:
::
    git clone https://github.com/dmvieira/driftage.git

2. If you already have Docker Compose installed, run in driftage folder:
::
    make example

3. Wait until Executor logs that already written drift and take a look on the file with drifts:
::
    cat example/health_monitor/build/executor/output.csv

For more details, take a look at :doc:`api`.