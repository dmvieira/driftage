from os import environ
from sqlalchemy import (
    Table, Column, String, Boolean, DateTime, PickleType, MetaData)

DRIFTAGE_TABLENAME = environ.get("DRIFTAGE_TABLENAME", "driftage_kb")

table = Table(DRIFTAGE_TABLENAME, MetaData(),
              Column('driftage_jid', String),
              Column('driftage_datetime_monitored', DateTime),
              Column('driftage_datetime_analysed', DateTime),
              Column('driftage_identifier', String),
              Column('driftage_data', PickleType),
              Column('driftage_predicted', Boolean)
              )
