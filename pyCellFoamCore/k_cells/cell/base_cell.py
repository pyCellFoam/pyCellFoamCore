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

        :param SuperBaseCell myReverse:
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
    labelSuffix = property(__get_label_suffix)
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
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':
    set_logging_format(logging.DEBUG)

    testBC = BaseCell()
    print(testBC)
