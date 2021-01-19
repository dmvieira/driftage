import os
import time
import logging
from datetime import datetime
from driftage.executor import Executor
from driftage.executor.sink import Sink

logger = logging.getLogger("csv_executor")
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class CsvSink(Sink):

    def __init__(self, path: str):
        self.path = path
        super().__init__(is_available_cache_ttl=30)

    def is_available(self) -> bool:
        try:
            with open("/tmp/test", "w") as test:  # nosec
                test.write("test")
            os.remove("/tmp/test")  # nosec
            logger.debug("Filesystem is ok to write")
            return True
        except Exception as e:
            logger.debug(f"Error writing to filesystem {e}")
            return False

    async def drain(self, data: dict):
        logger.debug(f"Writing data: {data} to {self.path}")
        now = datetime.utcnow()
        with open(self.path, "a") as f:
            f.write(
                f"{data['timestamp']}, {data['identifier']}, "
                f"{data['predicted']}, {now}\n"
            )


executor = Executor(  # nosec
    "executor@localhost",
    os.environ["EXECUTOR_PASSWORD"],
    CsvSink("/tmp/output.csv"))

logger.info("Waiting Ejabberd...")
time.sleep(25)
executor.start()
logger.info("Executor alive")

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
executor.stop()
logger.info("Executor stopped")
