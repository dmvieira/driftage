from asynctest import TestCase
from driftage.executor.retry_config import RetryConfig


class TestRetryConfig(TestCase):

    async def func(self):
        pass

    def test_should_return_decorator_for_retry(self):
        retry = RetryConfig()
        decorator = retry(self.func)
        self.assertTrue(callable(decorator))
