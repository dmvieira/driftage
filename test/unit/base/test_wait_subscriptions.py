from asynctest import TestCase, Mock
from driftage.base.behaviour.wait_subscriptions import WaitSubscriptions


class TestWaitSubscriptions(TestCase):

    def setUp(self):
        self.agent = Mock()
        self.agent.sent_data = dict()
        self.agent.available_contacts = dict()
        self.agent.cache = ["cache"]
        self.behaviour = WaitSubscriptions()
        self.behaviour.set_agent(self.agent)

    async def test_should_set_callbacks(self):
        await self.behaviour.run()
        self.assertTrue(
            self.agent.presence.is_available())
        self.assertEqual(
            self.agent.presence.on_subscribed, self.behaviour.on_subscribed)
        self.assertEqual(
            self.agent.presence.on_unsubscribed,
            self.behaviour.on_unsubscribed)
        self.assertEqual(
            self.agent.presence.on_available, self.behaviour.on_available)
        self.assertEqual(
            self.agent.presence.on_unavailable,
            self.behaviour.on_unavailable)

    async def test_should_add_on_subscribed(self):
        self.behaviour.on_subscribed("my jid")
        self.assertDictEqual(self.agent.sent_data, {"my jid": ["cache"]})

    async def test_should_remove_on_unsubscribed(self):
        self.behaviour.on_subscribed("my jid")
        self.assertDictEqual(self.agent.sent_data, {"my jid": ["cache"]})
        self.behaviour.on_unsubscribed("my jid")
        self.assertDictEqual(self.agent.sent_data, {})

    async def test_should_silent_error_on_unsubscribed_unexists(self):
        self.behaviour.on_unsubscribed("my jid")
        self.assertDictEqual(self.agent.sent_data, {})

    async def test_should_add_on_available(self):
        self.behaviour.on_available("my jid", "stanza")
        self.assertDictEqual(
            self.agent.available_contacts, {"my jid": "stanza"})

    async def test_should_remove_on_unavailable(self):
        self.behaviour.on_available("my jid", "stanza")
        self.assertDictEqual(
            self.agent.available_contacts, {"my jid": "stanza"})
        self.behaviour.on_unavailable("my jid", "stanza")
        self.assertDictEqual(self.agent.available_contacts, {})

    async def test_should_silent_error_on_unavailable_unexists(self):
        self.behaviour.on_unavailable("my jid", "stanza")
        self.assertDictEqual(self.agent.available_contacts, {})
