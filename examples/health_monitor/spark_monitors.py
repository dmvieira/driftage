import time
from driftage.monitor import Monitor
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType


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


class MonitorManager:
    """Examples using files from dataset
    https://archive.ics.uci.edu/ml/datasets/EMG+Physical+Action+Data+Set
    """

    def open(self, partition_id, epoch_id):

        self.monitors = []
        for identifier in ROWS:
            monitor = Monitor("monitor@localhost", "passw0rd", identifier)
            monitor.start()

            self.monitors.append(monitor)
        while not all([m.is_alive() for m in self.monitors]):
            time.sleep(0.1)
            print("Waiting all monitors alive")
        print("All monitors alive, starting...")
        
    def process(self, row):
        for monitor in self.monitors:
            monitor(
                dict(sensor=row[monitor._identifier])
            )

    def close(self, error):
        print("Closing all monitors")
        if error:
            print(f"Got error {error}")
        for monitor in self.monitors:
            monitor.stop()

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