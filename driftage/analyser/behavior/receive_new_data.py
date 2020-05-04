from spade.behaviour import CyclicBehaviour
from spade.template import Template
from driftage.analyser.behavior.store_new_data import StoreNewData


class ReceiveNewData(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg:
            self.agent.add_behaviour(StoreNewData(), Template(body=msg.body))
