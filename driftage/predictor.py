from abc import ABCMeta, abstractmethod
from pandas import DataFrame, Series
from driftage.db.connection import Connection


class Predictor(metaclass=ABCMeta):

    @property
    @abstractmethod
    def retrain_period(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def fit(self, connection: Connection):
        raise NotImplementedError

    @abstractmethod
    def predict(self, X: DataFrame) -> Series:
        raise NotImplementedError
