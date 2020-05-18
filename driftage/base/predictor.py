from abc import ABCMeta
from driftage.db.connection import Connection


class Predictor(metaclass=ABCMeta):

    def __init__(self, connection: Connection):
        self._connection = connection

    @property
    def connection(self):
        return self._connection
