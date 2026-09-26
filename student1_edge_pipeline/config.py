from pathlib import Path

# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "IMS"

OUTPUT_PATH = PROJECT_ROOT / "output"

OUTPUT_PATH.mkdir(exist_ok=True)


# ==========================================================
# SIGNAL PARAMETERS
# ==========================================================

# NASA IMS data sampling frequency
SAMPLING_FREQUENCY = 20000  # Hz

# Number of raw samples used in one analysis window
WINDOW_SIZE = 2048

# Number of samples by which window moves
STEP_SIZE = 1024


# ==========================================================
# ROLLING STATISTICS
# ==========================================================

# Number of previous windows used for baseline calculation
ROLLING_WINDOW_SIZE = 20

# Minimum number of samples required before calculating
# a reliable rolling Z-score
MIN_BASELINE_SAMPLES = 5


# ==========================================================
# OUTPUT FILES
# ==========================================================

FEATURE_OUTPUT_FILE = OUTPUT_PATH / "processed_features.csv"

STREAM_OUTPUT_FILE = OUTPUT_PATH / "feature_stream.json"