# utils.py

from datetime import datetime

import pandas as pd


def current_time():
    """
    Returns current date and time.
    """

    return datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )


def health_counts(dataframe):
    """
    Returns count of each health status.
    """

    return (
        dataframe["health_status"]
        .value_counts()
        .to_dict()
    )


def maintenance_counts(dataframe):
    """
    Returns maintenance recommendation counts.
    """

    return (
        dataframe[
            "maintenance_recommendation"
        ]
        .value_counts()
        .to_dict()
    )


def dataframe_summary(dataframe):
    """
    Computes useful dashboard statistics.
    """

    return {

        "samples": len(dataframe),

        "average_health":

            round(
                dataframe["health_index"].mean(),
                2
            ),

        "average_score":

            round(
                dataframe["anomaly_score"].mean(),
                2
            ),

        "average_rul":

            round(
                dataframe[
                    "remaining_useful_life"
                ].mean(),
                2
            )

    }


def status_percentage(dataframe):
    """
    Calculates percentage of Healthy,
    Warning and Critical samples.
    """

    counts = (
        dataframe["health_status"]
        .value_counts(normalize=True)
        * 100
    )

    return counts.round(2).to_dict()


def export_csv(dataframe):
    """
    Returns dataframe as CSV string.
    """

    return dataframe.to_csv(
        index=False
    )


def top_critical(dataframe, limit=10):
    """
    Returns top critical records.
    """

    critical = dataframe[

        dataframe["health_status"]
        == "Critical"

    ]

    return critical.head(limit)


def format_number(value):
    """
    Formats float values.
    """

    return f"{value:.2f}"


def validate_dataframe(dataframe):
    """
    Checks whether dataframe is empty.
    """

    if dataframe.empty:
        raise ValueError(
            "No data available."
        )

    return True