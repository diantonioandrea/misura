# Globals.


class style:
    """
    Styling global options for misura.
    """

    quantityHighlighting = True
    quantityPlusMinus = " \u00b1 "


class logic:
    """
    Logical global options for misura.
    """

    ignoreUncertainty = False


class currencies:
    """
    Currency global options.
    """

    path = ""  # File path for local rates.


class defined:
    """
    User defined units.
    """

    BASE_TABLE = {}
    DERIVED_TABLE = {}
    DERIVED_UNPACKING_TABLE = {}
