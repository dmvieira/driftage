from asynctest import TestCase, Mock
from driftage.monitor.behaviour.wait_monitor_subscriptions import (
    WaitMonitorSubscriptions
)


class TestWaitMonitorSubscriptions(TestCase):

    def setUp(self):
        self.agent = Mock()
        self.behaviour = WaitMonitorSubscriptions()
        self.behaviour.set_agent(self.agent)

    async def test_should_set_callbacks(self):
        await self.behaviour.run()
        self.assertEqual(
            self.agent.presence.on_subscribe,
            self.behaviour.on_subscribe)

    async def test_should_react_on_subscribe(self):
        self.behaviour.presence.approve = Mock()
        self.behaviour.presence.subscribe = Mock()
        self.behaviour.on_subscribe("my jid")
        self.behaviour.presence.approve.assert_called_with("my jid")
        self.behaviour.presence.subscribe.assert_called_with("my jid")
