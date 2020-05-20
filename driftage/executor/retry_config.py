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
        """[summary]

        :param send_timeout: [description], defaults to 1.0
        :type send_timeout: Optional[Union[int, float]], optional
        :param retry_backoff: [description], defaults to 1.0
        :type retry_backoff: Union[int, float], optional
        :param max_tries: [description], defaults to 3
        :type max_tries: int, optional
        :param all_tries_timeout: [description], defaults to None
        :type all_tries_timeout: Optional[Union[int, float]], optional
        :param retry_exceptions: [description], defaults to (Exception,)
        :type retry_exceptions: Tuple[Exception], optional
        """
        self._decorator = asyncbackoff(
            attempt_timeout=send_timeout,
            deadline=all_tries_timeout,
            pause=retry_backoff,
            max_tries=max_tries,
            exceptions=retry_exceptions
        )

    def __call__(self):
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        return self._decorator
