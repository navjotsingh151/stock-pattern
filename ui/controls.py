"""Sidebar input controls."""
from __future__ import annotations

import streamlit as st


def sidebar_inputs():
    """Render sidebar controls and return user inputs."""
    st.sidebar.header("Controls")
    ticker = st.sidebar.text_input("Ticker", value="AAPL").strip().upper()
    x_percent = st.sidebar.number_input(
        "X (%)", min_value=1, max_value=20, value=2, step=1
    )
    y_percent = st.sidebar.number_input(
        "Y (%)", min_value=101, max_value=200, value=110, step=1
    )
    run_btn = st.sidebar.button("Run Backtest")
    return ticker, int(x_percent), int(y_percent), run_btn
