from typing import Optional
from driftage.base.agent.collector import Collector
from driftage.base.behaviour.notify_contacts import NotifyContacts
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
        super().__init__(jid, password, cache_max_size, verify_security)
        self._identifier = identifier if identifier else self.name

    def collect(self, data: dict):
        self._cache.append({
            "data": data,
            "metadata": {
                "timestamp": datetime.now().timestamp(),
                "identifier": self._identifier
            }
        })
        self.add_behaviour(NotifyContacts())

    __call__ = collect
