from driftage.analyser.predictor import AnalyserPredictor


class HelperAnalyserPredictor(AnalyserPredictor):

    fitted = False

    @property
    def retrain_period(self):
        return 1

    def fit(self):
        self.fitted = True

    def predict(self, X):
        return [1]*len(X.index)
