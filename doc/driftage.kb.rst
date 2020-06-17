Knowledge Base
=========================
Store data collected and predicted by :doc:`driftage.analyser` can be queried by 
:doc:`driftage.analyser` for retraining or :doc:`driftage.planner` for predictions.

Connection
----------------------------------
Build on top of `SQLAlchemy <https://www.sqlalchemy.org/>`_ to interact with Knowledge Base.

.. automodule:: driftage.db.connection
   :members:
   :undoc-members:
   :show-inheritance:


Schema
----------------------------------
Schema from data stored and predicted.

Definitions from table where predicted drifts are stored:

    Table:
        **driftage_kb** or defined by *DRIFTAGE_TABLENAME* enviroment variable

    Columns:
        - **driftage_jid**: ID from Analyser that predicted and saved data
        - **driftage_datetime**: Datetime of collected data
        - **driftage_identifier**: Identifier from monitor that collected data 
        - **driftage_data**: Json type object from data collected
        - **driftage_predicted**: True or False depending if data is drift or not