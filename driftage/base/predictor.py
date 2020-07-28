from abc import ABCMeta
from driftage.db.connection import Connection


class Predictor(metaclass=ABCMeta):

    def __init__(self, connection: Connection):
        """Predictor base class for Concept Drift detection.

        :param connection: Knowledge Based connection
        :type connection: Connection
        """
        self._connection = connection

    @property
    def connection(self):
        """KB connection using SQLAlchemy

        :return: Connection object to database
        :rtype: Connection
        """
        return self._connection
