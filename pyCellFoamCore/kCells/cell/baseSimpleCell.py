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
from kCells.cell.superBaseCell import SuperBaseCell


#    Tools
# -------------------------------------------------------------------
import tools.tumcolor as tc
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

class BaseSimpleCell(SuperBaseCell):
    '''
    This class only inherits from the SuperBaseCell class.

    '''

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self, *args, belongsTo=None, **kwargs):
        '''
        :param Cell belongsTo: A cell that this simple cell is part of.
        :param SuperBaseCell myReverse:
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__

        '''
        super().__init__(*args, **kwargs)
        self.__belongsTo = belongsTo
        self.__tikZLabelPosition = None
        _log.debug('Initialized BaseSimpleCell')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getBelongsTo(self): return self.__belongsTo
    belongsTo = property(__getBelongsTo)
    '''
    This is the k-cell that this simple cell belongs to.

    '''

    def __getTikZLabelPosition(self):
        if self.__tikZLabelPosition is None and self.__belongsTo:
            return self.__belongsTo.tikZLabelPosition
        else:
            return self.__tikZLabelPosition

    def __setTikZLabelPosition(self, t):
        if t in ['left', 'right', 'above', 'below',
                 'below right', 'below left', 'above right', 'above left']:
            self.__tikZLabelPosition = t
        else:
            _log.error('Unknown position for TikZ label {}'.format(t))

    tikZLabelPosition = property(__getTikZLabelPosition,
                                 __setTikZLabelPosition)

    def __getLabel(self):
        if self.belongsTo:
            return self.belongsTo.label
        else:
            return 'SIMC'
    label = property(__getLabel)
    '''
    The label is the same as the k-cell that this simple cell belongs to.

    '''

    def __getIsGeometrical(self):
        if self.belongsTo:
            return self.belongsTo.isGeometrical
        else:
            _log.warning('Simple cell {} '.format(self.info_text) +
                                'does not belong to a real' +
                                'cell, using fixed standard value for ' +
                                'isGeometrical')
            return False
    isGeometrical = property(__getIsGeometrical)
    '''
    If the k-cell that the simple cell belongs to is geometrical, then the
    simple cell is geometrical, too.

    '''

    def __getColor(self):
        if self.belongsTo:
            return self.belongsTo.color
        else:
            _log.warning('Simple cell {} '.format(self.info_text) +
                                'does not belong to a real ' +
                                'cell, using fixed standard value for ' +
                                'color')
            return tc.TUMOrange()
    color = property(__getColor)
    '''
    Using the color of the corresponding k-cell.

    '''

    def __getNum(self):
        if self.belongsTo:
            return self.belongsTo.num
        else:
            _log.warning('Simple cell does not belong to a real cell,' +
                                ' using fixed standard value for num')
            return super().num
    num = property(__getNum)
    '''
    Using the number of the corresponding k-cell.

    '''

    def __getIsDual(self):
        if self.belongsTo:
            return self.belongsTo.isDual
        else:
            _log.warning('Simple cell does not belong to a real cell,' +
                                ' using fixed standard value for isDual')
            return super().isDual
    isDual = property(__getIsDual)
    '''
    If the k-cell that the simple cell belongs to is in a dual complex, then
    the simple cell is part of a dual complex, too.

    '''

    def __getCategoryText(self):
        if self.belongsTo:
            return self.belongsTo.categoryText
        else:
            _log.warning('Simple cell does not belong to a real cell,' +
                                ' using fixed standard value for categoryText')
            return super().categoryText
    categoryText = property(__getCategoryText)
    '''
    Using the category of the corresponding k-cell.

    '''

    def __getShowLabel(self):
        if self.belongsTo:
            return self.belongsTo.showLabel
        else:
            _log.warning('Simple cell {} '.format(self.info_text) +
                                'does not belong to a real' +
                                ' cell, using fixed standard value' +
                                ' for showLabel')
            return True
    showLabel = property(__getShowLabel)
    '''
    Showing label in the plot, if this is wanted for the corresponding k-cell.

    '''

    def __getGrayInTikz(self):
        if self.belongsTo:
            return self.belongsTo.grayInTikz
        else:
            _log.warning('Simple cell {}'.format(self.info_text) +
                                ' does not belong to a real cell, ' +
                                'using fixed standard value for grayInTikz')
            return False
    grayInTikz = property(__getGrayInTikz)
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

    cc.printBlue('Check if a standard value for isGeometrical is given')
    print(sc1.isGeometrical)

    cc.printBlue('Check if a standard value for color is given')
    print(sc1.color)

    cc.printBlue('Check if a standard value for num is given')
    print(sc1.num)

    cc.printBlue('Check if a standard value for isDual is given')
    print(sc1.isDual)

    cc.printBlue('Check if a standard value for categoryText is given')
    print(sc1.categoryText)

    cc.printBlue('Check that it does not belong to a cell')
    print('Belongs to:', sc1.belongsTo)

    cc.printBlue('Check that the label position can be set and read')
    sc1.tikZLabelPosition = 'below'
    print('TikZ Label:', sc1.tikZLabelPosition)
