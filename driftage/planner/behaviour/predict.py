from datetime import datetime
from spade.behaviour import PeriodicBehaviour
from driftage.planner.behaviour.notify_contacts import NotifyContacts


class Predict(PeriodicBehaviour):
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
                    "prediction": result.prediction
                })
                has_new_data = True
        if has_new_data:
            self.agent.add_behaviour(NotifyContacts())
