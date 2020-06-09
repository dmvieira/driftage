from spade.behaviour import CyclicBehaviour
from spade.template import Template
from driftage.executor.behaviour.send_new_data import SendNewData
from driftage.base.conf import getLogger


class ReceiveNewData(CyclicBehaviour):

    _logger = getLogger("receive_new_data")

    async def run(self):
        """[summary]
        """
        msg = await self.receive(timeout=10)
        if msg:
            self.agent.add_behaviour(SendNewData(), Template(body=msg.body))
            self._logger.debug(f"Message received {msg.body}")
