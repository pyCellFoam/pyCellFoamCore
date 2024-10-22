# -*- coding: utf-8 -*-
# =============================================================================
# BASE CELL
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Sep 21 15:17:19 2018

'''
Parent class for all k-Cells.

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

#    Complex & Grids
# -------------------------------------------------------------------


#    Tools
# -------------------------------------------------------------------
import tools.colorConsole as cc
import tools.myLogging as myLogging


# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class BaseCell(SuperBaseCell):
    '''
    This class only inherits from the SuperBaseCell class.

    '''

# =============================================================================
#    SLOTS
# =============================================================================
#    __slots__ = ('__tikZLabelPosition')

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self, *args, tikZLabelPosition='below right', **kwargs):
        '''

        :param SuperBaseCell myReverse:
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__

        '''

        super().__init__(*args, **kwargs)
        self.tikZLabelPosition = tikZLabelPosition
        self.logger.debug('Initialized BaseCell')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getLabelSuffix(self): return ''
    labelSuffix = property(__getLabelSuffix)
    '''
    k-cells  have no suffix (only simple cells do)

    '''

    def __getTikZLabelPosition(self): return self.__tikZLabelPosition

    def __setTikZLabelPosition(self, t):
        if t in ['left', 'right', 'above', 'below',
                 'below right', 'below left', 'above right', 'above left']:
            self.__tikZLabelPosition = t
        else:
            self.logger.error('Unknown position for TikZ label {}'.format(t))

    tikZLabelPosition = property(__getTikZLabelPosition,
                                 __setTikZLabelPosition)

# =============================================================================
#    METHODS
# =============================================================================


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':
    with myLogging.MyLogging('BaseCell', debug=True):
        cc.printBlue('Create base cell')
        testBC = BaseCell()
        print(testBC)
