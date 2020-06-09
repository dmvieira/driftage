import json
import pandas as pd
from datetime import datetime
from spade.behaviour import OneShotBehaviour
from driftage.db.schema import table
from driftage.base.conf import getLogger


class StoreNewData(OneShotBehaviour):

    _logger = getLogger("store_new_data")

    async def run(self):
        """[summary]
        """
        msg = json.loads(self.template.body)
        data = msg["data"]
        metadata = msg["metadata"]
        timestamp = metadata["timestamp"]
        identifier = metadata["identifier"]
        df = await self._parse(data, timestamp, identifier)
        predicted_df = await self._predict(df)
        await self._store(predicted_df)
        self._logger.debug(f"Data stored on database {data}")

    async def _parse(
            self,
            data: dict,
            timestamp: float,
            identifier: str) -> pd.DataFrame:
        """[summary]

        :param data: [description]
        :type data: dict
        :param timestamp: [description]
        :type timestamp: float
        :param identifier: [description]
        :type identifier: str
        :return: [description]
        :rtype: pd.DataFrame
        """
        return pd.DataFrame(
            {
                table.c.driftage_jid.name: [self.agent.name],
                table.c.driftage_data.name: [json.dumps(data)],
                table.c.driftage_datetime.name: [
                    datetime.fromtimestamp(timestamp)],
                table.c.driftage_identifier.name: [identifier]
            }
        )

    async def _predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """[summary]

        :param df: [description]
        :type df: pd.DataFrame
        :return: [description]
        :rtype: pd.DataFrame
        """
        df[table.c.driftage_predicted.name] = self.agent.predictor.predict(df)
        return df

    async def _store(self, df: pd.DataFrame):
        """[summary]

        :param df: [description]
        :type df: pd.DataFrame
        """
        await self.agent.connection.lazy_insert(df)
