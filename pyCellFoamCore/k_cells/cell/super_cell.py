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
#    Standard Libraries
# ------------------------------------------------------------------------

import logging


# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------

#    kCells
# -------------------------------------------------------------------
from pyCellFoamCore.k_cells.cell.super_base_cell import SuperBaseCell
from pyCellFoamCore.k_cells.cell.super_reversed_cell import SuperReversedCell


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

class SuperCell(SuperBaseCell):
    '''
    This class only inherits from the SuperBaseCell class.

    '''

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self, *args, my_reverse=None, **kwargs):
        '''


        :param SuperBaseCell my_reverse:
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__
        '''
        if my_reverse is None:
            my_reverse = SuperReversedCell(my_reverse=self, **kwargs)

        self.__is_deleted = False
        super().__init__(*args, my_reverse=my_reverse, **kwargs)

        _log.debug('Initialized SuperCell')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __get_label_prefix(self):
        return ''

    label_prefix = property(__get_label_prefix)
    '''
    Positive k-cells get no prefix.

    '''

    def __get_is_reverse(self):
        return False

    is_reverse = property(__get_is_reverse)
    '''
    All child k-cells are positive, therefor this is always false.

    '''

    def __get_is_deleted(self):
        return self.__is_deleted

    is_deleted = property(__get_is_deleted)
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
        Therefore the update_text() function is not needed to be implemented in
        the ReversedCell class, here is enough.

        '''
        super().update_text()
        if self.my_reverse:
            self.my_reverse.update_text()

    def delete(self):
        '''
        To keep track of deleted cells, they are not completely removed from
        memory but marked as "deleted"

        '''

        self.__is_deleted = True
        self.update_text()


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == "__main__":
    set_logging_format(logging.DEBUG)

    _log.info('Create Super Cell')
    testSUPC = SuperCell()

    _log.info('Check if both, Super Cell and its reverse, have been created')
    print(testSUPC, -testSUPC)
