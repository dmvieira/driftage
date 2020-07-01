import orjson
import pandas as pd
from datetime import datetime
from spade.behaviour import OneShotBehaviour
from driftage.db.schema import table
from driftage.base.conf import getLogger
from driftage.analyser.predictor import PredictionData


class StoreNewData(OneShotBehaviour):

    _logger = getLogger("store_new_data")

    async def run(self):
        """[summary]
        """
        msg = orjson.loads(self.template.body)
        data = await self._parse(msg)
        predicted = await self._predict(data)
        await self._store(data, predicted)
        self._logger.debug(f"Data stored on database {data}")

    async def _parse(self, msg: dict) -> pd.DataFrame:
        """[summary]

        :param msg: [description]
        :type msg: dict
        :return: [description]
        :rtype: PredictionData
        """
        data = msg["data"]
        metadata = msg["metadata"]

        return PredictionData(
            data=data,
            timestamp=datetime.fromtimestamp(metadata["timestamp"]),
            identifier=metadata["identifier"]
        )

    async def _predict(self, data: PredictionData) -> bool:
        """[summary]

        :param data: [description]
        :type data: PredictionData
        :return: [description]
        :rtype: bool
        """
        return await self.agent.predictor.predict(data)

    async def _store(self, data: PredictionData, prediction: bool):
        """[summary]

        :param data: [description]
        :type data: PredictionData
        :param prediction: [description]
        :type prediction: bool

        """
        df = pd.DataFrame(
            {
                table.c.driftage_jid.name: [self.agent.name],
                table.c.driftage_data.name: [
                    str(orjson.dumps(data.data), "utf-8")],
                table.c.driftage_datetime.name: [data.timestamp],
                table.c.driftage_identifier.name: [data.identifier],
                table.c.driftage_predicted.name: [prediction]
            }
        )
        await self.agent.connection.lazy_insert(df)
