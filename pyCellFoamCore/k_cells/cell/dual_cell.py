# -*- coding: utf-8 -*-
# =============================================================================
# DUAL CELL
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Oct 26 10:43:38 2018

'''
Parent class for all dual k-Cells.

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
from pyCellFoamCore.k_cells.cell.cell import Cell

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
#    CLASS DEFINITION
# =============================================================================

class DualCell(Cell):
    '''
    This class only inherits from the Cell class.

    '''

# =============================================================================
#    SLOTS
# =============================================================================
#    __slots__ = ()

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self, *args, **kwargs):
        '''

        :param int num: number of this k-cell
        :param str label: label of this k-cell
        :param bool showLabel: Should the label be shown in the plot?
        :param TUMColor color: The color of this cell in the plot.
        :param SuperBaseCell my_reverse:
        :param str category: The category (inner, border, additonal border),
            that this k-cell belongs to.
        :param bool isGeometrical: Set, if the k-cell is not part of the
            topology of the complex.
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__

        '''
        super().__init__(*args, **kwargs)
        _log.debug('Initialized DualCell')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================
    def __get_is_dual(self): return True
    is_dual = property(__get_is_dual)
    '''

    '''

# =============================================================================
#    METHODS
# =============================================================================
    def updateNum(self, myPrintInfo=None, myPrintError=None):
        '''

        '''
        if myPrintInfo is None:
            myPrintInfo = _log.info
        if myPrintError is None:
            _log.error

        if self.is_geometrical:
            myPrintInfo('Not copying number for geometrical kCell')
        else:
            if self.dualCell3D:
                self.num = self.dualCell3D.num
                myPrintInfo('Copying number of {} from 3D dual'.format(self))
            elif self.dualCell2D:
                self.num = self.dualCell2D.num
                myPrintInfo('Copying number of {} from 2D dual'.format(self))
            elif self.dualCell1D:
                self.num = self.dualCell1D.num
                myPrintInfo('Copying number of {} from 1D dual'.format(self))
            elif self.dualCell0D:
                self.num = self.dualCell0D.num
                myPrintInfo('Copying number of {} from 0D dual'.format(self))
            else:
                myPrintError('{} has no dual - '.format(self)
                             + 'cannot update number')


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================
if __name__ == '__main__':
    set_logging_format(logging.DEBUG)
    cc.printBlue('Creat dual cell')
    test = DualCell()
    cc.printBlue('Check that the isDual attribute ist set correctly')
    print(test.is_dual, test.my_reverse.isDual)
