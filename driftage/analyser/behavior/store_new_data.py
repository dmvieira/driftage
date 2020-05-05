import json
import pandas as pd
from datetime import datetime
from spade.behaviour import OneShotBehaviour


class StoreNewData(OneShotBehaviour):
    async def run(self):
        body = json.loads(self.template.body)
        for msg in body:
            data = msg["data"]
            metadata = msg["metadata"]
            timestamp = metadata["timestamp"]
            identifier = metadata["identifier"]
            df = await self._parse(data, timestamp, identifier)
            predicted_df = await self._predict(df)
            await self._store(predicted_df)

    async def _parse(
            self,
            data: dict,
            timestamp: float,
            identifier: str) -> pd.DataFrame:
        return pd.DataFrame(
            [data, datetime.fromtimestamp(timestamp), identifier],
            columns=(
                "driftage_data",
                "driftage_timestamp",
                "driftage_identifier")
        )

    async def _predict(self, df: pd.DataFrame) -> pd.DataFrame:
        df["driftage_predicted"] = self.agent.predictor.predict(df)
        return df

    async def _store(self, df: pd.DataFrame):
        self.agent.connection.lazy_insert(df)
