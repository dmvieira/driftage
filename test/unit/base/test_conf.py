from unittest import TestCase
from driftage.base.conf import getLogger


class TestConf(TestCase):

    def test_should_return_child_log(self):
        logger = getLogger("test")
        self.assertEqual(logger.name, "driftage.test")
        self.assertEqual(logger.level, 20)

    def test_should_return_child_log_with_new_level(self):
        logger = getLogger("test", "DEBUG")
        self.assertEqual(logger.name, "driftage.test")
        self.assertEqual(logger.level, 10)