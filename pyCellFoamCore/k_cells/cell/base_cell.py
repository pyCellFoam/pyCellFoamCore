# -*- coding: utf-8 -*-
# #############################################################################
# BASE CELL
# #############################################################################
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Sep 21 15:17:19 2018

"""
Parent class for all k-Cells.

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
import plotly.graph_objects as go

# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------

#    kCells
# -------------------------------------------------------------------
from pyCellFoamCore.k_cells.cell.super_base_cell import SuperBaseCell

#    Complex & Grids
# -------------------------------------------------------------------


#    Tools
# -------------------------------------------------------------------
from pyCellFoamCore.tools import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


# =============================================================================
#    CLASS BASE CELL
# =============================================================================

class BaseCell(SuperBaseCell):
    """
    This class only inherits from the SuperBaseCell class.

    """
    # ------------------------------------------------------------------------
    #    Slots
    # ------------------------------------------------------------------------
    __slots__ = ()

    # ------------------------------------------------------------------------
    #    Initialization
    # ------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """

        :param SuperBaseCell my_reverse:
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__

        """

        super().__init__(*args, **kwargs)

        _log.debug("Initialized BaseCell")

    # ------------------------------------------------------------------------
    #    Properties
    # ------------------------------------------------------------------------

    def __get_label_suffix(self):
        return ""
    label_suffix = property(__get_label_suffix)
    """
    k-cells  have no suffix (only simple cells do)

    """


# =============================================================================
#    PLOTLY CLASS FOR FAST PLOTTING
# =============================================================================

class BaseCellPlotly:
    """
    Class for fast plotting of k-Cells using Plotly.

    """

    def __init__(self):
        pass

    def _create_plotly_figure(self, old_fig=None, show_axes=None):

        if old_fig is None:
            plotly_figure = go.Figure()
        else:
            plotly_figure = old_fig

        plotly_figure.update_layout(
            scene={
                # "xaxis_title": "X",
                "xaxis_title": {
                    "text": "X",
                    "font": {"size": 30, "color": "black"},
                },
                "yaxis_title": {
                    "text": "Y",
                    "font": {"size": 30, "color": "black"},
                },
                "zaxis_title": {
                    "text": "Z",
                    "font": {"size": 30, "color": "black"},
                },
                "camera": {
                    "up": {"x": -0.234, "y": 0.908, "z": -0.344},
                    "center": {"x": 0, "y": 0, "z": 0},
                    "eye": {"x": 1.075, "y": 0.899, "z": 1.648},
                },
                "dragmode": "orbit",
                # "xaxis": {"visible": show_axes},
                # "yaxis": {"visible": show_axes},
                # "zaxis": {"visible": show_axes},
            },
            scene_camera_projection={"type": "perspective"},
            paper_bgcolor='white',
            plot_bgcolor='white',
            xaxis={
                "title": {
                    "text": "X Axis",
                    "font": {"size": 12, "color": "black"},
                },
            },
        )

        if show_axes is not None:
            plotly_figure.update_layout(
                scene={
                    "xaxis": {"visible": show_axes},
                    "yaxis": {"visible": show_axes},
                    "zaxis": {"visible": show_axes},
                }
            )

        return plotly_figure


# =============================================================================
#    TESTING
# =============================================================================

if __name__ == "__main__":
    set_logging_format(logging.DEBUG)

    testBC = BaseCell()
    print(testBC)
