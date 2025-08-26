"""Portfolio module managing state and proportional cost basis."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Portfolio:
    """Simple single-lot portfolio with proportional cost accounting."""
    qty: float = 0.0
    book_cost: float = 0.0
    realized_pnl: float = 0.0

    def value(self, price: float) -> float:
        """Return market value at ``price``.

        Parameters
        ----------
        price: float
            Current market price.
        """
        return round(price * self.qty, 2)

    def buy(self, qty: float, price: float) -> None:
        """Buy ``qty`` shares at ``price``.

        Updates quantity and book cost. Quantities are rounded to four
        decimals while cost is stored at two decimals.
        """
        qty = round(qty, 4)
        price = round(price, 2)
        self.qty += qty
        self.book_cost = round(self.book_cost + qty * price, 2)

    def sell(self, qty: float, price: float) -> None:
        """Sell ``qty`` shares at ``price`` with proportional cost basis.

        Raises
        ------
        ValueError
            If attempting to sell more than currently held.
        """
        if qty > self.qty:
            raise ValueError("Cannot sell more than current position")

        qty = round(qty, 4)
        price = round(price, 2)

        if self.qty == 0:
            return

        # proportional cost relieved
        proportional_cost = self.book_cost * (qty / self.qty)
        proportional_cost = round(proportional_cost, 2)

        self.book_cost = round(self.book_cost - proportional_cost, 2)
        self.qty = round(self.qty - qty, 4)

        proceeds = round(price * qty, 2)
        self.realized_pnl = round(self.realized_pnl + proceeds - proportional_cost, 2)
