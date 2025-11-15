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

    # Choose plotting method. Possible choices: pyplot, VTK, TikZ, None, plotly
    PLOTTING_METHOD = "plotly"

    match PLOTTING_METHOD:
        case "pyplot":
            (fig, ax) = pf.getFigures(numTotal=6)
            _log.warning("Not implemented yet.")

        case "VTK":
            _log.warning("Not implemented yet.")

        case "TikZ":
            _log.warning("Not implemented yet.")

        case "plotly":
            plotly_fig = go.Figure()
            plotly_fig.show()
            _log.warning("Not implemented yet.")

        case "None":
            _log.info("No plotting selected.")

        case _:
            _log.error(
                "Unknown plotting '%s' method selected.",
                PLOTTING_METHOD,
            )
