from collections import deque
import numpy as np


class RollingZScore:

    def __init__(
        self,
        window_size=20,
        epsilon=1e-8
    ):

        self.window_size = window_size

        self.epsilon = epsilon

        self.history = deque(
            maxlen=window_size
        )

    def update(self, current_value):

        self.history.append(
            current_value
        )

        values = np.array(
            self.history,
            dtype=np.float64
        )

        rolling_mean = np.mean(values)

        rolling_std = np.std(values)

        z_score = (
            current_value - rolling_mean
        ) / (
            rolling_std + self.epsilon
        )

        return {

            "rolling_mean": float(
                rolling_mean
            ),

            "rolling_std": float(
                rolling_std
            ),

            "z_score": float(
                z_score
            )

        }