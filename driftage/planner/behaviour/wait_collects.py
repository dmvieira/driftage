from collections import deque
from driftage.base.behaviour.wait_subscriptions import WaitSubscriptions


class WaitCollects(WaitSubscriptions):

    def on_available(self, jid, stanza):
        """[summary]

        :param jid: [description]
        :type jid: [type]
        :param stanza: [description]
        :type stanza: [type]
        """
        self.agent.sent_data[jid] = deque(
            [id(cache) for cache in self.agent.cache],
            self.agent.cache.maxlen
        )
        super().on_available(jid, stanza)

    def on_unavailable(self, jid, stanza):
        """[summary]

        :param jid: [description]
        :type jid: [type]
        :param stanza: [description]
        :type stanza: [type]
        """
        try:
            del self.agent.sent_data[jid]
        except KeyError:
            pass
        super().on_unavailable(jid, stanza)
