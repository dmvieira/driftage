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
        """[summary]

        :param circuit_breaker: [description], defaults to CircuitBreaker()
        :type circuit_breaker: CircuitBreaker, optional
        :param is_available_cache_ttl: [description], defaults to 1.0
        :type is_available_cache_ttl: Union[int, float], optional
        :param retry_config: [description], defaults to RetryConfig()
        :type retry_config: RetryConfig, optional
        """
        self.is_available = TTLCache(
            1, is_available_cache_ttl)(self.is_available)
        self.drain = circuit_breaker(retry_config(self.drain))

    @abstractmethod
    def is_available(self) -> bool:
        """[summary]

        :raises NotImplementedError: [description]
        :return: [description]
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    async def drain(self, data: dict):
        """[summary]

        :param data: [description]
        :type data: dict
        :raises NotImplementedError: [description]
        """
        raise NotImplementedError
