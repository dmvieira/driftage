from datetime import datetime
from driftage.planner.predictor import PlannerPredictor, PredictResult
from driftage.db.schema import table


class TestPlannerPredictor(PlannerPredictor):

    def predict_period(self):
        return 1

    async def predict(self):
        data = await self.connection.get(
            datetime(1970, 1, 1), datetime.utcnow())
        identifiers = data[table.c.driftage_identifier.name].unique().values()
        result = []
        for identifier in identifiers:
            result.append(
                PredictResult(
                    identifier=identifier,
                    predicted=True,
                    should_send=True
                )
            )
        return result
