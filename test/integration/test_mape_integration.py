import asyncio
import os
from datetime import datetime
from asynctest import TestCase, patch
from sqlalchemy import create_engine
from aiobreaker import CircuitBreaker

from driftage.monitor import Monitor
from driftage.analyser import Analyser
from driftage.planner import Planner
from driftage.executor import Executor
from driftage.db.connection import Connection

from test.integration.helpers.helper_analyser_predictor import (
    HelperAnalyserPredictor)
from test.integration.helpers.helper_planner_predictor import (
    HelperPlannerPredictor)
from test.integration.helpers.helper_sink import HelperSink


class TestMAPEIntegration(TestCase):

    async def setUp(self):
        self.monitor = Monitor("monitor@localhost", "passw0rd", "data0")
        self.engine = create_engine("sqlite:///database.sql")
        self.breaker = CircuitBreaker()
        self.cache_to_save = 10
        self.connection = Connection(
            self.engine, self.cache_to_save, 100000, self.breaker)
        self.analyser_predictor = HelperAnalyserPredictor(self.connection)
        self.sink = HelperSink(self.breaker)
        self.sink.external.reset_mock()
        self.analyser = Analyser(
            "analyser@localhost",
            "passw0rd",
            self.analyser_predictor,
            self.connection,
            ["monitor@localhost"]
        )
        self.executor = Executor("executor@localhost", "passw0rd", self.sink)
        self.planner_predictor = HelperPlannerPredictor(self.connection)
        self.planner = Planner(
            "planner@localhost",
            "passw0rd",
            self.planner_predictor,
            ["executor@localhost"]
        )
        self.monitor.start()
        self.executor.start()

        await asyncio.sleep(2)
        self.analyser.start()
        self.planner.start()

        await asyncio.sleep(2)

    def tearDown(self):
        self.monitor.stop()
        self.analyser.stop()
        self.planner.stop()
        self.executor.stop()
        self.breaker.close()
        os.unlink("database.sql")

    @patch("driftage.planner.behaviour.predict.datetime")
    async def test_should_execute_monitored_data(self, mock_dt):
        now = datetime.utcnow()
        mock_dt.utcnow.return_value = now
        for i in range(self.cache_to_save):
            self.monitor({"my data": i})
        await asyncio.sleep(1)
        self.sink.external.assert_called_once_with(
            {
                'timestamp': now.timestamp(),
                'identifier': 'data0',
                'predicted': True
            }
        )
