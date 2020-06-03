from spade.behaviour import OneShotBehaviour
from spade.message import Message


class FastNotifyContacts(OneShotBehaviour):

    async def run(self):
        """[summary]
        """
        for contact in self.agent.available_contacts:
            msg = Message(
                to=contact,
                body=self.template.body
            )
            await self.send(msg)
