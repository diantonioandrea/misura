# Currencies.
from __future__ import annotations

from typing import Any

from misura.quantities import quantity

from .exceptions import InitError, OperationError
from .quantities import compare, quantity
from .tables import fetchCurrencies, getCurrencies

# Checks currency rates on currencies import.
fetchCurrencies()


class currency(quantity):
    def __init__(self, value: Any, symbol: str = "") -> None:
        super().__init__(value, symbol)

        try:
            # Currencies should have one single unit.
            assert len(self.units) == 1
            assert all(self.units[u] == 1 for u in self.units)

        except AssertionError:
            raise InitError(value, symbol)

        table: dict = getCurrencies()
        if not any([any([u in table[family] for u in self.units]) for family in table]):
            raise InitError(value, symbol)

        else:
            # Valid currencies are always convertible.
            self.convertible = True
            self.dimensions = {"currency": 1}

    # STRINGS.
    # Removed uncertainty.

    def __str__(self) -> str:
        unit = self.unit(print=True)

        return "{}{}".format(
            round(self.value, 2),  # Default behaviour.
            (" " + unit) if self.units else "",
        )

    def __repr__(self) -> str:
        return str(self)

    def __format__(self, string) -> str:  # Unit highlighting works for print only.
        unit = self.unit(print=True)

        # This works best with print.
        return self.value.__format__(string) + ((" " + unit) if self.units else "")

    # MATH
    # Some modifications to quantities' math.

    # Abs.
    def __abs__(self) -> currency:
        return currency(abs(self.value), self.unit())

    # Positive.
    def __pos__(self) -> currency:
        return currency(+self.value, self.unit())

    # Negative.
    def __neg__(self) -> currency:
        return currency(-self.value, self.unit())

    # Round.
    def __round__(self, number: int) -> currency:
        return currency(round(self.value, number), self.unit())

    # Floor.
    def __floor__(self) -> currency:
        from math import floor

        return currency(floor(self.value), self.unit())

    # Ceil.
    def __ceil__(self) -> currency:
        from math import ceil

        return currency(ceil(self.value), self.unit())

    # Trunc.
    def __trunc__(self) -> currency:
        from math import trunc

        return currency(trunc(self.value), self.unit())

    # Addition.
    def __add__(self, other: currency) -> currency:
        if not isinstance(other, currency):
            raise OperationError(self, other, "+")

        if not compare(self, other):
            other = other.cto(self.unit())

        return currency(self.value + other.value, self.unit())

    # Subtraction.
    def __sub__(self, other: currency) -> currency:
        if not isinstance(other, currency):
            raise OperationError(self, other, "-")

        if not compare(self, other):
            other = other.cto(self.unit())

        return currency(self.value + other.value, self.unit())

    # Multiplication.
    def __mul__(self, other: Any) -> currency:
        if not isinstance(other, currency):
            return currency(self.value * other, self.unit())

        raise OperationError(self, other, "*")

    def __rmul__(self, other: Any) -> any:
        return self.__mul__(other)

    # Division.
    def __truediv__(self, other: Any) -> any:
        if not isinstance(other, currency):
            return currency(self.value / other, self.unit())

        raise OperationError(self, other, "/")

    def __rtruediv__(self, other: Any) -> any:
        raise OperationError(other, self, "/")

    def __floordiv__(self, other: Any) -> any:
        if not isinstance(other, currency):
            return currency(self.value // other, self.unit())

        raise OperationError(self, other, "//")

    def __rfloordiv__(self, other: Any) -> any:
        raise OperationError(other, self, "//")

    # Power.
    def __pow__(self, other: Any) -> quantity:
        raise OperationError(self, other, "**")

    def __rpow__(self, other: Any) -> quantity:
        raise OperationError(other, self, "**")
