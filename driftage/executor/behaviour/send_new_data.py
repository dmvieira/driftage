import orjson
from spade.behaviour import OneShotBehaviour
from driftage.base.conf import getLogger


class SendNewData(OneShotBehaviour):

    _logger = getLogger("send_new_data")

    async def run(self):
        """[summary]
        """
        body = orjson.loads(self.template.body)
        for msg in body:
            if self.agent.sink.is_available():
                await self.agent.sink.drain(msg)
                self._logger.debug(f"Message sent to Sink {msg}")
