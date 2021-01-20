from adwin_analyser import ADWINPredictor, main


class ADWINPredictiorWithTrain(ADWINPredictor):
    @property
    def retrain_period(self):
        return 0.01


main(ADWINPredictiorWithTrain)
