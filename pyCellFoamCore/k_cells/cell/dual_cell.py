# -*- coding: utf-8 -*-
# #############################################################################
# DUAL CELL
# #############################################################################
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
#    CLASS DUAL CELL
# =============================================================================

class DualCell(Cell):
    '''
    This class only inherits from the Cell class.

    '''

    # ------------------------------------------------------------------------
    #    Slots
    # ------------------------------------------------------------------------
    __slots__ = ()

    # ------------------------------------------------------------------------
    #    Initialization
    # ------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        '''

        :param int num: number of this k-cell
        :param str label: label of this k-cell
        :param bool showLabel: Should the label be shown in the plot?
        :param TUMColor color: The color of this cell in the plot.
        :param SuperBaseCell my_reverse:
        :param str category: The category (inner, border, additonal border),
            that this k-cell belongs to.
        :param bool is_geometrical: Set, if the k-cell is not part of the
            topology of the complex.
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__

        '''
        super().__init__(*args, **kwargs)
        _log.debug('Initialized DualCell')

    # ------------------------------------------------------------------------
    #    Properties
    # ------------------------------------------------------------------------
    def __get_is_dual(self):
        return True
    is_dual = property(__get_is_dual)
    '''

    '''

    # ------------------------------------------------------------------------
    #    Methods
    # ------------------------------------------------------------------------
    def updateNum(self, myPrintInfo=None, myPrintError=None):
        '''

        '''

        if self.is_geometrical:
            _log.info('Not copying number for geometrical kCell')
        else:
            if self.dualCell3D:
                self.num = self.dualCell3D.num
                _log.info('Copying number of %s from 3D dual', self)
            elif self.dualCell2D:
                self.num = self.dualCell2D.num
                _log.info('Copying number of %s from 2D dual', self)
            elif self.dualCell1D:
                self.num = self.dualCell1D.num
                _log.info('Copying number of %s from 1D dual', self)
            elif self.dualCell0D:
                self.num = self.dualCell0D.num
                _log.info('Copying number of %s from 0D dual', self)
            else:
                _log.error('%s has no dual - cannot update number', self)


# =============================================================================
#    TESTING
# =============================================================================
if __name__ == '__main__':
    set_logging_format(logging.DEBUG)
    cc.printBlue('Creat dual cell')
    test = DualCell()
    cc.printBlue('Check that the is_dual attribute ist set correctly')
    print(test.is_dual, test.my_reverse.is_dual)
