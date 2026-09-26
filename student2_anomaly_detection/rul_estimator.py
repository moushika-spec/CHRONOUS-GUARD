import os
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

class RULEstimator:
    def __init__(self, output_dir="../output"):
        self.output_dir = output_dir
        self.input_file = os.path.join(output_dir, "anomaly_results.csv")
        self.summary_file = os.path.join(output_dir, "pipeline_summary.json")
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()

    def _generate_synthetic_run_to_failure(self, n_samples=2000):
        time_steps = np.linspace(0, 100, n_samples)
        base_degradation = np.exp(time_steps / 25) - 1.0
        
        kurtosis = 3.0 + base_degradation + np.random.normal(0, 0.2, n_samples)
        z_score = base_degradation * 0.8 + np.random.normal(0, 0.15, n_samples)
        anomaly_score = 0.3 + (base_degradation / np.max(base_degradation)) * 0.45 + np.random.normal(0, 0.05, n_samples)
        health_index = np.clip(1.0 - (base_degradation / np.max(base_degradation)), 0, 1)
        
        rul_target = np.clip(100.0 - time_steps, 0, 100)
        
        X = np.column_stack([kurtosis, z_score, anomaly_score, health_index])
        return X, rul_target

    def train_model(self):
        X_train, y_train = self._generate_synthetic_run_to_failure()
        X_scaled = self.scaler.fit_transform(X_train)
        self.rf_model.fit(X_scaled, y_train)

    def predict_rul(self, df):
        feature_cols = ['kurtosis', 'z_score', 'anomaly_score', 'health_index']
        
        for col in feature_cols:
            if col not in df.columns:
                if col == 'kurtosis': df[col] = 3.0
                elif col == 'z_score': df[col] = 0.0
                elif col == 'anomaly_score': df[col] = 0.45
                elif col == 'health_index': df[col] = 0.78
        
        X_test = df[feature_cols].values
        X_test_scaled = self.scaler.transform(X_test)
        predicted_rul = self.rf_model.predict(X_test_scaled)
        
        # Smooth and save to both standard column names for compatibility
        smoothed_rul = pd.Series(predicted_rul).ewm(span=50).mean()
        df['remaining_useful_life'] = smoothed_rul
        df['rul'] = smoothed_rul
        return df

    def run(self):
        if not os.path.exists(self.input_file):
            print(f"Error: {self.input_file} not found.")
            return
            
        df = pd.read_csv(self.input_file)
        self.train_model()
        df = self.predict_rul(df)
        df.to_csv(self.input_file, index=False)

        # Update pipeline_summary.json stats
        if os.path.exists(self.summary_file):
            try:
                with open(self.summary_file, 'r') as f:
                    summary = json.load(f)
                
                avg_rul = float(df['remaining_useful_life'].mean())
                summary['average_rul'] = round(avg_rul, 2)
                summary['avg_rul'] = round(avg_rul, 2)

                with open(self.summary_file, 'w') as f:
                    json.dump(summary, f, indent=4)
            except Exception as e:
                print(f"Summary update warning: {e}")

        print("ML RUL Estimation and Summary Json updated successfully.")

if __name__ == "__main__":
    estimator = RULEstimator()
    estimator.run()