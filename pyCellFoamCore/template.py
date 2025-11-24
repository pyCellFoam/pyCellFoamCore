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

#    kCells
# -------------------------------------------------------------------

#    Tools
# -------------------------------------------------------------------

# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)

# =============================================================================
#    TESTING
# =============================================================================

if __name__ == "__main__":

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
