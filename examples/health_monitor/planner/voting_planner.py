import os
import logging
from datetime import datetime, timedelta
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

    voting_threashold = 2

    @property
    def predict_period(self):
        return 5

    async def predict(self) -> List[PredictResult]:
        now = datetime.utcnow()
        df = await self.connection.get_between(now - timedelta(seconds=5), now)
        result = []
        if df.empty:
            return result
        columns = [
            table.c.driftage_identifier.name, table.c.driftage_predicted.name]
        drifts = df[columns].groupby(
            table.c.driftage_identifier.name).sum().to_dict()
        drift_prediction = drifts[table.c.driftage_predicted.name]

        voting_counter = 0
        for identifier, prediction in drift_prediction.items():
            result.append(
                PredictResult(identifier, prediction, bool(prediction))
            )
            voting_counter += bool(prediction)
        if voting_counter < self.voting_threashold:
            result = []
        return result



engine = create_engine(os.environ["KB_CONNECTION_STRING"])

connection = Connection(engine, bulk_size=10)
predictor = VotingPredictor(connection)

planner = Planner(
    "planner@localhost",
    os.environ["PLANNER_PASSWORD"],
    predictor,
    connection,
    ["executor@localhost"])

logger.info("Waiting Ejabberd...")
time.sleep(10)
while not planner.is_alive():
    logger.info("Starting planner...")
    planner.start()
    time.sleep(1)
    while not all([contact.get("presence", False) for contact in planner.presence.get_contacts().values()]):
        analyser.stop()
        logger.info("Waiting executors...")
        time.sleep(1)

logger.info("Planner alive")
