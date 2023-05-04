# Exceptions.


class UnitError(Exception):
    """
    Raised on invalid unit passed to quantity(value: any, unit: str).
    """

    def __init__(self, unit: str) -> None:
        super().__init__(
            "unknown unit: {}".format(unit) if unit != "" else "empty unit"
        )


class QuantityError(Exception):
    """
    Raised on operations between incompatible quantities.
    """

    def __init__(self, first, second, operation: str) -> None:
        super().__init__(
            "unsupported operand unit(s) for {0}: '{1}' and '{2}'\nraised by: '{3}' {0} '{4}'".format(
                operation, first.unit(), second.unit(), first, second
            )
        )


class ConversionError(Exception):
    """
    Raised on errors during conversions.
    """

    def __init__(self, qnt, target: str) -> None:
        super().__init__(
            "cannot convert from '{0}' to '{1}'\nraised by: '{2}' -> '{1}'".format(
                qnt.unit(), target, qnt
            )
        )


class UnpackError(Exception):
    """
    Raised on errors during conversions.
    """

    def __init__(self, qnt, target: str) -> None:
        super().__init__(
            "cannot unpack '{1}' from '{0}'\nraised by: '{2}'".format(
                qnt.unit(), target, qnt
            )
        )


class PackError(Exception):
    """
    Raised on errors during conversions.
    """

    def __init__(self, qnt, target: str, full: bool = False) -> None:
        super().__init__(
            "cannot {3}pack '{0}' to '{1}'\nraised by: '{2}'".format(
                qnt.unit(), target, qnt, "fully " if full else ""
            )
            if target != ""
            else "cannot automatically pack"
        )


class DefinitionError(Exception):
    """
    Raised on errors during unit definition.
    """

    # Custom error defined in tables.py.
    def __init__(self, error: str = "") -> None:
        super().__init__(error)
