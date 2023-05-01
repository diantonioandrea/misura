# Unit class.

class unit:
    def __init__(self, value: float, symbol: str) -> None:
        self.value = value
        self.symbol = symbol

        self.power = 1

    # String.
    def __str__(self) -> str:
        if self.power:
            return "{} {}{}".format(self.value, self.symbol, "^{}".format(self.power) if self.power != 1 else "")
        
        else:
            return str(self.value)
    
    # Addition.
    def __add__(self, other: "unit") -> "unit":
        if self.symbol != other.symbol:
            raise SymbolError(self, other, "+")
        
        return unit(self.value + other.value, self.symbol)
    
    def __radd__(self, other: "unit") -> "unit":
        return self.__add__(other)
    
    # Subtraction.
    def __sub__(self, other: "unit") -> "unit":
        if self.symbol != other.symbol:
            raise SymbolError(self, other, "-")
        
        return unit(self.value - other.value, self.symbol)
    
    def __rsub__(self, other: "unit") -> "unit":
        return self.__sub__(other)

# Exceptions.

class UnitError(TypeError):
    def __init__(self, first: "unit", second: "unit", operation: str) -> None:
        super().__init__("SymbolError: unsupported operand symbol(s) for {}: \'{}\' and \'{}\'".format(first.symbol, second.symbol, operation))

class SymbolError(TypeError):
    def __init__(self, first: "unit", second: "unit", operation: str) -> None:
        super().__init__("SymbolError: unsupported operand symbol(s) for {}: \'{}\' and \'{}\'".format(first.symbol, second.symbol, operation))