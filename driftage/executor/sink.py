from typing import Union
from abc import abstractmethod
from aiobreaker import CircuitBreaker
from cachetools import TTLCache
from driftage.executor.retry_config import RetryConfig


class Sink:

    def __init__(
            self,
            circuit_breaker: CircuitBreaker = CircuitBreaker(),
            is_available_cache_ttl: Union[int, float] = 1.0,
            retry_config: RetryConfig = RetryConfig()):
        self.is_available = TTLCache(
            1, is_available_cache_ttl)(self.is_available)
        self.drain = circuit_breaker(retry_config(self.drain))

    @abstractmethod
    def is_available(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def drain(self, data: dict):
        raise NotImplementedError
