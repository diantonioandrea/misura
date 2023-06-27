# misura

import pkg_resources
from colorama import Style, init

init()

print("misura v" + pkg_resources.get_distribution("misura").version)

print(
    "\nPython library for easy unit handling and conversion for scientific & engineering applications."
)
print(
    "\nDeveloped by "
    + Style.BRIGHT
    + "Andrea Di Antonio"
    + Style.RESET_ALL
    + ", more on "
    + Style.BRIGHT
    + "https://github.com/diantonioandrea/misura"
    + Style.RESET_ALL
)
print(
    "Documentation on "
    + Style.BRIGHT
    + "https://misura.diantonioandrea.com"
    + Style.RESET_ALL
)
print(
    "Bug tracker on "
    + Style.BRIGHT
    + "https://github.com/diantonioandrea/misura/issues"
    + Style.RESET_ALL
)