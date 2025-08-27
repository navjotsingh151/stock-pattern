"""Formatting helpers for numbers and currency."""
from __future__ import annotations


def fmt_price(val: float) -> str:
    return f"{val:,.2f}"


def fmt_qty(val: float) -> str:
    return f"{val:,.4f}"
