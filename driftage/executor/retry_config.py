from aiomisc import asyncbackoff
from typing import Union, Tuple, Optional, Callable


class RetryConfig:
    def __init__(
            self,
            send_timeout: Optional[Union[int, float]] = 1.0,
            retry_backoff: Union[int, float] = 1.0,
            max_tries: int = 3,
            all_tries_timeout: Optional[Union[int, float]] = None,
            retry_exceptions: Tuple[Exception] = (Exception,)):
        """Retry configuration for Sink connection. configuring
        this retry it will be resilient when sending data to Sink.

        :param send_timeout: All timeouts when send in seconds,
            defaults to 1.0
        :type send_timeout: Optional[Union[int, float]], optional
        :param retry_backoff: Time to wait to another try in seconds,
            defaults to 1.0
        :type retry_backoff: Union[int, float], optional
        :param max_tries: Maximum number of tries, defaults to 3
        :type max_tries: int, optional
        :param all_tries_timeout: Total timeout from all retries in seconds,
            defaults to None
        :type all_tries_timeout: Optional[Union[int, float]], optional
        :param retry_exceptions: Exceptions that we should take in account
            to retry, defaults to (Exception,)
        :type retry_exceptions: Tuple[Exception], optional
        """
        self._decorator = asyncbackoff(
            attempt_timeout=send_timeout,
            deadline=all_tries_timeout,
            pause=retry_backoff,
            max_tries=max_tries,
            exceptions=retry_exceptions
        )

    def __call__(self, fn: Callable) -> Callable:
        """Retry decorator for Sink functions (internally used)

        :type fn: Callable, optional
        :param fn: function to decorate
        :return: Decorated function with retries
        :rtype: Callable
        """
        return self._decorator(fn)
