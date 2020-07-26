from datetime import datetime
from driftage.planner.predictor import PlannerPredictor, PredictResult
from driftage.db.schema import table


class HelperPlannerPredictor(PlannerPredictor):

    send = True

    @property
    def predict_period(self):
        return 1

    async def predict(self):
        data = await self.connection.get_between(
            table.c.driftage_datetime_monitored,
            datetime(1970, 1, 1), datetime.utcnow())
        result = []
        if not data.empty:
            identifiers = data[table.c.driftage_identifier.name].unique()
            for identifier in identifiers:
                result.append(
                    PredictResult(
                        identifier=identifier,
                        predicted=True,
                        should_send=self.send
                    )
                )
        return result
