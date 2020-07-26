import os
import time
import logging
from driftage.monitor import Monitor
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType

logger = logging.getLogger("spark_monitor")
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


ROWS = [
    "right_bicep",
    "right_tricep",
    "left_bicep",
    "left_tricep",
    "right_thigh",
    "right_hamstring",
    "left_thigh",
    "left_hamstring"
]

healthSchema = StructType()
for row in ROWS:
    healthSchema.add(row, "integer")


class MonitorManager():
    """Examples using files from dataset
    https://archive.ics.uci.edu/ml/datasets/EMG+Physical+Action+Data+Set
    """

    def open(self, partition_id, epoch_id):

        self.monitors = []
        for identifier in ROWS:
            monitor = Monitor("monitor@localhost",  # nosec
                              os.environ["MONITOR_PASSWORD"], identifier)
            monitor.start()

            self.monitors.append(monitor)
        while not all([m.is_alive() for m in self.monitors]):
            time.sleep(1)
            print("Waiting all monitors alive")
        while not all([bool(m.available_contacts) for m in self.monitors]):
            time.sleep(1)
            print(
                "Waiting analysers connected "
                f"{[len(m.available_contacts) for m in self.monitors]}")
        print("All monitors alive, starting...")
        return True

    def process(self, row):
        for monitor in self.monitors:
            monitor(
                dict(sensor=row[monitor._identifier])
            )
        time.sleep(0.001)  # simulating milisseconds

    def close(self, error):
        print("Closing all monitors...")
        if error:
            print(f"Got error {error}")
        for monitor in self.monitors:
            while not all([b.is_done() for b in monitor.behaviours]):
                left = sum([not b.is_done() for b in monitor.behaviours])
                print(f"Waiting monitors stop to send... {left} left")
                time.sleep(1)
            monitor.stop()
        print("All monitors stopped!")


spark = SparkSession \
    .builder \
    .appName("ProcessHealthData") \
    .getOrCreate()

lines = spark \
    .readStream \
    .option("sep", "\t") \
    .schema(healthSchema) \
    .csv("data/")

query = lines.writeStream.foreach(MonitorManager()).start()

query.awaitTermination()
