# config.py

from pathlib import Path

# ==========================================
# Project Information
# ==========================================

PROJECT_NAME = "Industrial Bearing Health Monitoring Dashboard"

PROJECT_VERSION = "1.0"

MODEL_NAME = "Isolation Forest"

DATASET_NAME = "NASA IMS Bearing Dataset"

# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

ASSETS_DIR = BASE_DIR / "assets"

CSV_FILE = DATA_DIR / "anomaly_results.csv"

SUMMARY_FILE = DATA_DIR / "pipeline_summary.json"

LOGO = ASSETS_DIR / "logo.png"

STYLE = ASSETS_DIR / "styles.css"

# ==========================================
# Dashboard
# ==========================================

PAGE_TITLE = PROJECT_NAME

PAGE_ICON = "⚙"

LAYOUT = "wide"

# ==========================================
# Auto Refresh
# ==========================================

AUTO_REFRESH_INTERVAL = 10

# ==========================================
# Health Status Labels
# ==========================================

HEALTHY = "Healthy"

WARNING = "Warning"

CRITICAL = "Critical"

# ==========================================
# Alert Thresholds
# ==========================================

LOW_RUL_THRESHOLD = 20

WARNING_RUL_THRESHOLD = 50

LOW_ANOMALY_SCORE = 0.40

HIGH_ANOMALY_SCORE = 0.70