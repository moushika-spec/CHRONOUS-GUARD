# type:ignore
import numpy as np


class HealthIndex:

    def calculate(
        self,
        anomaly_score
    ):

        minimum = np.min(anomaly_score)
        maximum = np.max(anomaly_score)

        health = 1 - (
            (anomaly_score - minimum)
            /
            (maximum - minimum)
        )

        return health

    def classify(
        self,
        health_index
    ):

        status = []

        for value in health_index:

            if value >= 0.70:

                status.append(
                    "Healthy"
                )

            elif value >= 0.40:

                status.append(
                    "Warning"
                )

            else:

                status.append(
                    "Critical"
                )

        return status