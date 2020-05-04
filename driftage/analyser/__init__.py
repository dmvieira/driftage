from spade.agent import Agent
from typing import Iterable
from driftage.analyser.behavior.receive_new_data import ReceiveNewData
from driftage.analyser.behavior.set_availability import SetAvailability
from driftage.analyser.behavior.learn_old_data import LearnOldData
from driftage.predictor import Predictor
from driftage.connection import Connection


class Analyser(Agent):
    def __init__(
            self,
            jid: str,
            password: str,
            predictor: Predictor,
            window_time: int,
            database_uri: str,
            verify_security: bool = False,
            monitors_jid: Iterable[str] = []
    ):

        self._monitors = monitors_jid
        self._database_uri = database_uri
        self._window_time = window_time
        self._predictor = predictor
        super(Analyser, self).__init__(jid, password, verify_security)

    @property
    def connection(self):
        return self._connection

    async def setup(self):
        self._connection = Connection(self.jid, self._database_uri)
        self.presence.approve_all = True
        for m in self._monitors:
            self.presence.subscribe(m)
        self.add_behaviour(ReceiveNewData())
        self.add_behaviour(SetAvailability(period=self._window_time))
        if self._predictor.retrain_period:
            self.add_behaviour(
                LearnOldData(period=self._predictor.retrain_period))
