# -*- coding: utf-8 -*-
# =============================================================================
# BASE SIMPLE CELL
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Oct 17 15:08:57 2018

'''
Parent class for all simple cells.

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


#    Tools
# -------------------------------------------------------------------
import pyCellFoamCore.tools.tumcolor as tc
import pyCellFoamCore.tools.colorConsole as cc
from pyCellFoamCore.tools import set_logging_format

# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


# =============================================================================
#    CLASS DEFINITION
# =============================================================================

class BaseSimpleCell(SuperBaseCell):
    '''
    This class only inherits from the SuperBaseCell class.

    '''

    # =========================================================================
    #    INITIALIZATION
    # =========================================================================
    def __init__(self, *args, belongsTo=None, **kwargs):
        '''
        :param Cell belongsTo: A cell that this simple cell is part of.
        :param SuperBaseCell my_reverse:
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__

        '''
        super().__init__(*args, **kwargs)
        self.__belongs_to = belongsTo
        self.__tikz_label_position = None
        _log.debug('Initialized BaseSimpleCell')

    # =========================================================================
    #    SETTER AND GETTER
    # =========================================================================

    def __get_belongs_to(self): return self.__belongs_to
    belongs_to = property(__get_belongs_to)
    '''
    This is the k-cell that this simple cell belongs to.

    '''

    def __get_tikz_label_position(self):
        if self.__tikz_label_position is None and self.__belongs_to:
            return self.__belongs_to.tikZLabelPosition
        else:
            return self.__tikz_label_position

    def __set_tikz_label_position(self, t):
        if t in ['left', 'right', 'above', 'below',
                 'below right', 'below left', 'above right', 'above left']:
            self.__tikz_label_position = t
        else:
            _log.error('Unknown position for TikZ label %s', t)

    tikz_label_position = property(
        __get_tikz_label_position,
        __set_tikz_label_position,
    )

    def __get_label(self):
        if self.belongs_to:
            return self.belongs_to.label
        else:
            return 'SIMC'
    label = property(__get_label)
    '''
    The label is the same as the k-cell that this simple cell belongs to.

    '''

    def __get_is_geometrical(self):
        if self.belongs_to:
            return self.belongs_to.is_geometrical

        _log.warning(
            "Simple cell does not belong to a real cell, using fixed "
            "standard value for is_geometrical",
        )
        return False
    is_geometrical = property(__get_is_geometrical)
    '''
    If the k-cell that the simple cell belongs to is geometrical, then the
    simple cell is geometrical, too.

    '''

    def __get_color(self):
        if self.belongs_to:
            return self.belongs_to.color

        _log.warning(
            "Simple cell does not belong to a real cell, using fixed "
            "standard value for color",
        )

        return tc.TUMOrange()
    color = property(__get_color)
    '''
    Using the color of the corresponding k-cell.

    '''

    def __get_num(self):
        if self.belongs_to:
            return self.belongs_to.num

        _log.warning(
            "Simple cell does not belong to a real cell, using fixed "
            "standard value for num",
        )
        return super().num

    num = property(__get_num)
    '''
    Using the number of the corresponding k-cell.

    '''

    def __get_is_dual(self):
        if self.belongs_to:
            return self.belongs_to.is_dual

        _log.warning(
            "Simple cell does not belong to a real cell, using fixed "
            "standard value for is_dual",
        )
        return super().is_dual

    is_dual = property(__get_is_dual)
    '''
    If the k-cell that the simple cell belongs to is in a dual complex, then
    the simple cell is part of a dual complex, too.

    '''

    def __get_category_text(self):
        if self.belongs_to:
            return self.belongs_to.category_text

        _log.warning(
            "Simple cell does not belong to a real cell, using fixed "
            "standard value for category_text",
        )
        return super().category_text

    category_text = property(__get_category_text)
    '''
    Using the category of the corresponding k-cell.

    '''

    def __get_show_label(self):
        if self.belongs_to:
            return self.belongs_to.showLabel

        _log.warning(
            "Simple cell does not belong to a real cell, using fixed "
            "standard value for showLabel",
        )
        return True

    showLabel = property(__get_show_label)
    '''
    Showing label in the plot, if this is wanted for the corresponding k-cell.

    '''

    def __get_gray_in_tikz(self):
        if self.belongs_to:
            return self.belongs_to.gray_in_tikz

        _log.warning(
            "Simple cell does not belong to a real cell, using fixed "
            "standard value for gray_in_tikz",
        )
        return False

    gray_in_tikz = property(__get_gray_in_tikz)
    '''

    '''

# =============================================================================
#    METHODS
# =============================================================================


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':
    set_logging_format(logging.DEBUG)

    cc.printBlue('Create Base Simple Cell')
    sc1 = BaseSimpleCell()

    cc.printBlue('Check if a standard value for is_geometrical is given')
    print(sc1.is_geometrical)

    cc.printBlue('Check if a standard value for color is given')
    print(sc1.color)

    cc.printBlue('Check if a standard value for num is given')
    print(sc1.num)

    cc.printBlue('Check if a standard value for is_dual is given')
    print(sc1.is_dual)

    cc.printBlue('Check if a standard value for category_text is given')
    print(sc1.category_text)

    cc.printBlue('Check that it does not belong to a cell')
    print('Belongs to:', sc1.belongs_to)

    cc.printBlue('Check that the label position can be set and read')
    sc1.tikz_label_position = 'below'
    print('TikZ Label:', sc1.tikz_label_position)
