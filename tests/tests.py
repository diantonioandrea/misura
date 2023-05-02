# Test suite for misura.

from misura import unit, convert, unpack

num0 = unit(5, "m2")
num1 = unit(67, "km")
num2 = unit(12, "A s")
num3 = unit(1, "C mW")
num4 = unit(900, "J")
num5 = unit(15, "H TT")

# Math.
print(num0 ** .5)

# Logical.
print(num0 > 10)
print(num0 ** .5 < num1)
print(num0 < 0.02 * num1 ** 2)
print(num1 == num2)
print(num1 != num2)

# Conversions
print(num0 ** .5 + num1)
print(convert(num0, "dm2"))
print(convert(num1, "m"))
print(convert(num2, "mA", partial=True))

# Unpacking.
print(unpack(num3))
print(unpack(num4 ** 3))
print(unpack(num5, "T"))