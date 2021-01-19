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

        self.monitor = Monitor("monitor@localhost",  # nosec
                               os.environ["MONITOR_PASSWORD"], ROWS[0])
        self.monitor.start()

        while not self.monitor.is_alive():
            time.sleep(1)
            print("Waiting monitor alive")
        while not bool(self.monitor.available_contacts):
            time.sleep(1)
            print(
                "Waiting analyser connected "
                f"{len(self.monitor.available_contacts)}")
        print("Monitor alive, starting...")
        return True

    def process(self, row):
        self.monitor(
            dict(sensor=row[self.monitor._identifier])
        )

    def close(self, error):
        print("Closing monitor...")
        if error:
            print(f"Got error {error}")
        while not all([b.is_done() for b in self.monitor.behaviours]):
            left = sum([not b.is_done() for b in self.monitor.behaviours])
            print(f"Waiting monitor stop to send... {left} left")
            time.sleep(1)
        self.monitor.stop()
        print("Monitor stopped!")


time.sleep(5)

spark = SparkSession \
    .builder \
    .appName("ProcessHealthDataSimple") \
    .getOrCreate()

lines = spark \
    .readStream \
    .option("sep", "\t") \
    .schema(healthSchema) \
    .csv("data/")

query = lines.writeStream.foreach(MonitorManager()).start()

query.awaitTermination(1000)
print("done")
