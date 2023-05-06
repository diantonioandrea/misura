# Utilities.
from re import findall


def checkIter(obj: any) -> bool:
    try:
        _ = iter(obj)
        return True

    except TypeError:
        return False


def uAll(obj: any) -> bool:
    """
    Python's 'all' for (non)iterable objects.
    """

    return all(obj) if checkIter(obj) else bool(obj)


def uAny(obj: any) -> bool:
    """
    Python's 'any' for (non)iterable objects.
    """

    return any(obj) if checkIter(obj) else bool(obj)


def dictFromUnit(unit: str) -> dict:
    from .exceptions import UnitError

    """
    Returns the dictionary of units from a properly formatted string.
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
