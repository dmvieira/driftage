from typing import List
from abc import abstractmethod
from pandas import DataFrame
from driftage.base.predictor import Predictor


class AnalyserPredictor(Predictor):

    @property
    @abstractmethod
    def retrain_period(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def fit(self):
        raise NotImplementedError

    @abstractmethod
    def predict(self, X: DataFrame) -> List[bool]:
        raise NotImplementedError
