# type:ignore
from sklearn.ensemble import IsolationForest
class AnomalyDetector:

    def __init__(
        self,
        n_estimators,
        contamination,
        random_state
    ):

        self.model = IsolationForest(

            n_estimators=n_estimators,

            contamination=contamination,

            random_state=random_state

        )

    def fit_predict(
        self,
        dataframe
    ):

        prediction = self.model.fit_predict(
            dataframe
        )

        score = -self.model.score_samples(
            dataframe
        )

        return prediction, score