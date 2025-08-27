"""Backtest engine iterating over hourly bars with daily HOLD rows."""
from __future__ import annotations

from typing import Dict, Tuple

import pandas as pd

from .portfolio import Portfolio
from .strategy import apply_bar


def run_backtest(
    hourly_df: pd.DataFrame,
    daily_map: Dict[pd.Timestamp, Tuple[float, float]],
    x_percent: int,
    y_percent: int = 110,
):
    """Run the backtest and return trades and KPI summary.

    Parameters
    ----------
    hourly_df : DataFrame
        Hourly OHLC data with price column ``Close``.
    daily_map : dict
        Mapping of ``date`` -> ``(open, close)``.
    x_percent : int
        BUY threshold X.
    y_percent : int, default 110
        SELL threshold Y as a percentage of book cost.

    Returns
    -------
    (trades_df, kpis_dict)
    """

    portfolio = Portfolio()
    transactions = []
    bought_days = set()

    for day in sorted(daily_map.keys()):
        day_open, day_close = daily_map[day]
        day_hours = hourly_df[hourly_df.index.date == day]
        day_has_txn = False

        for ts, row in day_hours.iterrows():
            price = float(row["Close"])
            allow_buy = day not in bought_days
            txns = apply_bar(
                ts,
                day_open,
                day_close,
                price,
                portfolio,
                x_percent,
                y_percent,
                allow_buy=allow_buy,
            )
            if txns:
                transactions.extend(txns)
                day_has_txn = True
                if any(t["Action"] == "BUY" for t in txns):
                    bought_days.add(day)

        if not day_has_txn:
            transactions.append(
                {
                    "Date": pd.Timestamp(day),
                    "Open Price": day_open,
                    "Close Price": day_close,
                    "Transaction Price": day_close,
                    "Action": "HOLD",
                    "Portfolio Value": portfolio.value(day_close),
                    "Portfolio Book Cost": portfolio.book_cost,
                    "Transaction Quantity": 0.0,
                    "Portfolio Quantity": portfolio.qty,
                }
            )

    trades_df = pd.DataFrame(transactions)

    # KPIs
    last_price = (
        hourly_df["Close"].iloc[-1]
        if not hourly_df.empty
        else (list(daily_map.values())[-1][1] if daily_map else 0.0)
    )
    final_pv = portfolio.value(last_price)
    kpis = {
        "Final PQ": portfolio.qty,
        "Final PV": final_pv,
        "Realized PnL": portfolio.realized_pnl,
        "Unrealized PnL": round(final_pv - portfolio.book_cost, 2),
        "Total Buys": float(
            trades_df.loc[trades_df["Action"] == "BUY", "Transaction Quantity"].sum()
        ),
        "Total Sells": float(
            trades_df.loc[trades_df["Action"] == "SELL", "Transaction Quantity"].sum()
        ),
    }

    return trades_df, kpis

