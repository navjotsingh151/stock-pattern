"""Streamlit entrypoint for intraday backtesting app."""
from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from core import data_loader
from core.backtest import run_backtest
from ui.controls import sidebar_inputs
from ui.views import render_kpis, render_table, render_chart


def main():
    st.title("Hourly Backtest")
    st.caption("Evaluation order per bar: SELL then BUY")

    ticker, x_percent, y_percent, run_btn = sidebar_inputs()

    if run_btn:
        if not ticker:
            st.error("Ticker must not be empty")
            return

        end = datetime.utcnow()
        start = end - timedelta(days=365)

        daily_df = data_loader.get_daily(ticker, start, end)
        hourly_df = data_loader.get_hourly(ticker, start, end)

        if daily_df.empty or hourly_df.empty:
            st.warning("Insufficient data fetched for the given range.")
            return

        timezone = str(hourly_df.index.tz)
        if timezone == "None":
            timezone = "UTC"

        daily_map = {
            idx.date(): (row["Open"], row["Close"]) for idx, row in daily_df.iterrows()
        }

        trades_df, kpis = run_backtest(hourly_df, daily_map, x_percent, y_percent)

        st.subheader("Results")
        st.text(f"Timezone: {timezone}")

        render_kpis(kpis)
        render_chart(hourly_df, trades_df)
        render_table(trades_df)

    with st.expander("Help"):
        st.write(
            """Rules:\n- BUY X shares if hourly price ≥ (1 - X/100) × day open.\n- SELL 50% of position when portfolio value ≥ Y% of book cost (default 110%).\nEvaluation order per bar: SELL then BUY."""
        )


if __name__ == "__main__":
    main()
