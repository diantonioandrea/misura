from __future__ import annotations

from colorama import Style

from .exceptions import (
    UnitError,
    QuantityError,
    ConversionError,
    UnpackError,
    PackError,
)
from .tables import getBase, getDerived, getDerivedUnpacking, getFamily, getRep
from .utilities import dictFromUnit, unitFromDict

# QUANTITIES


class quantity:
    """
    The main class of misura, the class of quantities.
    """

    def __init__(self, value: any, unit: str) -> None:
        """
        value: Can be anything that can be somewhat treated as a number.
        unit: A properly formatted string including all the units with their exponents. e.g. "m s-1".
        """

        try:
            assert isinstance(unit, str)
            assert unit != ""

        except AssertionError:
            raise UnitError(unit)

        self.value: any = value

        table: dict = getBase()
        table.update(getDerived())

        # From unit: str to self.units: dict.
        self.units: dict = dictFromUnit(unit)

        # Checks whether the unit can be converted with the available units.
        self.convertible: bool = all(
            [any([unit in table[family] for family in table]) for unit in self.units]
        )

        # Define quantity's dimentsionality based on self.units.
        self.dimensionalities: dict = (
            {getFamily(unit): self.units[unit] for unit in self.units}
            if self.convertible
            else dict()
        )

    def unit(self, print: bool = False) -> str:
        """
        Returns a readable version of the quantity's unit.
        print = True makes the output fancier.
        """
        from .globals import style  # Unit highlighting.

        # Fancy version.
        if print:
            # {"m": 1, "s": -1} -> "[m / s]".
            numerator = " ".join(
                sorted(
                    [
                        unit
                        + (
                            "({})".format(self.units[unit])
                            if self.units[unit] != 1
                            else ""
                        )
                        for unit in self.units
                        if self.units[unit] > 0
                    ]
                )
            )
            denominator = (
                (
                    " / "
                    + " ".join(
                        sorted(
                            [
                                unit
                                + (
                                    "({})".format(-1 * self.units[unit])
                                    if self.units[unit] != -1
                                    else ""
                                )
                                for unit in self.units
                                if self.units[unit] < 0
                            ]
                        )
                    )
                )
                if len([unit for unit in self.units if self.units[unit] < 0])
                else ""
            )

            if not numerator and denominator:
                numerator = "1"

            if style.quantityHighlighting:
                return (
                    Style.BRIGHT + numerator + denominator + Style.RESET_ALL
                    if numerator
                    else ""
                )

            return "[" + numerator + denominator + "]" if numerator else ""

        # {"m": 1, "s": -1} -> "m s-1".
        return unitFromDict(self.units)

    def dimensionality(self) -> str:
        """
        Returns a readable version of the quantity's dimensionality.
        No fancy style.
        """

        if not len(self.dimensionalities):
            return ""

        # {"length": 2, "time": -1} -> "[length(2) / time]".
        numerator = " * ".join(
            sorted(
                [
                    dim
                    + (
                        "({})".format(self.dimensionalities[dim])
                        if self.dimensionalities[dim] != 1
                        else ""
                    )
                    for dim in self.dimensionalities
                    if self.dimensionalities[dim] > 0
                ]
            )
        )
        denominator = (
            (
                " / "
                + " * ".join(
                    sorted(
                        [
                            dim
                            + (
                                "({})".format(-1 * self.dimensionalities[dim])
                                if self.dimensionalities[dim] != -1
                                else ""
                            )
                            for dim in self.dimensionalities
                            if self.dimensionalities[dim] < 0
                        ]
                    )
                )
            )
            if len(
                [dim for dim in self.dimensionalities if self.dimensionalities[dim] < 0]
            )
            else ""
        )

        if not numerator and denominator:
            numerator = "1"

        return "[" + numerator + denominator + "]" if numerator else ""

    # STRINGS.

    def __str__(self) -> str:
        return (
            "{} {}".format(self.value, self.unit(print=True))
            if self.unit()
            else str(self.value)
        )

    def __repr__(self) -> str:
        return str(self)

    def __format__(self, string) -> str:  # Unit highlighting works for print only.
        # This works with print only.
        return self.value.__format__(string) + (
            " " + self.unit(print=True) if self.unit() else ""
        )

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
    def __abs__(self) -> quantity:
        return quantity(abs(self.value), self.unit())

    # Positive.
    def __pos__(self) -> quantity:
        return quantity(+self.value, self.unit())

    # Negative.
    def __neg__(self) -> quantity:
        return quantity(-self.value, self.unit())

    # Invert.
    def __invert__(self) -> quantity:
        return quantity(~self.value, self.unit())

    # Round.
    def __round__(self, number: int) -> quantity:
        return quantity(round(self.value, number), self.unit())

    # Floor.
    def __floor__(self) -> quantity:
        from math import floor

        return quantity(floor(self.value), self.unit())

    # Ceil.
    def __ceil__(self) -> quantity:
        from math import ceil

        return quantity(ceil(self.value), self.unit())

    # Trunc.
    def __trunc__(self) -> quantity:
        from math import trunc

        return quantity(trunc(self.value), self.unit())

    # Addition.
    def __add__(self, other: quantity) -> quantity:
        if self.unit() != other.unit():
            if self.convertible and other.convertible:
                # Chooses the one to convert.
                first = convert(self, other.unit())
                second = convert(other, self.unit())

                self, other = (
                    (first, other)
                    if len(first.unit()) < len(second.unit())
                    else (self, second)
                )

            else:
                raise QuantityError(self, other, "+")

        return quantity(self.value + other.value, self.unit())

    def __radd__(self, other: quantity) -> quantity:
        return self.__add__(other)

    # Subtraction.
    def __sub__(self, other: quantity) -> quantity:
        if self.unit() != other.unit():
            if self.convertible and other.convertible:
                # Chooses the one to convert.
                first = convert(self, other.unit())
                second = convert(other, self.unit())

                self, other = (
                    (first, other)
                    if len(first.unit()) < len(second.unit())
                    else (self, second)
                )

            else:
                raise QuantityError(self, other, "-")

        return quantity(self.value - other.value, self.unit())

    def __rsub__(self, other: quantity) -> quantity:
        return self.__sub__(other)

    # Multiplication.
    def __mul__(self, other: any) -> any:
        if not isinstance(other, quantity):
            return quantity(self.value * other, self.unit())

        newUnits = self.units.copy()

        if self.convertible and other.convertible:
            other = convert(other, self.unit(), partial=True)

        for unit in newUnits:
            if unit in other.units:
                newUnits[unit] += other.units[unit]

        for unit in other.units:
            if unit not in newUnits:
                newUnits[unit] = other.units[unit]

        return (
            quantity(self.value * other.value, unitFromDict(newUnits))
            if unitFromDict(newUnits)
            else self.value * other.value
        )

    def __rmul__(self, other: any) -> any:
        return self.__mul__(other)

    # Division.
    def __truediv__(self, other: any) -> any:
        if not isinstance(other, quantity):
            return quantity(self.value / other, self.unit())

        newUnits = self.units.copy()

        if self.convertible and other.convertible:
            other = convert(other, self.unit(), partial=True)

        for unit in newUnits:
            if unit in other.units:
                newUnits[unit] -= other.units[unit]

        for unit in other.units:
            if unit not in newUnits:
                newUnits[unit] = -other.units[unit]

        return (
            quantity(self.value / other.value, unitFromDict(newUnits))
            if unitFromDict(newUnits)
            else self.value / other.value
        )

    def __floordiv__(self, other: any) -> quantity:
        return quantity(self.value // other, self.unit())

    def __rtruediv__(self, other: any) -> any:
        return self**-1 * other

    # Power.
    def __pow__(self, other: any) -> quantity:
        if other == 0:
            return 1

        newUnits = self.units.copy()

        for unit in newUnits:
            newUnits[unit] *= other

        return quantity(self.value**other, unitFromDict(newUnits))

    # Modulo.
    def __mod__(self, other: any) -> quantity:
        return quantity(self.value % other, self.unit())

    # COMPARISONS.

    # Less than.
    def __lt__(self, other: any) -> quantity:
        if not isinstance(other, quantity):
            return self.value < other

        if self.unit() != other.unit():
            if self.convertible and other.convertible:
                other = convert(other, self.unit())

            else:
                raise QuantityError(self, other, "<")

        return self.value < other.value

    # Less or equal.
    def __le__(self, other: any) -> quantity:
        if not isinstance(other, quantity):
            return self.value <= other

        if self.unit() != other.unit():
            if self.convertible and other.convertible:
                other = convert(other, self.unit())

            else:
                raise QuantityError(self, other, "<=")

        return self.value <= other.value

    # Greater than.
    def __gt__(self, other: any) -> quantity:
        if not isinstance(other, quantity):
            return self.value > other

        if self.unit() != other.unit():
            if self.convertible and other.convertible:
                other = convert(other, self.unit())

            else:
                raise QuantityError(self, other, ">")

        return self.value > other.value

    # Greater or equal.
    def __ge__(self, other: any) -> quantity:
        if not isinstance(other, quantity):
            return self.value >= other

        if self.unit() != other.unit():
            if self.convertible and other.convertible:
                other = convert(other, self.unit())

            else:
                raise QuantityError(self, other, ">=")

        return self.value >= other.value

    # Equal.
    def __eq__(self, other: any) -> quantity:
        if not isinstance(other, quantity):
            return self.value == other

        return self.value == other.value and self.unit() == other.unit()

    # Not equal.
    def __ne__(self, other: any) -> quantity:
        if not isinstance(other, quantity):
            return self.value != other

        return self.value != other.value or self.unit() != other.unit()


# CONVERSION, UNPACKING AND PACKING


def convert(
    qnt: quantity, targets: str, partial: bool = False, un_pack: bool = True
) -> quantity:
    """
    Conversion function; converts the passed quantity object to the specified target units.

    "partial = True" converts only the specified units and "un_pack = True" enables automatic (un)packing.
    """

    if not qnt.convertible:
        raise ConversionError(qnt, targets)

    # Check dimensionality.
    if not partial:
        if (
            unpack(qnt).dimensionality()
            != unpack(quantity(1, targets)).dimensionality()
        ):
            raise ConversionError(qnt, targets)

    # Automatic (un)packing.
    # Version 1.
    if un_pack and not partial:
        try:
            return convert(pack(qnt, targets), targets, un_pack=False)

        except ConversionError:
            pass

        return convert(
            unpack(qnt),
            unpack(quantity(1, targets)).unit(),
            un_pack=False,
        )

    factor: float = 1.0
    units: dict = qnt.units.copy()
    targetUnits: dict = dictFromUnit(targets)

    partialTargets: dict = dict()

    table: dict = getBase()
    table.update(getDerived())

    for unit in units.keys():
        family = getFamily(unit)
        familyCounter = 0

        for targetSym in targetUnits:
            if targetSym in table[family]:
                targetUnit = targetSym
                familyCounter += 1

        if familyCounter == 0:
            if not partial:
                raise ConversionError(qnt, targets)

            partialTargets[unit] = units[unit]
            continue

        elif familyCounter > 1:
            raise ConversionError(qnt, targets)

        elif unit != targetUnit:
            if units[unit] != targetUnits[targetUnit]:
                raise ConversionError(qnt, targets)

            factor *= (table[family][unit] / table[family][targetUnit]) ** units[unit]
            partialTargets[targetUnit] = targetUnits[targetUnit]
            continue

        elif partial:
            partialTargets[unit] = units[unit]

    return (
        quantity(qnt.value * factor, targets)
        if not partial
        else quantity(qnt.value * factor, unitFromDict(partialTargets))
    )


def unpack(qnt: quantity, targets: str = "") -> quantity:
    """
    Unpacking function; unpacks the passed targets units form the quantity object.

    'targets = ""' completely unpacks the quantity.
    """

    unpackTable: dict = getDerivedUnpacking()
    derivedTable: dict = getDerived()

    if targets == "":  # Unpacks all derived units.
        targets = " ".join(
            [unit for unit in qnt.units if getFamily(unit) in derivedTable]
        )

        if targets == "":
            return qnt

    for target in dictFromUnit(targets):
        if getFamily(target) not in [getFamily(unit) for unit in qnt.units]:
            raise UnpackError(qnt, target)

        conversionTarget = getRep(getFamily(target))
        conversionTargetPower = [
            qnt.units[unit]
            for unit in qnt.units
            if getFamily(unit) == getFamily(target)
        ].pop()

        qnt = convert(
            qnt,
            conversionTarget + str(conversionTargetPower),
            partial=True,
            un_pack=False,
        )

        if conversionTarget not in unpackTable:
            raise UnpackError(qnt, target)

        newUnits = {key: qnt.units[key] for key in qnt.units if key != conversionTarget}
        qnt = (
            quantity(qnt.value, unitFromDict(newUnits)) if len(newUnits) else qnt.value
        ) * (quantity(1, unpackTable[conversionTarget]) ** qnt.units[conversionTarget])

    return qnt


# Packing function.
def pack(qnt: quantity, targets: str, ignore: str = "", full: bool = False) -> quantity:
    """
    Packing function; packs the passed quantity object's unit according to the targets and the ones to ignore.

    'full = True' fully pack a unit.
    """

    packTable: dict = getDerivedUnpacking()

    unitsTable: dict = getBase()
    unitsTable.update(getDerived())

    if targets == "":
        raise PackError(qnt, "")

    # Simplify qnt -> base unit.
    for unit in qnt.units:
        conversionTarget = [
            unit
            for unit in unitsTable[getFamily(unit)]
            if unitsTable[getFamily(unit)][unit] == 1
        ].pop()
        qnt = convert(
            qnt, conversionTarget + str(qnt.units[unit]), partial=True, un_pack=False
        )

    # Unpack only relevant units.
    if ignore:
        for ignored in dictFromUnit(ignore):
            if getFamily(ignored) not in [getFamily(unit) for unit in qnt.units]:
                raise PackError(qnt, targets, ignore)

    qnt = (
        quantity(
            qnt.value,
            unitFromDict(
                {
                    unit: qnt.units[unit]
                    for unit in qnt.units
                    if unit in dictFromUnit(ignore)
                }
            ),
        )
        * unpack(
            quantity(
                1,
                unitFromDict(
                    {
                        unit: qnt.units[unit]
                        for unit in qnt.units
                        if unit not in dictFromUnit(ignore)
                    }
                ),
            )
        )
        if ignore
        else unpack(qnt)
    )

    for target in dictFromUnit(targets):
        if target not in packTable:
            continue

        targetUnits = dictFromUnit(packTable[target])

        # Packing powers.
        powers = {
            # Updated from // to / to account for fractional powers.
            qnt.units[targetUnit] / targetUnits[targetUnit]
            for targetUnit in targetUnits
            if targetUnit in qnt.units
        }

        if not len(powers):
            raise PackError(qnt, targets)

        if full:
            # Packability check.
            for targetUnit in targetUnits:
                if targetUnit not in qnt.units:
                    raise PackError(qnt, targets, full=True)

                if qnt.units[targetUnit] % targetUnits[targetUnit]:
                    raise PackError(qnt, targets, full=True)

            if min(powers) < max(powers) or max(powers) < 0:
                raise PackError(qnt, targets, full=True)

        qnt *= (quantity(1, target) / quantity(1, unitFromDict(targetUnits))) ** max(
            powers
        )

    return qnt
