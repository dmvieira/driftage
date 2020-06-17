from collections import deque
from typing import Iterable
from driftage.base.agent.subscriptor import Subscriptor
from driftage.planner.behaviour.predict import Predict
from driftage.planner.behaviour.wait_collects import WaitCollects
from driftage.planner.predictor import PlannerPredictor
from driftage.base.conf import getLogger


class Planner(Subscriptor):
    def __init__(
            self,
            jid: str,
            password: str,
            predictor: PlannerPredictor,
            executors_jid: Iterable[str],
            cache_max_size: int = 10,
            verify_security: bool = False
    ):
        """Agent to predict Concept Drifts from KB using a customized
        Predictor for that. This agent authenticates on XMPP server.

        :param jid: Id for XMPP authentication. Ex: user@localhost
        :type jid: str
        :param password: Password for XMPP authentication.
        :type password: str
        :param predictor: Predictor for Concept Drift detection.
        :type predictor: PlannerPredictor
        :param executors_jid: List of executors that this planner will
        send detected Concept Drifts.
        :type executors_jid: Iterable[str]
        :param cache_max_size: Cache list if executor is unavailable,
        defaults to 10
        :type cache_max_size: int, optional
        :param verify_security: [description], defaults to False
        :type verify_security: bool, optional
        """

        self._predictor = predictor
        self._executors = executors_jid
        self._cache = deque([], cache_max_size)
        self._sent_data = {}
        self._logger = getLogger("planner")
        super().__init__(jid, password, verify_security)

    @property
    def sent_data(self):
        """Stores a cache for each executor for data sent.

        :return: dict of executor -> data sent
        :rtype: dict
        """
        return self._sent_data

    @property
    def cache(self):
        """Stores a cache for predicted items to send.

        :return: deque with last itens predicted
        :rtype: deque
        """
        return self._cache

    @property
    def predictor(self):
        """Predictor property

        :return: Predictor for Concept Drift detection.
        :rtype: PlannerPredictor
        """
        return self._predictor

    async def setup(self):
        """Agent startup for behaviours.
        """
        self.add_behaviour(WaitCollects())
        for e in self._executors:
            self.presence.subscribe(e)
        self.add_behaviour(
            Predict(period=self.predictor.predict_period))
        self.presence.set_available()
        self._logger.info("Planner started")
