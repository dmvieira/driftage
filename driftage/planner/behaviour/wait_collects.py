from collections import deque
from aioxmpp import Presence
from driftage.base.behaviour.wait_subscriptions import WaitSubscriptions


class WaitCollects(WaitSubscriptions):

    def on_available(self, jid: str, stanza: Presence):
        """[summary]

        :param jid: [description]
        :type jid: [str]
        :param stanza: [description]
        :type stanza: [Presence]
        """
        self.agent.sent_data[jid] = deque(
            [id(cache) for cache in self.agent.cache],
            self.agent.cache.maxlen
        )
        super().on_available(jid, stanza)

    def on_unavailable(self, jid: str, stanza: Presence):
        """[summary]

        :param jid: [description]
        :type jid: [str]
        :param stanza: [description]
        :type stanza: [Presence]
        """
        try:
            del self.agent.sent_data[jid]
        except KeyError:
            pass
        super().on_unavailable(jid, stanza)
