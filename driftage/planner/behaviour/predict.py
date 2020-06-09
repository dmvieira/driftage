from datetime import datetime
from spade.behaviour import PeriodicBehaviour
from driftage.planner.behaviour.notify_contacts import NotifyContacts
from driftage.base.conf import getLogger


class Predict(PeriodicBehaviour):

    _logger = getLogger("predict")

    async def run(self):
        """[summary]
        """
        predictor = self.agent.predictor
        results = await predictor.predict()
        has_new_data = False
        for result in results:
            if result.should_send:
                self.agent.cache.append({
                    "timestamp": datetime.utcnow().timestamp(),
                    "identifier": result.identifier,
                    "predicted": result.predicted
                })
                has_new_data = True
        if has_new_data:
            self.agent.add_behaviour(NotifyContacts())
            self._logger.debug("Notified new predictions")
