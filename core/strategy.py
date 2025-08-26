"""Trading strategy rules evaluated on each bar."""
from __future__ import annotations

from typing import Dict, List, Any

from .portfolio import Portfolio


def should_sell(price: float, pq: float, pbc: float) -> bool:
    """Return True if portfolio value is >= 120% of book cost."""
    if pq <= 0:
        return False
    return price * pq >= 1.2 * pbc


def sell_qty(pq: float) -> float:
    """Sell 50% of current quantity."""
    return round(pq * 0.5, 4)


def should_buy(price: float, day_open: float, x_percent: int) -> bool:
    """Return ``True`` when the hourly price has fallen sufficiently.

    A BUY is triggered if the current hourly price is less than or equal to
    ``(1 - X/100)`` times the day's open. For example, with ``day_open=100`` and
    ``X=2`` the threshold becomes ``98``. Any price of ``98`` or below will
    satisfy the condition and we purchase ``X`` shares.
    """
    if day_open is None:
        return False
    threshold = (1 - x_percent / 100) * day_open
    return price <= threshold


def buy_qty(x_percent: int) -> int:
    """Buy floor(x_percent) shares."""
    return int(x_percent)


def apply_bar(ts, day_open, day_close, price, portfolio: Portfolio, x_percent: int) -> List[Dict[str, Any]]:
    """Apply strategy on a single bar.

    Parameters
    ----------
    ts : Timestamp
        Hourly timestamp.
    day_open : float
        Day's open price.
    day_close : float
        Day's close price.
    price : float
        Current hourly price used for transactions.
    portfolio : Portfolio
        Portfolio instance to mutate.
    x_percent : int
        Threshold X in percent.

    Returns
    -------
    list[dict]
        A list of transaction dictionaries (0..2 entries) representing
        post-transaction state.
    """
    transactions: List[Dict[str, Any]] = []

    # SELL evaluation
    if should_sell(price, portfolio.qty, portfolio.book_cost):
        qty = sell_qty(portfolio.qty)
        portfolio.sell(qty, price)
        transactions.append(
            {
                "Date": ts,
                "Open Price": day_open,
                "Close Price": day_close,
                "Transaction Price": price,
                "Action": "SELL",
                "Portfolio Value": portfolio.value(price),
                "Portfolio Book Cost": portfolio.book_cost,
                "Transaction Quantity": qty,
                "Portfolio Quantity": portfolio.qty,
            }
        )

    # BUY evaluation (after potential sell)
    if should_buy(price, day_open, x_percent):
        qty = buy_qty(x_percent)
        portfolio.buy(qty, price)
        transactions.append(
            {
                "Date": ts,
                "Open Price": day_open,
                "Close Price": day_close,
                "Transaction Price": price,
                "Action": "BUY",
                "Portfolio Value": portfolio.value(price),
                "Portfolio Book Cost": portfolio.book_cost,
                "Transaction Quantity": qty,
                "Portfolio Quantity": portfolio.qty,
            }
        )

    return transactions
