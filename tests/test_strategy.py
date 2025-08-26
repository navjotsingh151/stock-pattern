import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd

from core.portfolio import Portfolio
from core.strategy import (
    should_sell,
    should_buy,
    sell_qty,
    buy_qty,
    apply_bar,
)


def test_rules():
    assert should_sell(120, 10, 1000)
    assert not should_sell(110, 10, 1000)

    assert should_buy(98, 100, 2)  # equality at threshold should buy
    assert should_buy(97, 100, 2)
    assert not should_buy(99, 100, 2)

    assert sell_qty(10) == 5
    assert buy_qty(5) == 5


def test_apply_bar_sell_then_buy():
    p = Portfolio()
    p.buy(2, 10)
    ts = pd.Timestamp("2023-01-01 11:00")
    txns = apply_bar(ts, 100, 102, 98, p, 2)
    # Should sell then buy => two transactions
    assert len(txns) == 2
    assert txns[0]["Action"] == "SELL"
    assert txns[1]["Action"] == "BUY"
    # After sell then buy: qty should be 3
    assert p.qty == 3


def test_apply_bar_buy_blocked():
    p = Portfolio()
    ts = pd.Timestamp("2023-01-01 11:00")
    # Even though price triggers a buy, allow_buy=False prevents it
    txns = apply_bar(ts, 100, 102, 98, p, 2, allow_buy=False)
    assert txns == []
    assert p.qty == 0
