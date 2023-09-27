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
#    Local Libraries
# ------------------------------------------------------------------------

#    kCells
# -------------------------------------------------------------------
from kCells.cell.superBaseCell import SuperBaseCell


#    Tools
# -------------------------------------------------------------------
import tools.colorConsole as cc
from tools import MyLogging


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
        :param SuperBaseCell myReverse:
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__
        '''
        super().__init__(*args, **kwargs)
        self.logger.debug('Initialized SuperReversedCell')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getLabelPrefix(self): return '-'

    labelPrefix = property(__getLabelPrefix)
    '''
    Negative k-cells get a "-" sign as prefix.

    '''

    def __getLabel(self):
        if self.myReverse is None:
            return 'NOLABEL'
        else:
            return self.myReverse.label

    def __setLabel(self, s):
        if self.myReverse is None:
            print('ERROR: no reverse')
        else:
            self.myReverse.label = s

    label = property(__getLabel, __setLabel)
    '''
    The label is stored in the corresponding positive k-cell

    '''

    def __getIsReverse(self): return True
    isReverse = property(__getIsReverse)
    '''
    All child k-cells are negative, therefor this is always true.

    '''

    def __getIsDeleted(self):
        if self.myReverse:
            return self.myReverse.isDeleted
        else:
            return super().isDeleted

    isDeleted = property(__getIsDeleted)
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
        if self.myReverse:
            self.myReverse.delete()
        else:
            self.logger.error('Cannot delete reversed cell that does not ' +
                              'belong to a cell')


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':

    with MyLogging('SuperReversedCell'):
        cc.printBlue('Create Super Reversed Cell')
        testSUPRC = SuperReversedCell()
        cc.printBlue('The reversed should not be defined')
        print(-testSUPRC)
