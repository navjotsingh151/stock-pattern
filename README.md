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

Buy `X` shares when the hourly price is at least `(1 - X/100)` times the day's
open. For example, with a day open of `100` and `X = 2`, any hourly price of
`98` or above will trigger a purchase of two shares at that price.

**SELL**

If the portfolio value reaches or exceeds 120% of its book cost, sell 50% of
the current position.

## Portfolio Calculations

- **Portfolio Value** = `current price × portfolio quantity`.
- **Portfolio Book Cost** tracks total cost basis after buys and sells. On a
  buy, book cost increases by `qty × price`. On a sell, the cost relieved is
  proportional to the fraction of shares sold.

The app displays all hourly bars for the last year. Hours without trades are
marked with the action `HOLD` to explain periods where the SELL rule did not
trigger (e.g. price never reached 120% of book cost).
