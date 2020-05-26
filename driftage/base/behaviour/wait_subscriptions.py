from spade.behaviour import OneShotBehaviour


class WaitSubscriptions(OneShotBehaviour):

    def on_subscribed(self, jid):
        """[summary]

        :param jid: [description]
        :type jid: [type]
        """
        self.agent.sent_data[jid] = self.agent.cache

    def on_unsubscribed(self, jid):
        """[summary]

        :param jid: [description]
        :type jid: [type]
        """
        del self.agent.sent_data[jid]

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
        del self.agent.available_contacts[jid]

    async def run(self):
        """[summary]
        """
        self.presence.approve_all = True
        self.presence.set_available()
        self.presence.on_subscribed = self.on_subscribed
        self.presence.on_unsubscribed = self.on_unsubscribed
        self.presence.on_available = self.on_available
        self.presence.on_unavailable = self.on_unavailable
