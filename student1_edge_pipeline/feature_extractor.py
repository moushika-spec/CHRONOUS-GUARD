import numpy as np
from scipy.stats import kurtosis


class VibrationFeatureExtractor:

    def extract_features(self, signal_window):

        signal_window = np.asarray(
            signal_window,
            dtype=np.float64
        )

        mean_value = np.mean(signal_window)

        rms_value = np.sqrt(
            np.mean(
                np.square(signal_window)
            )
        )

        standard_deviation = np.std(
            signal_window
        )

        kurtosis_value = kurtosis(
            signal_window,
            fisher=False
        )

        peak_value = np.max(
            np.abs(signal_window)
        )

        crest_factor = (
            peak_value / rms_value
            if rms_value != 0
            else 0
        )

        return {

            "mean": float(mean_value),

            "rms": float(rms_value),

            "std": float(standard_deviation),

            "kurtosis": float(kurtosis_value),

            "peak": float(peak_value),

            "crest_factor": float(crest_factor)

        }