![GitHub](https://img.shields.io/github/license/diantonioandrea/misura)

![PyPI](https://img.shields.io/pypi/v/misura?label=misura%20on%20pypi)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/misura)
![PyPI - Downloads](https://img.shields.io/pypi/dm/misura)

![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/diantonioandrea/misura)
![GitHub last commit](https://img.shields.io/github/last-commit/diantonioandrea/misura)
![GitHub Release Date](https://img.shields.io/github/release-date/diantonioandrea/misura)

![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/diantonioandrea/misura/latest)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# misura

```python
>>> from misura.quantities import quantity
>>> quantity(7, "m", 1.5) / quantity(2, "s")
3.5 ± 0.75 m / s

>>> from misura.currencies import currency
>>> currency(2, "EUR") + currency(3, "USD")
5.17 USD
```

Python library providing effortless unit handling and currency conversion for scientific and engineering purposes.

**misura** is a powerful Python library designed to facilitate the efficient handling of units of measure for scientific and engineering applications, including currencies handling and conversion with constantly updated exchange rates. With its unified interface for dealing with different units and their conversions, you can quickly and accurately complete calculations without the need for complex manual conversions. Additionally, **misura** supports uncertainty handling allowing you to work with physical quantities and their associated uncertainties in a user-friendly and intuitive fashion. What's more, **misura** grants you the flexibility to create custom units of measure, so you can work in your preferred units.

Make sure to take a look at the [documentation](https://misura.diantonioandrea.com), at the [contributing guidelines](https://github.com/diantonioandrea/.github/blob/main/CONTRIBUTING.md) and at the [examples](#examples).

### Features

- Mathematical and logical operations between quantities: [Example](#mathematical-operations), [example](#comparisons)
- Currencies handling with daily updated exchange rates. ![New feature](https://img.shields.io/badge/new-green)
- Uncertainty handling: [Example](#mathematical-operations) ![New feature](https://img.shields.io/badge/new-green)
- Manual conversions: [Example](#manual-and-automatic-conversion)
- Automatic conversions on operations: [Example](#manual-and-automatic-conversion)
- Unpack and pack derived units: [Example](#unpack-derived-units), [example](#pack-units)
- User defined base and derived units: [Example](#user-defined-units-of-measure)
- Large compatibility with other libraries: [Example](#working-with-other-libraries)
- Custom exceptions: [Example](#comparisons)

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

you'll be able to verify the installation of **misura** along getting some informations about the library:

```
misura

Python library providing effortless unit handling and currency conversion for scientific and engineering purposes.

Developed by Andrea Di Antonio, more on https://github.com/diantonioandrea/misura
Documentation on https://misura.diantonioandrea.com
Bug tracker on https://github.com/diantonioandrea/misura/issues
```

### Importing misura

**misura** can be imported by:

```
import misura
```

## Examples

See [EXAMPLES.md](./EXAMPLES.md).
