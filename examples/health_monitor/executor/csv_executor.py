import os
import time
import logging
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
            return True
        except Exception:
            return False

    async def drain(self, data: dict):
        logger.debug(f"Writing data: {data} to {self.path}")
        with open(self.path, "a") as f:
            f.write(
                f"{data['timestamp']} {data['identifier']}, "
                f"{data['predicted']}\n"
            )


executor = Executor(  # nosec
    "executor@localhost",
    os.environ["EXECUTOR_PASSWORD"],
    CsvSink("/tmp/output.csv"))

logger.info("Waiting Ejabberd...")
time.sleep(10)
executor.start()
while not executor.is_alive():
    logger.info("Starting executor...")
    time.sleep(1)

logger.info("Executor alive")
