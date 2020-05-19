from spade.behaviour import CyclicBehaviour
from spade.template import Template
from driftage.executor.behaviour.send_new_data import SendNewData


class ReceiveNewData(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg:
            self.agent.add_behaviour(SendNewData(), Template(body=msg.body))
