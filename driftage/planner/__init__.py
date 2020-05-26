from typing import Iterable
from driftage.base.agent.collector import Collector
from driftage.planner.behaviour.predict import Predict
from driftage.planner.predictor import PlannerPredictor
from driftage.base.behaviour.wait_subscriptions import WaitSubscriptions


class Planner(Collector):
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
        super().__init__(jid, password, cache_max_size, verify_security)

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
        self.add_behaviour(WaitSubscriptions())
        for e in self._executors:
            self.presence.subscribe(e)
        self.add_behaviour(
            Predict(period=self.predictor.predict_period))
