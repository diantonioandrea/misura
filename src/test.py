# Test suite for misura.

from colorama import Style
from misura.quantities import quantity, convert, unpack, pack
from misura.tables import addUnit

addUnit("bananas", {"bnn": 1, "dabnn": 10, "hbnn": 100, "kbnn": 1000})

num0 = quantity(5, "m2")
num1 = quantity(67, "km")
num2 = quantity(12, "A s")
num3 = quantity(1, "C mW")
num4 = quantity(900, "J")
num5 = quantity(15, "H TT")
num6 = quantity(12, "km2 s-2")
num7 = quantity(3, "kg km2")
num8 = quantity(13, "J")
num9 = quantity(0.9, "mN km")
num10 = quantity(3, "N m T")
num11 = quantity(12, "kbnn")
num12 = quantity(2, "kg", 0.04)
num13 = quantity(0.8, "m3", 0.16)
num14 = quantity(3, "", 1)

print("Tests for {}.".format(Style.BRIGHT + "misura" + Style.RESET_ALL))

# Dimensions.
print("\nDIMENSIONS TESTS.\n")
print("{}: {}".format(num10, num10.dimension()))

# Math.
print("\nMATH TESTS.\n")
print("({}) ** 0.5: {}".format(num0, num0**0.5))
print("7 - ({}): {}".format(num14, 7 - num14))
print("2 ** ({}): {}".format(num14, 2**num14))

# Logical.
print("\nLOGICAL TESTS.\n")
print("{} > 10: {}".format(num0, num0 > 10))
print("({}) ** 0.5 < {}: {}".format(num0, num1, num0**0.5 < num1))
print("{} < 0.02 * {}**2: {}".format(num0, num1, num0 < 0.02 * num1**2))
print("{} == {}: {}".format(num1, num2, num1 == num2))
print("{} != {}: {}".format(num1, num2, num1 != num2))

# Conversions.
print("\nCONVERSIONS.\n")
print("({}) ** 0.5 + {}: {}".format(num0, num1, num0**0.5 + num1))
print("{} to 'm': {}".format(num1, convert(num1, "m")))
print("{} to 'mA', partial: {}".format(num2, convert(num2, "mA", partial=True)))

# Unpacking.
print("\nUNPACKING.\n")
print("{}: {}".format(num3, unpack(num3)))
print("({}) ** 3: {}".format(num4, unpack(num4**3)))
print("{} unpacking 'T': {}".format(num5, unpack(num5, "T")))

# Packing.
print("\nPACKING.\n")
print("{} fully packed to 'Sv': {}".format(num6, pack(num6, "Sv", full=True)))
print("{} packed to 'J': {}".format(num7, pack(num7, "J")))

# Automatic conversion with (un)packing.
print("\nAUTOMATIC CONVERSION WITH (UN)PACKING.\n")
print("{} + {}: {}".format(num8, num9, num8 + num9))
print("{} + {}: {}".format(num9, num8, num9 + num8))
print("{} packed to 'J', ignoring 'T': {}".format(num10, pack(num10, "J", ignore="T")))

# Custom units of measure.
print("\nCUSTOM UNITS OF MEASURE.\n")
print("{} to 'bnn': {}".format(num11, convert(num11, "bnn")))

# Uncertainty.
print("\nUNCERTAINTY.\n")
print("({}) ** 2: {}".format(num12, num12**2))
print("({}) / ({}): {}".format(num12, num13, num12 / num13))
