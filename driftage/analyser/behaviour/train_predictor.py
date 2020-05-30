from spade.behaviour import PeriodicBehaviour


class TrainPredictor(PeriodicBehaviour):
    async def run(self):
        """[summary]
        """
        self.agent.predictor.fit()
