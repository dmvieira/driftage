import json
from spade.behaviour import OneShotBehaviour
from spade.message import Message


class NotifyAnalysers(OneShotBehaviour):

    async def run(self):
        contact = self.template.to
        if self.agent.sent_data[contact][-1] == self.agent.cache[-1]:
            return

        to_send = []
        for item in self.agent.cache:
            if item in self.agent.sent_data[contact]:
                continue
            to_send.append(item)
        msg = Message(
            to=contact,
            body=json.dumps(to_send)
        )
        await self.send(msg)
        self.agent.sent_data[contact].expand(to_send)
