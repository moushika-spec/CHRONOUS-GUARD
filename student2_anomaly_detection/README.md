### 3. `student2_anomaly_detection/README.md`

Paste this directly into `student2_anomaly_detection/README.md`[cite: 5]:

```markdown
# Chronos-Guard: Anomaly Detection & ML RUL Estimation (Student 2)

This module provides unsupervised anomaly detection, health index calculation, and machine learning-driven Remaining Useful Life (RUL) estimation for industrial bearings.

## Key Algorithms
- **Isolation Forest**: Unsupervised high-dimensional outlier scoring.
- **Statistical Thresholding**: Kurtosis spike and Z-Score baseline shift analysis.
- **Random Forest RUL Regressor**: Non-linear degradation curve fitting for remaining operational cycle prediction.

## System Requirements
- Python 3.9+
- Dependencies: `scikit-learn`, `pandas`, `numpy`, `matplotlib`

## Architecture Flow