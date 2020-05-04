class Connection:
    def __init__(self, jid: str, uri: str):
        self._jid = jid

    def upsert(self, timestamp: float):
        pass

    def get(self, timestamp: float):
        pass

    def select(self, from_timestamp: float, to_timestamp: float):
        pass
