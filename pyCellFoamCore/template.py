# -*- coding: utf-8 -*-

# =============================================================================
# NAME
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:

"""
Template for imports and logging structure.

"""

# =============================================================================
#    IMPORTS
# =============================================================================

# ------------------------------------------------------------------------
#    Standard Libraries
# ------------------------------------------------------------------------
import logging

# ------------------------------------------------------------------------
#    Third-Party Libraries
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------

#    k-Cells
# -------------------------------------------------------------------

#    Complex
# -------------------------------------------------------------------

#    Grids
# -------------------------------------------------------------------

#    Bounding Box
# -------------------------------------------------------------------

#    Tools
# -------------------------------------------------------------------
from pyCellFoamCore.tools.logging_formatter import set_logging_format

# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


# =============================================================================
#    CLASS TEMPLATE
# =============================================================================

class Template:
    """
    Template class.

    """
    # ------------------------------------------------------------------------
    #    Slots
    # ------------------------------------------------------------------------
    __slots__ = (
        # Add slot names here
        "__example_variable",
    )

    # ------------------------------------------------------------------------
    #    Initialization
    # ------------------------------------------------------------------------
    def __init__(self, example_variable=None):
        """
        Initialization of the Template class.

        """
        self.__example_variable = example_variable

    # ------------------------------------------------------------------------
    #    Setters and Getters
    # ------------------------------------------------------------------------

    # Example Variable
    # --------------------------------------------------------------------
    def __get_example_variable(self):
        return self.__example_variable

    def __set_example_variable(self, value):
        self.__example_variable = value

    example_variable = property(__get_example_variable, __set_example_variable)
    """
    Example variable property.
    """

    # ------------------------------------------------------------------------
    #    Magic Methods
    # ------------------------------------------------------------------------
    def __repr__(self):
        return f"Template(example_variable={self.__example_variable})"

    # ------------------------------------------------------------------------
    #    Methods
    # ------------------------------------------------------------------------

    # Example Method
    # --------------------------------------------------------------------
    def example_method(self):
        """
        Example method.

        """
        # Example implementation
        # ................................................................
        _log.info("This is an example method.")


# =============================================================================
#    TESTING
# =============================================================================

if __name__ == "__main__":

    set_logging_format(logging.DEBUG)

    # --------------------------------------------------------------------
    #    Create sample data
    # --------------------------------------------------------------------

    # --------------------------------------------------------------------
    #    Plotting
    # --------------------------------------------------------------------

    # Choose plotting method. Possible choices: pyplot, VTK, TikZ, plotly, None
    PLOTTING_METHOD = "plotly"

    match PLOTTING_METHOD:
        case "pyplot":
            _log.info("Plotting with pyplot selected.")
            _log.warning("Not implemented yet.")

        case "VTK":
            _log.info("Plotting with VTK selected.")
            _log.warning("Not implemented yet.")

        case "TikZ":
            _log.info("Plotting with TikZ selected.")
            _log.warning("Not implemented yet.")

        case "plotly":
            _log.info("Plotting with plotly selected.")
            _log.warning("Not implemented yet.")

        case "None":
            _log.info("No plotting selected.")

        case _:
            _log.error(
                "Unknown plotting '%s' method selected.",
                PLOTTING_METHOD,
            )
