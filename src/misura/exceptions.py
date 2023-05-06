# Exceptions.


class UnitError(Exception):
    """
    Raised on invalid units.
    """

    def __init__(self, unit: str) -> None:
        super().__init__("invalid unit '{}'".format(unit))


class InitError(Exception):
    """
    Raised on invalid parameters passed to quantity.__init__().
    """

    def __init__(self, value: any, unit: str = "", uncertainty: any = 0) -> None:
        from .utilities import uAny

        super().__init__(
            "wrong parameters on quantity definition\nraised by: quantity({}{}{})".format(
                value,
                ", {}".format(unit) if unit else "",
                ", {}".format(uncertainty) if uAny(uncertainty) else "",
            )
        )


class QuantityError(Exception):
    """
    Raised on operators between incompatible quantities.
    """

    def __init__(self, first, second, operator: str) -> None:
        super().__init__(
            "unsupported operand unit(s) for {0}: '{1}' and '{2}'\nraised by: '{3}' {0} '{4}'".format(
                operator, first.unit(), second.unit(), first, second
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

    def __init__(self, qnt, target: str, ignore: str = "", full: bool = False) -> None:
        if ignore:  # Error on ignore.
            super().__init__(
                "cannot ignore '{1}'\nraised by: '{0}'".format(qnt, ignore)
            )

        elif not target:  # Missing target.
            super().__init__("cannot automatically pack\nraised by: '{0}'".format(qnt))

        elif full:
            super().__init__(
                "cannot fully pack '{2}' to '{1}'\nraised by: '{0}'".format(
                    qnt, target, qnt.unit()
                )
            )

        else:
            super().__init__(
                "cannot pack '{2}' to '{1}'\nraised by: '{0}'".format(
                    qnt, target, qnt.unit()
                )
            )


class UncertaintyComparisonError(Exception):
    """
    Raised on comparing quantities with uncertainty.
    """

    def __init__(self, first, second, operator: str) -> None:
        super().__init__(
            "cannot compare uncertain quantities\nraised by: '{}' {} '{}'".format(
                first, operator, second
            )
        )


class DefinitionError(Exception):
    """
    Raised on errors during unit definition.
    """

    # Custom error defined in tables.py.
    def __init__(self, error: str = "") -> None:
        super().__init__(error)
