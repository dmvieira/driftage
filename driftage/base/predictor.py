from abc import ABCMeta
from driftage.db.connection import Connection


class Predictor(metaclass=ABCMeta):

    def __init__(self, connection: Connection):
        """[summary]

        :param connection: [description]
        :type connection: Connection
        """
        self._connection = connection

    @property
    def connection(self):
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        return self._connection
