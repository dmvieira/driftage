import json
import pylru
from spade.agent import Agent
from driftage.monitor.behavior.wait_subscriptions import WaitSubscriptions
from datetime import datetime


class Monitor(Agent):
    def __init__(
            self,
            jid: str,
            password: str,
            verify_security: bool = False,
            cache_max_size: int = 3):

        self._cache = pylru.lrucache(cache_max_size)
        super(Monitor, self).__init__(jid, password, verify_security)

    @property
    def cache(self):
        return json.dumps(dict(self._cache.items()))

    async def setup(self):
        self.add_behaviour(WaitSubscriptions)

    def __call__(self, data):
        self._cache[datetime.timestamp()] = data
