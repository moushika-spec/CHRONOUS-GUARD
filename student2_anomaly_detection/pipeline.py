# type:ignore
import json
from pathlib import Path

import pandas as pd

from config import (
    OUTPUT_FILE,
    N_ESTIMATORS,
    CONTAMINATION,
    RANDOM_STATE
)

from data_loader import FeatureLoader
from anomaly_detector import AnomalyDetector
from health_index import HealthIndex
from rul_estimator import RULEstimator


def main():

    # ======================================
    # Load Student 1 Features
    # ======================================

    loader = FeatureLoader()

    dataframe = loader.load()

    print(f"Loaded {len(dataframe)} feature windows.")

    # ======================================
    # Select Features
    # ======================================

    feature_columns = [

        "rms",

        "kurtosis",

        "crest_factor",

        "rms_z_score",

        "kurtosis_z_score"

    ]

    X = dataframe[feature_columns]

    # ======================================
    # Isolation Forest
    # ======================================

    detector = AnomalyDetector(

        N_ESTIMATORS,

        CONTAMINATION,

        RANDOM_STATE

    )

    prediction, anomaly_score = detector.fit_predict(X)

    dataframe["prediction"] = prediction

    dataframe["anomaly_score"] = anomaly_score

    # ======================================
    # Health Index
    # ======================================

    hi = HealthIndex()

    dataframe["health_index"] = hi.calculate(
        anomaly_score
    )

    dataframe["health_status"] = hi.classify(
        dataframe["health_index"]
    )

    # ======================================
    # Remaining Useful Life
    # ======================================

    rul = RULEstimator()

    dataframe["remaining_useful_life"] = rul.estimate(
        dataframe["health_index"]
    )

    dataframe["maintenance_recommendation"] = (
        rul.recommendation(
            dataframe["health_status"]
        )
    )

    # ======================================
    # Save CSV
    # ======================================

    dataframe.to_csv(

        OUTPUT_FILE,

        index=False

    )

    # ======================================
    # Pipeline Summary
    # ======================================

    summary = {

        "windows_processed": int(len(dataframe)),

        "healthy": int(
            (dataframe["health_status"] == "Healthy").sum()
        ),

        "warning": int(
            (dataframe["health_status"] == "Warning").sum()
        ),

        "critical": int(
            (dataframe["health_status"] == "Critical").sum()
        ),

        "anomalies_detected": int(
            (dataframe["prediction"] == -1).sum()
        ),

        "average_health_index": round(
            float(
                dataframe["health_index"].mean()
            ),
            4
        ),

        "average_rul": round(
            float(
                dataframe["remaining_useful_life"].mean()
            ),
            2
        ),

        "status": "completed"

    }

    summary_file = Path(
        OUTPUT_FILE
    ).parent / "pipeline_summary.json"

    with open(
        summary_file,
        "w"
    ) as file:

        json.dump(
            summary,
            file,
            indent=4
        )

    # ======================================
    # Console Output
    # ======================================

    print()

    print("=" * 45)

    print("STUDENT 2 PIPELINE COMPLETED")

    print("=" * 45)

    print(f"Windows Processed : {len(dataframe)}")

    print(f"Output File       : {OUTPUT_FILE}")

    print(f"Summary File      : {summary_file}")

    print()

    print("Health Status Counts")

    print("----------------------------")

    print(
        dataframe["health_status"].value_counts()
    )

    print()

    print("Maintenance Recommendations")

    print("----------------------------")

    print(
        dataframe[
            "maintenance_recommendation"
        ].value_counts()
    )

    print()

    print("Sample Output")

    print("----------------------------")

    print(
        dataframe.head()
    )


if __name__ == "__main__":

    main()