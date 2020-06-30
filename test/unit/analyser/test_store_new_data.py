import orjson
from pandas import Timestamp
from freezegun import freeze_time
from datetime import datetime
from asynctest import TestCase, Mock, CoroutineMock
from spade.template import Template
from driftage.analyser.behaviour.store_new_data import StoreNewData
from driftage.db.schema import table


class TestStoreNewData(TestCase):
    maxDiff = None

    @freeze_time("1989-08-12", tz_offset=0)
    def setUp(self):
        self.agent = Mock()
        self.agent.name = "my agent"
        self.behaviour = StoreNewData()
        self.behaviour.receive = CoroutineMock()
        self.behaviour.set_agent(self.agent)
        self.body = dict(
            data=dict(test="any data"),
            metadata=dict(
                timestamp=datetime.utcnow().timestamp(),
                identifier="my data"
            )
        )
        self.template = Template(body=str(orjson.dumps(self.body), "utf-8"))
        self.behaviour.set_template(self.template)
        self.agent.connection.lazy_insert = CoroutineMock()

    @freeze_time("1989-08-12", tz_offset=0)
    async def test_should_parse_and_store_data(self):
        await self.behaviour.run()
        self.agent.connection.lazy_insert.assert_awaited_once()
        self.agent.predictor.predict.assert_called_once()
        df = self.agent.connection.lazy_insert.mock_calls[0][1][0]
        self.assertDictEqual(
            {
                table.c.driftage_jid.name: {0: "my agent"},
                table.c.driftage_data.name: {0: str(
                    orjson.dumps(self.body["data"]), "utf-8")},
                table.c.driftage_datetime.name: {
                    0: Timestamp(1989, 8, 12)},
                table.c.driftage_identifier.name: {0: "my data"},
                table.c.driftage_predicted.name: {
                    0: self.agent.predictor.predict()}
            },
            df.to_dict()
        )
