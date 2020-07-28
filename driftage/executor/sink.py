from typing import Union
from abc import abstractmethod
from aiobreaker import CircuitBreaker
from cachetools import TTLCache, cached
from driftage.executor.retry_config import RetryConfig


class Sink:

    def __init__(
            self,
            circuit_breaker: CircuitBreaker = CircuitBreaker(),
            is_available_cache_ttl: Union[int, float] = 1.0,
            retry_config: RetryConfig = RetryConfig()):
        """Sink base class to implement custom Sinks like Kafka, RabbitMQ
        MariaDB, or even an API.

        :param circuit_breaker: Circuit breaker to protect Sink if it's down,
            defaults to CircuitBreaker()
        :type circuit_breaker: CircuitBreaker, optional
        :param is_available_cache_ttl: Healthcheck cache means the time to
            is_available method in how many seconds, defaults to 1.0
        :type is_available_cache_ttl: Union[int, float], optional
        :param retry_config: Retry configuration to send data to Sink,
            defaults to RetryConfig()
        :type retry_config: RetryConfig, optional
        """
        cache = TTLCache(1, is_available_cache_ttl)
        self.is_available = cached(cache)(self.is_available)
        self.drain = circuit_breaker(retry_config(self.drain))

    @abstractmethod
    def is_available(self) -> bool:
        """Healthcheck function to know if Sink is available to receive data.

        :raises NotImplementedError: Needs to be implemented when overridden
        :return: True if it is available or False if not
        :rtype: bool
        """
        raise NotImplementedError

    @abstractmethod
    async def drain(self, data: dict):
        """Method that sends data to the Sink.
        This receives predicted data from the Planner and sends it out.

        :param data: Predicted data with timestamp, predicted and identifier
        :type data: dict
        :raises NotImplementedError: Needs to be implemented when overridden
        """
        raise NotImplementedError
