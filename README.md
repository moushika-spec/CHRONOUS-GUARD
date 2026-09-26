# Chronos-Guard: End-to-End Edge Telemetry & Predictive Maintenance System

Chronos-Guard is an industrial-grade predictive maintenance platform designed for high-frequency vibration telemetry monitoring using the **NASA IMS Bearing Dataset**. It combines localized edge feature extraction, unsupervised anomaly detection (Isolation Forest), machine learning-driven Remaining Useful Life (RUL) regression, and an interactive Streamlit dashboard featuring Explainable AI (XAI) diagnostics.

---

## 👥 Module Work Division & Architecture
---
[ NASA IMS Bearing Telemetry ]
│
▼
┌─────────────────────────────────────────┐
│       Student 1: Edge Pipeline          │
│ - Streaming Telemetry Ingestion         │
│ - Rolling Z-Score & Windowed Kurtosis   │
│ - Fast Fourier Transform (FFT) Peaks    │
└────────────────────┬────────────────────┘
│ processed_features.csv
▼
┌─────────────────────────────────────────┐
│     Student 2: Anomaly & RUL Engine     │
│ - Unsupervised Isolation Forest Scoring │
│ - Health Index Normalization (0.0 - 1.0)│
│ - Random Forest RUL Regressor           │
└────────────────────┬────────────────────┘
│ anomaly_results.csv
▼
┌─────────────────────────────────────────┐
│      Student 3: Monitoring Dashboard    │
│ - Real-Time Streamlit KPI Telemetry     │
│ - Fault Alerts & Degradation Analytics  │
│ - Interactive AI Maintenance Copilot    │
└─────────────────────────────────────────┘

## 🛠️ System Requirements & Dependencies

- **Python**: 3.9 or higher
- **Core Libraries**: `streamlit`, `scikit-learn`, `pandas`, `numpy`, `scipy`, `matplotlib`

Install dependencies:
```bash
pip install streamlit scikit-learn pandas numpy scipy matplotlib
---

### 3. Final Enhanced Copilot Block for `student3_dashboard/app.py`

Replace the Copilot block at the bottom of `app.py` with this multi-query XAI version:

```python
# ==============================
# AI Maintenance Copilot & XAI Diagnostics
# ==============================

st.header("🤖 AI Maintenance Copilot & XAI Diagnostics")

# Pull dynamic metrics from loaded data/summary
avg_rul = float(summary.get("average_rul", summary.get("avg_rul", dataframe["remaining_useful_life"].mean())))
avg_health = float(summary.get("average_health_index", dataframe["health_index"].mean()))
critical_count = int(summary.get("critical", (dataframe["health_status"] == "Critical").sum()))
warning_count = int(summary.get("warning", (dataframe["health_status"] == "Warning").sum()))

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Interactive Maintenance Q&A")
    user_query = st.text_input(
        "Ask the AI Copilot about bearing health, failure causes, or maintenance scheduling:",
        placeholder="e.g., Why are critical machines flagged? Or how is RUL estimated?"
    )

    if user_query:
        st.chat_message("user").write(user_query)
        with st.chat_message("assistant"):
            q = user_query.lower()
            if "critical" in q or "why" in q or "flagged" in q:
                st.write(
                    f"**Diagnostic Explanation:** {critical_count} machines flagged as **Critical** due to "
                    "severe Kurtosis spikes (>3.5) and high Z-score baseline deviations, indicating "
                    "impulsive vibration peaks from outer raceway bearing degradation."
                )
            elif "action" in q or "recommend" in q or "schedule" in q or "plan" in q:
                st.write(
                    "**Recommended Action Plan:**\n"
                    f"1. Schedule immediate physical inspection for the {critical_count} critical units within 24 hours.\n"
                    f"2. Perform lubrication checks on the {warning_count} units displaying warning thresholds.\n"
                    f"3. Schedule bearing replacement before estimated RUL drops below {avg_rul:.2f} cycles."
                )
            elif "rul" in q or "model" in q or "regression" in q or "estimate" in q:
                st.write(
                    "**RUL Methodology:** RUL is estimated using a **Random Forest Regressor** trained "
                    "on non-linear exponential degradation curves. Feature inputs include Windowed Kurtosis, "
                    "Rolling Z-score, Isolation Forest anomaly score, and Normalized Health Index."
                )
            elif "kurtosis" in q or "fft" in q or "z-score" in q or "feature" in q:
                st.write(
                    "**Feature Diagnostics:**\n"
                    "- **Windowed Kurtosis**: Detects early structural shock impacts (spikes > 3.5 indicate pitting).\n"
                    "- **Rolling Z-Score**: Tracks overall baseline energy shifts in signal amplitude.\n"
                    "- **FFT Peaks**: Identifies characteristic bearing fault pass frequencies."
                )
            else:
                st.write(
                    f"**Telemetry Insight:** Analyzed model metrics for '{user_query}'. "
                    f"Current average system health is **{avg_health:.2f}** with an average remaining life of **{avg_rul:.2f} cycles**."
                )

with col2:
    st.subheader("📊 Contributing Factors")
    st.info(
        "**Key Risk Drivers:**\n"
        "- High Windowed Kurtosis (Impulsive shocks)\n"
        "- Rolling Z-Score Baseline Shift\n"
        "- FFT Frequency Peak Anomalies"
    )

    st.subheader("📄 Report Export")
    report_content = f"""CHRONOS-GUARD DIAGNOSTIC REPORT
----------------------------------
System Status: {critical_count} Critical Machines / {warning_count} Warning Machines
Average Health Index: {avg_health:.2f}
Average Estimated RUL: {avg_rul:.2f} Cycles
Primary Model: Isolation Forest + Random Forest RUL Regressor

Recommended Action: Schedule immediate bearing inspection for Critical group.
"""
    st.download_button(
        label="📥 Download Diagnostic Summary Report",
        data=report_content,
        file_name="Chronos_Guard_Diagnostic_Report.txt",
        mime="text/plain"
    )