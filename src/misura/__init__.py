from colorama import init
from .globals import currencies
from platform import system
import os

init()

if system.lower() == "darwin":
    currencies.path = ""

if system.lower() == "linux":
    currencies.path = ""

if system.lower() == "windows":
    currencies.path = ""

# os.makedirs(currencies.path, exist_ok=True)
currencies.path += "misura.json"
