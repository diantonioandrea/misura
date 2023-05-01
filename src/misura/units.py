# Unit class.

from colorama import Style
from re import findall

class unit:
    def __init__(self, value: any, symbol: str) -> None:
        try:
            assert type(symbol) == str
            assert symbol != ""

        except(AssertionError):
            raise UnitError(symbol)

        self.value = value
        
        # From symbol: str to self.symbols: dict.
        self.symbols = dict()
        symbols = symbol.split(" ")
        
        for sym in symbols:
            candidate = findall(r"-?\d+\.?\d*", sym)

            if len(candidate) == 1:
                power = candidate[0]
            
            elif len(candidate) > 1:
                raise UnitError(symbol)
            
            else:
                power = "1"

            self.symbols[sym.replace(power, "")] = float(power)

    # Returns a readable symbol.
    def symbol(self, print: bool = False) -> str:
        from .globals import style # Unit highlighting.

        # Fancy version.
        if print:
            # {"m": 1, "s": -1} -> "[m / s]".
            numerator = " ".join(sorted([sym + ("({})".format(self.symbols[sym]) if self.symbols[sym] != 1 else "") for sym in self.symbols if self.symbols[sym] > 0]))
            denominator = (" / " + " ".join(sorted([sym + ("({})".format(-1 * self.symbols[sym]) if self.symbols[sym] != -1 else "") for sym in self.symbols if self.symbols[sym] < 0]))) if len([sym for sym in self.symbols if self.symbols[sym] < 0]) else ""

            if not numerator and denominator:
                numerator = "1"

            if style.unitHighlighting:
                return Style.BRIGHT + numerator + denominator + Style.RESET_ALL if numerator else ""
            
            return "[" + numerator + denominator + "]" if numerator else ""
        
        # {"m": 1, "s": -1} -> "m s-1".
        return symbolFromDict(self.symbols)


    # STRINGS


    def __str__(self) -> str:
        return "{} {}".format(self.value, self.symbol(print=True)) if self.symbol() else str(self.value)
    
    def __repr__(self) -> str:
        return str(self)
    
    def __format__(self, string) -> str: # Unit highlighting works for print only.
        return self.value.__format__(string) + (" " + self.symbol(print=True) if self.symbol() else "")


    # PYTHON TYPES CONVERSION.


    # Int.
    def __int__(self) -> int:
        return int(self.value)
    
    # Float.
    def __float__(self) -> float:
        return float(self.value)
    
    # Complex.
    def __complex__(self) -> complex:
        return complex(self.value)

    # Bool.
    def __bool__(self) -> bool:
        return bool(self.value)


    # MATH


    # Abs.
    def __abs__(self) -> "unit":
        return unit(abs(self.value), self.symbol())
    
    # Positive.
    def __pos__(self) -> "unit":
        return unit(+self.value, self.symbol())
    
    # Negative.
    def __neg__(self) -> "unit":
        return unit(-self.value, self.symbol())
    
    # Invert.
    def __invert__(self) -> "unit":
        return unit(~self.value, self.symbol())
    
    # Round.
    def __round__(self, number: int) -> "unit":
        return unit(round(self.value, number), self.symbol())
    
    # Floor.
    def __floor__(self) -> "unit":
        from math import floor
        return unit(floor(self.value), self.symbol())
    
    # Ceil.
    def __ceil__(self) -> "unit":
        from math import ceil
        return unit(ceil(self.value), self.symbol())
    
    # Trunc.
    def __trunc__(self) -> "unit":
        from math import trunc
        return unit(trunc(self.value), self.symbol())
    
    # Addition.
    def __add__(self, other: "unit") -> "unit":
        if self.symbol() != other.symbol():
            raise SymbolError(self, other, "+")
        
        return unit(self.value + other.value, self.symbol())
    
    def __radd__(self, other: "unit") -> "unit":
        return self.__add__(other)
    
    # Subtraction.
    def __sub__(self, other: "unit") -> "unit":
        if self.symbol() != other.symbol():
            raise SymbolError(self, other, "-")
        
        return unit(self.value - other.value, self.symbol())
    
    def __rsub__(self, other: "unit") -> "unit":
        return self.__sub__(other)

    # Multiplication.
    def __mul__(self, other: any) -> any:
        if type(other) != unit:
            return unit(self.value * other, self.symbol())
        
        newSymbols = self.symbols.copy()

        for sym in newSymbols:
            if sym in other.symbols:
                newSymbols[sym] += other.symbols[sym]
        
        for sym in other.symbols:
            if sym not in newSymbols:
                newSymbols[sym] = other.symbols[sym]
        
        return unit(self.value * other.value, symbolFromDict(newSymbols)) if symbolFromDict(newSymbols) else self.value * other.value
    
    def __rmul__(self, other: any) -> any:
        return self.__mul__(other)
    
    # Division.
    def __truediv__(self, other: any) -> any:
        if type(other) != unit:
            return unit(self.value / other, self.symbol())
        
        newSymbols = self.symbols.copy()

        for sym in newSymbols:
            if sym in other.symbols:
                newSymbols[sym] -= other.symbols[sym]
        
        for sym in other.symbols:
            if sym not in newSymbols:
                newSymbols[sym] = -other.symbols[sym]
        
        return unit(self.value / other.value, symbolFromDict(newSymbols)) if symbolFromDict(newSymbols) else self.value / other.value
    
    def __floordiv__(self, other: any) -> "unit":
        return unit(self.value // other, self.symbol())

    def __rtruediv__(self, other: any) -> any:
        return self ** -1 * other
    
    # Power.
    def __pow__(self, other: any) -> "unit":
        if other == 0:
            return 1

        newSymbols = self.symbols.copy()

        for sym in newSymbols:
            newSymbols[sym] *= other

        return unit(self.value ** other, symbolFromDict(newSymbols))
    
    # Modulo.
    def __mod__(self, other: any) -> "unit":
        return unit(self.value % other, self.symbol())
    

    # COMPARISONS


    # Less than.
    def __lt__(self, other: any) -> "unit":
        if type(other) != unit:
            return self.value < other
        
        if self.symbol() != other.symbol():
            raise SymbolError(self, other, "<")
        
        return self.value < other.value
    
    # Less or equal.
    def __le__(self, other: any) -> "unit":
        if type(other) != unit:
            return self.value <= other
        
        if self.symbol() != other.symbol():
            raise SymbolError(self, other, "<=")
        
        return self.value <= other.value
    
    # Greater than.
    def __gt__(self, other: any) -> "unit":
        if type(other) != unit:
            return self.value > other
        
        if self.symbol() != other.symbol():
            raise SymbolError(self, other, ">")
        
        return self.value > other.value
    
    # Greater or equal.
    def __ge__(self, other: any) -> "unit":
        if type(other) != unit:
            return self.value >= other
        
        if self.symbol() != other.symbol():
            raise SymbolError(self, other, ">=")
        
        return self.value >= other.value
    
    # Equal.
    def __eq__(self, other: any) -> "unit":
        if type(other) != unit:
            return self.value == other
        
        return self.value == other.value and self.symbol() == other.symbol()

    # Not equal.
    def __ne__(self, other: any) -> "unit":
        if type(other) != unit:
            return self.value != other
        
        return self.value != other.value or self.symbol() != other.symbol()

# Utilities.

def symbolFromDict(symbols: dict) -> str:
    return " ".join(sorted([sym + ("{}".format(symbols[sym]) if symbols[sym] != 1 else "") for sym in symbols if symbols[sym] != 0]))

# Exceptions.

class UnitError(TypeError):
    def __init__(self, symbol: str) -> None:
        super().__init__("unknown symbol: {}".format(symbol))

class SymbolError(Exception):
    def __init__(self, first: "unit", second: "unit", operation: str) -> None:
        super().__init__("unsupported operand symbol(s) for {}: \'{}\' and \'{}\'".format(operation, first.symbol(), second.symbol()))