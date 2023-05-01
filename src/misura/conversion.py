from .units import unit

def convert(first: unit, second: unit) -> unit:
    pass

class ConversionError(Exception):
    def __init__(self, first, second) -> None:
        super().__init__("Cannot convert from {} to {}".format(first.symbol(), second.symbol()))