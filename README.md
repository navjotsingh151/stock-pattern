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

Buy `X` shares when the hourly price is less than or equal to `(1 - X/100)`
times the day's open. For example, with a day open of `100` and `X = 2`, any
hourly price of `98` or below will trigger a purchase of two shares at that
price. Only one BUY is allowed per day; after a BUY executes, additional BUYs
are suppressed until the next trading day.

**SELL**

If the portfolio value reaches or exceeds `Y%` of its book cost (default 110%),
sell 50% of the current position.

## Portfolio Calculations

- **Portfolio Value** = `current price × portfolio quantity`.
- **Portfolio Book Cost** tracks total cost basis after buys and sells. On a
  buy, book cost increases by `qty × price`. On a sell, the cost relieved is
  proportional to the fraction of shares sold.

The table includes one row per trading day. Days without a BUY or SELL are
recorded as `HOLD` rows using the day's close price.
