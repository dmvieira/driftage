from asynctest import TestCase, Mock, call, patch
from driftage.planner import Planner


class TestPlanner(TestCase):

    def setUp(self):
        self.predictor = Mock()
        self.predictor.predict_period = 3
        self.connection = Mock()
        self.executors = ["e1", "e2", "e3"]
        self.planner = Planner(
            "user_test", "pass_test", self.predictor,
            self.executors, 10
        )
        self.planner.presence = Mock()

    def tearDown(self):
        self.planner.container.stop()

    @patch("driftage.planner.WaitCollects")
    @patch("driftage.planner.Predict")
    async def test_should_subscribe_to_executors(
            self, wait_mock, predict_mock):
        await self.planner.setup()
        self.assertEqual(
            self.planner.presence.subscribe.call_count, len(self.executors))
        self.planner.presence.subscribe.assert_has_calls(
            map(call, self.executors))

    @patch("driftage.planner.WaitCollects")
    @patch("driftage.planner.Predict")
    async def test_should_add_behaviours(self, wait_mock, predict_mock):
        self.planner.add_behaviour = Mock()
        await self.planner.setup()
        self.assertEqual(
            self.planner.add_behaviour.call_count, 2)
        self.planner.add_behaviour.assert_has_calls([
            call(wait_mock()),
            call(predict_mock(period=3))
        ], any_order=True)
