"""Data loading utilities with caching using yfinance."""
from __future__ import annotations

from datetime import datetime
from typing import Any

import pandas as pd
import streamlit as st
import yfinance as yf


@st.cache_data(show_spinner=False)
def _fetch(ticker: str, start: datetime, end: datetime, interval: str) -> pd.DataFrame:
    ticker_obj = yf.Ticker(ticker)
    df = ticker_obj.history(start=start, end=end, interval=interval)
    if df.empty:
        st.warning(f"No data returned for {ticker} interval {interval}.")
    return df


def get_daily(ticker: str, start: datetime, end: datetime) -> pd.DataFrame:
    """Fetch daily data for ``ticker``."""
    return _fetch(ticker, start, end, "1d")


def get_hourly(ticker: str, start: datetime, end: datetime) -> pd.DataFrame:
    """Fetch hourly data for ``ticker``."""
    return _fetch(ticker, start, end, "1h")
