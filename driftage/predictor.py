from abc import ABCMeta, abstractmethod
from pandas import DataFrame, Series


class Predictor(metaclass=ABCMeta):

    @property
    @abstractmethod
    def retrain_period(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def fit(self, X: DataFrame) -> 'Predictor':
        raise NotImplementedError

    @abstractmethod
    def predict(self, X: DataFrame) -> Series:
        raise NotImplementedError
