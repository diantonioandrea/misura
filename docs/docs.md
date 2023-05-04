# misura's documentation

## Projects built with misura

<a href="mailto:mail@diantonioandrea.com?subject=misura's project">Let me know<a> should you want your project listed here.

## Table of Contents

- [Projects built with misura](#projects-built-with-misura)
- [Introduction](#introduction)
- [Quantities](#quantities)
	- [Methods](#methods)
	- [Operations](#operations)
- [Units of measure](#units-of-measure)
	- [Defaults](#defaults)
	- [User defined units of measure](#user-defined-units-of-measure)
- [Conversions, unpacking and packing](#conversions-unpacking-and-packing)
	- [Conversion](#conversion)
	- [Unpacking](#unpacking)
	- [Packing](#packing)
- [Global options](#global-options)
- [Exceptions](#exceptions)
- [Examples](#examples)

## Introduction

Python library for easy unit handling and conversion for scientific & engineering applications.

**misura** is a Python library designed to simplify the _handling of units of measure_ for scientific and engineering applications. It provides a unified interface for _dealing with different units and their conversions_, allowing for quick and accurate calculations without the need for complex manual conversions.

**misura** is written in Python and developed by [Andrea Di Antonio](https://github.com/diantonioandrea).

## Quantities

[Go back to ToC](#table-of-contents)

Quantities are defined as `misura.quantity(value: any, unit: str)` objects.

`values` stands for the value of the quantity itself, while `unit` represents its unit of measure.  
`quantity(2, "kg")` is a well-defined quantity.

`unit` must be a string in which the different units of measure must be _separated by a space_ and _followed by their exponent_, if different from `1`.  
`quantity(3, "m s-1")` is a well-defined quantity.

### Methods

`misura.quantity` objects implement the following methods:

```python
def unit(self, print: bool = False) -> str
def dimensionality(self) -> str
```

which:

- `unit()`: Returns the units string of the quantity. It returns it in a fancier way if `print = True`.
- `dimensionality()`: Returns the dimensionality string of the quantity if it is convertible.

### Operations

`misura.quantity` objects implement the following dunder methods:

```python
def __str__(self) -> str
def __repr__(self) -> str
def __format__(self, string) -> str

def __int__(self) -> int
def __float__(self) -> float
def __complex__(self) -> complex
def __bool__(self) -> bool

def __abs__(self) -> any
def __pos__(self) -> any
def __neg__(self) -> any
def __invert__(self) -> any
def __round__(self, number: int) -> any
def __floor__(self, number: int) -> any
def __ceil__(self, number: int) -> any
def __trunc__(self, number: int) -> any

def __add__(self, other: any) -> any
def __sub__(self, other: any) -> any
def __mul__(self, other: any) -> any
def __truediv__(self, other: any) -> any
def __floordiv__(self, other: any) -> any
def __pow__(self, other: any) -> any
def __mod__(self, other: any) -> any

def __lt__(self, other: any) -> any
def __le__(self, other: any) -> any
def __gt__(self, other: any) -> any
def __ge__(self, other: any) -> any
def __eq__(self, other: any) -> any
def __ne__(self, other: any) -> any
```

For a quantity to be well-defined, `value` should implement all of the methods in this list which will be called during the execution of the program.

Take a look at these [examples](#quantities-1).

## Units of measure

[Go back to ToC](#table-of-contents)

### Defaults

**misura** currently supports the following _families_ (physical quantities):

- SI base units:
	- Time, Second, **s**.
	- Length, Metre, **m**.
	- Mass, Kilogram, **kg**.
	- Electric current, Ampere, **A**.
	- Thermodynamic temperature, Kelvin, **K**.
	- Amount of substance, Mole, **mol**.
	- Luminous intensity, Candela, **cd**.
- SI derived units.
	- Plane angle, Radian, **rad**.
	- Solid angle, Steradian, **sr**.
	- Frequency, Hertz, **Hz**.
	- Force, Newton, **N**.
	- Pressure, Pascal, **Pa**.
	- Energy, Joule, **J**.
	- Power, Watt, **W**.
	- Electric charge, Coulomb, **C**.
	- Electric potential, Volt, **V**.
	- Capacitance, Farad, **F**.
	- Resistance, Ohm, **Ω**.
	- Electrical conductance, Siemens, **S**.
	- Magnetic flux, Weber, **Wb**.
	- Magentic flux density, Tesla, **T**.
	- Inductance, Henry, **H**.
	- Luminous flux, Lumen, **lm**.
	- Illuminance, Lux, **lx**.
	- Radionuclide activity, Becquerel, **Bq**.
	- Absorbed dose, Gray, **Gy**.
	- Equivalent dose, Sievert, **Sv**.
	- Catalytic activity, Katal, **kat**.

with the following orders of magnitude:

		q  =  1e-30
		r  =  1e-27
		y  =  1e-24
		z  =  1e-21
		a  =  1e-18
		f  =  1e-15
		p  =  1e-12
		n  =  1e-09
		µ  =  1e-06
		m  =  1e-03
		c  =  1e-02
		d  =  1e-01
		------------
		da =  1e+01
		h  =  1e+02
		k  =  1e+03
		M  =  1e+06
		G  =  1e+09
		T  =  1e+12
		P  =  1e+15
		E  =  1e+18
		Z  =  1e+21
		Y  =  1e+24
		R  =  1e+27
		Q  =  1e+30

### User defined units of measure

``` python
misura.addUnit(family: str, units: dict, unpacks: str = "") -> None
```

The function `addUnit` takes a string `family`, a dictionary `units` and an optional string `unpacks`.

- `family: str` is the family (physical quantity) of the to-be-defined unit of measure.
- `units: dict` is the dictionary of the available symbols for the specified family and it is structured as `{"symbol1": factor1, ..., "symbol": 1, ..., "symbolN": factorN}`.
- `unpacks: str` is the string of the units to which the new unit unpacks, if it does. In this case the new unit becomes a derived unit.

Note that the `units` dictionary must have a **reference unit**, a defining unit for that family, for which its factor is equal to `1`.

Take a look at these [examples](#units-of-measure-1)

## Conversions, unpacking and packing

[Go back to ToC](#table-of-contents)

### Conversion

```python
misura.convert(converted: quantity, target: str, partial: bool = False, un_pack: bool = False) -> quantity
```

The function `convert` takes a `quantity` object, converted, a string, `targets`, and two flags: `partial` and `un_pack`.

- `qnt: quantity` is the quantity that needs to be converted.
- `targets: str` is the string of target units, the units that need to be matched after conversion.
- `partial: bool` whether or not the conversion should be partial, e.g. `"m s-1" -> "km s-1"`.
- `un_pack: bool` whether or not to (un)pack derived units during conversion.

### unpacking

```python
misura.unpack(qnt: quantity, targets: str = "") -> quantity
```

The function `unpack` takes a `quantity` object, qnt and an optional string, `targets`.

- `qnt: quantity` is the quantity that needs to be converted.
- `targets: str = ""` is the string of target units, the derived units that need to be unpacked. If empty, it unpacks every derived unit.

### packing

```python
misura.pack(qnt: quantity, targets: str, full: bool = False) -> quantity
```

The function `pack` takes a `quantity` object, qnt, two strings, `targets` and `ignore`, and a flag, `full`.

- `qnt: quantity` is the quantity that needs to be converted.
- `targets: str` is the string of target units, the derived units that need to be matched.
- `ignore: str = ""` Due to the fact that `pack` works by first unpacking the units, some units can be manually ignored to enhance the final result.
- `full: bool = False` whether or not to fully pack a unit.

Take a look at these [examples](#conversions-unpacking-and-packing-1).

## Global options

[Go back to ToC](#table-of-contents)

**misura** implements the following global options:

- `misura.style.unitHighlighting`, bool: Enables units of measure highlighting. Dafault: `True`.

Take a look at these [examples](#global-options-1)

## Exceptions

[Go back to ToC](#table-of-contents)

**misura** implements the following exceptions:

- `UnitError`: raised on invalid `unit` passed to `quantity(value, unit)`.
- `QuantityError`: raised on operations between incompatible quantities.
- `ConversionError`: raised on errors during conversions.
- `UnpackError`: raised on errors during unpacking.
- `PackError`: raised on errors during packing.
- `DefinitionError`: raised on errors during unit definition.

## Examples

[Go back to ToC](#table-of-contents)

### Quantities

```python
from misura import quantity
import numpy

num1 = quantity(7, "m s-1")
num2 = quantity(4, "km")
num3 = numpy.array([quantity(2, "m"), quantity(4, "km")])
num4 = quantity(numpy.array([1, 2, 3]), "T")

print(num1.unit(print=True))
print(num1.dimensionality())
print(num1 * 3)
print(num2 ** 2 < 16)
print(numpy.sum(num3))
print(num4)
```

The output is:

```
m / s
[length / time]
21 m / s
False
4002.0 m
[1 2 3] T
```

### Units of measure

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

### Conversions, unpacking and packing

```python
from misura import quantity, convert, unpack, pack

num1 = quantity(2, "m2")
num2 = quantity(4, "kg")
num3 = quantity(2, "J2")
num4 = quantity(4, "C H")
num5 = quantity(7, "N m")
num6 = quantity(9, "J")
num7 = quantity(45, "A2 s2")

print(convert(num1, "cm2"))
print(num2 + quantity(5, "g"))
print(unpack(num3))
print(unpack(num4, "H"))
print(num5 + num6)
print(pack(num7, "C", full=True))
```

The output is:

```
20000.0 cm(2)
4.005 kg
2.0 kg(2) m(4) / s(4)
4.0 C kg m(2) / A(2) s(2)
16.0 J
45.0 C(2)
```

### Global options

```python
from misura import quantity
from misura import style

style.quantityHighlighting = False

num1 = quantity(2, "m s-1")
num2 = quantity(5, "s")

print(num1)
print(num2)
```

The output is:

```
2 [m / s]
5 [s]
```
