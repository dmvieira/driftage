from asynctest import TestCase, Mock, patch
from freezegun import freeze_time
from driftage.monitor import Monitor


class TestMonitor(TestCase):

    def setUp(self):

        self.monitor = Monitor(
            "user_test@local", "pass_test", "identif"
        )

    def tearDown(self):
        self.monitor.container.stop()

    def test_should_set_identifier_or_agent_name(self):
        self.assertEqual(
            self.monitor._identifier,
            "identif"
        )
        monitor = Monitor(
            "user_test2@local", "pass_test"
        )
        self.assertEqual(
            monitor._identifier,
            "user_test2"
        )
        monitor.container.stop()

    @patch("driftage.monitor.WaitMonitorSubscriptions")
    async def test_should_add_subscription_behaviour(self, behaviour_mock):
        self.monitor.add_behaviour = Mock()
        await self.monitor.setup()
        self.monitor.add_behaviour.assert_called_once_with(
            behaviour_mock()
        )

    @freeze_time("1989-08-12")
    @patch("driftage.monitor.NotifyContacts")
    def test_should_notify_contacts_on_new_data(self, behaviour_mock):
        self.monitor.add_behaviour = Mock()
        self.monitor.collect({"my data": 1})
        self.monitor.add_behaviour.assert_called_once_with(
            behaviour_mock()
        )
        self.assertDictEqual(
            {
                "data": {"my data": 1},
                "metadata": {
                    "timestamp": 618883200.0,
                    "identifier": "identif"
                }
            },
            self.monitor.cache[0]
        )

    @freeze_time("1989-08-12")
    @patch("driftage.monitor.NotifyContacts")
    def test_should_notify_contacts_on_new_data_with_call(
            self, behaviour_mock):
        self.monitor.add_behaviour = Mock()
        self.monitor({"my data": 1})
        self.monitor.add_behaviour.assert_called_once_with(
            behaviour_mock()
        )
        self.assertDictEqual(
            {
                "data": {"my data": 1},
                "metadata": {
                    "timestamp": 618883200.0,
                    "identifier": "identif"
                }
            },
            self.monitor.cache[0]
        )
