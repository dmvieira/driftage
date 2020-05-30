from asynctest import TestCase
from driftage.base.agent.collector import Collector


class TestCollector(TestCase):

    def setUp(self):
        self.collector = Collector("user_test", "pass_test")

    def tearDown(self):
        self.collector.container.stop()

    async def test_should_up_without_crash(self):
        await self.collector.setup()
