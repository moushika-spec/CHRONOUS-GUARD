# download.py

import json
import streamlit as st


class Download:

    def __init__(self, dataframe, summary):

        self.df = dataframe
        self.summary = summary

    def show(self):

        st.subheader("⬇ Download Results")

        csv = self.df.to_csv(index=False)

        st.download_button(

            label="Download anomaly_results.csv",

            data=csv,

            file_name="anomaly_results.csv",

            mime="text/csv"

        )

        st.download_button(

            label="Download pipeline_summary.json",

            data=json.dumps(
                self.summary,
                indent=4
            ),

            file_name="pipeline_summary.json",

            mime="application/json"

        )