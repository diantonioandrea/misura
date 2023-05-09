# Quantities.
from __future__ import annotations

from colorama import Style
from math import sqrt, log

from .exceptions import (
    InitError,
    QuantityError,
    ConversionError,
    UnpackError,
    PackError,
    UncertaintyComparisonError,
)
from .tables import getBase, getDerived, getDerivedUnpacking, getFamily, getRep
from .utilities import checkIter, uAll, uAny
from .utilities import unitFromDict as ufd
from .utilities import dictFromUnit as dfu
from .globals import style, logic


class quantity:
    """
    misura's quantity class.
    """

    def __init__(self, value: any, unit: str = "", uncertainty: any = 0) -> None:
        """
        Quantity initialization.

        - value: Can be anything that can be somewhat treated as a number.
        - unit: A properly formatted string including all the units with their exponents. e.g. "m s-1".
        - uncertainty: Value's uncertainty.
        """

        try:
            assert isinstance(unit, str)
            assert uAll(uncertainty >= 0)
            assert (
                (checkIter(value) == checkIter(uncertainty))
                if uAny(uncertainty)
                else True
            )

        except AssertionError:
            raise InitError(value, unit, uncertainty)

        self.value: any = value
        self.uncertainty = uncertainty

        table: dict = getBase()
        table.update(getDerived())

        # From unit: str to self.units: dict.
        self.units: dict = dfu(unit)

        # Checks whether the unit can be converted with the available units.
        self.convertible: bool = all(
            [any([unit in table[family] for family in table]) for unit in self.units]
        )

        # Define quantity's dimentsionality based on self.units.
        self.dimensions: dict = (
            {getFamily(unit): self.units[unit] for unit in self.units}
            if self.convertible
            else dict()
        )

    def unit(self, print: bool = False) -> str:
        """
        Returns a readable version of the quantity's unit.

        'print = True' makes the output fancier.
        """

        if not len(self.units):
            return ""

        uts: dict = self.units.copy()
        # ut: short for unit.

        if not print:
            # Plain version.
            # {"m": 1, "s": -1} -> "m s-1".
            return ufd(self.units)

        # Fancy version.
        # {"m": 1, "s": -1} -> "[m / s]".

        # Numerator with exponent
        numeratorWE = [
            "{}({})".format(ut, uts[ut]) for ut in uts if uts[ut] > 0 and uts[ut] != 1
        ]

        # Denominator with exponent
        denominatorWE = [
            "{}({})".format(ut, -uts[ut]) for ut in uts if uts[ut] < 0 and uts[ut] != 1
        ]

        # Numerator without exponent
        numeratorWOE = [ut for ut in uts if uts[ut] > 0 and uts[ut] == 1]

        # Denominator without exponent
        denominatorWOE = [ut for ut in uts if uts[ut] < 0 and uts[ut] == 1]

        numerator = " ".join(sorted(numeratorWE + numeratorWOE))
        denominator = " ".join(sorted(denominatorWE + denominatorWOE))

        if not numerator and denominator:
            numerator = "1"

        fraction = numerator + " / " + denominator if denominator else numerator

        if style.quantityHighlighting:
            return Style.BRIGHT + fraction + Style.RESET_ALL if numerator else ""

        return "[" + fraction + "]" if numerator else ""

    def dimension(self) -> str:
        """
        Returns a readable version of the quantity's dimension.
        """

        if not len(self.dimensions):
            return ""

        uts: dict = self.units.copy()
        # ut: short for unit.

        # Numerator with exponent
        numeratorWE = [
            "{}({})".format(getFamily(ut), uts[ut])
            for ut in uts
            if uts[ut] > 0 and uts[ut] != 1
        ]

        # Denominator with exponent
        denominatorWE = [
            "{}({})".format(getFamily(ut), -uts[ut])
            for ut in uts
            if uts[ut] < 0 and uts[ut] != 1
        ]

        # Numerator without exponent
        numeratorWOE = [getFamily(ut) for ut in uts if uts[ut] > 0 and uts[ut] == 1]

        # Denominator without exponent
        denominatorWOE = [getFamily(ut) for ut in uts if uts[ut] < 0 and uts[ut] == 1]

        numerator = " * ".join(sorted(numeratorWE + numeratorWOE))
        denominator = " * ".join(sorted(denominatorWE + denominatorWOE))

        if not numerator and denominator:
            numerator = "1"

        fraction = numerator + " / " + denominator if denominator else numerator

        return "[" + fraction + "]" if numerator else ""

    # STRINGS.

    def __str__(self) -> str:
        pm = style.quantityPlusMinus
        unit = self.unit(print=True)
        uncert = self.uncertainty

        return "{}{}{}".format(
            self.value, "{}{} ".format(pm, uncert) if uAny(uncert) else " ", unit
        )

    def __repr__(self) -> str:
        return str(self)

    def __format__(self, string) -> str:  # Unit highlighting works for print only.
        pm = style.quantityPlusMinus
        unit = self.unit(print=True)
        uncert = self.uncertainty

        # This works best with print.
        return (
            self.value.__format__(string)
            + ((pm + uncert.__format__(string)) if uAny(uncert) else "")
            + (" " + unit)
        )

    # PYTHON TYPES CONVERSION.
    # int, float and complex don't care about uncertainty.

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
        return bool(uAny(self.value) or uAny(self.uncertainty))

    # MATH.

    # Abs.
    def __abs__(self) -> quantity:
        # Ignores the case in which abs(uncertainty) > abs(value).
        return quantity(abs(self.value), self.unit(), self.uncertainty)

    # Positive.
    def __pos__(self) -> quantity:
        return quantity(+self.value, self.unit(), self.uncertainty)

    # Negative.
    def __neg__(self) -> quantity:
        return quantity(-self.value, self.unit(), self.uncertainty)

    # Invert.
    # def __invert__(self) -> quantity:
    #     return quantity(~self.value, self.unit())

    # Round.
    def __round__(self, number: int) -> quantity:
        return quantity(
            round(self.value, number), self.unit(), round(self.uncertainty, number + 1)
        )

    # Floor.
    def __floor__(self) -> quantity:
        from math import floor

        return quantity(floor(self.value), self.unit(), floor(self.uncertainty))

    # Ceil.
    def __ceil__(self) -> quantity:
        from math import ceil

        return quantity(ceil(self.value), self.unit(), ceil(self.uncertainty))

    # Trunc.
    def __trunc__(self) -> quantity:
        from math import trunc

        return quantity(trunc(self.value), self.unit(), trunc(self.uncertainty))

    # Addition.
    def __add__(self, other: any) -> quantity:
        if not isinstance(other, quantity):
            # Addition between pure numbers.
            if self.unit():
                raise QuantityError(self, quantity(other, ""), "+")

            return quantity(self.value + other, "", self.uncertainty)

        if self.unit() != other.unit():
            if self.convertible and other.convertible:
                # Chooses the one to convert based on unit length.
                first = convert(self, other.unit())
                second = convert(other, self.unit())

                self, other = (
                    (first, other)
                    if len(first.unit()) < len(second.unit())
                    else (self, second)
                )

            else:
                raise QuantityError(self, other, "+")

        return quantity(
            self.value + other.value,
            self.unit(),
            sqrt(self.uncertainty**2 + other.uncertainty**2),
        )

    def __radd__(self, other: quantity) -> quantity:
        return self.__add__(other)

    # Subtraction.
    def __sub__(self, other: any) -> quantity:
        if not isinstance(other, quantity):
            # Subtraction between pure numbers.
            if self.unit():
                raise QuantityError(self, quantity(other, ""), "-")

            return quantity(self.value - other, "", self.uncertainty)

        if self.unit() != other.unit():
            if self.convertible and other.convertible:
                # Chooses the one to convert based on unit length.
                first = convert(self, other.unit())
                second = convert(other, self.unit())

                self, other = (
                    (first, other)
                    if len(first.unit()) < len(second.unit())
                    else (self, second)
                )

            else:
                raise QuantityError(self, other, "-")

        return quantity(
            self.value - other.value,
            self.unit(),
            sqrt(self.uncertainty**2 + other.uncertainty**2),
        )

    def __rsub__(self, other: quantity) -> quantity:
        return self.__sub__(other) * (-1)

    # Multiplication.
    def __mul__(self, other: any) -> any:
        if not isinstance(other, quantity):
            return quantity(
                self.value * other, self.unit(), abs(self.uncertainty * other)
            )

        newUnits = self.units.copy()

        if self.convertible and other.convertible:
            other = convert(other, self.unit(), partial=True)

        for unit in newUnits:
            if unit in other.units:
                newUnits[unit] += other.units[unit]

        for unit in other.units:
            if unit not in newUnits:
                newUnits[unit] = other.units[unit]

        return quantity(
            self.value * other.value,
            ufd(newUnits),
            sqrt(
                (other.value * self.uncertainty) ** 2
                + (self.value * other.uncertainty) ** 2
            ),
        )

    def __rmul__(self, other: any) -> any:
        return self.__mul__(other)

    # Division.
    def __truediv__(self, other: any) -> any:
        if not isinstance(other, quantity):
            return quantity(
                self.value / other, self.unit(), abs(self.uncertainty / other)
            )

        newUnits = self.units.copy()

        if self.convertible and other.convertible:
            other = convert(other, self.unit(), partial=True)

        for unit in newUnits:
            if unit in other.units:
                newUnits[unit] -= other.units[unit]

        for unit in other.units:
            if unit not in newUnits:
                newUnits[unit] = -other.units[unit]

        return quantity(
            self.value / other.value,
            ufd(newUnits),
            sqrt(
                (self.uncertainty / other.value) ** 2
                + (self.value * other.uncertainty / (other.value**2)) ** 2
            ),
        )

    def __floordiv__(self, other: any) -> quantity:
        return quantity(
            self.value // other, self.unit(), abs(self.uncertainty // other)
        )

    def __rtruediv__(self, other: any) -> any:
        return self**-1 * other

    # Power.
    def __pow__(self, other: any) -> quantity:
        if isinstance(other, quantity):
            raise QuantityError(self, other, "**")

        if other == 0:
            return quantity(1 * bool(self.value), "", 1 * self.uncertainty != 0)

        if other == 1:
            return self

        newUnits = self.units.copy()

        for unit in newUnits:
            newUnits[unit] *= other

        return quantity(
            self.value**other,
            ufd(newUnits),
            abs(other) * (self.value ** (other - 1)) * self.uncertainty,
        )

    def __rpow__(self, other: any) -> quantity:
        if isinstance(other, quantity):
            raise QuantityError(other, self, "**")

        if uAny(other <= 0):
            raise ValueError(
                "math domain error\nraised on '{}' ** '{}'".format(other, self)
            )

        return quantity(
            other**self.value,
            "",
            abs(log(other) * (other**self.value) * self.uncertainty),
        ) * (other != 1) + self * (other == 1)

    # Modulo.
    def __mod__(self, other: any) -> quantity:
        return quantity(self.value % other, self.unit(), self.uncertainty % other)

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

        if (
            uAny(self.uncertainty) or uAny(self.uncertainty)
        ) and not logic.ignoreUncertainty:
            raise UncertaintyComparisonError(self, other, "<")

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

        if (
            uAny(self.uncertainty) or uAny(self.uncertainty)
        ) and not logic.ignoreUncertainty:
            raise UncertaintyComparisonError(self, other, "<=")

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

        if (
            uAny(self.uncertainty) or uAny(self.uncertainty)
        ) and not logic.ignoreUncertainty:
            raise UncertaintyComparisonError(self, other, ">")

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

        if (
            uAny(self.uncertainty) or uAny(self.uncertainty)
        ) and not logic.ignoreUncertainty:
            raise UncertaintyComparisonError(self, other, ">=")

        return self.value >= other.value

    # Equal.
    def __eq__(self, other: any) -> quantity:
        if not isinstance(other, quantity):
            return self.value == other

        if (
            uAny(self.uncertainty) or uAny(self.uncertainty)
        ) and not logic.ignoreUncertainty:
            raise UncertaintyComparisonError(self, other, "==")

        return self.value == other.value and self.unit() == other.unit()

    # Not equal.
    def __ne__(self, other: any) -> quantity:
        if not isinstance(other, quantity):
            return self.value != other

        if (
            uAny(self.uncertainty) or uAny(self.uncertainty)
        ) and not logic.ignoreUncertainty:
            raise UncertaintyComparisonError(self, other, "!=")

        return self.value != other.value or self.unit() != other.unit()

    # SHORTCUTS

    def cto(
        self, targets: str, partial: bool = False, un_pack: bool = True
    ) -> quantity:  # Convert to.
        return convert(self, targets, partial, un_pack)

    def uto(self, targets: str = "") -> quantity:  # Unpack to.
        return unpack(self, targets)

    def pto(
        self, targets: str, ignore: str = "", full: bool = False
    ) -> quantity:  # Pack to.
        return pack(self, targets, ignore, full)


# CONVERSION, UNPACKING AND PACKING


# Conversion function.
def convert(
    qnt: quantity, targets: str, partial: bool = False, un_pack: bool = True
) -> quantity:
    """
    Conversion function; converts the passed quantity object to the specified target units.

    "partial = True" converts only the specified units and "un_pack = True" enables automatic (un)packing.
    """

    # Cannot convert non-convertible units.
    if not qnt.convertible:
        raise ConversionError(qnt, targets)

    # Check dimension.
    if not partial:
        if unpack(qnt).dimension() != unpack(quantity(1, targets)).dimension():
            raise ConversionError(qnt, targets)

    # Automatic (un)packing, version 2.
    if un_pack and not partial:
        # Tries to pack qnt.
        target = quantity(1, targets)
        packUnits = {ut: target.units[ut] for ut in target.units if ut not in qnt.units}
        ignoreUnits = {ut: qnt.units[ut] for ut in qnt.units if ut not in target.units}

        for tr in range(3):
            try:
                if tr == 0:
                    # First try: uses ignore and full packing.
                    return convert(
                        pack(qnt, ufd(packUnits), ignore=ufd(ignoreUnits), full=True),
                        targets,
                        un_pack=False,
                    )

                if tr == 1:
                    # Second try: uses ignore.
                    return convert(
                        pack(qnt, ufd(packUnits), ignore=ufd(ignoreUnits)),
                        targets,
                        un_pack=False,
                    )

                elif tr == 2:
                    # Third try: does not use ignore.
                    return convert(
                        pack(qnt, ufd(packUnits)),
                        targets,
                        un_pack=False,
                    )

            except (PackError, ConversionError):
                pass

        # Completely unpacks units.
        return convert(
            unpack(qnt),
            unpack(target).unit(),
            un_pack=False,
        )

    factor: float = 1.0
    tUnits: dict = dfu(targets)  # Target units.

    pTargets: dict = dict()  # Partial targets.

    table: dict = getBase()
    table.update(getDerived())

    for unit in qnt.units.keys():
        family = getFamily(unit)

        # Number of corresponding families.
        families = len([tgt for tgt in tUnits if tgt in table[family]])

        # Check target presence if not partial.
        if families == 0 and not partial:
            raise ConversionError(qnt, targets)

        # Partial conversion.
        elif families == 0 and partial:
            pTargets[unit] = qnt.units[unit]
            continue

        # Target.
        target = [tgt for tgt in tUnits if tgt in table[family]].pop()

        # Too many units: errror.
        if families > 1:
            raise ConversionError(qnt, targets)

        # Wrong power.
        if unit != target and qnt.units[unit] != tUnits[target]:
            raise ConversionError(qnt, targets)

        # Conversion.
        elif unit != target and qnt.units[unit] == tUnits[target]:
            factor *= (table[family][unit] / table[family][target]) ** qnt.units[unit]
            pTargets[target] = tUnits[target]
            continue

        # Partial conversion.
        elif partial:
            pTargets[unit] = qnt.units[unit]

    return (
        quantity(qnt.value * factor, targets, qnt.uncertainty * factor)
        if not partial
        else quantity(qnt.value * factor, ufd(pTargets), qnt.uncertainty * factor)
    )


# Unpacking function.
def unpack(qnt: quantity, targets: str = "") -> quantity:
    """
    Unpacking function; unpacks the passed targets units form the quantity object.

    'targets = ""' completely unpacks the quantity.
    """

    unpackTable: dict = getDerivedUnpacking()
    derivedTable: dict = getDerived()

    if not targets:  # Unpacks all derived units.
        targets = " ".join(
            [unit for unit in qnt.units if getFamily(unit) in derivedTable]
        )

    for target in dfu(targets):
        # Checks target.
        if getFamily(target) not in [getFamily(unit) for unit in qnt.units]:
            raise UnpackError(qnt, target)

        cTarget = getRep(getFamily(target))  # Conversion target.
        cTargetPower = [  # Conversion target's power.
            qnt.units[unit]
            for unit in qnt.units
            if getFamily(unit) == getFamily(target)
        ].pop()

        # Raises an error if the program does not know how to unpack a unit.
        if cTarget not in unpackTable:
            raise UnpackError(qnt, target)

        # Converts the quantity to an unpackable one.
        qnt = convert(
            qnt,
            cTarget + str(cTargetPower),
            partial=True,
            un_pack=False,
        )

        # Units that werent't involved in the previous conversion.
        newUnits = {key: qnt.units[key] for key in qnt.units if key != cTarget}

        # Uncertainty should not vary on packing.
        uncertainty = qnt.uncertainty
        qnt = (quantity(qnt.value, ufd(newUnits)) if len(newUnits) else qnt.value) * (
            quantity(1, unpackTable[cTarget]) ** qnt.units[cTarget]
        )
        qnt.uncertainty = uncertainty

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
        cTarget = [
            unit
            for unit in unitsTable[getFamily(unit)]
            if unitsTable[getFamily(unit)][unit] == 1
        ].pop()
        qnt = convert(qnt, cTarget + str(qnt.units[unit]), partial=True, un_pack=False)

    # Unpack only relevant units.
    if ignore:
        for ignored in dfu(ignore):
            if getFamily(ignored) not in [getFamily(unit) for unit in qnt.units]:
                raise PackError(qnt, targets, ignore)

        val = qnt.value
        uts: dict = qnt.units.copy()
        # ut: short for unit.

        # Does not completely unpack the quantity qnt but unpacks the non-ignored units
        # and then merges them with the ignored ones.
        ignored = quantity(val, ufd({ut: uts[ut] for ut in uts if ut in dfu(ignore)}))
        packed = quantity(1, ufd({ut: uts[ut] for ut in uts if ut not in dfu(ignore)}))

        qnt = ignored * unpack(packed)

    else:
        qnt = unpack(qnt)

    for target in dfu(targets):
        # Ignores non-packable units.
        if target not in packTable:
            continue

        targetUnits = dfu(packTable[target])

        # Packing powers.
        powers = {
            # Updated from // to / to account for fractional powers.
            qnt.units[targetUnit] / targetUnits[targetUnit]
            for targetUnit in targetUnits
            if targetUnit in qnt.units
        }

        if not len(powers):
            raise PackError(qnt, targets)

        # Full packing is a stricter form of packing which
        # requires that "no other units are produced from the packing process".
        if full:  # Full-packability check.
            for targetUnit in targetUnits:
                if targetUnit not in qnt.units:
                    raise PackError(qnt, targets, full=True)

                if qnt.units[targetUnit] % targetUnits[targetUnit]:
                    raise PackError(qnt, targets, full=True)

            if min(powers) < max(powers) or max(powers) < 0:
                raise PackError(qnt, targets, full=True)

        # Uncertainty should not vary on packing.
        uncertainty = qnt.uncertainty
        qnt *= (quantity(1, target) / quantity(1, ufd(targetUnits))) ** max(powers)
        qnt.uncertainty = uncertainty

    return qnt
