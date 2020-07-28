import pandas as pd
from typing import Union
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy.engine import Engine
from sqlalchemy.sql import select
from aiobreaker import CircuitBreaker

from driftage.db.schema import table
from driftage.base.conf import getLogger


class Connection:
    def __init__(
            self,
            db_engine: Engine,
            bulk_size: int,
            bulk_time: Union[int, float],
            circuit_breaker: CircuitBreaker = CircuitBreaker()):
        """Connects with SQLAlchemy Engine to store and query
        data for concept drift datection.

        :param db_engine: SQLAlchemy Engine to use as backend
        :type db_engine: Engine
        :param bulk_size: Quantity of data that connection will
            wait to make bulk insert
        :type bulk_size: int
        :param bulk_time: Time in seconds between last insert and now.
            If bulk_size is not reached in bulk_time interval,
            then an insert was done
        :type bulk_time: Union[int, float]
        :param circuit_breaker: Circuit Breaker configuration to
            connect with Database, defaults to CircuitBreaker()
        :type circuit_breaker: CircuitBreaker, optional
        """
        self._jid = None
        self._conn = db_engine
        self._bulk_size = bulk_size
        self._bulk_time = bulk_time
        self._last_insert_time = datetime.utcnow()
        self._bulk_df = pd.DataFrame()
        self.get_between = circuit_breaker(self.get_between)
        self._insert = circuit_breaker(self._insert)
        self._logger = getLogger("connection")

    async def _insert(self):
        """Really insert to database with Pandas.
        """
        self._bulk_df.to_sql(
            name=table.name,
            con=self._conn,
            if_exists='append',
            index=False,
            method="multi"
        )
        self._logger.debug(f"Inserted on table {table.name}")
        self._bulk_df = pd.DataFrame()

    async def lazy_insert(self, df: pd.DataFrame):
        """Insert in database if bulk size or bulk time reached.

        :param df: Data to be inserted
        :type df: pd.DataFrame
        """
        now = datetime.utcnow()
        self._bulk_df = pd.concat([self._bulk_df, df])
        if ((len(self._bulk_df.index) >= self._bulk_size) or
                ((now - self._last_insert_time).seconds > self._bulk_time)):
            await self._insert()
            self._last_insert_time = now

    async def get_between(
            self,
            column: Column,
            from_datetime: datetime,
            to_datetime: datetime) -> pd.DataFrame:
        """Collects data between dates from database.

        :param column: Database column from schema
        :type column: Column
        :param from_datetime: Start Datetime to search
        :type from_datetime: datetime
        :param to_datetime: End Datetime to search
        :type to_datetime: datetime
        :return: Data got from specified date range
        :rtype: pd.DataFrame
        """
        selectable = select([table]).where(
            (column > str(from_datetime)) &
            (column < str(to_datetime))
        )
        select_obj = selectable.compile(self._conn,
                                        compile_kwargs={"literal_binds": True})
        query = str(select_obj)
        try:
            return pd.read_sql_query(
                sql=query,
                con=self._conn,
                parse_dates=[
                    table.c.driftage_datetime_monitored.name,
                    table.c.driftage_datetime_analysed.name
                ]
            )
            self._logger.debug(f"Query executed: {query}")
        except Exception as e:
            self._logger.exception(e)
            return pd.DataFrame()
