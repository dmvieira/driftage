from typing import Optional
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from driftage.base.predictor import Predictor


@dataclass
class PredictionData:
    """Dataclass to stores data to predict.

    :param data: Data that comes from Monitor.
    :type data: dict
    :param created_at: Datetime object that message was created.
    :type created_at: datetime
    :param identifier: Data identifier that comes from Monitor or any
        identifier you want.
    :type identifier: str
    """
    data: dict
    timestamp: datetime
    identifier: str


class AnalyserPredictor(Predictor):

    def retrain_period(self) -> Optional[int]:
        """Retrain time period (in seconds).
        This property defines how long AnalyserPredictor will wait
        until next fit call.
        Retrain is optional and if returns None, fit method is
        never called.

        :return: Time to wait for retrain in seconds or None if no retrain
        :rtype: Optional[int]
        """
        return None

    async def fit(self):
        """Load new model or get old data for model retrain.
        If you set None to retrain_period, than you can ignore
        this function on inheritance.
        """
        pass

    @abstractmethod
    async def predict(self, X: PredictionData) -> bool:
        """Receives PredictionData and
        predicts if new data is a Concept Drift of not.

        :param X: Data to be predicted as Concept Drift
        :type X: PredictionData
        :raises NotImplementedError: Need to be implemented when override
        :return: Prediction for that PredictionData if is drift or not
        :rtype: bool
        """
        raise NotImplementedError
