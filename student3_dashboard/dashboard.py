# dashboard.py

import streamlit as st
import plotly.express as px


class Dashboard:

    def __init__(self, dataframe, summary):

        self.df = dataframe
        self.summary = summary

    def show_header(self):

        st.title("Industrial Bearing Health Monitoring Dashboard")

        st.caption(
            "NASA IMS Bearing Dataset | Student 3 Dashboard"
        )

    def show_metrics(self):

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Samples",
            self.summary["windows_processed"]
        )

        c2.metric(
            "Healthy",
            self.summary["healthy"]
        )

        c3.metric(
            "Warning",
            self.summary["warning"]
        )

        c4.metric(
            "Critical",
            self.summary["critical"]
        )

        st.divider()

        c5, c6, c7 = st.columns(3)

        c5.metric(
            "Average Health Index",
            round(
                self.summary["average_health_index"],
                2
            )
        )

        c6.metric(
            "Average RUL",
            round(
                self.summary["average_rul"],
                2
            )
        )

        c7.metric(
            "Detected Anomalies",
            self.summary["anomalies_detected"]
        )

    def health_chart(self):

        st.subheader("Health Index")

        fig = px.line(
            self.df,
            y="health_index",
            title="Health Index Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    def anomaly_chart(self):

        st.subheader("Anomaly Scores")

        fig = px.scatter(
            self.df,
            y="anomaly_score",
            color="health_status",
            title="Anomaly Score Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    def rul_chart(self):

        st.subheader("Remaining Useful Life")

        fig = px.line(
            self.df,
            y="remaining_useful_life",
            title="Estimated Remaining Useful Life"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    def status_chart(self):

        st.subheader("Health Status Distribution")

        count = (
            self.df["health_status"]
            .value_counts()
            .reset_index()
        )

        count.columns = [
            "Health Status",
            "Count"
        ]

        fig = px.pie(
            count,
            values="Count",
            names="Health Status"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    def recommendation_table(self):

        st.subheader(
            "Maintenance Recommendations"
        )

        st.dataframe(

            self.df[

                [

                    "health_status",
                    "health_index",
                    "remaining_useful_life",
                    "maintenance_recommendation"

                ]

            ],

            use_container_width=True

        )

    def download_button(self):

        st.download_button(

            label="Download Results CSV",

            data=self.df.to_csv(
                index=False
            ),

            file_name="anomaly_results.csv",

            mime="text/csv"

        )