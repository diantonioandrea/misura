from colorama import init
from .globals import currencies
import os

init()

# Safe place to store currency exchange rates.
# Set to $HOME/.misura/misura.json.
currencies.path = os.path.expanduser("~") + "/.misura/"

# Creates the directory ".misura" and defines the full path.
os.makedirs(currencies.path, exist_ok=True)
currencies.path += "misura.json"
