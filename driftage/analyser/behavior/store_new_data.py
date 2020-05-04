from spade.behaviour import OneShotBehaviour


class StoreNewData(OneShotBehaviour):
    async def run(self):
        body = self.template.body
        # parse
        # call predict
        # store
        for msg in body:
            data = msg["data"]
            metadata = msg["metadata"]
            timestamp = metadata["timestamp"]
            await self.parse(data, metadata, timestamp)

    async def parse(self, data, metadata, timestamp):
        pass
