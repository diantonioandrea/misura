# Exceptions.

class UnitError(Exception):
    def __init__(self, unit: str) -> None:
        super().__init__("unknown unit: {}".format(unit) if unit != "" else "empty unit")

class QuantityError(Exception):
    def __init__(self, first, second, operation: str) -> None:
        super().__init__("unsupported operand unit(s) for {0}: \'{1}\' and \'{2}\'\nraised by: \'{3}\' {0} \'{4}\'".format(operation, first.unit(), second.unit(), first, second))
        
class ConversionError(Exception):
    def __init__(self, first, target: str) -> None:
        super().__init__("cannot convert from \'{0}\' to \'{1}\'\nraised by: \'{2}\' -> \'{1}\'".format(first.unit(), target, first))

class UnpackError(Exception):
    def __init__(self, quantity, target: str) -> None:
        super().__init__("cannot unpack \'{1}\' from \'{0}\'\nraised by: \'{2}\'".format(quantity.unit(), target, quantity))

class PackError(Exception):
    def __init__(self, quantity, target: str, full: bool = False) -> None:
        super().__init__("cannot {3}pack \'{0}\' to \'{1}\'\nraised by: \'{2}\'".format(quantity.unit(), target, quantity, "fully " if full else "") if target != "" else "cannot automatically pack")