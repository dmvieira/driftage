from os import environ
from sqlalchemy import (
    Table, Column, String, Boolean, DateTime, PickleType, MetaData)

DRIFTAGE_TABLENAME = environ.get("DRIFTAGE_TABLENAME", "driftage_data")

table = Table(DRIFTAGE_TABLENAME, MetaData(),
              Column('driftage_jid', String, primary_key=True),
              Column('dirftage_datetime', DateTime, primary_key=True),
              Column('driftage_identifier', String, primary_key=True),
              Column('driftage_data', PickleType),
              Column('driftage_predicted', Boolean)
              )
