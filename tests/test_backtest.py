import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd

from core.backtest import run_backtest


def test_run_backtest_basic():
    idx = [
        pd.Timestamp("2023-01-01 10:00"),
        pd.Timestamp("2023-01-01 11:00"),
        pd.Timestamp("2023-01-01 12:00"),
    ]
    hourly_df = pd.DataFrame({"Close": [98, 97, 120]}, index=idx)
    daily_map = {pd.Timestamp("2023-01-01").date(): (100, 102)}
    trades_df, kpis = run_backtest(hourly_df, daily_map, 2)
    assert list(trades_df["Action"]) == ["BUY", "SELL"]
    assert kpis["Final PQ"] == 1
    assert kpis["Total Buys"] == 2
    assert kpis["Total Sells"] == 1
