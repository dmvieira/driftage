from collections import deque
from spade.agent import Agent
from driftage.base.behaviour.wait_subscriptions import WaitSubscriptions


class Collector(Agent):
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
        super().__init__(jid, password, verify_security)

    @property
    def available_contacts(self):
        return self._contacts

    @property
    def sent_data(self):
        return self._sent_data

    @property
    def cache(self):
        return self._cache

    async def setup(self):
        self.add_behaviour(WaitSubscriptions())
