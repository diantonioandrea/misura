from re import findall

from .exceptions import UnitError
from .tables import SI_TABLE, SI_DERIVED_TABLE

# Utilities.

def dictFromUnit(unit: str) -> dict:
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

        except(ValueError):
            units[sym.replace(power, "")] = float(power)

    return units

def unitFromDict(units: dict) -> str:
    return " ".join(sorted([sym + ("{}".format(units[sym]) if units[sym] != 1 else "") for sym in units if units[sym] != 0]))

def getFamily(unit: str) -> str:
    # Returns the family of a convertible unit (length, mass, ...).
    table = SI_TABLE.copy()
    table.update(SI_DERIVED_TABLE)

    for family in table:
        if unit in table[family]:
            return family
        
    return ""