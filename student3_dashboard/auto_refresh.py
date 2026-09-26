# auto_refresh.py

import time
import streamlit as st


class AutoRefresh:

    def __init__(self, seconds=10):

        self.seconds = seconds

    def refresh(self):

        st.sidebar.markdown("---")

        auto = st.sidebar.checkbox(
            "Enable Auto Refresh",
            value=False
        )

        if auto:

            st.sidebar.success(
                f"Refreshing every {self.seconds} seconds"
            )

            time.sleep(self.seconds)

            st.rerun()