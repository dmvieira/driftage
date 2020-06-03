from asynctest import TestCase, Mock, patch, CoroutineMock
from driftage.planner.behaviour.predict import Predict
from driftage.planner.predictor import PredictResult


class TestPredict(TestCase):
    def setUp(self):
        self.agent = Mock()
        self.agent.predictor.predict = CoroutineMock()
        self.agent.add_behaviour = Mock()
        self.behaviour = Predict(period=1)
        self.behaviour.set_agent(self.agent)

    @patch("driftage.planner.behaviour.predict.NotifyContacts")
    async def test_should_predict_and_do_nothing_with_empty_result(
            self, notify_mock):
        await self.behaviour.run()
        self.agent.predictor.predict.assert_called_once_with()
        notify_mock.assert_not_called()
        self.agent.add_behaviour.assert_not_called()

    @patch("driftage.planner.behaviour.predict.NotifyContacts")
    async def test_should_predict_and_notify_contacts(self, notify_mock):
        self.agent.predictor.predict.return_value = [PredictResult(
            "identfier", 1, True
        )]
        await self.behaviour.run()
        self.agent.predictor.predict.assert_called_once_with()
        notify_mock.assert_called_once_with()
        self.agent.add_behaviour.assert_called_once_with(
            notify_mock()
        )

    @patch("driftage.planner.behaviour.predict.NotifyContacts")
    async def test_should_predict_and_dont_notify_without_should_send(
            self, notify_mock):
        self.agent.predictor.predict.return_value = [PredictResult(
            "identfier", 1, False
        )]
        await self.behaviour.run()
        self.agent.predictor.predict.assert_called_once_with()
        notify_mock.assert_not_called()
        self.agent.add_behaviour.assert_not_called()
