from typing import Any
from collections import deque
from spade.agent import Agent
from spade.template import Template
from driftage.monitor.behavior.wait_subscriptions import WaitSubscriptions
from driftage.monitor.behavior.notify_analysers import NotifyAnalysers
from datetime import datetime


class Monitor(Agent):
    def __init__(
            self,
            jid: str,
            password: str,
            cache_max_size: int = 10,
            verify_security: bool = False
    ):

        self._cache = deque([], cache_max_size)
        self._contacts = {}
        self._sent_data = {}
        super(Monitor, self).__init__(jid, password, verify_security)

    @property
    def available_contacts(self):
        return self._contacts

    @property
    def sent_data(self):
        return self._sent_data

    @property
    def cache(self):
        return self._cache.copy()

    async def setup(self):
        self.add_behaviour(WaitSubscriptions())

    def collect(self, data: Any):
        template = Template()
        self._cache.append({
            "data": data,
            "metadata": {
                "timestamp": datetime.now().timestamp()
            }
        })
        for contact in self.available_contacts:
            template.to = contact
            self.add_behaviour(NotifyAnalysers(), template)

    __call__ = collect
