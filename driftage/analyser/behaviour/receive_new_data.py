from spade.behaviour import CyclicBehaviour
from spade.template import Template
from driftage.analyser.behaviour.store_new_data import StoreNewData
from driftage.base.conf import getLogger


class ReceiveNewData(CyclicBehaviour):

    _logger = getLogger("receive_new_data")

    async def run(self):
        """[summary]
        """
        msg = await self.receive(timeout=10)
        if msg:
            self.agent.add_behaviour(StoreNewData(), Template(body=msg.body))
            self._logger.debug(f"Message received {msg.body}")
