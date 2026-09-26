import os
import sys
import subprocess
import json
import pandas as pd

def print_header(text):
    print("\n" + "=" * 65)
    print(f"  {text}")
    print("=" * 65)

print_header("⚡ CHRONOS-GUARD: END-TO-END PIPELINE ORCHESTRATOR")

# ------------------------------------------------------------------------------
# STEP 1: Execute Student 1 Edge Telemetry Pipeline
# ------------------------------------------------------------------------------
print("\n[Step 1/3] Running Student 1 Edge Telemetry Pipeline...")
s1_dir = "student1_edge_pipeline"
if os.path.exists(s1_dir):
    try:
        if os.path.exists(os.path.join(s1_dir, "feature_extractor.py")):
            subprocess.run([sys.executable, "feature_extractor.py"], cwd=s1_dir, check=True)
            print("  ✓ Edge Feature Extraction Completed.")
        else:
            print("  ℹ feature_extractor.py not found in Student 1, skipping.")
    except subprocess.CalledProcessError as e:
        print(f"  ⚠ Student 1 Execution Error: {e}")
else:
    print("  ℹ Student 1 directory not found, assuming pre-generated telemetry.")

# ------------------------------------------------------------------------------
# STEP 2: Execute Student 2 Anomaly Detection & ML RUL Engine
# ------------------------------------------------------------------------------
print("\n[Step 2/3] Running Student 2 Anomaly Detection & ML RUL Engine...")
s2_dir = "student2_anomaly_detection"
if os.path.exists(s2_dir):
    try:
        if os.path.exists(os.path.join(s2_dir, "anomaly_detector.py")):
            subprocess.run([sys.executable, "anomaly_detector.py"], cwd=s2_dir, check=True)
            print("  ✓ Anomaly Detector Completed.")
        if os.path.exists(os.path.join(s2_dir, "rul_estimator.py")):
            subprocess.run([sys.executable, "rul_estimator.py"], cwd=s2_dir, check=True)
            print("  ✓ ML Random Forest RUL Estimator Completed.")
    except subprocess.CalledProcessError as e:
        print(f"  ⚠ Student 2 Execution Error: {e}")

# ------------------------------------------------------------------------------
# STEP 3: Validate Outputs & Print Summary Report
# ------------------------------------------------------------------------------
print("\n[Step 3/3] Validating System Output Integrity...")

candidate_paths = [
    "output/anomaly_results.csv",
    "student3_dashboard/data/anomaly_results.csv",
    "../output/anomaly_results.csv"
]

target_csv = next((p for p in candidate_paths if os.path.exists(p)), None)

if target_csv:
    df = pd.read_csv(target_csv)
    avg_rul = df["remaining_useful_life"].mean() if "remaining_useful_life" in df.columns else 0.0
    critical_count = (df["health_status"] == "Critical").sum() if "health_status" in df.columns else 0
    warning_count = (df["health_status"] == "Warning").sum() if "health_status" in df.columns else 0
    
    print(f"  ✓ Output File Verified: '{target_csv}'")
    print(f"    - Total Ingested Samples : {len(df)}")
    print(f"    - Average Calculated RUL : {avg_rul:.2f} cycles")
    print(f"    - Critical Units Flagged : {critical_count}")
    print(f"    - Warning Units Flagged  : {warning_count}")
else:
    print("  ⚠ Output CSV file not found. Check pipeline execution paths.")

print_header("🎉 PIPELINE READY! Launch Dashboard with:")
print("   cd student3_dashboard")
print("   python -m streamlit run app.py")
print("=" * 65 + "\n")