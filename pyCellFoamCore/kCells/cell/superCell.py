# -*- coding: utf-8 -*-
# =============================================================================
# SUPER CELLL
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Sat Oct  6 12:12:48 2018

'''
Parent class for all positive (simple) k-Cells.

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
from pyCellFoamCore.kCells.cell.super_base_cell import SuperBaseCell
from kCells.cell.superReversedCell import SuperReversedCell


#    Tools
# -------------------------------------------------------------------
import tools.colorConsole as cc
from tools import MyLogging
from tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


# =============================================================================
#    CLASS DEFINITION
# =============================================================================

class SuperCell(SuperBaseCell):
    '''
    This class only inherits from the SuperBaseCell class.

    '''

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self, *args, myReverse=None, **kwargs):
        '''


        :param SuperBaseCell myReverse:
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__
        '''
        if myReverse is None:
            myReverse = SuperReversedCell(myReverse=self, **kwargs)

        self.__isDeleted = False
        super().__init__(*args, my_reverse=myReverse, **kwargs)

        _log.debug('Initialized SuperCell')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __get_label_prefix(self): return ''

    labelPrefix = property(__get_label_prefix)
    '''
    Positive k-cells get no prefix.

    '''

    def __getIsReverse(self): return False

    isReverse = property(__getIsReverse)
    '''
    All child k-cells are positive, therefor this is always false.

    '''

    def __get_is_deleted(self): return self.__isDeleted

    isDeleted = property(__get_is_deleted)
    '''
    To keep track of deleted cells, they are not completely removed from
    memory but marked as "deleted"

    '''

# ------------------------------------------------------------------------
#    Standard values for properties that will be defined in child classes
#    but that are needed for methods in this class
# ------------------------------------------------------------------------

    def __get_label(self):
        _log.warning('Using standard value for label')
        return 'SUPC'

    label = property(__get_label)
    '''
    The label is typically just one letter describing the type of the k-cell.
    This should be implemented in child classes. Using standard value here.

    '''

# =============================================================================
#    METHODS
# =============================================================================

    def update_text(self):
        '''
        The label can only be changed in the cell, not in the reversed cell.
        Therefore the updateText() function is not needed to be implemented in
        the ReversedCell class, here is enough.

        '''
        super().update_text()
        if self.my_reverse:
            self.my_reverse.updateText()

    def delete(self):
        '''
        To keep track of deleted cells, they are not completely removed from
        memory but marked as "deleted"

        '''

        self.__isDeleted = True
        self.update_text()


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == "__main__":
    set_logging_format(logging.DEBUG)

    cc.printBlue('Create Super Cell')
    testSUPC = SuperCell()

    cc.printBlue('Check if both, Super Cell and its reverse, ' +
                 'have been created')
    print(testSUPC, -testSUPC)
