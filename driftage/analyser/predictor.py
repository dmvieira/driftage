from typing import List, Optional
from abc import abstractmethod
from pandas import DataFrame
from driftage.base.predictor import Predictor


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

    def fit(self):
        """Load new model or get old data for model retrain.
        If you set None to retrain_period, than you can ignore
        this function on inheritance.
        """
        pass

    @abstractmethod
    def predict(self, X: DataFrame) -> List[bool]:
        """Receives Pandas DataFrame and
        predicts if new data is a Concept Drift of not.
        DataFrame has the same schema as Database Schema,
        but without predict result.

        :param X: Data to be predicted as Concept Drift
        :type X: DataFrame
        :raises NotImplementedError: Need to be implemented when override
        :return: Predictions for that DataFrame as a List if is drift or not
        :rtype: List[bool]
        """
        raise NotImplementedError
