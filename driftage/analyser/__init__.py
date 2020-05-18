from spade.agent import Agent
from typing import Iterable
from driftage.analyser.behaviour.receive_new_data import ReceiveNewData
from driftage.analyser.behaviour.train_predictor import TrainPredictor
from driftage.analyser.predictor import AnalyserPredictor
from driftage.db.connection import Connection


class Analyser(Agent):
    def __init__(
            self,
            jid: str,
            password: str,
            predictor: AnalyserPredictor,
            database_connection: Connection,
            monitors_jid: Iterable[str] = [],
            verify_security: bool = False
    ):

        self._monitors = monitors_jid
        self._connection = database_connection
        self._predictor = predictor
        super().__init__(jid, password, verify_security)

    @property
    def connection(self):
        return self._connection

    @property
    def predictor(self):
        return self._predictor

    async def setup(self):
        self.presence.approve_all = True
        for m in self._monitors:
            self.presence.subscribe(m)
        self.add_behaviour(ReceiveNewData())
        if self._predictor.retrain_period:
            self.add_behaviour(
                TrainPredictor(period=self.predictor.retrain_period))
        self.presence.set_available()
