"""Rendering views for KPIs, tables, and charts."""
from __future__ import annotations

import pandas as pd
import streamlit as st
import altair as alt

from core.formatting import fmt_price, fmt_qty


def render_kpis(kpis: dict):
    """Render KPI metrics."""
    cols = st.columns(len(kpis))
    for col, (k, v) in zip(cols, kpis.items()):
        if "PQ" in k or "Qty" in k:
            col.metric(k, fmt_qty(v))
        else:
            col.metric(k, fmt_price(v))


def render_table(trades_df: pd.DataFrame):
    """Render trades table with highlighting and download."""

    def highlight(row):
        if row.Action == "BUY":
            color = "background-color: yellow"
        elif row.Action == "SELL":
            color = "background-color: lightgreen"
        else:
            color = ""
        return [color] * len(row)

    styled = trades_df.style.apply(highlight, axis=1).format(
        {
            "Open Price": fmt_price,
            "Close Price": fmt_price,
            "Transaction Price": fmt_price,
            "Portfolio Value": fmt_price,
            "Portfolio Book Cost": fmt_price,
            "Transaction Quantity": fmt_qty,
            "Portfolio Quantity": fmt_qty,
        }
    )

    st.dataframe(styled, use_container_width=True)
    csv = trades_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv, file_name="trades.csv", mime="text/csv")


def render_chart(hourly_df: pd.DataFrame, trades_df: pd.DataFrame):
    """Render price chart with trade markers."""
    if hourly_df.empty:
        st.warning("No price data available.")
        return

    price_df = hourly_df.reset_index().rename(columns={hourly_df.index.name or "index": "Date"})
    price_chart = (
        alt.Chart(price_df)
        .mark_line()
        .encode(x="Date:T", y="Close:Q")
        .interactive()
    )

    trade_points = trades_df[trades_df["Action"].isin(["BUY", "SELL"])]
    if not trade_points.empty:
        trade_chart = (
            alt.Chart(trade_points)
            .mark_point(size=80)
            .encode(
                x="Date:T",
                y="Transaction Price:Q",
                color="Action:N",
                shape="Action:N",
            )
        )
        chart = price_chart + trade_chart
    else:
        chart = price_chart

    st.altair_chart(chart, use_container_width=True)
