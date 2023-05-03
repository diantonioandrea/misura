# Test suite for misura.

from misura import quantity, convert, unpack

num0 = quantity(5, "m2")
num1 = quantity(67, "km")
num2 = quantity(12, "A s")
num3 = quantity(1, "C mW")
num4 = quantity(900, "J")
num5 = quantity(15, "H TT")

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