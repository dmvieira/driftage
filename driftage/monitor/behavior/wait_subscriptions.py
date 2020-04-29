from spade.behaviour import OneShotBehaviour
from spade.template import Template
from driftage.monitor.behavior.notify_analysers import NotifyAnalysers


class WaitSubscriptions(OneShotBehaviour):
    def on_subscribe(self, jid):
        self.presence.approve(jid)
        self.presence.subscribe(jid)

    def on_available(self, jid, stanza):
        template = Template(to=jid, sender=self.agent.jid)
        template.set_metadata("performative", "inform")
        self.agent.add_behaviour(NotifyAnalysers(), template)

    async def run(self):
        self.presence.set_available()
        self.presence.on_subscribe = self.on_subscribe
        self.presence.on_available = self.on_available
