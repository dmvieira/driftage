from asynctest import TestCase, Mock
from driftage.analyser.behaviour.train_predictor import TrainPredictor


class TestTrainPredictor(TestCase):
    def setUp(self):
        self.agent = Mock()
        self.behaviour = TrainPredictor(period=1)
        self.behaviour.set_agent(self.agent)

    async def test_should_train(self):
        await self.behaviour.run()
        self.agent.predictor.fit.assert_called_once_with()
