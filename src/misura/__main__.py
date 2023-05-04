# misura

import pkg_resources
from colorama import Style, init

init()

from .tables import SI_DERIVED_TABLE, SI_DERIVED_UNPACKING_TABLE, SI_TABLE, getRep

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
    + "https://github.com/diantonioandrea/misura/blob/main/docs/docs.md"
    + Style.RESET_ALL
)
print(
    "Bug tracker on "
    + Style.BRIGHT
    + "https://github.com/diantonioandrea/misura/issues"
    + Style.RESET_ALL
)

print(
    "\nHere's the list of available units.\n\n{2}BASE UNITS{3}\n\n{0}\n\n{2}DERIVED UNITS{3}\n\n{1}".format(
        "\n".join(
            [
                "{}: {}.".format(
                    family[0].upper() + family[1:],
                    Style.BRIGHT + getRep(family) + Style.RESET_ALL,
                )
                for family in SI_TABLE
            ]
        ),
        "\n".join(
            [
                "{}: {}{}.".format(
                    family[0].upper() + family[1:],
                    Style.BRIGHT + getRep(family) + Style.RESET_ALL,
                    (" [" + SI_DERIVED_UNPACKING_TABLE[getRep(family)] + "]")
                    if getRep(family) in SI_DERIVED_UNPACKING_TABLE
                    else "",
                )
                for family in SI_DERIVED_TABLE
            ]
        ),
        Style.BRIGHT,
        Style.RESET_ALL,
    )
)
