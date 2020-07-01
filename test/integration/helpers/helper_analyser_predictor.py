from driftage.analyser.predictor import AnalyserPredictor


class HelperAnalyserPredictor(AnalyserPredictor):

    fitted = False

    @property
    def retrain_period(self):
        return 1

    async def fit(self):
        self.fitted = True

    async def predict(self, X):
        return True
