import asyncio
import os
import time
from datetime import datetime
from asynctest import TestCase
from sqlalchemy import create_engine
from aiobreaker import CircuitBreaker

from driftage.monitor import Monitor
from driftage.analyser import Analyser
from driftage.db.connection import Connection
from driftage.db.schema import table

from test.integration.helpers.helper_analyser_predictor import (
    HelperAnalyserPredictor)


class TestMonitorAnalyseIntegration(TestCase):

    async def setUp(self):
        self.monitor = Monitor("monitor@localhost", "passw0rd", "data0")
        self.engine = create_engine("sqlite:///database.sql")
        self.breaker = CircuitBreaker()
        self.connection = Connection(
            self.engine, 10, 10000, self.breaker)
        self.predictor = HelperAnalyserPredictor(self.connection)
        self.analyser = Analyser(
            "analyser@localhost",
            "passw0rd",
            self.predictor,
            self.connection,
            ["monitor@localhost"]
        )
        self.monitor.start()
        await asyncio.sleep(2)
        self.analyser.start()
        await asyncio.sleep(1)

    def tearDown(self):
        self.monitor.stop()
        self.analyser.stop()
        self.breaker.close()
        os.unlink("database.sql")

    async def test_should_analyse_monitored_data(self):
        dt_from = datetime.utcnow()

        for i in range(10):
            self.monitor({"my data": i})
        dt_to = datetime.utcnow()
        time.sleep(1)
        df = await self.connection.get_between(
            table.c.driftage_datetime_monitored, dt_from, dt_to)
        self.assertEqual(len(df.index), 10)

    async def test_should_not_save_monitored_data_less_than_bulk(self):
        dt_from = datetime.utcnow()

        for i in range(9):
            self.monitor({"my data": i})
        dt_to = datetime.utcnow()
        time.sleep(1)
        df = await self.connection.get_between(
            table.c.driftage_datetime_monitored, dt_from, dt_to)
        self.assertEqual(len(df.index), 0)
