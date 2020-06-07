import logging
import json
from driftage.executor import Sink


class TestSink(Sink):

    logger = logging.getLogger("test_sink")
    logger.setLevel("INFO")

    def is_available(self):
        return True

    async def drain(self, data: dict):
        self.logger.info(json.dumps(data))
