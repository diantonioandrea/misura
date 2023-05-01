# Unit class.

from colorama import Style
import re

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
            candidate = re.findall(r"-?\d+\.?\d*", sym)

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

    # String.
    def __str__(self) -> str:
        return "{} {}".format(self.value, self.symbol(print=True)) if self.symbol() else str(self.value)
    
    def __repr__(self) -> str:
        return str(self)
    

    # MATH


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
    
    def __rtruediv__(self, other: any) -> any:
        return self ** -1 * other
    
    # Power.
    def __pow__(self, exponent: any) -> "unit":
        if exponent == 0:
            return 1

        newSymbols = self.symbols.copy()

        for sym in newSymbols:
            newSymbols[sym] *= exponent

        return unit(self.value ** exponent, symbolFromDict(newSymbols))


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