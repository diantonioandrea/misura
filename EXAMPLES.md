# Examples

These are some examples of operations between quantities.  
Note that, by enabling `globals.style.unitHighlighting`, **misura** uses colorama to highlight units of measure. by disabling it, the output is in the form of `num [unit]`

## Mathematical operations

```python
from misura.quantities import quantity

num1 = quantity(2, "m s-1")
num2 = quantity(4, "m s-1")
num3 = quantity(2, "s", .5)

print(num1 + num2)
print((num1 + num2).dimension())
print(num1 * num2)
print(num1 / num3)
print(num3 ** 2)
```

The output is:

```
6 m / s
[length / time]
8 m(2) / s(2)
1.0 ± 0.25 m / s(2)
4 ± 2.0 s(2)
```

## Currencies

```python
from misura.currencies import currency

cur1 = currency(2, "EUR")
cur2 = currency(3, "USD")

print(cur0 * 2)
print(cur1 + cur0)
```

The output is:

```
4 EUR
5.17 USD
```

## Working with other libraries

```python
from misura.quantities import quantity, convert
from decimal import Decimal, getcontext
import numpy

getcontext().prec = 40

arr1 = numpy.array([quantity(2, "m"), quantity(50, "m s-1"), quantity(2, "kg")])
arr2 = quantity(numpy.array([1, 2, 3]), "J")
num2 = quantity(numpy.sqrt(Decimal(5)), "kg")

print(arr1 * 3)
print(arr2 ** 2)
print(num2)
```

The output is:

```
[6 m 150 m / s 6 kg]
[1 4 9] J(2)
2.236067977499789696409173668731276235441 kg
```

Unit highlighting helps distinguish between different numbers.

## User defined units of measure

```python
from misura.quantities import quantity, convert
from misura.tables import addUnit

addUnit("volume", {"L": 1, "daL": 10, "hL": 100, "kL": 1000, "dL": 0.1, "cL": 0.01, "mL": 0.001}, "dm3")

num1 = quantity(3, "L")

print(convert(num1, "cm3"))
```

The output is:

```
3000.0 cm(3)
```

## Manual and automatic conversion

```python
from misura.quantities import quantity, convert

num1 = quantity(2, "m2")
num2 = quantity(4, "kg")
num3 = quantity(400, "m s-1")

print(convert(num1, "cm2"))
print(num2 + quantity(5, "g"))
print(convert(num3, "km", partial=True))
```

The output is:

```
20000.0 cm(2)
4.005 kg
0.4 km / s
```

## Unpack derived quantities

```python
from misura.quantities import quantity, unpack

num1 = quantity(2, "J2")
num2 = quantity(4, "C H")

print(unpack(num1))
print(unpack(num2, "H"))
```

The output is:

```
2.0 kg(2) m(4) / s(4)
4.0 C kg m(2) / A(2) s(2)
```

## Pack derived quantities

```python
from misura.quantities import quantity, pack

num1 = quantity(3, "N m T")
num2 = quantity(45, "A2 s2")

print(pack(num1, "J", ignore="T"))
print(pack(num2, "C", full=True))
```

The output is:

```
3.0 J T
45.0 C(2)
```

## Comparisons

```python
from misura.quantities import quantity

num1 = quantity(2, "m s-1")
num2 = quantity(4, "m s-1")
num3 = quantity(2, "s")

print(num1 > num2)
print(num2 < 6)
print(num1 > num3)
```

The output is:

```
False
True

misura.conversion.ConversionError: cannot convert from 's' to 'm s-1'
raised by: '2 s' -> 'm s-1'
```

## Unary operators and functions

```python
from misura.quantities import quantity
from misura.globals import style
from math import trunc

style.quantityHighlighting = False

num1 = quantity(2, "m s-1")
num2 = quantity(4.5, "m s-1")
num3 = quantity(-2, "s")

print(-num1)
print(trunc(num2))
print(abs(num3))
```

The output is:

```
-2 [m / s]
4 [m / s]
2 [s]
```

## Formatting

```python
from misura.quantities import quantity

num1 = quantity(2000, "m s-1")

print("Exponential notation: {:.2e}".format(num1))
```

The output is:

```
Exponential notation: 2.00e+00 m / s
```