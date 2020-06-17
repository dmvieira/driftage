import asyncio
from os import path
from datetime import datetime
from asynctest import TestCase, patch
from sqlalchemy import create_engine
from aiobreaker import CircuitBreaker

from driftage.planner import Planner
from driftage.executor import Executor
from driftage.db.connection import Connection

from test.integration.helpers.helper_planner_predictor import (
    HelperPlannerPredictor)
from test.integration.helpers.helper_sink import HelperSink


@patch.dict(
    "driftage.db.schema.environ", {"DRIFTAGE_TABLENAME": "driftage_data"})
class TestPlannerExecutorIntegration(TestCase):

    async def setUp(self):
        if not path.exists("test/resources/database.dump"):
            raise IOError("database not exists")
        self.engine = create_engine("sqlite:///test/resources/database.dump")
        self.breaker = CircuitBreaker()
        self.connection = Connection(
            self.engine, 10, self.breaker)
        self.sink = HelperSink(self.breaker)
        self.sink.external.reset_mock()
        self.executor = Executor("executor@localhost", "passw0rd", self.sink)
        self.planner_predictor = HelperPlannerPredictor(self.connection)
        self.cache_number = 3
        self.planner = Planner(
            "planner@localhost",
            "passw0rd",
            self.planner_predictor,
            ["executor@localhost"],
            self.cache_number
        )

    def tearDown(self):
        self.planner_predictor.send = True
        self.planner.stop()
        self.executor.stop()
        self.breaker.close()

    @patch("driftage.planner.behaviour.predict.datetime")
    async def test_should_export_to_sink(self, mock_dt):
        now = datetime.utcnow()
        mock_dt.utcnow.return_value = now
        self.executor.start()
        await asyncio.sleep(2)
        self.planner.start()
        await asyncio.sleep(2)
        self.sink.external.assert_called_with(
            {
                "timestamp": now.timestamp(),
                "identifier": "data0",
                "predicted": True
            }
        )

    async def test_should_continualy_export_to_sink(self):
        self.executor.start()
        await asyncio.sleep(2)
        self.planner.start()
        await asyncio.sleep(2)
        for i in range(1, 5):
            self.assertGreaterEqual(self.sink.external.call_count, i)
            self.assertLessEqual(self.sink.external.call_count, i+1)
            await asyncio.sleep(self.planner_predictor.predict_period)

    async def test_should_wait_executor_up(self):
        self.executor.start()
        await asyncio.sleep(2)
        self.planner.start()
        self.executor.stop()
        await asyncio.sleep(self.cache_number+2)
        self.assertEqual(len(self.planner.cache), self.cache_number)
        self.assertEqual(len(self.planner.sent_data.values()), 0)
        self.executor.start()
        await asyncio.sleep(2)
        self.assertEqual(len(self.planner.cache), self.cache_number)
        self.assertEqual(len(self.planner.sent_data.values()), 1)
        self.assertEqual(
            len(list(self.planner.sent_data.values())[0]), self.cache_number)

    async def test_should_never_send_if_predictor_say(self):
        self.executor.start()
        await asyncio.sleep(2)
        self.planner_predictor.send = False
        self.planner.start()
        await asyncio.sleep(2)
        self.planner_predictor.send = True
        await asyncio.sleep(1)
        self.assertEqual(len(self.planner.cache), 1)
        self.assertEqual(len(self.planner.sent_data.values()), 1)
        self.planner_predictor.send = False
        await asyncio.sleep(1)
        await asyncio.sleep(self.cache_number)
        self.assertEqual(len(self.planner.cache), 1)
        self.assertEqual(
            len(self.planner.sent_data.values()), 1)
