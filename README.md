# ⚙️ CHRONOUS-GUARD: Industrial AI Predictive Maintenance Platform

[![Live Webpage](https://img.shields.io/badge/GitHub%20Pages-Live%20Portal-blue?style=for-the-badge&logo=github)](https://moushika-spec.github.io/CHRONOUS-GUARD/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%200.100+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit%201.30+-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)

**CHRONOUS-GUARD** is an end-to-end industrial predictive maintenance (PdM) platform designed for real-time vibration telemetry analysis, anomaly detection, Remaining Useful Life (RUL) estimation, and automated Computerized Maintenance Management System (CMMS) dispatch. Built on the **NASA IMS Bearing Dataset**, the system processes 20kHz high-frequency telemetry signals to flag early raceway degradation and automate field engineering workflows.

---

## 🔗 Project Links

- **Live GitHub Pages Webpage:** [https://moushika-spec.github.io/CHRONOUS-GUARD/](https://moushika-spec.github.io/CHRONOUS-GUARD/)
- **GitHub Source Code Repository:** [https://github.com/moushika-spec/CHRONOUS-GUARD](https://github.com/moushika-spec/CHRONOUS-GUARD)
- **Course Reference:** `23AID205 - Artificial Intelligence & Data Science Project`

---

## 🏗️ Repository Architecture

```text
student3_dashboard/
├── api/
│   └── __init__.py
├── data/
│   ├── bearing_vibration.csv
│   └── summary.json
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py              # FastAPI CMMS Webhook Dispatch Microservice
│   ├── features.py              # Signal Processing (Kurtosis, FFT, Z-Score)
│   └── model.py                 # Isolation Forest & Random Forest Regressor
├── alerts.py                    # Real-time Threshold & Alerting Component
├── app.py                       # 10/10 Production Streamlit Dashboard
├── auto_refresh.py              # Live Data Auto-Refresh Controller
├── charts.py                    # Plotly & Matplotlib Analytics Engines
├── config.py                    # Dashboard Environment Configurations
├── dashboard.py                 # Header & Diagnostic Recommendation Tables
├── data_loader.py               # Robust Data Ingestion Engine
├── download.py                  # Localized Summary Report Exporter
├── index.html                   # GitHub Pages Portal Landing Page
├── metrics.py                   # KPI Calculation Cards
├── requirements.txt             # Python Package Dependencies
├── run_pipeline.py              # Full Pipeline Orchestration Script
└── sidebar.py                   # ROI Calculator & Control Side Panel
