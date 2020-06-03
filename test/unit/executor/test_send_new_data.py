from asynctest import TestCase, Mock, CoroutineMock, call
from spade.template import Template
from driftage.executor.behaviour.send_new_data import SendNewData


class TestSendNewData(TestCase):
    def setUp(self):
        self.agent = Mock()
        self.behaviour = SendNewData()
        self.behaviour.set_agent(self.agent)
        self.behaviour.set_template(Template(body='[1, 2, 3]'))
        self.agent.sink.drain = CoroutineMock()

    async def test_should_drain_if_sink_is_available(self):
        self.agent.sink.is_available.return_value = True
        await self.behaviour.run()
        self.assertEqual(3, self.agent.sink.drain.call_count)
        self.agent.sink.drain.has_calls(
            [call(1), call(2), call(3)], any_order=True
        )

    async def test_should_do_nothing_with_no_sink(self):
        self.agent.sink.is_available.return_value = False
        await self.behaviour.run()
        self.agent.sink.drain.assert_not_awaited()
