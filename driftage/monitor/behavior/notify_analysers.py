from spade.behaviour import OneShotBehaviour
from spade.message import Message


class NotifyAnalysers(OneShotBehaviour):

    async def run(self):
        msg = Message(
            to=self.template.to,
            body=self.agent.cache,
            metadata=self.template.metadata
        )
        await self.send(msg)
