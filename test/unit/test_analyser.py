from asynctest import TestCase, Mock, call, patch
from driftage.analyser import Analyser


class TestAnalyser(TestCase):

    def setUp(self):
        self.predictor = Mock()
        self.predictor.retrain_period = 3
        self.connection = Mock()
        self.monitors = ["m1", "m2", "m3"]
        self.analyser = Analyser(
            "user_test", "pass_test", self.predictor,
            self.connection, self.monitors
        )
        self.analyser.presence = Mock()

    async def test_should_subscribe_to_monitors(self):
        await self.analyser.setup()
        self.assertEqual(
            self.analyser.presence.subscribe.call_count, len(self.monitors))
        self.analyser.presence.subscribe.assert_has_calls(
            map(call, self.monitors))

    @patch("driftage.analyser.TrainPredictor")
    @patch("driftage.analyser.ReceiveNewData")
    async def test_should_add_behaviours(self, receive_data, train_predictor):
        self.analyser.add_behaviour = Mock()
        await self.analyser.setup()
        self.assertEqual(
            self.analyser.add_behaviour.call_count, 2)
        self.analyser.add_behaviour.assert_has_calls([
            call(receive_data()),
            call(train_predictor(period=3))
        ])

    @patch("driftage.analyser.TrainPredictor")
    @patch("driftage.analyser.ReceiveNewData")
    async def test_should_call_retrain_only_if_set(
            self, receive_data, train_predictor):
        self.predictor.retrain_period = None
        self.analyser.add_behaviour = Mock()
        await self.analyser.setup()
        self.assertEqual(
            self.analyser.add_behaviour.call_count, 1)
        self.analyser.add_behaviour.assert_has_calls([
            call(receive_data())
        ])
