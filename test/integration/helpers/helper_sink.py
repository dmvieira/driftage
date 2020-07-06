from asynctest import Mock
from driftage.executor import Sink


class HelperSink(Sink):

    external = Mock()
    available = True

    def is_available(self):
        return self.available

    async def drain(self, data: dict):
        self.external(data)
