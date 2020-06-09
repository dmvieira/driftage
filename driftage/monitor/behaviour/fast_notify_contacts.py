from spade.behaviour import OneShotBehaviour
from spade.message import Message
from driftage.base.conf import getLogger


class FastNotifyContacts(OneShotBehaviour):

    _logger = getLogger("fast_notify_contacts")

    async def run(self):
        """[summary]
        """
        for contact in self.agent.available_contacts:
            msg = Message(
                to=contact,
                body=self.template.body
            )
            await self.send(msg)
        self._logger.debug(f"Sent {self.template.body} to all contacts")
