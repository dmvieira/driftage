from spade.behaviour import OneShotBehaviour


class WaitSubscriptions(OneShotBehaviour):

    def on_available(self, jid, stanza):
        """[summary]

        :param jid: [description]
        :type jid: [type]
        :param stanza: [description]
        :type stanza: [type]
        """
        self.agent.available_contacts[jid] = stanza

    def on_unavailable(self, jid, stanza):
        """[summary]

        :param jid: [description]
        :type jid: [type]
        :param stanza: [description]
        :type stanza: [type]
        """
        try:
            del self.agent.available_contacts[jid]
        except KeyError:
            pass

    async def run(self):
        """[summary]
        """
        self.presence.on_available = self.on_available
        self.presence.on_unavailable = self.on_unavailable
        self.presence.set_available()
