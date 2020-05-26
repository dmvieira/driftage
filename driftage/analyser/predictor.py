from typing import List, Optional
from abc import abstractmethod
from pandas import DataFrame
from driftage.base.predictor import Predictor


class AnalyserPredictor(Predictor):

    @property
    @abstractmethod
    def retrain_period(self) -> Optional[int]:
        """[summary]

        :raises NotImplementedError: [description]
        :return: [description]
        :rtype: Optional[int]
        """
        raise NotImplementedError

    @abstractmethod
    def fit(self):
        """[summary]

        :raises NotImplementedError: [description]
        """
        raise NotImplementedError

    @abstractmethod
    def predict(self, X: DataFrame) -> List[bool]:
        """[summary]

        :param X: [description]
        :type X: DataFrame
        :raises NotImplementedError: [description]
        :return: [description]
        :rtype: List[bool]
        """
        raise NotImplementedError
