# Streamlit Backtesting App

This project provides a simple intraday backtesting application using Streamlit and Yahoo Finance data.

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
streamlit run app.py
```

Use the sidebar to choose ticker and X% threshold, then run the backtest to view results.

## Strategy Rules

The backtest evaluates each hourly bar in **SELL then BUY** order.

**BUY**

Buy `X` shares when the hourly price is at most `(1 - X/100)` times the day's
open. For example, with a day open of `100` and `X = 2`, any hourly price of
`98` or below will trigger a purchase of two shares at that price.

**SELL**

If the portfolio value reaches or exceeds 120% of its book cost, sell 50% of
the current position.
