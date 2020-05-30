import time
from datetime import datetime
from asynctest import TestCase
from sqlalchemy import create_engine
from aiobreaker import CircuitBreaker

from driftage.monitor import Monitor
from driftage.analyser import Analyser
from driftage.db.connection import Connection

from test.integration.helpers.analyser_predictor import AnalyserPredictor


class TestMonitorAnalyseIntegration(TestCase):
    def setUp(self):
        self.monitor = Monitor("monitor@localhost", "passw0rd", "data0")
        self.engine = create_engine("sqlite://")
        self.breaker = CircuitBreaker()
        self.connection = Connection(
            self.engine, 10, self.breaker)
        self.predictor = AnalyserPredictor(self.connection)
        self.analyser = Analyser(
            "analyser@localhost",
            "passw0rd",
            self.predictor,
            self.connection,
            ["monitor@localhost"]
        )
        self.monitor.start()
        self.analyser.start()

    def tearDown(self):
        self.monitor.container.stop()
        self.analyser.container.stop()
        self.breaker.close()

    async def test_should_analyse_monitored_data(self):
        dt_from = datetime.utcnow()
        for i in range(50):
            self.monitor({"my data": 123})
        time.sleep(1)
        dt_to = datetime.utcnow()
        await self.connection.get(dt_from, dt_to)
