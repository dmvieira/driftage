from spade.behaviour import OneShotBehaviour
from aioxmpp import Presence
from driftage.base.conf import getLogger


class WaitSubscriptions(OneShotBehaviour):

    _logger = getLogger("wait_subscriptions")

    def on_available(self, jid: str, stanza: Presence):
        """[summary]

        :param jid: [description]
        :type jid: [str]
        :param stanza: [description]
        :type stanza: [Presence]
        """
        self.agent.available_contacts[jid] = stanza
        self._logger.debug(f"Contact added {jid}")

    def on_unavailable(self, jid: str, stanza: Presence):
        """[summary]

        :param jid: [description]
        :type jid: [str]
        :param stanza: [description]
        :type stanza: [Presence]
        """
        try:
            del self.agent.available_contacts[jid]
            self._logger.debug(f"Contact removed {jid}")
        except KeyError:
            pass

    async def run(self):
        """[summary]
        """
        self.presence.on_available = self.on_available
        self.presence.on_unavailable = self.on_unavailable
        self.presence.set_available()
