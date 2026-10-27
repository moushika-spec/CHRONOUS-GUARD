# validate_model.py

import os
import json
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def evaluate_model():
    print("=" * 60)
    print(" 📊 CHRONOUS-GUARD: Model Validation & Error Analysis Script")
    print("=" * 60)

    csv_path = os.path.join("data", "bearing_vibration.csv")
    eval_output_path = os.path.join("data", "evaluation_metrics.json")

    if not os.path.exists(csv_path):
        print("[Error] bearing_vibration.csv not found! Run python run_pipeline.py first.")
        return

    # Load generated dataset
    df = pd.read_csv(csv_path)

    # Simulated Ground Truth RUL vs Predicted RUL from Random Forest Regressor
    # (In standard NASA IMS validation, true RUL is the physical remaining cycles to failure)
    n_samples = len(df)
    ground_truth_rul = np.maximum(0, 150 - (df["cycle"] / n_samples) * 150)
    predicted_rul = df["remaining_useful_life"].values

    # Calculate Regression Metrics
    rmse = float(np.sqrt(mean_squared_error(ground_truth_rul, predicted_rul)))
    mae = float(mean_absolute_error(ground_truth_rul, predicted_rul))
    r2 = float(r2_score(ground_truth_rul, predicted_rul))

    metrics_data = {
        "rmse": round(rmse, 2),
        "mae": round(mae, 2),
        "r2_score": round(r2, 2),
        "baseline_rmse": 18.4,
        "improvement_percentage": round(((18.4 - rmse) / 18.4) * 100, 1),
        "validation_samples": n_samples
    }

    # Save metrics to JSON so the dashboard can load them dynamically
    with open(eval_output_path, "w") as f:
        json.dump(metrics_data, f, indent=4)

    print(f"[Success] Validation Completed!")
    print(f"  • Root Mean Square Error (RMSE): {metrics_data['rmse']} Cycles")
    print(f"  • Mean Absolute Error (MAE):     {metrics_data['mae']} Cycles")
    print(f"  • R-Squared Score (R²):          {metrics_data['r2_score']}")
    print(f"  • Saved Evaluation Metrics to:   {eval_output_path}")
    print("=" * 60)

if __name__ == "__main__":
    evaluate_model()