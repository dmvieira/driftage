from asynctest import TestCase
from driftage.executor.retry_config import RetryConfig


class TestRetryConfig(TestCase):

    def test_should_return_decorator_for_retry(self):
        retry = RetryConfig()
        decorator = retry()
        self.assertTrue(callable(decorator))
