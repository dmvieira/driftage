from typing import List, Union
from abc import abstractmethod, abstractproperty
from dataclasses import dataclass
from driftage.base.predictor import Predictor


@dataclass
class PredictResult:
    """Dataclass to store each prediction,
    result and if this prediction should be sent to Executor.

    :param identifier: Data identifier that comes from Monitor or any
        identifier you want.
    :type identifier: str
    :param predicted: Value predicted from Drift detection algorithm. This can
        even inform type of drift to Executor.
    :type predicted: Union[bool, str, int, float]
    :param should_send: If this prediction should be sent to Executor.
        Sometimes your Planner can decide to not send it because of time or
        other business rules.
    :type should_send: bool
    """
    identifier: str
    predicted: Union[bool, str, int, float]
    should_send: bool


class PlannerPredictor(Predictor):

    @abstractproperty
    def predict_period(self) -> Union[float, int]:
        """Predict time period (in seconds).
        This property defines how long PlannerPredictor will wait
        until next predict call.

        :raises NotImplementedError:  Needs to be implemented when overridden
        :return: Time it takes to wait for predict in seconds
        :rtype: Union[float, int]
        """
        raise NotImplementedError

    @abstractmethod
    async def predict(self) -> List[PredictResult]:
        """Using data stored on KB predicts if this data is a
        Concept Drift of not, to then send or not to the Executor.

        :raises NotImplementedError:  Needs to be implemented when overridden
        :return: Results predicted that should or shouldn't be sent to
            the Executor
        :rtype: List[PredictResult]
        """
        raise NotImplementedError
