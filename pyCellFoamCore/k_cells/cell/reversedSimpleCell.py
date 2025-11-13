# -*- coding: utf-8 -*-
# =============================================================================
# REVERSED SIMPLE CELL
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Oct 17 15:25:00 2018

'''
Parent class for all negative simple cells.

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
from k_cells.cell.baseSimpleCell import BaseSimpleCell
from k_cells.cell.superReversedCell import SuperReversedCell


#    Tools
# -------------------------------------------------------------------
from tools import MyLogging
import tools.colorConsole as cc
from tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class ReversedSimpleCell(BaseSimpleCell, SuperReversedCell):
    '''
    This class inherits from the BaseSimpleCell and the SuperReversedCell
    classes.

    '''

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self, *args, **kwargs):
        '''
        :param SuperBaseCell myReverse:
        :param Cell belongsTo: A cell that this simple cell is part of.
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__

        '''
        super().__init__(**kwargs)
        _log.debug('Initialized ReversedSimpleCell')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __get_label_suffix(self):
        if self.my_reverse:
            return self.my_reverse.labelSuffix
        else:
            return super().label_suffix

    def __setLabelSuffix(self, s):
        if self.my_reverse:
            self.my_reverse.labelSuffix = s
        else:
            _log.error('Cannot set label suffix')

    labelSuffix = property(__get_label_suffix, __setLabelSuffix)
    '''
    The label is stored in the corresponding positive simple cell.

    '''

# =============================================================================
#    METHODS
# =============================================================================


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':
    set_logging_format(logging.DEBUG)
    cc.printBlue('Create Reversed Simple Cell')
    rc1 = ReversedSimpleCell()
    cc.printBlue('Check name of created reversed simple cell')
    print(rc1)
    cc.printBlue('Label suffix should not be settable')
    rc1.labelSuffix = '(t)'
