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

        self._predictor = predictor
        super().__init__(jid, password, cache_max_size, verify_security)

    @property
    def predictor(self):
        return self._predictor

    async def setup(self):
        self.add_behaviour(
            Predict(period=self.predictor.predict_period))
        await super().setup()
