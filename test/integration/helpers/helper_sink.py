from asynctest import Mock
from driftage.executor import Sink


class HelperSink(Sink):

    external = Mock()

    def is_available(self):
        return True

    async def drain(self, data: dict):
        self.external(data)
