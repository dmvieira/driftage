from typing import List, Union
from abc import abstractmethod
from dataclasses import dataclass
from driftage.base.predictor import Predictor


@dataclass
class PredictResult:
    """[summary]
    """
    identifier: str
    predicted: Union[bool, str, int, float]
    should_send: bool


class PlannerPredictor(Predictor):

    @property
    @abstractmethod
    def predict_period(self) -> int:
        """[summary]

        :raises NotImplementedError: [description]
        :return: [description]
        :rtype: int
        """
        raise NotImplementedError

    @abstractmethod
    async def predict(self) -> List[PredictResult]:
        """[summary]

        :raises NotImplementedError: [description]
        :return: [description]
        :rtype: List[PredictResult]
        """
        raise NotImplementedError
