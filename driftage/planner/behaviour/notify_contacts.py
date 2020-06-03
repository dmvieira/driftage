import json
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class NotifyContacts(OneShotBehaviour):

    async def run(self):
        """[summary]
        """
        for contact in self.agent.available_contacts:
            contact_data = self.agent.sent_data[contact]
            if ((len(contact_data) > 0) and
                    (contact_data[-1] == id(self.agent.cache[-1]))):
                continue

            to_send = []
            to_send_id = []
            for item in self.agent.cache:
                if id(item) in contact_data:
                    continue
                to_send.append(item)
                to_send_id.append(id(item))
            msg = Message(
                to=contact,
                body=json.dumps(to_send)
            )
            await self.send(msg)
            self.agent.sent_data[contact].extend(to_send_id)
