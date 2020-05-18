import pandas as pd
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy.sql import select
from driftage.db.schema import table


class Connection:
    def __init__(self, db_engine: Engine, table: str, bulk_size: int):
        self._jid = None
        self._conn = db_engine
        self._table = table
        self._bulk_size = bulk_size
        self._bulk_df = pd.DataFrame()

    async def _insert(self):
        self._bulk_df.to_sql(
            name=self._table,
            con=self._conn,
            if_exists='append',
            index=False
        )
        self._bulk_df = pd.DataFrame()

    async def lazy_insert(self, df: pd.DataFrame):
        self._bulk_df = pd.concat([self._bulk_df, df])
        if (len(self._bulk_df.index) >= self._bulk_size):
            await self._insert()

    async def get(
            self,
            from_datetime: datetime,
            to_datetime: datetime) -> pd.DataFrame:
        selectable = select([table]).where(
            (table.c.dirftage_datetime > from_datetime) &
            (table.c.dirftage_datetime < to_datetime)
        )
        return pd.read_sql(
            sql=selectable,
            con=self._conn,
            parse_dates=[table.c.dirftage_datetime.name]
        )
