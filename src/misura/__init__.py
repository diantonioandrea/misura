from os import makedirs
from os.path import expanduser

from colorama import init

from .globals import currencies

init()

# Safe place to store currency exchange rates.
# Set to $HOME/.misura/misura.json.
currencies.path = expanduser("~") + "/.misura/"

# Creates the directory ".misura" and defines the full path.
makedirs(currencies.path, exist_ok=True)
currencies.path += "misura.json"

# Removes init imports.
del makedirs, currencies, init
