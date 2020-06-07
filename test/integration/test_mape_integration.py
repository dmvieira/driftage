import asyncio
# import os
import pytest
# from datetime import datetime
from asynctest import TestCase
from sqlalchemy import create_engine
from aiobreaker import CircuitBreaker

from driftage.monitor import Monitor
from driftage.analyser import Analyser
from driftage.planner import Planner
from driftage.executor import Executor
from driftage.db.connection import Connection

from test.integration.helpers.test_analyser_predictor import (
    TestAnalyserPredictor)
from test.integration.helpers.test_planner_predictor import (
    TestPlannerPredictor)
from test.integration.helpers.test_sink import TestSink


@pytest.mark.serial
class TestMAPEIntegration(TestCase):

    async def setUp(self):
        self.monitor = Monitor("monitor@localhost", "passw0rd", "data0")
        self.engine = create_engine("sqlite:///database.sql")
        self.breaker = CircuitBreaker()
        self.connection = Connection(
            self.engine, 10, self.breaker)
        self.analyser_predictor = TestAnalyserPredictor(self.connection)
        self.sink = TestSink(self.breaker)
        self.analyser = Analyser(
            "analyser@localhost",
            "passw0rd",
            self.analyser_predictor,
            self.connection,
            ["monitor@localhost"]
        )
        self.executor = Executor("executor@localhost", "passw0rd", self.sink)
        self.planner_predictor = TestPlannerPredictor(self.connection)
        self.planner = Planner(
            "planner.localhost",
            "passw0rd",
            self.planner_predictor,
            ["executor@localhost"]
        )
        self.monitor.start()
        self.executor.start()
        await asyncio.sleep(2)
        self.analyser.start()
        self.planner.start()
        await asyncio.sleep(1)

    def tearDown(self):
        self.monitor.stop()
        self.analyser.stop()
        self.planner.stop()
        self.executor.stop()
        self.breaker.close()
        # os.unlink("database.sql")

    async def test_should_execute_monitored_data(self):
        pass
        # dt_from = datetime.utcnow()

        # with self.assertLogs(self.sink.logger, "INFO") as cm:
        # for i in range(10):
        #     self.monitor({"my data": i})
        # dt_to = datetime.utcnow()
        # await asyncio.sleep(1)
        # df = await self.connection.get(dt_from, dt_to)
        # import pdb; pdb.set_trace()
