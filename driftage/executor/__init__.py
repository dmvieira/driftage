from typing import Iterable
from spade.agent import Agent
from driftage.executor.sink import Sink
from driftage.executor.behaviour.receive_new_data import ReceiveNewData


class Executor(Agent):
    def __init__(
            self,
            jid: str,
            password: str,
            sink: Sink,
            planners_jid: Iterable[str],
            verify_security: bool = False
    ):
        self._sink = sink
        self._planners = planners_jid
        super().__init__(jid, password, verify_security)

    @property
    def sink(self):
        return self._sink

    def setup(self):
        self.presence.approve_all = True
        for p in self._planners:
            self.presence.subscribe(p)
        self.add_behaviour(ReceiveNewData())
        self.presence.set_available()
