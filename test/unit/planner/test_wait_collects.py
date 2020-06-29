from collections import deque
from asynctest import TestCase, Mock
from driftage.planner.behaviour.wait_collects import WaitCollects


class TestWaitCollects(TestCase):

    def setUp(self):
        self.agent = Mock()
        self.agent.available_contacts = dict()
        self.agent.jid.localpart = "other_agent"
        self.agent.cache = deque([], 10)
        self.agent.sent_data = dict()
        self.agent.presence.get_contacts.return_value = {}
        self.behaviour = WaitCollects()
        self.behaviour.set_agent(self.agent)

    async def test_should_get_contacts_on_startup(self):
        presence_mock = Mock()
        presence_mock.type_.name = "AVAILABLE"
        self.agent.presence.get_contacts.return_value = {
            "agent": {
                "presence": presence_mock
            }
        }
        self.behaviour.on_available = Mock()
        await self.behaviour.run()
        self.behaviour.on_available.assert_called_once_with(
            "agent", presence_mock
        )

    async def test_should_ignore_unavailable_contacts_on_startup(self):
        presence_mock = Mock()
        presence_mock.type_.name = "UNAVAILABLE"
        self.agent.presence.get_contacts.return_value = {
            "agent": {
                "presence": presence_mock
            }
        }
        self.behaviour.on_available = Mock()
        await self.behaviour.run()
        self.behaviour.on_available.assert_not_called()

    async def test_should_ignore_with_no_presence_contacts_on_startup(self):
        self.agent.presence.get_contacts.return_value = {
            "agent": {}
        }
        self.behaviour.on_available = Mock()
        await self.behaviour.run()
        self.behaviour.on_available.assert_not_called()

    async def test_should_set_callbacks(self):
        await self.behaviour.run()
        self.assertTrue(
            self.agent.presence.is_available())
        self.assertEqual(
            self.agent.presence.on_available, self.behaviour.on_available)
        self.assertEqual(
            self.agent.presence.on_unavailable,
            self.behaviour.on_unavailable)

    async def test_should_add_on_available(self):
        self.behaviour.on_available("my jid", "stanza")
        self.assertDictEqual(
            self.agent.sent_data, {"my jid": self.agent.cache})

    async def test_should_remove_on_unavailable(self):
        self.behaviour.on_available("my jid", "stanza")
        self.assertDictEqual(
            self.agent.sent_data, {"my jid": self.agent.cache})
        self.behaviour.on_unavailable("my jid", "stanza")
        self.assertDictEqual(self.agent.sent_data, {})

    async def test_should_silent_error_on_unavailable_unexists(self):
        self.behaviour.on_unavailable("my jid", "stanza")
        self.assertDictEqual(self.agent.sent_data, {})
