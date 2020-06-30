from asynctest import TestCase, Mock, CoroutineMock, patch
from driftage.planner.behaviour.notify_contacts import NotifyContacts


class TestNotifyContacts(TestCase):

    def setUp(self):
        self.agent = Mock()
        self.behaviour = NotifyContacts()
        self.behaviour.set_agent(self.agent)
        self.behaviour.send = CoroutineMock()

    async def test_should_do_nothing_if_already_notified_same_data(self):
        self.agent.available_contacts = {"my agent": "stanza"}
        self.agent.cache = ["data 1"]
        self.agent.sent_data = {"my agent": [id("data 1")]}
        await self.behaviour.run()
        self.behaviour.send.assert_not_awaited()

    @patch("driftage.planner.behaviour.notify_contacts.Message")
    async def test_should_send_new_data(self, message_mock):
        self.agent.available_contacts = {"my agent": "stanza"}
        self.agent.cache = ["data 1", "data 2", "data 3"]
        self.agent.sent_data = {"my agent": [id("data 1")]}
        await self.behaviour.run()
        message_mock.assert_called_once_with(
            to="my agent", body='["data 2","data 3"]')
        self.behaviour.send.assert_awaited_once_with(message_mock())
        self.assertDictEqual(
            self.agent.sent_data,
            {"my agent": [id("data 1"), id("data 2"), id("data 3")]}
        )
