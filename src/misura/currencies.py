# Currencies.
from __future__ import annotations

from misura.quantities import quantity

from .exceptions import InitError, OperationError
from .quantities import quantity


class currency(quantity):
    def __init__(self, value: any, symbol: str = "") -> None:
        super().__init__(value, symbol)

        try:
            assert len(self.units) == 1

            self.symbol = list(self.units.copy()).pop()

            assert self.units[self.symbol] == 1

        except AssertionError:
            raise InitError(value, symbol)

    # MATH
    # Some modifications to quantities.

    # Multiplication.
    def __mul__(self, other: any) -> currency:
        if not isinstance(other, currency):
            return currency(self.value * other, self.unit())

        raise OperationError(self, other, "*")

    def __rmul__(self, other: any) -> any:
        return self.__mul__(other)

    # Division.
    def __truediv__(self, other: any) -> any:
        if not isinstance(other, currency):
            return currency(self.value / other, self.unit())

        raise OperationError(self, other, "/")

    def __rtruediv__(self, other: any) -> any:
        raise OperationError(other, self, "/")

    # Power.
    def __pow__(self, other: any) -> quantity:
        raise OperationError(self, other, "**")

    def __rpow__(self, other: any) -> quantity:
        raise OperationError(other, self, "**")
