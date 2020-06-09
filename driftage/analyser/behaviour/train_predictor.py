from spade.behaviour import PeriodicBehaviour
from driftage.base.conf import getLogger


class TrainPredictor(PeriodicBehaviour):

    _logger = getLogger("train_predictor")

    async def run(self):
        """[summary]
        """
        self.agent.predictor.fit()
        self._logger.debug("Analyser model fitted")
