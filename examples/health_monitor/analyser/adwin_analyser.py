import time
from driftage.analyser import Analyser
from driftage.analyser.predictor import AnalyserPredictor, PredictionData
from driftage.db.connection import Connection
from skmultiflow.drift_detection import ADWIN
from sqlalchemy import create_engine


class ADWINPredictor(AnalyserPredictor):

    def __init__(self,
                 connection: Connection,
                 drift_rate_up=0.1,
                 drift_rate_down=0.0001):
        self.delta = 1.0
        self.drift_rate_up = drift_rate_up
        self.drift_rate_down = drift_rate_down
        self.last_width = {}
        self.detectors = {}
        super().__init__(connection)

    @property
    def retrain_period(self):
        return 1

    def fit(self):
        for identifier in self.detectors:
            detector = self.detectors[identifier]
            if ((detector.width > 0) and
                (self.last_width.get(identifier, 0) <= detector.width) and
                    ((self.drift_rate_up * detector.width) > 0)):
                self.last_width[identifier] = detector.width
                drift_rate = detector.n_detections / detector.width
                if drift_rate >= self.drift_rate_up:
                    delta = detector.delta * 0.1
                    if delta >= self.drift_rate_down * 0.1:
                        self.detectors[identifier].delta = delta
                        print(f"delta down to {delta} on {identifier} with rate {drift_rate}")
                elif drift_rate <= self.drift_rate_down:
                    delta = detector.delta * 10
                    if delta <= self.drift_rate_up * 10:
                        self.detectors[identifier].delta = delta
                        print(f"delta up to {delta} on {identifier} with rate {drift_rate}")

    def predict(self, X: PredictionData) -> bool:
        detector = self.detectors.get(X.identifier, ADWIN(self.delta))
        self.detectors[X.identifier] = detector
        detector.add_element(X.data["sensor"])

        return detector.detected_change()


engine = create_engine("sqlite:///database.sql")

connection = Connection(engine, bulk_size=1000)
predictor = ADWINPredictor(connection)

analyser = Analyser(
    "analyser@localhost",
    "passw0rd",
    predictor,
    connection,
    ["monitor@localhost"])
analyser.start()
while not analyser.is_alive():
    print("starting analyser...")
    time.sleep(1)
print("Analyser alive")
