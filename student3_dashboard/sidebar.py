# sidebar.py

import streamlit as st
from datetime import datetime


class Sidebar:

    def __init__(self, dataframe, summary):

        self.df = dataframe
        self.summary = summary

    def show(self):

        st.sidebar.title("📊 Dashboard")

        st.sidebar.markdown("---")

        st.sidebar.header("Project")

        st.sidebar.write(
            "Predictive Maintenance using NASA IMS Bearing Dataset"
        )

        st.sidebar.markdown("---")

        st.sidebar.header("Dataset")

        st.sidebar.write(
            f"Samples : {len(self.df)}"
        )

        st.sidebar.write(
            f"Healthy : {self.summary['healthy']}"
        )

        st.sidebar.write(
            f"Warning : {self.summary['warning']}"
        )

        st.sidebar.write(
            f"Critical : {self.summary['critical']}"
        )

        st.sidebar.markdown("---")

        st.sidebar.header("Pipeline")

        st.sidebar.write(
            "Model : Isolation Forest"
        )

        st.sidebar.write(
            f"Status : {self.summary['status'].title()}"
        )

        st.sidebar.write(
            f"Anomalies : {self.summary['anomalies_detected']}"
        )

        st.sidebar.markdown("---")

        st.sidebar.header("Statistics")

        st.sidebar.write(
            f"Average Health : {self.summary['average_health_index']:.2f}"
        )

        st.sidebar.write(
            f"Average RUL : {self.summary['average_rul']:.2f}"
        )

        st.sidebar.markdown("---")

        st.sidebar.caption(
            f"Last Updated\n{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        )