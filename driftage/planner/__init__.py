from driftage.base.agent.collector import Collector
from driftage.planner.behaviour.predict import Predict
from driftage.planner.predictor import PlannerPredictor


class Planner(Collector):
    def __init__(
            self,
            jid: str,
            password: str,
            predictor: PlannerPredictor,
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
        :param cache_max_size: [description], defaults to 10
        :type cache_max_size: int, optional
        :param verify_security: [description], defaults to False
        :type verify_security: bool, optional
        """

        self._predictor = predictor
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
        self.add_behaviour(
            Predict(period=self.predictor.predict_period))
        await super().setup()
