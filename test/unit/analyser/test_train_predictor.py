from asynctest import TestCase, Mock, CoroutineMock
from driftage.analyser.behaviour.train_predictor import TrainPredictor


class TestTrainPredictor(TestCase):
    def setUp(self):
        self.agent = Mock()
        self.agent.predictor.fit = CoroutineMock()
        self.behaviour = TrainPredictor(period=1)
        self.behaviour.set_agent(self.agent)

    async def test_should_train(self):
        await self.behaviour.run()
        self.agent.predictor.fit.assert_awaited_once_with()
