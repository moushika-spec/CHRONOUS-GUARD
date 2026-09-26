# Industrial Bearing Health Monitoring & Predictive Maintenance System

## 1. Project Overview
An end-to-end predictive maintenance solution leveraging the NASA IMS Bearing Dataset to detect early structural anomalies, project Remaining Useful Life (RUL), and automate maintenance workflows.

## 2. Dataset Source & Description
* **Dataset:** NASA IMS Bearing Run-to-Failure Dataset (20kHz high-frequency vibration signals).
* **Source:** https://www.nasa.gov/content/prognostics-center-of-excellence-data-set-repository
* **Note on Local Data:** Due to repository storage limits, a sample dataset is included for execution testing.

## 3. Installation & Usage Instructions
To run this project locally:

1. Clone the repository:
   git clone https://github.com/moushika-spec/CHRONOUS-GUARD.git
   cd CHRONOUS-GUARD

2. Install dependencies:
   pip install -r requirements.txt

3. Launch the Streamlit Dashboard:
   streamlit run app.py

## 4. Test Cases & Validation Procedures
* **Anomaly Detection Validation:** Verified via Isolation Forest score distribution bounds across healthy (0.40–0.48), warning (0.48–0.58), and critical (>0.58) regimes.
* **RUL Regressor Validation:** Evaluated via Root Mean Squared Error (RMSE) against true bearing degradation life cycles.

## 5. Model Architecture Benchmark

| Architecture | RUL RMSE (Cycles) | Edge Latency (ms) | Memory Footprint | Deployment Decision |
| :--- | :---: | :---: | :---: | :--- |
| Linear Thresholding | 18.4 | < 1.0 ms | < 1 MB | Rejected (Linear Drift Assumption) |
| Random Forest Regressor | 4.2 | 12.4 ms | 12 MB | Selected (Optimal Accuracy/Speed) |
| XGBoost Regressor | 4.0 | 18.2 ms | 15 MB | Evaluated (Higher Overhead) |
| LSTM Neural Network | 3.8 | 145.0 ms | 85 MB | Rejected (High Edge Memory Footprint) |
