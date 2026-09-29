import numpy as np
from scipy.stats import kurtosis

def compute_windowed_kurtosis(signal_window):
    """Computes 4th-order statistical moment over a 2048-sample window."""
    return kurtosis(signal_window, fisher=False)

def compute_rolling_z_score(kurtosis_history, window_size=50):
    """Calculates adaptive Z-score over recent Kurtosis history."""
    if len(kurtosis_history) < window_size:
        return 0.0
    recent = kurtosis_history[-window_size:]
    mu = np.mean(recent)
    sigma = np.std(recent) + 1e-6
    return (kurtosis_history[-1] - mu) / sigma