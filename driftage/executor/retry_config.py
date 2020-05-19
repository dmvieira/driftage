from aiomisc import asyncbackoff
from typing import Union, Tuple, Optional


class RetryConfig:
    def __init__(
            self,
            send_timeout: Optional[Union[int, float]] = 1.0,
            retry_backoff: Union[int, float] = 1.0,
            max_tries: int = 3,
            all_tries_timeout: Optional[Union[int, float]] = None,
            retry_exceptions: Tuple[Exception] = (Exception,)):

        self._decorator = asyncbackoff(
            attempt_timeout=send_timeout,
            deadline=all_tries_timeout,
            pause=retry_backoff,
            max_tries=max_tries,
            exceptions=retry_exceptions
        )

    def __call__(self):
        return self._decorator
