import json
from pathlib import Path
import pandas as pd


class DataLoader:

    def __init__(
        self,
        csv_path=None,
        json_path=None
    ):
        # Resolve target files across potential directory structures
        default_csv_paths = [
            Path("../output/anomaly_results.csv"),
            Path("output/anomaly_results.csv"),
            Path("data/anomaly_results.csv")
        ]
        
        default_json_paths = [
            Path("../output/pipeline_summary.json"),
            Path("output/pipeline_summary.json"),
            Path("data/pipeline_summary.json")
        ]

        if csv_path:
            self.csv_path = Path(csv_path)
        else:
            self.csv_path = next((p for p in default_csv_paths if p.exists()), Path("data/anomaly_results.csv"))

        if json_path:
            self.json_path = Path(json_path)
        else:
            self.json_path = next((p for p in default_json_paths if p.exists()), Path("data/pipeline_summary.json"))

    def validate_inputs(self):
        """Verify Student 2 outputs."""

        if not self.csv_path.exists():
            raise FileNotFoundError(
                f"Missing file: {self.csv_path}"
            )

        if not self.json_path.exists():
            raise FileNotFoundError(
                f"Missing file: {self.json_path}"
            )

        return True

    def load_csv(self):

        self.validate_inputs()

        dataframe = pd.read_csv(self.csv_path)

        required_columns = [

            "prediction",
            "anomaly_score",
            "health_index",
            "health_status",
            "remaining_useful_life",
            "maintenance_recommendation"

        ]

        missing = [

            column
            for column in required_columns
            if column not in dataframe.columns

        ]

        if missing:
            raise ValueError(
                f"Missing columns: {missing}"
            )

        if dataframe.isnull().sum().sum() > 0:
            raise ValueError(
                "CSV contains missing values."
            )

        return dataframe

    def load_summary(self):

        self.validate_inputs()

        with open(self.json_path) as file:
            summary = json.load(file)

        required_keys = [

            "windows_processed",
            "healthy",
            "warning",
            "critical",
            "anomalies_detected",
            "average_health_index",
            "average_rul",
            "status"

        ]

        missing = [

            key
            for key in required_keys
            if key not in summary

        ]

        if missing:
            raise ValueError(
                f"Missing JSON keys: {missing}"
            )

        return summary