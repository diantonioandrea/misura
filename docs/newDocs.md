# misura's documentation

## Projects built with misura

<a href="mailto:mail@diantonioandrea.com?subject=misura's project">Let me know<a> should you want your project listed here.

## Table of Contents

* [Projects built with misura](#projects-built-with-misura)
* [Introduction](#introduction)
* [Quantities](#quantities)
* [Operating with quantities](#quantities)
* [Conversions, unpacking and packing](#conversions-unpacking-and-packing)
* [Global options](#global-options)
* [Examples](#examples) 

## Introduction

Python library for easy unit handling and conversion for scientific & engineering applications.  

**misura** is a Python library designed to simplify the *handling of units of measure* for scientific and engineering applications. It provides a unified interface for *dealing with different units and their conversions*, allowing for quick and accurate calculations without the need for complex manual conversions.  

**misura** is written in Python and developed by [Andrea Di Antonio](https://github.com/diantonioandrea).

## Quantities

[Go back to ToC](#table-of-contents)

Quantities are defined as `misura.quantity(value: any, unit: str)` objects.  

`values` stands for the value of the quantity itself, while `unit` represents its unit of measure.  
`quantity(2, "kg")` is a well-defined quantity.  

`unit` must be a string in which the different units of measure are separated by a space and followed by their exponent, if present.  
`quantity(3, "m s-1")` is a well-defined quantity.

`misura.quantity` objects implement the following methods:

``` python
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

## Conversions, unpacking and packing

[Go back to ToC](#table-of-contents)

### Conversion

``` python
misura.convert(converted: quantity, target: str, partial: bool = False, un_pack: bool = False) -> quantity
```

### unpacking

``` python
misura.unpack(converted: quantity, targets: str = "") -> quantity
```

### packing

``` python
misura.pack(converted: quantity, targets: str = "") -> quantity
```

Take a look at these [examples](#conversions-unpacking-and-packing-1).

## Global options

[Go back to ToC](#table-of-contents)

Take a look at these [examples](#global-options-1)

## Exceptions

[Go back to ToC](#table-of-contents)

Take a look at these [examples](#exceptions-1)

## Examples

[Go back to ToC](#table-of-contents)

### Quantities

``` python
from misura import quantity
import numpy

num0 = quantity(7, "m s-1")
num1 = quantity(4, "km")
num2 = numpy.array([quantity(2, "m"), quantity(4, "km")])
num3 = quantity(numpy.array([1, 2, 3]), "T")

print(num0 * 3)
print(num1 ** 2 < 16)
print(numpy.sum(num2))
print(num3)
```

The output is:

	21 m / s
	False
	4002.0 m
	[1 2 3] T

### Conversions, unpacking and packing

### Global options

### Exceptions