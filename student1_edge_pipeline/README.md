# Chronos-Guard: Deep Edge Telemetry Pipeline (Student 1)

This module handles low-latency vibration telemetry ingestion, localized statistical feature extraction, and frequency-domain spectrum transformation at the edge level.

## Features
- **Data Ingestion**: Streaming interface for NASA IMS bearing vibration telemetry.
- **Localized Signal Profiling**: Rolling Z-Score and Windowed Kurtosis calculation.
- **Frequency Domain Analytics**: Fast Fourier Transform (FFT) spectrum analysis for high-frequency shock detection.

## Hardware & System Requirements
- Python 3.9+
- Dependencies: `numpy`, `pandas`, `scipy`, `matplotlib`

## Pipeline Architecture