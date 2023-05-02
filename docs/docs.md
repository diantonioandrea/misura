# misura's documentation

## Projects built with misura

<a href="mailto:mail@diantonioandrea.com?subject=misura's project">Let me know<a> should you want your project listed here.

## Table of Contents

0. [Projects built with misura](#projects-built-with-misura)
1. [Introduction](#introduction)
	1. [Globals](#globals)
2. [Units of measure](#units-of-measure)
	1. [Creation of quantities with units of measure](#creation-of-quantities-with-units-of-measure)
3. [Unit conversions](#unit-conversions)
	1. [Available units](#available-units)
	2. [Manually convert a quantity](#manually-convert-a-quantity)
	3. [Partially convert a quantity](#partially-convert-a-quantity)
	4. [Automatic conversion](#automatic-conversion)
4. [Unit unpacking](#unit-unpacking)
	1. [Manually unpacking a quantity](#manually-unpacking-a-quantity)

## Introduction

Python library for easy unit handling and conversion for scientific & engineering applications.  

**misura** is a Python library designed to simplify the *handling of units of measure* for scientific and engineering applications. It provides a unified interface for *dealing with different units and their conversions*, allowing for quick and accurate calculations without the need for complex manual conversions.  

**misura** is written in Python and developed by [Andrea Di Antonio](https://github.com/diantonioandrea).

### Globals

misura has some "global options" to allow personalization.  
Available options are:

* `misura.style.unitHighlighting`, bool: Enables units of measure highlighting. Dafault: `True`.

## Units of measure

[Go back to ToC](#table-of-contents)

### Creation of quantities with units of measure

``` python
misura.units.unit
	__init__(self, value: any, symbol: str)
```
`value` must be an object which implements the following methods, which are the available operations between *misura.unit* objects[^1]:

[^1]: Not all of them are needed but only the ones used.

``` python
def __str__(self) -> str
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

`symbol` must be the string of the units of measure, separated by a space and followed by their exponents.  
Some examples are:

* Metres: `"m"`.
* Metres squared: `"m2"`.
* Metres per second: `"m s-1"`.
* Metres per second squared: `"m s-2"`.
* kilograms: `"kg"`.
* Litres: `"L"`.
* `"kg2 m-3 s4 K2.5"`

## Unit conversions

[Go back to ToC](#table-of-contents)

### Available units

Currently available units are:

* SI base units:
	* Time, Second, **s**.
	* Length, Metre, **m**.
	* Mass, Kilogram, **kg**.
	* Electric current, Ampere, **A**.
	* Thermodynamic temperature, Kelvin, **K**.
	* Amount of substance, Mole, **mol**.
	* Luminous intensity, Candela, **cd**.
* SI derived units.
	* Plane angle, Radian, **rad**.
	* Solid angle, Steradian, **sr**.
	* Frequency, Hertz, **Hz**.
	* Force, Newton, **N**.
	* Pressure, Pascal, **Pa**.
	* Energy, Joule, **J**.
	* Power, Watt, **W**.
	* Electric charge, Coulomb, **C**.
	* Electric potential, Volt, **V**.
	* Capacitance, Farad, **F**.
	* Resistance, Ohm, **Ω**.
	* Electrical conductance, Siemens, **S**.
	* Magnetic flux, Weber, **Wb**.
	* Magentic flux density, Tesla, **T**.
	* Inductance, Henry, **H**.
	* Luminous flux, Lumen, **lm**.
	* Illuminance, Lux, **lx**.
	* Radionuclide activity, Becquerel, **Bq**.
	* Absorbed dose, Gray, **Gy**.
	* Equivalent dose, Sievert, **Sv**.
	* Catalytic activity, Katal, **kat**.

For every SI unit there's the possibility to access the following prefixes and orders of magnitude:

	q-  =  1e-30
	r-  =  1e-27
	y-  =  1e-24
	z-  =  1e-21
	a-  =  1e-18
	f-  =  1e-15
	p-  =  1e-12
	n-  =  1e-09
	µ-  =  1e-06
	m-  =  1e-03
	c-  =  1e-02
	d-  =  1e-01
	------------
	da- =  1e+01
	h-  =  1e+02
	k-  =  1e+03
	M-  =  1e+06
	G-  =  1e+09
	T-  =  1e+12
	P-  =  1e+15
	E-  =  1e+18
	Z-  =  1e+21
	Y-  =  1e+24
	R-  =  1e+27
	Q-  =  1e+30

so that all the following example conversions are possible:

* from `"m2"` to `"mm2"`.
* from `"g"` to `"kg"`.
* from `"mW"` to `"MW"`.
* from `"QJ"` to `"qJ"`.

At the moment *it is not possible* to convert from base units to derived units and viceversa.

### Manually convert a quantity

``` python
misura.units.convert(first: unit, target: str, partial: bool = False) -> unit
```

The function `convert` takes a misura.unit and a target symbol string and tries to convert it, raising a `ConversionError` should this fail.

An example is:

``` python
from misura import unit, convert

num1 = unit(0.2, "m2")

print(convert(num1, "cm2"))
print(convert(num1, "kg"))
```

The output is:

	2000.0 cm(2)
	
	misura.conversion.ConversionError: cannot convert from 'm2' to 'kg'
	raised by: '0.2 m(2)' -> 'kg'

### Partially convert a quantity

``` python
misura.units.convert(first: unit, target: str, partial: bool = False) -> unit
```

A partial conversion takes place when only some of the units of measure of a quantity get converted.

An example is:

``` python
from misura import unit, convert

num1 = unit(200, "m s-1")

print(convert(num1, "km"))
```

The output is:

	0.2 km / s

The partial conversions works on the family of units that exists both in the unit and in the target passed to `convert`.

### Automatic conversion

During operations between quantities with compatible but different units of measure, the second quantity gets converted, partially or totally, according to the first quantity's unit of measure.

An example is:

``` python
from misura import unit

num1 = unit(2, "m s-1")
num2 = unit(4, "cm das-1")
num3 = unit(5, "kg")

print(num1 + num2)
print(num1 + num3)
```

The output is:

	2.004 m / s
	
	misura.conversion.ConversionError: cannot convert from 'kg' to 'm s-1'
	raised by: '5 kg' -> 'm s-1'

Total conversion is used for operations such as addition and subraction, while partial conversion is used for multiplication and division.

An example is:

``` python
from misura import unit

num1 = unit(2, "m")
num2 = unit(4, "cm s")

print(num1 * num2)
```

The output is:

	0.08 m(2) s

## Unit unpacking

[Go back to ToC](#table-of-contents)

### Manually unpacking a quantity

``` python
def unpack(first: unit, targets: str = "") -> unit:
```

The function `unpack` takes a misura.unit and an optional target symbol string and tries to unpack the specified derived units, raising a `UnpackError` should this fail.  
Leaving `targets` empty will unpack every derived unit.

An example is:

``` python
from misura import unit, unpack

num1 = unit(0.2, "C2 W")

print(unpack(num1))
print(unpack(num1, "C"))
print(unpack(num1, "kg"))
```

The output is:

	0.2 A(2) kg m(2) / s
	0.2 A(2) W s(2)

	misura.conversion.UnpackError: cannot unpack 'kg' from 'C2 W'
	raised by: '0.2 C(2) W'