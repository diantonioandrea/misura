from colorama import Style

from .exceptions import *
from .tables import SI_TABLE, SI_DERIVED_TABLE, SI_DERIVED_UNPACKING_TABLE
from .utilities import dictFromUnit, unitFromDict, getFamily

# QUANTITIES

class quantity:
    def __init__(self, value: any, unit: str) -> None:
        try:
            assert type(unit) == str
            assert unit != ""

        except(AssertionError):
            raise UnitError(unit)

        self.value = value

        table = SI_TABLE.copy()
        table.update(SI_DERIVED_TABLE)

        # From unit: str to self.units: dict.
        self.units = dictFromUnit(unit)

        # Checks whether the unit can be converted with the available units.
        self.convertible = all([any([unit in table[family] for family in table]) for unit in self.units])
       
        # Define quantity's dimentsionality based on self.units.
        self.dimensionalities = {getFamily(unit): self.units[unit] for unit in self.units}

    # Returns a readable unit.
    def unit(self, print: bool = False) -> str:
        from .globals import style # Unit highlighting.

        # Fancy version.
        if print:
            # {"m": 1, "s": -1} -> "[m / s]".
            numerator = " ".join(sorted([sym + ("({})".format(self.units[sym]) if self.units[sym] != 1 else "") for sym in self.units if self.units[sym] > 0]))
            denominator = (" / " + " ".join(sorted([sym + ("({})".format(-1 * self.units[sym]) if self.units[sym] != -1 else "") for sym in self.units if self.units[sym] < 0]))) if len([sym for sym in self.units if self.units[sym] < 0]) else ""

            if not numerator and denominator:
                numerator = "1"

            if style.unitHighlighting:
                return Style.BRIGHT + numerator + denominator + Style.RESET_ALL if numerator else ""
            
            return "[" + numerator + denominator + "]" if numerator else ""
        
        # {"m": 1, "s": -1} -> "m s-1".
        return unitFromDict(self.units)

    # Returns a readable dimensionality.
    # No fancy style.
    def dimensionality(self) -> str:
        if not len(self.dimensionalities):
            return ""
        
        # {"length": 2, "time": -1} -> "[length(2) / time]".
        numerator = " * ".join(sorted([sym + ("({})".format(self.dimensionalities[sym]) if self.dimensionalities[sym] != 1 else "") for sym in self.dimensionalities if self.dimensionalities[sym] > 0]))
        denominator = (" / " + " * ".join(sorted([sym + ("({})".format(-1 * self.dimensionalities[sym]) if self.dimensionalities[sym] != -1 else "") for sym in self.dimensionalities if self.dimensionalities[sym] < 0]))) if len([sym for sym in self.dimensionalities if self.dimensionalities[sym] < 0]) else ""

        if not numerator and denominator:
            numerator = "1"
        
        return "[" + numerator + denominator + "]" if numerator else ""
    
    # STRINGS.


    def __str__(self) -> str:
        return "{} {}".format(self.value, self.unit(print=True)) if self.unit() else str(self.value)
    
    def __repr__(self) -> str:
        return str(self)
    
    def __format__(self, string) -> str: # Unit highlighting works for print only.
        # This works with units only.
        return self.value.__format__(string) + (" " + self.unit(print=True) if self.unit() else "")


    # PYTHON TYPES CONVERSION.


    # Int.
    def __int__(self) -> int:
        return int(self.value)
    
    # Float.
    def __float__(self) -> float:
        return float(self.value)
    
    # Complex.
    def __complex__(self) -> complex:
        return complex(self.value)

    # Bool.
    def __bool__(self) -> bool:
        return bool(self.value)


    # MATH.


    # Abs.
    def __abs__(self) -> "quantity":
        return quantity(abs(self.value), self.unit())
    
    # Positive.
    def __pos__(self) -> "quantity":
        return quantity(+self.value, self.unit())
    
    # Negative.
    def __neg__(self) -> "quantity":
        return quantity(-self.value, self.unit())
    
    # Invert.
    def __invert__(self) -> "quantity":
        return quantity(~self.value, self.unit())
    
    # Round.
    def __round__(self, number: int) -> "quantity":
        return quantity(round(self.value, number), self.unit())
    
    # Floor.
    def __floor__(self) -> "quantity":
        from math import floor
        return quantity(floor(self.value), self.unit())
    
    # Ceil.
    def __ceil__(self) -> "quantity":
        from math import ceil
        return quantity(ceil(self.value), self.unit())
    
    # Trunc.
    def __trunc__(self) -> "quantity":
        from math import trunc
        return quantity(trunc(self.value), self.unit())
    
    # Addition.
    def __add__(self, other: "quantity") -> "quantity":
        if self.unit() != other.unit():
            if self.convertible and other.convertible:
                other = convert(other, self.unit())

            else:
                raise UnitError(self, other, "+")
        
        return quantity(self.value + other.value, self.unit())
    
    def __radd__(self, other: "quantity") -> "quantity":
        return self.__add__(other)
    
    # Subtraction.
    def __sub__(self, other: "quantity") -> "quantity":
        if self.unit() != other.unit():
            if self.convertible and other.convertible:
                other = convert(other, self.unit())

            else:
                raise UnitError(self, other, "-")
        
        return quantity(self.value - other.value, self.unit())
    
    def __rsub__(self, other: "quantity") -> "quantity":
        return self.__sub__(other)

    # Multiplication.
    def __mul__(self, other: any) -> any:
        if type(other) != quantity:
            return quantity(self.value * other, self.unit())
        
        newUnits = self.units.copy()

        if self.convertible and other.convertible:
            other = convert(other, self.unit(), partial=True)

        for sym in newUnits:
            if sym in other.units:
                newUnits[sym] += other.units[sym]
        
        for sym in other.units:
            if sym not in newUnits:
                newUnits[sym] = other.units[sym]
        
        return quantity(self.value * other.value, unitFromDict(newUnits)) if unitFromDict(newUnits) else self.value * other.value
    
    def __rmul__(self, other: any) -> any:
        return self.__mul__(other)
    
    # Division.
    def __truediv__(self, other: any) -> any:
        if type(other) != quantity:
            return quantity(self.value / other, self.unit())
        
        newUnits = self.units.copy()

        if self.convertible and other.convertible:
            other = convert(other, self.unit(), partial=True)

        for sym in newUnits:
            if sym in other.units:
                newUnits[sym] -= other.units[sym]
        
        for sym in other.units:
            if sym not in newUnits:
                newUnits[sym] = -other.units[sym]
        
        return quantity(self.value / other.value, unitFromDict(newUnits)) if unitFromDict(newUnits) else self.value / other.value
    
    def __floordiv__(self, other: any) -> "quantity":
        return quantity(self.value // other, self.unit())

    def __rtruediv__(self, other: any) -> any:
        return self ** -1 * other
    
    # Power.
    def __pow__(self, other: any) -> "quantity":
        if other == 0:
            return 1

        newUnits = self.units.copy()

        for sym in newUnits:
            newUnits[sym] *= other

        return quantity(self.value ** other, unitFromDict(newUnits))
    
    # Modulo.
    def __mod__(self, other: any) -> "quantity":
        return quantity(self.value % other, self.unit())
    

    # COMPARISONS.


    # Less than.
    def __lt__(self, other: any) -> "quantity":
        if type(other) != quantity:
            return self.value < other
        
        if self.unit() != other.unit():
            if self.convertible and other.convertible:
                other = convert(other, self.unit())

            else:
                raise UnitError(self, other, "<")
        
        return self.value < other.value
    
    # Less or equal.
    def __le__(self, other: any) -> "quantity":
        if type(other) != quantity:
            return self.value <= other
        
        if self.unit() != other.unit():
            if self.convertible and other.convertible:
                other = convert(other, self.unit())

            else:
                raise UnitError(self, other, "<=")
        
        return self.value <= other.value
    
    # Greater than.
    def __gt__(self, other: any) -> "quantity":
        if type(other) != quantity:
            return self.value > other
        
        if self.unit() != other.unit():
            if self.convertible and other.convertible:
                other = convert(other, self.unit())

            else:
                raise UnitError(self, other, ">")
        
        return self.value > other.value
    
    # Greater or equal.
    def __ge__(self, other: any) -> "quantity":
        if type(other) != quantity:
            return self.value >= other
        
        if self.unit() != other.unit():
            if self.convertible and other.convertible:
                other = convert(other, self.unit())

            else:
                raise UnitError(self, other, ">=")
        
        return self.value >= other.value
    
    # Equal.
    def __eq__(self, other: any) -> "quantity":
        if type(other) != quantity:
            return self.value == other
        
        return self.value == other.value and self.unit() == other.unit()

    # Not equal.
    def __ne__(self, other: any) -> "quantity":
        if type(other) != quantity:
            return self.value != other
        
        return self.value != other.value or self.unit() != other.unit()
    
# CONVERSION, UNPACKING AND PACKING

# Conversion function.
def convert(converted: quantity, target: str, partial: bool = False, un_pack: bool = False) -> quantity:
    # un_pack: automatic (un)packing. To be written [1.(3/4).0].
    if not converted.convertible:
        raise ConversionError(converted, target)
    
    # Check compatibility.
    if not partial:
        if unpack(converted).dimensionality() != unpack(quantity(1, target)).dimensionality():
            raise ConversionError(converted, target)

    factor = 1.0
    units = converted.units.copy()
    targetUnits = dictFromUnit(target)

    partialTargets = []

    table = SI_TABLE.copy()
    table.update(SI_DERIVED_TABLE)

    for sym in units.keys():
        family = getFamily(sym)
        familyCounter = 0

        for targetSym in targetUnits:
            if targetSym in table[family]:
                targetUnit = targetSym
                familyCounter += 1

        if familyCounter == 0:
            if not partial:
                raise ConversionError(converted, target)
            
            partialTargets.append(sym + str(units[sym]))
            continue

        elif familyCounter > 1:
            raise ConversionError(converted, target)
        
        elif sym != targetUnit:
            if units[sym] != targetUnits[targetUnit]:
                raise ConversionError(converted, target)
            
            factor *= (table[family][sym] / table[family][targetUnit]) ** units[sym]
            partialTargets.append(targetUnit + str(targetUnits[targetUnit]))
            continue
        
        elif partial:
            partialTargets.append(sym + str(units[sym]))
    
    return quantity(converted.value * factor, target) if not partial else quantity(converted.value * factor, " ".join(partialTargets))

# Unpacking function.
def unpack(converted: quantity, targets: str = "") -> quantity:
    unpackTable = SI_DERIVED_UNPACKING_TABLE.copy()
    derivedTable = SI_DERIVED_TABLE.copy()

    if targets == "": # Unpacks all derived units.
        targets = " ".join([unit for unit in converted.units if getFamily(unit) in derivedTable])

        if targets == "":
            return converted

    for target in targets.split(" "):
        # This shouldn't raise an IndexError as long as there's a reference quantity for every family.
        conversionTarget = [unit for unit in derivedTable[getFamily(target)] if derivedTable[getFamily(target)][unit] == 1].pop()
        converted = convert(converted, conversionTarget, partial=True, un_pack=False)
        
        if conversionTarget not in unpackTable:
            raise UnpackError(converted, target)

        newUnits = {key: converted.units[key] for key in converted.units if key != conversionTarget}
        converted = (quantity(converted.value, unitFromDict(newUnits)) if len(newUnits) else converted.value) * (quantity(1, unpackTable[conversionTarget]) ** converted.units[conversionTarget])
    
    return converted

# Packing (simplifying) function.
def pack(converted: quantity, target: str = "") -> quantity:
    # To be written [1.3.0].
    pass