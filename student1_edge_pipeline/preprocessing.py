import numpy as np
from scipy import signal


class SignalPreprocessor:

    def __init__(self, sampling_frequency):

        self.sampling_frequency = sampling_frequency

    def clean_signal(self, vibration_signal):

        vibration_signal = np.asarray(
            vibration_signal,
            dtype=np.float64
        )

        # Remove NaN values
        vibration_signal = np.nan_to_num(
            vibration_signal,
            nan=0.0,
            posinf=0.0,
            neginf=0.0
        )

        return vibration_signal

    def detrend_signal(self, vibration_signal):

        return signal.detrend(vibration_signal)

    def normalize_signal(self, vibration_signal):

        mean_value = np.mean(vibration_signal)

        standard_deviation = np.std(vibration_signal)

        if standard_deviation == 0:

            return vibration_signal

        normalized_signal = (
            vibration_signal - mean_value
        ) / standard_deviation

        return normalized_signal

    def create_windows(
        self,
        vibration_signal,
        window_size,
        step_size
    ):

        windows = []

        signal_length = len(vibration_signal)

        start = 0

        while start + window_size <= signal_length:

            end = start + window_size

            window = vibration_signal[start:end]

            windows.append(window)

            start += step_size

        return windows