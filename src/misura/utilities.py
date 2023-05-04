from re import findall

from .exceptions import UnitError

# Utilities.


def dictFromUnit(unit: str) -> dict:
    """
    Returns the dictionary of units from a properly formatted string..
    """

    units = dict()

    for sym in unit.split(" "):
        candidate = findall(r"-?\d+\.?\d*", sym)

        if len(candidate) == 1:
            power = candidate[0]

        elif len(candidate) > 1:
            raise UnitError(unit)

        else:
            power = "1"

        try:
            units[sym.replace(power, "")] = int(power)

        except ValueError:
            units[sym.replace(power, "")] = float(power)

    return units


def unitFromDict(units: dict) -> str:
    """
    Returns a properly formatted unit string from a dictionary.
    """

    return " ".join(
        sorted(
            [
                sym + ("{}".format(units[sym]) if units[sym] != 1 else "")
                for sym in units
                if units[sym] != 0
            ]
        )
    )
