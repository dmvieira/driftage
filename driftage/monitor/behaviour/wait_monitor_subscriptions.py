from driftage.base.behaviour.wait_subscriptions import WaitSubscriptions
from driftage.base.conf import getLogger


class WaitMonitorSubscriptions(WaitSubscriptions):

    _logger = getLogger("wait_monitor_subscriptions")

    def on_subscribe(self, jid: str):
        """[summary]

        :param jid: [description]
        :type jid: [str]
        """
        self.presence.approve(jid)
        self.presence.subscribe(jid)
        self._logger.debug(f"Approved and subscribing to {jid}")

    async def run(self):
        """[summary]
        """
        self.presence.on_subscribe = self.on_subscribe
        await super().run()
