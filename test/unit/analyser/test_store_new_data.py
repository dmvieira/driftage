import json
from datetime import datetime
from asynctest import TestCase, Mock, CoroutineMock, patch
from spade.template import Template
from driftage.analyser.behaviour.store_new_data import StoreNewData
from driftage.db.schema import table


class TestReceiveNewData(TestCase):
    maxDiff = None
    
    def setUp(self):
        self.agent = Mock()
        self.agent.name = "my agent"
        self.behaviour = StoreNewData()
        self.behaviour.receive = CoroutineMock()
        self.behaviour.set_agent(self.agent)
        self.body = [dict(
            data=dict(test="any data"),
            metadata=dict(
                timestamp=0.0,
                identifier="my data"
            )
        )]
        self.template = Template(body=json.dumps(self.body))
        self.behaviour.set_template(self.template)
        self.agent.connection.lazy_insert = CoroutineMock()

    async def test_should_parse_and_store_data(self):
        await self.behaviour.run()
        self.agent.connection.lazy_insert.assert_awaited_once()
        self.agent.predictor.predict.assert_called_once()
        df = self.agent.connection.lazy_insert.mock_calls[0][1][0]
        self.assertDictEqual(
            {
                table.c.driftage_jid.name: {0: "my agent"},
                table.c.driftage_data.name: {0: self.body[0]["data"]},
                table.c.driftage_datetime.name: {0: datetime(1970, 1, 1)},
                table.c.driftage_identifier.name: {0: "my data"},
                table.c.driftage_predicted.name: {
                    0: self.agent.predictor.predict()}
            },
            df.to_dict()
        )