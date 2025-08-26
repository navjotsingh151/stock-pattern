import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from core.portfolio import Portfolio


def test_buy_sell_flow():
    p = Portfolio()
    p.buy(10, 100)
    assert p.qty == 10
    assert p.book_cost == 1000

    p.sell(5, 120)
    assert round(p.qty, 4) == 5
    assert p.book_cost == 500
    assert p.realized_pnl == 100  # 5*(120-100)

    assert p.value(120) == 600
