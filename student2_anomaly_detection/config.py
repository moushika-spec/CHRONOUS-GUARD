
# type:ignore
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INPUT_FILE = os.path.join(
    BASE_DIR,
    "output",
    "processed_features.csv"
)

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "output",
    "anomaly_results.csv"
)

N_ESTIMATORS = 100
CONTAMINATION = 0.02
RANDOM_STATE = 42