from colorama import init
from .globals import currencies
from os import path, makedirs

init()

# Safe place to store currency exchange rates.
# Set to $HOME/.misura/misura.json.
currencies.path = path.expanduser("~") + "/.misura/"

# Creates the directory ".misura" and defines the full path.
makedirs(currencies.path, exist_ok=True)
currencies.path += "misura.json"

# Removes init imports.
del path, makedirs, currencies, init
