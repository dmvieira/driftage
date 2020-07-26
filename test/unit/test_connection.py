import pandas as pd
import asyncio
from freezegun import freeze_time
from datetime import datetime
from asynctest import TestCase, Mock, CoroutineMock, patch
from driftage.db.connection import Connection
from driftage.db.schema import table


class TestConnection(TestCase):
    def setUp(self):
        self.engine = Mock()
        self.connection = Connection(
            self.engine,
            10,
            0.9
        )

    async def test_should_not_insert_with_less_than_bulk_size(self):
        df = pd.DataFrame([1, 2, 3, 4, 5])
        self.connection._insert = CoroutineMock()
        await self.connection.lazy_insert(df)
        self.connection._insert.assert_not_awaited()

    async def test_should_insert_with_equal_more_than_bulk_size(self):
        df = pd.DataFrame([1, 2, 3, 4, 5])
        self.connection._insert = CoroutineMock()
        await self.connection.lazy_insert(df)
        await self.connection.lazy_insert(df)
        self.connection._insert.assert_awaited_once_with()

    async def test_should_insert_with_less_than_bulk_size_but_more_than_time(
            self):
        df = pd.DataFrame([1, 2, 3, 4, 5])
        self.connection._insert = CoroutineMock()
        initial_datetime = datetime.now()
        with freeze_time(initial_datetime) as frozen_datetime:
            frozen_datetime.tick()
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
            sql=str(select_mock().where().compile())
        )
