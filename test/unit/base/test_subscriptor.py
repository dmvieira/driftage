from asynctest import TestCase
from driftage.base.agent.subscriptor import Subscriptor


class TestSubscriptor(TestCase):

    def setUp(self):
        self.collector = Subscriptor("user_test", "pass_test")

    def tearDown(self):
        self.collector.container.stop()

    async def test_should_up_without_crash(self):
        await self.collector.setup()
