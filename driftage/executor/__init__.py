from spade.agent import Agent
from driftage.executor.sink import Sink
from driftage.executor.behaviour.receive_new_data import ReceiveNewData
from driftage.base.conf import getLogger


class Executor(Agent):
    def __init__(
            self,
            jid: str,
            password: str,
            sink: Sink,
            verify_security: bool = False
    ):
        """Agent to send predicted drifts to Sink.
        This agent authenticates on XMPP server.

        :param jid: Id for XMPP authentication. Ex: user@localhost
        :type jid: str
        :param password: Password for XMPP authentication.
        :type password: str
        :param sink: Where predicted Concept Drifts will be dispatched.
        :type sink: Sink
        :param verify_security: Security validation with XMPP server,
            defaults to False.
        :type verify_security: bool, optional
        """
        self._sink = sink
        self._logger = getLogger("executor")
        super().__init__(jid, password, verify_security)

    @property
    def sink(self):
        """Sink property

        :return: Sink to dispatch Concept Drifts detected.
        :rtype: Sink
        """
        return self._sink

    async def setup(self):
        """Agent startup for behaviours.
        """
        self.presence.approve_all = True
        self.add_behaviour(ReceiveNewData())
        self.presence.set_available()
        self._logger.info("Executor started")
