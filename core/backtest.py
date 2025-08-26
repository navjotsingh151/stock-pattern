"""Backtest engine iterating over hourly bars."""
from __future__ import annotations

from typing import Dict, Tuple

import pandas as pd

from .portfolio import Portfolio
from .strategy import apply_bar


def run_backtest(hourly_df: pd.DataFrame, daily_map: Dict[pd.Timestamp, Tuple[float, float]], x_percent: int):
    """Run the backtest and return trades and KPI summary.

    Parameters
    ----------
    hourly_df : DataFrame
        Hourly OHLC data with price column ``Close``.
    daily_map : dict
        Mapping of ``date`` -> ``(open, close)``.
    x_percent : int
        Strategy threshold X.

    Returns
    -------
    (trades_df, kpis_dict)
    """
    portfolio = Portfolio()
    transactions = []

    for ts, row in hourly_df.iterrows():
        day_info = daily_map.get(ts.date())
        if not day_info:
            continue
        day_open, day_close = day_info
        price = float(row["Close"])
        txns = apply_bar(ts, day_open, day_close, price, portfolio, x_percent)
        transactions.extend(txns)

    trades_df = pd.DataFrame(transactions)

    # KPIs
    last_price = hourly_df["Close"].iloc[-1] if not hourly_df.empty else 0.0
    final_pv = portfolio.value(last_price)
    kpis = {
        "Final PQ": portfolio.qty,
        "Final PV": final_pv,
        "Realized PnL": portfolio.realized_pnl,
        "Unrealized PnL": round(final_pv - portfolio.book_cost, 2),
        "Total Buys": float(trades_df[trades_df["Action"] == "BUY"]["Transaction Quantity"].sum()) if not trades_df.empty else 0.0,
        "Total Sells": float(trades_df[trades_df["Action"] == "SELL"]["Transaction Quantity"].sum()) if not trades_df.empty else 0.0,
    }

    return trades_df, kpis
