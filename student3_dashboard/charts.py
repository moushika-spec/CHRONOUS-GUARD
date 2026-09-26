# charts.py

import streamlit as st
import plotly.express as px


class Charts:

    def __init__(self, dataframe):

        self.df = dataframe

    def health_index_chart(self):

        st.subheader("Health Index Trend")

        fig = px.line(

            self.df,

            x=self.df.index,

            y="health_index",

            title="Health Index"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    def anomaly_chart(self):

        st.subheader("Anomaly Scores")

        fig = px.scatter(

            self.df,

            x=self.df.index,

            y="anomaly_score",

            color="health_status",

            hover_data=[
                "remaining_useful_life"
            ],

            title="Isolation Forest Scores"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    def rul_chart(self):

        st.subheader(
            "Remaining Useful Life"
        )

        fig = px.line(

            self.df,

            x=self.df.index,

            y="remaining_useful_life",

            title="Estimated RUL"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    def health_distribution(self):

        st.subheader(
            "Health Status Distribution"
        )

        counts = (
            self.df["health_status"]
            .value_counts()
            .reset_index()
        )

        counts.columns = [
            "Health Status",
            "Count"
        ]

        fig = px.pie(

            counts,

            values="Count",

            names="Health Status"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    def maintenance_chart(self):

        st.subheader(
            "Maintenance Recommendations"
        )

        counts = (
            self.df[
                "maintenance_recommendation"
            ]
            .value_counts()
            .reset_index()
        )

        counts.columns = [
            "Recommendation",
            "Count"
        ]

        fig = px.bar(

            counts,

            x="Recommendation",

            y="Count",

            text="Count"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    def anomaly_boxplot(self):

        st.subheader("Anomaly Score Outlier Analysis")

        fig = px.box(

            self.df,

            y="anomaly_score",

            color="health_status",

            points="outliers",

            title="Anomaly Score Distribution with Outliers"

        )

        fig.update_layout(

            xaxis_title="Health Status",

            yaxis_title="Anomaly Score",

            height=500

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )