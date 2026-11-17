# -*- coding: utf-8 -*-
# #############################################################################
# SIMPLE CELL
# #############################################################################
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Dec  7 14:16:21 2017

'''
Parent class for all positive simple cells.

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
from pyCellFoamCore.k_cells.cell.base_simple_cell import BaseSimpleCell
from pyCellFoamCore.k_cells.cell.super_cell import SuperCell
from pyCellFoamCore.k_cells.cell.reversed_simple_cell import ReversedSimpleCell

#    Complex & Grids
# -------------------------------------------------------------------


#    Tools
# -------------------------------------------------------------------
import pyCellFoamCore.tools.colorConsole as cc
from pyCellFoamCore.tools import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


# =============================================================================
#    CLASS SIMPLE CELL
# =============================================================================


class SimpleCell(BaseSimpleCell, SuperCell):
    '''
    This class inherits from the BaseSimpleCell and the SuperCell classes.

    '''

    # ------------------------------------------------------------------------
    #    Slots
    # ------------------------------------------------------------------------
    __slots__ = (
        "__label_suffix",
        "__belongs_to"
    )

    # ------------------------------------------------------------------------
    #    Initialization
    # ------------------------------------------------------------------------
    def __init__(self, *args, my_reverse=None, belongsTo=None,
                 label_suffix='NO_SUFFIX', **kwargs):
        '''

        :param SuperBaseCell my_reverse:
        :param Cell belongsTo: A cell that this simple cell is part of.
        :param str label_suffix: The suffix is used if a k-cell consists of more
            than one simple cell. It can be any str.
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__

        '''

        my_reverse = ReversedSimpleCell(my_reverse=self, **kwargs)

        super().__init__(*args,
                         my_reverse=my_reverse,
                         **kwargs)
        self.__label_suffix = label_suffix
        self.__belongs_to = belongsTo
        _log.debug('Initialized SimpleCell')

    # ------------------------------------------------------------------------
    #    Properties
    # ------------------------------------------------------------------------

    def __get_belongs_to(self): return self.__belongs_to
    belongs_to = property(__get_belongs_to)
    '''
    This is the k-cell that this simple cell belongs to.

    '''

    def __get_label_suffix(self):
        return self.__label_suffix

    def __set_label_suffix(self, s):
        self.__label_suffix = s
        self.update_text()

    label_suffix = property(__get_label_suffix, __set_label_suffix)
    '''
    The suffix is used if a k-cell consists of more than one simple cell.

    '''

# =============================================================================
#    TESTING
# =============================================================================


if __name__ == '__main__':
    set_logging_format(logging.DEBUG)
    cc.printBlue('Create a Simple Cell without a suffix')
    sc1 = SimpleCell()
    cc.printBlue('Check name')
    print(sc1)

    cc.printBlue('Create a Simple Cell with a suffix')
    sc2 = SimpleCell(label_suffix='(a)')
    cc.printBlue('Check name')
    print(sc2)

    cc.printBlue('Check label text')
    print(sc2.label_text)

    cc.printBlue('Get associated reversed simple cell')
    rsc1 = -sc1

    cc.printBlue('Change label suffix of the reversed simple cell')
    rsc1.label_suffix = '(b)'

    cc.printBlue('Check that the label suffix of the original simple ' +
                 'cell has changed as well')
    print(sc1, rsc1)
