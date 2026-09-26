# alerts.py

import streamlit as st


class Alerts:

    def __init__(self, dataframe):

        self.df = dataframe

    def show(self):

        critical = (
            self.df["health_status"] == "Critical"
        ).sum()

        warning = (
            self.df["health_status"] == "Warning"
        ).sum()

        avg_rul = self.df[
            "remaining_useful_life"
        ].mean()

        avg_score = self.df[
            "anomaly_score"
        ].mean()

        if critical > 0:

            st.error(
                f"🚨 {critical} Critical machines detected."
            )

        elif warning > 0:

            st.warning(
                f"⚠ {warning} machines require maintenance."
            )

        else:

            st.success(
                "✅ All machines are operating normally."
            )

        if avg_rul < 20:

            st.error(
                f"Remaining Useful Life is low ({avg_rul:.1f})."
            )

        elif avg_rul < 50:

            st.warning(
                f"Average RUL = {avg_rul:.1f}"
            )

        else:

            st.success(
                f"Average RUL = {avg_rul:.1f}"
            )

        if avg_score > 0.70:

            st.error(
                "High anomaly score detected."
            )

        elif avg_score > 0.40:

            st.warning(
                "Moderate anomaly behaviour detected."
            )

        else:

            st.success(
                "Anomaly scores are within expected range."
            )