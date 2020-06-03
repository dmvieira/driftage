from asynctest import TestCase, Mock, CoroutineMock, patch
from spade.template import Template
from driftage.monitor.behaviour.fast_notify_contacts import FastNotifyContacts


class TestFastNotifyContacts(TestCase):

    def setUp(self):
        self.agent = Mock()
        self.behaviour = FastNotifyContacts()
        self.behaviour.set_agent(self.agent)
        self.behaviour.set_template(
            Template(body='["data 1", "data 2", "data 3"]'))
        self.behaviour.send = CoroutineMock()

    @patch("driftage.monitor.behaviour.fast_notify_contacts.Message")
    async def test_should_send_new_data(self, message_mock):
        self.agent.available_contacts = {"my agent": "stanza"}
        await self.behaviour.run()
        message_mock.assert_called_once_with(
            to="my agent", body='["data 1", "data 2", "data 3"]')
        self.behaviour.send.assert_awaited_once_with(message_mock())
