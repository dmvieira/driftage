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
        """[summary]

        :param jid: [description]
        :type jid: str
        :param password: [description]
        :type password: str
        :param predictor: [description]
        :type predictor: PlannerPredictor
        :param executors_jid: [description]
        :type executors_jid: Iterable[str]
        :param cache_max_size: [description], defaults to 10
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
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        return self._sent_data

    @property
    def cache(self):
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        return self._cache

    @property
    def predictor(self):
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        return self._predictor

    async def setup(self):
        """[summary]
        """
        self.add_behaviour(WaitCollects())
        for e in self._executors:
            self.presence.subscribe(e)
        self.add_behaviour(
            Predict(period=self.predictor.predict_period))
        self.presence.set_available()
        self._logger.info("Planner started")
