from asynctest import TestCase, Mock, CoroutineMock, patch
from driftage.analyser.behaviour.receive_new_data import ReceiveNewData


class TestReceiveNewData(TestCase):
    def setUp(self):
        self.agent = Mock()
        self.behaviour = ReceiveNewData()
        self.behaviour.receive = CoroutineMock()
        self.behaviour.set_agent(self.agent)

    @patch("driftage.analyser.behaviour.receive_new_data.StoreNewData")
    @patch("driftage.analyser.behaviour.receive_new_data.Template")
    async def test_should_store_data_on_message(self, template, callback):
        message = Mock(1)
        message.body = "testing"
        self.behaviour.receive.return_value = message
        await self.behaviour.run()
        self.behaviour.receive.assert_awaited_once_with()
        self.agent.add_behaviour.assert_called_once_with(
            callback(), template(body="testing"))

    async def test_should_do_nothing_with_no_message(self):
        message = None
        self.behaviour.receive.return_value = message
        await self.behaviour.run()
        self.behaviour.receive.assert_awaited_once_with()
        self.agent.add_behaviour.assert_not_called()
