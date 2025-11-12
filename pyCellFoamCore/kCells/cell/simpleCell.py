# -*- coding: utf-8 -*-
# =============================================================================
# SIMPLE CELL
# =============================================================================
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
from kCells.cell.baseSimpleCell import BaseSimpleCell
from kCells.cell.superCell import SuperCell
from kCells.cell.reversedSimpleCell import ReversedSimpleCell

#    Complex & Grids
# -------------------------------------------------------------------


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


class SimpleCell(BaseSimpleCell, SuperCell):
    '''
    This class inherits from the BaseSimpleCell and the SuperCell classes.

    '''

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self, *args, myReverse=None, belongsTo=None,
                 labelSuffix='NO_SUFFIX', **kwargs):
        '''

        :param SuperBaseCell myReverse:
        :param Cell belongsTo: A cell that this simple cell is part of.
        :param str labelSuffix: The suffix is used if a k-cell consists of more
            than one simple cell. It can be any str.
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__

        '''
        if myReverse is None:
            if belongsTo is not None:
                belongsToReversed = belongsTo.myReverse
            else:
                belongsToReversed = None
            myReverse = ReversedSimpleCell(myReverse=self,
                                           belongsTo=belongsToReversed,
                                           **kwargs)
        super().__init__(*args,
                         belongsTo=belongsTo,
                         myReverse=myReverse,
                         **kwargs)
        self.__labelSuffix = labelSuffix
        _log.debug('Initialized SimpleCell')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __get_label_suffix(self): return self.__labelSuffix

    def __setLabelSuffix(self, s):
        self.__labelSuffix = s
        self.update_text()

    labelSuffix = property(__get_label_suffix, __setLabelSuffix)
    '''
    The suffix is used if a k-cell consists of more than one simple cell.

    '''

# =============================================================================
#    METHODS
# =============================================================================


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':
    set_logging_format(logging.DEBUG)
    cc.printBlue('Create a Simple Cell without a suffix')
    sc1 = SimpleCell()
    cc.printBlue('Check name')
    print(sc1)

    cc.printBlue('Create a Simple Cell with a suffix')
    sc2 = SimpleCell(labelSuffix='(a)')
    cc.printBlue('Check name')
    print(sc2)

    cc.printBlue('Check label text')
    print(sc2.label_text)

    cc.printBlue('Get associated reversed simple cell')
    rsc1 = -sc1

    cc.printBlue('Change label suffix of the reversed simple cell')
    rsc1.labelSuffix = '(b)'

    cc.printBlue('Check that the label suffix of the original simple ' +
                 'cell has changed as well')
    print(sc1, rsc1)
