import json
from spade.behaviour import OneShotBehaviour


class SendNewData(OneShotBehaviour):
    async def run(self):
        """[summary]
        """
        body = json.loads(self.template.body)
        for msg in body:
            if self.agent.sink.is_available():
                await self.agent.sink.drain(msg)
