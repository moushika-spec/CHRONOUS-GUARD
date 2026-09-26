# metrics.py

import streamlit as st


class Metrics:

    def __init__(self, dataframe):

        self.df = dataframe

    def display(self):

        total = len(self.df)

        healthy = (
            self.df["health_status"] == "Healthy"
        ).sum()

        warning = (
            self.df["health_status"] == "Warning"
        ).sum()

        critical = (
            self.df["health_status"] == "Critical"
        ).sum()

        avg_health = self.df["health_index"].mean()

        avg_score = self.df["anomaly_score"].mean()

        avg_rul = self.df[
            "remaining_useful_life"
        ].mean()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("Total Samples", total)

        c2.metric("Healthy", healthy)

        c3.metric("Warning", warning)

        c4.metric("Critical", critical)

        st.divider()

        c5, c6, c7 = st.columns(3)

        c5.metric(
            "Average Health",
            f"{avg_health:.2f}"
        )

        c6.metric(
            "Average Score",
            f"{avg_score:.2f}"
        )

        c7.metric(
            "Average RUL",
            f"{avg_rul:.2f}"
        )