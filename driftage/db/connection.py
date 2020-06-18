import pandas as pd
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy.sql import select
from sqlalchemy.exc import OperationalError
from aiobreaker import CircuitBreaker

from driftage.db.schema import table
from driftage.base.conf import getLogger


class Connection:
    def __init__(
            self,
            db_engine: Engine,
            bulk_size: int,
            circuit_breaker: CircuitBreaker = CircuitBreaker()):
        """Connects with SQLAlchemy Engine to store and query for
        data for concept drift datection.

        :param db_engine: SQLAlchemy Engine to use as backend
        :type db_engine: Engine
        :param bulk_size: Quantity of data that connection will
            wait to make bulk insert
        :type bulk_size: int
        :param circuit_breaker: Circuit Breaker configuration to
            connect with Database, defaults to CircuitBreaker()
        :type circuit_breaker: CircuitBreaker, optional
        """
        self._jid = None
        self._conn = db_engine
        self._bulk_size = bulk_size
        self._bulk_df = pd.DataFrame()
        self.get = circuit_breaker(self.get)
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
        """Insert in database if bulk size reached.

        :param df: Data to be inserted
        :type df: pd.DataFrame
        """
        self._bulk_df = pd.concat([self._bulk_df, df])
        if (len(self._bulk_df.index) >= self._bulk_size):
            await self._insert()

    async def get(
            self,
            from_datetime: datetime,
            to_datetime: datetime) -> pd.DataFrame:
        """Get data between dates from database.

        :param from_datetime: Start Datetime to search
        :type from_datetime: datetime
        :param to_datetime: End Datetime to search
        :type to_datetime: datetime
        :return: Data got from date range specified
        :rtype: pd.DataFrame
        """
        selectable = select([table]).where(
            (table.c.driftage_datetime > from_datetime) &
            (table.c.driftage_datetime < to_datetime)
        )
        query = str(selectable.compile(self._conn))
        try:
            return pd.read_sql_query(
                sql=query,
                con=self._conn,
                parse_dates=[table.c.driftage_datetime.name],
                params=[from_datetime, to_datetime]
            )
            self._logger.debug(f"Query executed: {query}")
        except (OperationalError, KeyError) as e:
            self._logger.exception(e)
            return pd.DataFrame()
