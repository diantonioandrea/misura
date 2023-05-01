# misura's documentation

## Projects built with misura

<a href="mailto:mail@diantonioandrea.com?subject=misura's project">Let me know<a> should you want your project listed here.

## Table of Contents

0. [Projects built with CLIbrary](#projects-built-with-misura)
1. [Introduction](#introduction)
	1. [Globals](#globals)
2. [Units of measure](#units-of-measure)

## Introduction

Python library for easy unit conversions for scientific & engineering applications.  

**misura** is a Python library designed to simplify the *handling of units of measure* for scientific and engineering applications. It provides a unified interface for *dealing with different units and their conversions*, allowing for quick and accurate calculations without the need for complex manual conversions.  

**misura** is written in Python and developed by [Andrea Di Antonio](https://github.com/diantonioandrea).

### Globals

misura has some "global options" to allow personalization.  
Available options are:

* `misura.style.unitHighlighting`, bool: Enables units of measure highlighting. Dafault: `True`.

## Units of measure

[Go back to ToC](#table-of-contents)

### Creation of numbers with units of measure

``` python
class unit
	def __init__(self, value: any, symbol: str)
```
**value** must be an object which implements the following methods, which are the available operations between *misura.unit* objects[^1]:

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

**symbol** must be the string of the units of measure, separated by a space and followed by their exponents.  
Some examples are:

* Metres: `"m"`.
* Metres squared: `"m2"`.
* Metres per second: `"m s-1"`.
* Metres per second squared: `"m s-2"`.
* kilograms: `"kg"`.
* Litres: `"L"`.
* `"kg2 m-3 s4 K2.5"`