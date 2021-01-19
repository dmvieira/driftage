import os
import time
import logging
from typing import List
from datetime import datetime
from driftage.planner import Planner
from driftage.planner.predictor import PlannerPredictor, PredictResult
from driftage.db.connection import Connection
from driftage.db.schema import table
from sqlalchemy import create_engine

logger = logging.getLogger("voting_planner")
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class VotingPredictor(PlannerPredictor):

    start_time = datetime.utcnow()
    last_time = datetime.utcnow()
    voting_low_threashold = 2
    voting_high_threashold = 7

    @property
    def predict_period(self):
        return 1

    async def predict(self) -> List[PredictResult]:
        now = datetime.utcnow()
        logger.debug(
            f"Starting prediction from dates {self.last_time} and {now}")
        df = await self.connection.get_between(
            table.c.driftage_datetime_analysed, self.last_time, now)
        result = []
        if df.empty:
            return result

        self.last_time = now

        columns = [
            table.c.driftage_identifier.name, table.c.driftage_predicted.name]

        from_now_df = df[
            df[table.c.driftage_datetime_monitored.name] > self.start_time
        ]
        drifts = from_now_df[columns].groupby(
            table.c.driftage_identifier.name).sum().to_dict()
        drift_prediction = drifts[table.c.driftage_predicted.name]

        voting_counter = 0
        for identifier, prediction in drift_prediction.items():
            result.append(
                PredictResult(identifier, prediction, bool(prediction))
            )
            voting_counter += bool(prediction)
        if ((self.voting_low_threashold >= voting_counter) or
                (voting_counter >= self.voting_high_threashold)):
            result = []
        logger.debug(f"Sending Result {result}")
        return result


engine = create_engine(os.environ["KB_CONNECTION_STRING"])

connection = Connection(engine, bulk_size=10, bulk_time=1)
predictor = VotingPredictor(connection)

planner = Planner(  # nosec
    "planner@localhost",
    os.environ["PLANNER_PASSWORD"],
    predictor,
    ["executor@localhost"])

logger.info("Waiting Ejabberd...")
time.sleep(25)
logger.info("Starting planner...")
planner.start()
logger.info("Planner alive")

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
planner.stop()
logger.info("Planner stopped")
