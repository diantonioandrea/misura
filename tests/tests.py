# Test suite for misura.

from misura import quantity, convert, unpack, pack
from misura import addUnit

addUnit("bananas", {"bnn": 1, "dabnn": 10, "hbnn": 100, "kbnn": 1000})

num0 = quantity(5, "m2")
num1 = quantity(67, "km")
num2 = quantity(12, "A s")
num3 = quantity(1, "C mW")
num4 = quantity(900, "J")
num5 = quantity(15, "H TT")
num6 = quantity(12, "m2 s-2")
num7 = quantity(3, "kg km2")
num8 = quantity(13, "J")
num9 = quantity(0.9, "mN km")
num10 = quantity(3, "N m T")
num11 = quantity(12, "kbnn")

# Math.
print(num0**0.5)

# Logical.
print(num0 > 10)
print(num0**0.5 < num1)
print(num0 < 0.02 * num1**2)
print(num1 == num2)
print(num1 != num2)

# Conversions
print(num0**0.5 + num1)
print(convert(num0, "dm2"))
print(convert(num1, "m"))
print(convert(num2, "mA", partial=True))

# Unpacking.
print(unpack(num3))
print(unpack(num4**3))
print(unpack(num5, "T"))

# Packing.
print(pack(num6, "Sv", full=True))
print(pack(num7, "J"))

# Automatic conversion with (un)packing.
print(num8 + num9)
print(num9 + num8)
print(pack(num10, "J", ignore="T"))

# Custom units conversions.
print(convert(num11, "bnn"))
