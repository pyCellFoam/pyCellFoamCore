# -*- coding: utf-8 -*-
# =============================================================================
# BASE CELL
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Sep 21 15:17:19 2018

'''
Parent class for all k-Cells.

'''
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
import numpy as np
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
#    CLASS DEFINITION
# =============================================================================


class BaseCell(SuperBaseCell):
    '''
    This class only inherits from the SuperBaseCell class.

    '''

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self, *args, tikZLabelPosition='below right', **kwargs):
        '''

        :param SuperBaseCell my_reverse:
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__

        '''

        super().__init__(*args, **kwargs)
        if self.__check_tikz_label_position(tikZLabelPosition):
            self.__tikz_label_position = tikZLabelPosition
        else:
            self.__tikz_label_position = 'below right'

        _log.debug('Initialized BaseCell')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __get_label_suffix(self):
        return ''
    label_suffix = property(__get_label_suffix)
    '''
    k-cells  have no suffix (only simple cells do)

    '''

    def __get_tikz_label_position(self):
        return self.__tikz_label_position

    def __set_tikz_label_position(self, t):
        if self.__check_tikz_label_position(t):
            self.__tikz_label_position = t

    tikz_label_position = property(
        __get_tikz_label_position,
        __set_tikz_label_position,
    )

# =============================================================================
#    METHODS
# =============================================================================

    def __check_tikz_label_position(self, label_position):
        if label_position in [
            'left', 'right', 'above', 'below', 'below right', 'below left',
            'above right', 'above left'
        ]:
            return True

        _log.error('Unknown position for TikZ label %s', label_position)
        return False


# =============================================================================
#    PLOTLY CLASS FOR FAST PLOTTING
# =============================================================================

class BaseCellPlotly:
    '''
    Class for fast plotting of k-Cells using Plotly.

    '''

    def __init__(self):
        pass

    def _create_plotly_figure(self, old_fig=None, show_axes=None):

        if old_fig is None:
            plotly_figure = go.Figure()
        else:
            plotly_figure = old_fig

        # plotly_figure.update_layout(
        #     scene={
        #         "xaxis_title": "X Axis",
        #         "yaxis_title": "Y Axis",
        #         "zaxis_title": "Z Axis",
        #     },
        #     paper_bgcolor='white',
        #     plot_bgcolor='white'
        # )

        # plotly_figure.update_layout(
        #     scene=dict(
        #         xaxis_title='X Axis',
        #         yaxis_title='Y Axis',
        #         zaxis_title='Z Axis',
        #         camera=dict(
        #             up=dict(x=0, y=0, z=1),
        #             center=dict(x=0, y=0, z=0),
        #             eye=dict(x=1.25, y=1.25, z=1.25)
        #         ),
        #         dragmode='orbit'
        #     ),
        #     scene_camera_projection=dict(type='perspective')
        # )

        plotly_figure.update_layout(
            scene={
                "xaxis_title": "X Axis",
                "yaxis_title": "Y Axis",
                "zaxis_title": "Z Axis",
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
            plot_bgcolor='white'
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
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':
    set_logging_format(logging.DEBUG)

    testBC = BaseCell()
    print(testBC)
