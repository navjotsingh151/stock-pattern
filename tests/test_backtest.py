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
    trades_df, kpis = run_backtest(hourly_df, daily_map, 2, 110)
    assert list(trades_df["Action"]) == ["BUY", "SELL"]
    assert kpis["Final PQ"] == 1
    assert kpis["Total Buys"] == 2
    assert kpis["Total Sells"] == 1


def test_hold_row_added():
    idx = [
        pd.Timestamp("2023-01-01 10:00"),
        pd.Timestamp("2023-01-01 11:00"),
        pd.Timestamp("2023-01-02 10:00"),
    ]
    hourly_df = pd.DataFrame({"Close": [98, 97, 103]}, index=idx)
    daily_map = {
        pd.Timestamp("2023-01-01").date(): (100, 102),
        pd.Timestamp("2023-01-02").date(): (104, 106),
    }
    trades_df, _ = run_backtest(hourly_df, daily_map, 2, 110)
    # Expect a HOLD row for second day since no trades occur on 2023-01-02
    actions = list(trades_df["Action"])
    assert actions[0] == "BUY"
    assert actions[1] == "HOLD"
