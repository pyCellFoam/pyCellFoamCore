# -*- coding: utf-8 -*-
# =============================================================================
# SUPER REVERSED CELL
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Sat Oct  6 12:18:32 2018

'''
Parent class for all negative (simple) k-Cells.

'''

# =============================================================================
#    IMPORTS
# =============================================================================
# ------------------------------------------------------------------------
#    Change to Main Directory
# ------------------------------------------------------------------------
import os
if __name__ == '__main__':
    os.chdir('../../')

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
import pyCellFoamCore.tools.colorConsole as cc
from pyCellFoamCore.tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


# =============================================================================
#    CLASS DEFINITION
# =============================================================================
class SuperReversedCell(SuperBaseCell):
    '''
    This class only inherits from the SuperBaseCell class.

    '''

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self, *args, **kwargs):
        '''
        :param SuperBaseCell my_reverse:
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__
        '''
        super().__init__(*args, **kwargs)
        _log.debug('Initialized SuperReversedCell')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __get_label_prefix(self): return '-'

    label_prefix = property(__get_label_prefix)
    '''
    Negative k-cells get a "-" sign as prefix.

    '''

    def __get_label(self):
        if self.my_reverse is None:
            return 'NOLABEL'
        else:
            return self.my_reverse.label

    def __setLabel(self, s):
        if self.my_reverse is None:
            print('ERROR: no reverse')
        else:
            self.my_reverse.label = s

    label = property(__get_label, __setLabel)
    '''
    The label is stored in the corresponding positive k-cell

    '''

    def __getis_reverse(self): return True
    is_reverse = property(__getis_reverse)
    '''
    All child k-cells are negative, therefor this is always true.

    '''

    def __get_is_deleted(self):
        if self.my_reverse:
            return self.my_reverse.is_deleted
        else:
            return super().is_deleted

    is_deleted = property(__get_is_deleted)
    '''
    The negative k-cell is always deleted with its positive counterpart.

    '''


# =============================================================================
#    METHODS
# =============================================================================

    def delete(self):
        '''
        The negative k-cell is always deleted with its positive counterpart.

        '''
        if self.my_reverse:
            self.my_reverse.delete()
        else:
            _log.error('Cannot delete reversed cell that does not ' +
                              'belong to a cell')


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':

    set_logging_format(logging.DEBUG)
    cc.printBlue('Create Super Reversed Cell')
    testSUPRC = SuperReversedCell()
    cc.printBlue('The reversed should not be defined')
    print(-testSUPRC)
