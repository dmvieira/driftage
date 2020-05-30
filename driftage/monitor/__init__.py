from typing import Optional
from driftage.base.agent.collector import Collector
from driftage.base.behaviour.notify_contacts import NotifyContacts
from driftage.monitor.behaviour.wait_monitor_subscriptions import (
    WaitMonitorSubscriptions)
from datetime import datetime


class Monitor(Collector):
    def __init__(
            self,
            jid: str,
            password: str,
            identifier: Optional[str] = None,
            cache_max_size: int = 10,
            verify_security: bool = False
    ):
        """[summary]

        :param jid: [description]
        :type jid: str
        :param password: [description]
        :type password: str
        :param identifier: [description], defaults to None
        :type identifier: Optional[str], optional
        :param cache_max_size: [description], defaults to 10
        :type cache_max_size: int, optional
        :param verify_security: [description], defaults to False
        :type verify_security: bool, optional
        """
        super().__init__(jid, password, cache_max_size, verify_security)
        self._identifier = identifier if identifier else self.name

    async def setup(self):
        """[summary]
        """
        self.add_behaviour(WaitMonitorSubscriptions())

    def collect(self, data: dict):
        """[summary]

        :param data: [description]
        :type data: dict
        """
        self._cache.append({
            "data": data,
            "metadata": {
                "timestamp": datetime.utcnow().timestamp(),
                "identifier": self._identifier
            }
        })
        self.add_behaviour(NotifyContacts())

    __call__ = collect
