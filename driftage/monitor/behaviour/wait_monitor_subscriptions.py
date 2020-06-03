from driftage.base.behaviour.wait_subscriptions import WaitSubscriptions


class WaitMonitorSubscriptions(WaitSubscriptions):

    def on_subscribe(self, jid):
        """[summary]

        :param jid: [description]
        :type jid: [type]
        """
        self.presence.approve(jid)
        self.presence.subscribe(jid)

    async def run(self):
        """[summary]
        """
        self.presence.on_subscribe = self.on_subscribe
        await super().run()
