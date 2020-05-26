from spade.agent import Agent
from driftage.executor.sink import Sink
from driftage.executor.behaviour.receive_new_data import ReceiveNewData


class Executor(Agent):
    def __init__(
            self,
            jid: str,
            password: str,
            sink: Sink,
            verify_security: bool = False
    ):
        """[summary]

        :param jid: [description]
        :type jid: str
        :param password: [description]
        :type password: str
        :param sink: [description]
        :type sink: Sink
        :param verify_security: [description], defaults to False
        :type verify_security: bool, optional
        """
        self._sink = sink
        super().__init__(jid, password, verify_security)

    @property
    def sink(self):
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        return self._sink

    def setup(self):
        """[summary]
        """
        self.presence.approve_all = True
        self.add_behaviour(ReceiveNewData())
        self.presence.set_available()
