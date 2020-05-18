from spade.behaviour import PeriodicBehaviour


class TrainPredictor(PeriodicBehaviour):
    async def run(self):
        predictor = self.agent.predictor
        predictor.train(self.agent.connection)
