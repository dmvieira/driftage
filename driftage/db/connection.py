import pandas as pd
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy.sql import select
from driftage.db.schema import table
from aiobreaker import CircuitBreaker


class Connection:
    def __init__(
            self,
            db_engine: Engine,
            table: str,
            bulk_size: int,
            circuit_breaker: CircuitBreaker = CircuitBreaker()):
        """[summary]

        :param db_engine: [description]
        :type db_engine: Engine
        :param table: [description]
        :type table: str
        :param bulk_size: [description]
        :type bulk_size: int
        :param circuit_breaker: [description], defaults to CircuitBreaker()
        :type circuit_breaker: CircuitBreaker, optional
        """
        self._jid = None
        self._conn = db_engine
        self._table = table
        self._bulk_size = bulk_size
        self._bulk_df = pd.DataFrame()
        self.get = circuit_breaker(self.get)
        self._insert = circuit_breaker(self._insert)

    async def _insert(self):
        """[summary]
        """
        self._bulk_df.to_sql(
            name=self._table,
            con=self._conn,
            if_exists='append',
            index=False
        )
        self._bulk_df = pd.DataFrame()

    async def lazy_insert(self, df: pd.DataFrame):
        """[summary]

        :param df: [description]
        :type df: pd.DataFrame
        """
        self._bulk_df = pd.concat([self._bulk_df, df])
        if (len(self._bulk_df.index) >= self._bulk_size):
            await self._insert()

    async def get(
            self,
            from_datetime: datetime,
            to_datetime: datetime) -> pd.DataFrame:
        """[summary]

        :param from_datetime: [description]
        :type from_datetime: datetime
        :param to_datetime: [description]
        :type to_datetime: datetime
        :return: [description]
        :rtype: pd.DataFrame
        """
        selectable = select([table]).where(
            (table.c.dirftage_datetime > from_datetime) &
            (table.c.dirftage_datetime < to_datetime)
        )
        return pd.read_sql(
            sql=selectable,
            con=self._conn,
            parse_dates=[table.c.dirftage_datetime.name]
        )
