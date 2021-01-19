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
        self.counter = 0
        self.delta = 1.0
        self.drift_rate_up = drift_rate_up
        self.drift_rate_down = drift_rate_down
        self.last_rate = {}
        self.detectors = {}
        super().__init__(connection)

    @property
    def retrain_period(self):
        return 0

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
        start = time.time()
        detector = self.detectors.get(X.identifier, ADWIN(self.delta))
        self.detectors[X.identifier] = detector
        detector.add_element(X.data["sensor"])
        change = detector.detected_change()
        print(f"Time to predict: {time.time()-start}")
        return change


engine = create_engine(os.environ["KB_CONNECTION_STRING"])

connection = Connection(engine, bulk_size=1000, bulk_time=1)
predictor = ADWINPredictor(connection)


analyser = Analyser(  # nosec
    "analyser@localhost",
    os.environ["ANALYSER_PASSWORD"],
    predictor,
    connection,
    ["monitor@localhost"])

logger.info("Waiting Ejabberd...")
time.sleep(30)
logger.info("Starting analyser...")
analyser.start()
logger.info("Analyser alive")

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
analyser.stop()
logger.info("Analyser stopped")
