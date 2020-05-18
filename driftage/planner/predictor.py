from typing import List
from abc import abstractmethod
from dataclasses import dataclass
from driftage.base.predictor import Predictor


@dataclass
class PredictResult:
    identifier: str
    predicted: bool


class PlannerPredictor(Predictor):

    @property
    @abstractmethod
    def predict_period(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def predict(self) -> List[PredictResult]:
        raise NotImplementedError
