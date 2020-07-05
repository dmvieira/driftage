Examples
=============

An example was 
`built as a health monitor <https://github.com/dmvieira/driftage/tree/master/examples/health_monitor>`_ 
when an user is punching. Data was 
`EMG Physical Action Data Set <https://archive.ics.uci.edu/ml/datasets/EMG+Physical+Action+Data+Set>`_ 
collected from UCI Machine Learning.

There is a 
`Jupyter Notebook analysis <https://github.com/dmvieira/driftage/blob/master/examples/health_monitor/Data%20Analysis.ipynb>`_ 
that illustrate how different are voltage signals collected from the following muscles:

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

* `Spark Monitor <https://github.com/dmvieira/driftage/tree/master/examples/health_monitor/monitor>`_: as a monitor integrated with `Apache Spark <https://spark.apache.org/>`_ Structured Streaming to read csv punching signals from muscles.
* `ADWIN Analyser <https://github.com/dmvieira/driftage/tree/master/examples/health_monitor/analyser>`_: as an analyser for each muscle signal using ADWIN from `Skmultiflow <https://scikit-multiflow.github.io/>`_ to detect drifts on muscle activity.
* `Voting Planner <https://github.com/dmvieira/driftage/tree/master/examples/health_monitor/planner>`_: as a planner for voting with a threashold X=2. If more than a X muscle signals are interpreted having drift, than it alerts a drift to executor.
* `Csv Executor <https://github.com/dmvieira/driftage/tree/master/examples/health_monitor/executor>`_: as an executor that validates if filesystem is ok and saves detected Concept Drift.

As Knowledge Base `TimescaleDB <https://www.timescale.com/>`_ was choose because it is full compatible with 
SQLAlchemy used in :doc:`connection adapter <driftage.analyser>` and handle timeseries data very well.

The full example can be executed using `Docker Compose <https://docs.docker.com/compose/install/>`_ following these 3 steps:

1. Cloning the repository:
::
    git clone https://github.com/dmvieira/driftage.git

2. If you already have Docker Compose installed, run in driftage folder:
::
    make example

3. Wait until executor logs that wrote date and take a look on the file with drifts:
::
    cat example/health_monitor/build/executor/output.csv