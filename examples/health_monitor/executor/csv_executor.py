import os
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
        super()__init__(is_available_cache_ttl=30)

    def is_available(self) -> bool:
        try:
            with open("/tmp/test", "w") as test:
                test.write("test")
            os.remove("/tmp/test")
            return True
        except Exception:
            return False

    async def drain(self, data: dict):
        with open(self.path, "a") as f:
            f.write(
                f"{data['timestamp']} {data['identifier']}, {data['predicted']}\n"
            )


executor = Executor(
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
