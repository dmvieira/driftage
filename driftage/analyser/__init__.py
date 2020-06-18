from spade.agent import Agent
from typing import Iterable
from driftage.analyser.behaviour.receive_new_data import ReceiveNewData
from driftage.analyser.behaviour.train_predictor import TrainPredictor
from driftage.analyser.predictor import AnalyserPredictor
from driftage.db.connection import Connection
from driftage.base.conf import getLogger


class Analyser(Agent):
    def __init__(
            self,
            jid: str,
            password: str,
            predictor: AnalyserPredictor,
            database_connection: Connection,
            monitors_jid: Iterable[str],
            verify_security: bool = False
    ):
        """Agent to predict Concept Drifts using a customized
        Predictor for that. This agent authenticates on XMPP server.

        :param jid: Id for XMPP authentication. Ex: user@localhost
        :type jid: str
        :param password: Password for XMPP authentication.
        :type password: str
        :param predictor: Predictor for Concept Drift detection.
        :type predictor: AnalyserPredictor
        :param database_connection: Database connection using SQLAlchemy.
        :type database_connection: Connection
        :param monitors_jid: List of monitors that this analyser will
            predict Concept Drifts.
        :type monitors_jid: Iterable[str]
        :param verify_security: Security validation with XMPP server,
            defaults to False.
        :type verify_security: bool, optional
        """
        self._monitors = monitors_jid
        self._connection = database_connection
        self._predictor = predictor
        self._logger = getLogger("analyser")
        super().__init__(jid, password, verify_security)

    @property
    def connection(self):
        """Connection property.

        :return: Database connection using SQLAlchemy.
        :rtype: Connection
        """
        return self._connection

    @property
    def predictor(self):
        """Predictor property

        :return: Predictor for Concept Drift detection.
        :rtype: AnalyserPredictor
        """
        return self._predictor

    async def setup(self):
        """Agent startup for behaviours.
        """
        self.presence.approve_all = True
        self.presence.set_available()
        for m in self._monitors:
            self.presence.subscribe(m)
        self.add_behaviour(ReceiveNewData())
        if self._predictor.retrain_period:
            self.add_behaviour(
                TrainPredictor(period=self.predictor.retrain_period))
        self._logger.info("Analyser started")
