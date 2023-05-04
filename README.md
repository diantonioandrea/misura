![GitHub](https://img.shields.io/github/license/diantonioandrea/misura)

![PyPI](https://img.shields.io/pypi/v/misura?label=misura%20on%20pypi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/misura)
![PyPI - Downloads](https://img.shields.io/pypi/dm/misura)

![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/diantonioandrea/misura)
![GitHub last commit](https://img.shields.io/github/last-commit/diantonioandrea/misura)
![GitHub Release Date](https://img.shields.io/github/release-date/diantonioandrea/misura)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# misura

```python
>>> from misura import quantity as qnt
>>> (qnt(2, "m") + qnt(50, "cm")) / qnt(4, "s")
0.625 m / s
```

Python library for easy unit handling and conversion for scientific & engineering applications.

**misura** is a Python library designed to simplify the _handling of units of measure_ for scientific and engineering applications. It provides a unified interface for _dealing with different units and their conversions_, allowing for quick and accurate calculations without the need for complex manual conversions.

Make sure to take a look at the [documentation](https://github.com/diantonioandrea/misura/blob/main/docs/docs.md), at the [contributing guidelines](https://github.com/diantonioandrea/.github/blob/main/CONTRIBUTING.md) and at the [examples](#examples).

### Features

- Mathematical and logical operations between quantities: [Example](#mathematical-operations), [example](#comparisons).
- Manual conversions: [Example](#manual-and-automatic-conversion).
- Automatic conversions on operations: [Example](#manual-and-automatic-conversion).
- Unpack and pack derived units: [Example](#unpack-derived-units), [example](#pack-units).
- User defined base and derived units: [Example](#user-defined-units-of-measure).
- Large compatibility with other libraries: [Example](#working-with-other-libraries).
- Custom exceptions: [Example](#comparisons).

## Installation

### Installing misura

**misura** can be installed from [PyPI](https://pypi.org) by:

```
python3 -m pip install --upgrade misura
```

### Verifying installation and base informations

By:

```
python -m misura
```

you'll be able to verify the installation of **misura** along getting some informations about the library and on the available units of measure[^1]:

[^1]: Examle referring to version 1.3.1

```
misura v1.3.1

Python library for easy unit handling and conversion for scientific & engineering applications.

Developed by Andrea Di Antonio, more on https://github.com/diantonioandrea/misura
Documentation on https://github.com/diantonioandrea/misura/blob/main/docs/docs.md
Bug tracker on https://github.com/diantonioandrea/misura/issues

Here's the list of available units.

BASE UNITS

Time: s.
Length: m.
Mass: kg.
Electric current: A.
Thermodynamic temperature: K.
Amount of substance: mol.
Luminous intensity: cd.

DERIVED UNITS

Plane angle: rad.
Solid angle: sr.
Frequency: Hz [s-1].
Force: N [kg m s-2].
Pressure: Pa [kg m-1 s-2].
Energy: J [kg m2 s-2].
Power: W [kg m2 s-3].
Electric charge: C [A s].
Electric potential: V [kg m2 s-3 A-1].
Capacitance: F [kg-1 m-2 s4 A2].
Resistance: Ω [kg m2 s-3 A-2].
Electrical conductance: S [kg-1 m-2 s3 A2].
Magnetic flux: Wb [kg m2 s-2 A-1].
Magnetic flux density: T [kg s-2 A-1].
Inductance: H [kg m2 s-2 A-2].
Luminous flux: lm [cd sr].
Illuminance: lx [cd sr m-2].
Radionuclide activity: Bq [s-1].
Absorbed dose: Gy [m2 s-2].
Equivalent dose: Sv [m2 s-2].
Catalyc activity: kat [mol s-1].
```

### Importing misura

**misura** can be imported by:

```
import misura
```

## Examples

These are some examples of operations between quantities.  
Note that, by enabling `misura.style.unitHighlighting`, **misura** uses colorama to highlight units of measure. by disabling it, the output is in the form of `num [unit]`

### Mathematical operations

```python
from misura import quantity

num1 = quantity(2, "m s-1")
num2 = quantity(4, "m s-1")
num3 = quantity(2, "s")

print(num1 + num2)
print((num1 + num2).dimensionality())
print(num1 * num2)
print(num1 / num3)
print(num3 ** 2)
```

The output is:

```
6 m / s
[length / time]
8 m(2) / s(2)
1.0 m / s(2)
4 s(2)
```

### Working with other libraries

```python
from misura import quantity, convert
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

### User defined units of measure

```python
from misura import quantity, convert, addUnit

addUnit("volume", {"L": 1, "daL": 10, "hL": 100, "kL": 1000, "dL": 0.1, "cL": 0.01, "mL": 0.001}, "dm3")

num1 = quantity(3, "L")

print(convert(num1, "cm3"))
```

The output is:

```
3000.0 cm(3)
```

### Manual and automatic conversion

```python
from misura import quantity, convert

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

### Unpack derived quantities

```python
from misura import quantity, unpack

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

### Pack derived quantities

```python
from misura import quantity, pack

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

### Comparisons

```python
from misura import quantity

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

### Unary operators and functions

```python
from misura import quantity
from misura import style
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

### Formatting

```python
from misura import quantity

num1 = quantity(2000, "m s-1")

print("Exponential notation: {:.2e}".format(num1))
```

The output is:

```
Exponential notation: 2.00e+00 m / s
```