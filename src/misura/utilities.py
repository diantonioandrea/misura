from re import findall

from .exceptions import UnitError
from .tables import SI_TABLE, SI_DERIVED_TABLE, SI_DERIVED_UNPACKING_TABLE

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

def getRep(family: str) -> str:
    base = SI_TABLE.copy()
    derived = SI_DERIVED_TABLE.copy()

    unpackTable = SI_DERIVED_UNPACKING_TABLE.copy()

    if family in base:
        return [unit for unit in base[family] if base[family][unit] == 1].pop()
    
    if family in derived:
        unit = [unit for unit in derived[family] if derived[family][unit] == 1].pop()
        return "{} [{}]".format(unit, unpackTable[unit]) if unit in unpackTable else unit

def getFamily(unit: str) -> str:
    # Returns the family of a convertible unit (length, mass, ...).
    table = SI_TABLE.copy()
    table.update(SI_DERIVED_TABLE)

    for family in table:
        if unit in table[family]:
            return family
        
    return ""