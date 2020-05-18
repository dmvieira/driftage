from datetime import datetime
from spade.behaviour import PeriodicBehaviour
from driftage.base.behaviour.notify_contacts import NotifyContacts


class Predict(PeriodicBehaviour):
    async def run(self):
        predictor = self.agent.predictor
        results = await predictor.predict()
        has_new_data = False
        for result in results:
            if result.predicted:
                self.agent.cache.append({
                    "timestamp": datetime.now().timestamp(),
                    "identifier": result.identifier
                })
                has_new_data = True
        if has_new_data:
            self.agent.add_behaviour(NotifyContacts())
