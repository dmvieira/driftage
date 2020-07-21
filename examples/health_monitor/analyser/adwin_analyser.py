import os
import time
import logging
from driftage.analyser import Analyser
from driftage.analyser.predictor import AnalyserPredictor, PredictionData
from driftage.db.connection import Connection
from skmultiflow.drift_detection import ADWIN
from sqlalchemy import create_engine

logger = logging.getLogger("adwin_analyser")
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class ADWINPredictor(AnalyserPredictor):

    def __init__(self,
                 connection: Connection,
                 drift_rate_up=0.1,
                 drift_rate_down=0.0001):
        self.delta = 1.0
        self.drift_rate_up = drift_rate_up
        self.drift_rate_down = drift_rate_down
        self.last_rate = {}
        self.detectors = {}
        super().__init__(connection)

    @property
    def retrain_period(self):
        return 5

    async def fit(self):
        for identifier in self.detectors:
            detector = self.detectors[identifier]
            if ((detector.width > 0) and
                    ((self.drift_rate_up * detector.width) > 0)):

                drift_rate = detector.n_detections / detector.width
                if ((self.last_rate.get(identifier, 0) <= drift_rate) and
                        (drift_rate >= self.drift_rate_up)):
                    delta = detector.delta / 10
                    if delta >= self.drift_rate_down:
                        self.detectors[identifier].delta = delta
                        logger.debug(
                            f"delta down to {delta} on {identifier}"
                            f" with rate {drift_rate}")
                        self.last_rate[identifier] = drift_rate
                elif drift_rate <= self.drift_rate_down:
                    delta = detector.delta * 10
                    if delta <= self.drift_rate_up:
                        self.detectors[identifier].delta = delta
                        logger.debug(
                            f"delta up to {delta} on {identifier}"
                            f" with rate {drift_rate}")
                        self.last_rate[identifier] = drift_rate

    async def predict(self, X: PredictionData) -> bool:
        detector = self.detectors.get(X.identifier, ADWIN(self.delta))
        self.detectors[X.identifier] = detector
        detector.add_element(X.data["sensor"])

        return detector.detected_change()


engine = create_engine(os.environ["KB_CONNECTION_STRING"])

connection = Connection(engine, bulk_size=1000)
predictor = ADWINPredictor(connection)

analyser = Analyser(  # nosec
    "analyser@localhost",
    os.environ["ANALYSER_PASSWORD"],
    predictor,
    connection,
    ["monitor@localhost"])

logger.info("Waiting Ejabberd...")
time.sleep(20)
while not analyser.is_alive():
    logger.info("Starting analyser...")
    analyser.start()
    time.sleep(1)
    condition = [contact.get("presence", False)
                 for contact in analyser.presence.get_contacts().values()]
    while not all(condition):
        analyser.stop()
        logger.info("Waiting monitors...")
        time.sleep(1)
    time.sleep(1)

logger.info("Analyser alive")
