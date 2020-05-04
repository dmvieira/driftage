from spade.behaviour import PeriodicBehaviour


class SetAvailability(PeriodicBehaviour):
    async def run(self):
        if self.presence.is_available():
            self.presence.set_unavailable()
        else:
            self.presence.set_available()
