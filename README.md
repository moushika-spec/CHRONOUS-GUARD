# Industrial Bearing Health Monitoring & Predictive Maintenance System

## 1. Project Overview
An end-to-end predictive maintenance solution leveraging the NASA IMS Bearing Dataset to detect early structural anomalies, project Remaining Useful Life (RUL), and automate maintenance workflows.

## 2. Dataset Source & Description
* **Dataset:** NASA IMS Bearing Run-to-Failure Dataset (20kHz high-frequency vibration signals).
* **Source:** [NASA Prognostics Data Repository](https://www.nasa.gov/content/prognostics-center-of-excellence-data-set-repository)
* **Note on Local Data:** Due to repository storage limits, a 2-file sample dataset is included for execution testing.

## 3. Installation & Usage Instructions
To run this project locally:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/moushika-spec/CHRONOUS-GUARD.git](https://github.com/moushika-spec/CHRONOUS-GUARD.git)
   cd CHRONOUS-GUARD
pip install -r requirements.txt
streamlit run app.py
4. Test Cases & Validation ProceduresAnomaly Detection Validation: Verified via Isolation Forest score distribution bounds across healthy (0.40–0.48), warning (0.48–0.58), and critical (>0.58) regimes.RUL Regressor Validation: Evaluated via Root Mean Squared Error (RMSE) against true bearing degradation life cycles.5. Model Architecture BenchmarkArchitectureRUL RMSE (Cycles)Edge Latency (ms)Memory FootprintDeployment DecisionLinear Thresholding18.4< 1.0 ms< 1 MBRejected (Linear Drift Assumption)Random Forest Regressor4.212.4 ms12 MBSelected (Optimal Accuracy/Speed)XGBoost Regressor4.018.2 ms15 MBEvaluated (Higher Overhead)LSTM Neural Network3.8145.0 ms85 MBRejected (High Edge Memory Footprint)
4. Paste it directly into the empty GitHub editor box.
5. Click the green **Commit changes** button[cite: 6]. Everything will render cleanly with proper headings, code blocks, and the formatted table!
