import pandas as pd
import asyncio
from datetime import datetime
from asynctest import TestCase, Mock, CoroutineMock, patch
from driftage.db.connection import Connection
from driftage.db.schema import table


class TestConnection(TestCase):
    def setUp(self):
        self.engine = Mock()
        self.connection = Connection(
            self.engine,
            10
        )

    async def test_should_not_insert_with_less_than_bulk_size(self):
        df = pd.DataFrame([1, 2, 3, 4, 5])
        self.connection._insert = CoroutineMock()
        await self.connection.lazy_insert(df)
        self.connection._insert.assert_not_awaited()
        await self.connection.lazy_insert(df)
        self.connection._insert.assert_awaited_once_with()

    @patch("driftage.db.connection.pd")
    @patch("driftage.db.connection.select")
    async def test_should_get_with_right_query(self, select_mock, pd_mock):
        from_dt = datetime.utcnow()
        await asyncio.sleep(1)
        to_dt = datetime.utcnow()
        await self.connection.get_between(from_dt, to_dt)
        select_mock.assert_called_once_with([table])
        pd_mock.read_sql_query.assert_called_with(
            con=self.engine,
            parse_dates=[table.c.driftage_datetime.name],
            sql=str(select_mock().where().compile()),
            params=[from_dt, to_dt]
        )
