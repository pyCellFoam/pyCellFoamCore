# -*- coding: utf-8 -*-
# =============================================================================
# REVERSED CELL
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Oct 17 13:21:02 2018

'''
Parent class for all negative k-Cells.

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
from kCells.cell.baseCell import BaseCell
from kCells.cell.superCell import SuperReversedCell

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


class ReversedCell(BaseCell, SuperReversedCell):
    '''
    This class inherits from the BaseCell and the SuperCell classes.

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

        :param SuperBaseCell myReverse:
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__

        '''
        super().__init__(*args, **kwargs)
        _log.debug('Initialized Reversed Cell')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getNum(self):
        if self.myReverse:
            return self.myReverse.num
        else:
            return super().num

    def __setNum(self, n): self.myReverse.num = n

    num = property(__getNum, __setNum)
    '''
    The number is stored in the non-reversed cell.

    '''

    def __getLabel(self):
        if self.myReverse:
            return self.myReverse.label
        else:
            return super().label

    def __setLabel(self, s): self.myReverse.label = s

    label = property(__getLabel, __setLabel)
    '''
    The label is stored in the non-reversed cell.

    '''

    def __getColor(self): return self.myReverse.color

    def __setColor(self, c): self.myReverse.color = c

    color = property(__getColor, __setColor)
    '''
    The color is stored in the non-reversed cell.

    '''

    def __getShowLabel(self): return self.myReverse.showLabel

    def __setShowLabel(self, show): self.myReverse.showLabel = show

    showLabel = property(__getShowLabel, __setShowLabel)
    '''
    The label is shown depending on the setting in the non-reversed cell

    '''

    def __getGeometryChanged(self):
        if self.myReverse:
            return self.myReverse.geometryChanged
        else:
            _log.warning('No reverse defined')
            return False

    def __setGeometryChanged(self, t):
        if self.myReverse:
            self.myReverse.geometryChanged = t
        else:
            _log.error('Cannot set geometryChanged')

    geometryChanged = property(__getGeometryChanged, __setGeometryChanged)
    '''
    Geometry changes according to the non-reversed cell

    '''

    def __getCategory(self):
        if self.myReverse:
            return self.myReverse.category
        else:
            return super().category

    def __setCategory(self, t): self.myReverse.category = t

    category = property(__getCategory, __setCategory)
    '''
    The category is stored in the non-reversed cell.

    '''

    def __getCategory1(self):
        if self.myReverse:
            return self.myReverse.category1
        else:
            return super().category1

    def __setCategory1(self, t): self.myReverse.category1 = t

    category1 = property(__getCategory1, __setCategory1)
    '''
    Category 1 is stored in the non-reversed cell.

    '''

    def __getCategory2(self):
        if self.myReverse:
            return self.myReverse.category2
        else:
            return super().category2

    def __setCategory2(self, t): self.myReverse.category2 = t

    category2 = property(__getCategory2, __setCategory2)
    '''
    Category 2 is stored in the non-reversed cell.

    '''

    def __getCategoryText(self):
        if self.myReverse:
            return self.myReverse.categoryText
        else:
            return super().categoryText
    categoryText = property(__getCategoryText)
    '''
    The text for a category is stored in the non-reversed cell.

    '''

    def __getIsGeometrical(self):
        if self.myReverse:
            return self.myReverse.isGeometrical
        else:
            _log.error('No reverse defined')
            return None

    def __setIsGeometrical(self, i):
        if self.myReverse:
            self.myReverse.isGeometrical = i
        else:
            _log.error('Cannot set isGeometrical')

    isGeometrical = property(__getIsGeometrical, __setIsGeometrical)
    '''
    The reversed cell is geometrical, if the non-reversed cell is geometrical.

    '''

    def __getIsDual(self):
        if self.myReverse:
            return self.myReverse.isDual
        else:
            return super().isDual
    isDual = property(__getIsDual)
    '''
    The reversed cell is dual, if the non-reversed cell is dual.

    '''

    def __getDualCell0D(self):
        if self.myReverse:
            if self.myReverse.dualCell0D.myReverse:
                return self.myReverse.dualCell0D.myReverse
            else:
                return self.myReverse.dualCell0D
        else:
            _log.error('No reverse defined, cannot return dualCell0D')
            return False

    def __setDualCell0D(self, d):
        if self.myReverse:
            if d.myReverse:
                self.myReverse.dualCell0D = d.myReverse
            else:
                self.myReverse.dualCell0D = d
        else:
            _log.error('No reverse defined, cannot set dualCell0D')

    dualCell0D = property(__getDualCell0D, __setDualCell0D)
    '''
    0D dual of this k-cell

    '''

    def __getDualCell1D(self):
        if self.myReverse:
            if self.myReverse.dualCell1D.myReverse:
                return self.myReverse.dualCell1D.myReverse
            else:
                return self.myReverse.dualCell1D
        else:
            _log.error('No reverse defined, cannot return dualCell1D')
            return False

    def __setDualCell1D(self, d):
        if self.myReverse:
            if d.myReverse:
                self.myReverse.dualCell1D = d.myReverse
            else:
                self.myReverse.dualCell1D = d
        else:
            _log.error('No reverse defined, cannot set dualCell1D')

    dualCell1D = property(__getDualCell1D, __setDualCell1D)
    '''
    1D dual of this k-cell

    '''

    def __getDualCell2D(self):
        if self.myReverse:
            if self.myReverse.dualCell2D:
                if self.myReverse.dualCell2D.myReverse:
                    return self.myReverse.dualCell2D.myReverse
                else:
                    return self.myReverse.dualCell2D
            else:
                return None
        else:
            _log.error('No reverse defined, cannot return dualCell2D')
            return False

    def __setDualCell2D(self, d):
        if self.myReverse:
            if d.myReverse:
                self.myReverse.dualCell2D = d.myReverse
            else:
                self.myReverse.dualCell2D = d
        else:
            _log.error('No reverse defined, cannot set dualCell2D')

    dualCell2D = property(__getDualCell2D, __setDualCell2D)
    '''
    2D dual of this k-cell

    '''

    def __getDualCell3D(self):
        if self.myReverse:
            if self.myReverse.dualCell3D:
                if self.myReverse.dualCell3D.myReverse:
                    return self.myReverse.dualCell3D.myReverse
                else:
                    return self.myReverse.dualCell3D
            else:
                return self.myReverse.dualCell3D
        else:
            _log.error('No reverse defined, cannot return dualCell3D')
            return False

    def __setDualCell3D(self, d):
        if self.myReverse:
            if d.myReverse:
                self.myReverse.dualCell3D = d.myReverse
            else:
                self.myReverse.dualCell3D = d
        else:
            _log.error('No reverse defined, cannot set dualCell3D')

    dualCell3D = property(__getDualCell3D, __setDualCell3D)
    '''
    3D dual of this k-cell

    '''

    def __getShowInPlot(self):
        if self.myReverse:
            return self.myReverse.showInPlot
        else:
            _log.error('No reverse defined, cannot return showInPlot')

    def __setShowInPlot(self, s):
        if self.myReverse:
            self.myReverse.showInPlot = s
        else:
            _log.error('No reverse defined, cannot set showInPlot')

    showInPlot = property(__getShowInPlot, __setShowInPlot)
    '''
    Hide the cell in a plot.
    This function can be useful when k-cells are stored in large lists an some
    k-cells need to be excluded from the plotting but should stay in the list.

    '''

    def __getGrayInTikz(self):
        if self.myReverse:
            return self.myReverse.grayInTikz
        else:
            _log.error('No reverse defined, cannot return grayInTikz')

    def __setGrayInTikz(self, g):
        if self.myReverse:
            self.myReverse.grayInTikz = g
        else:
            _log.error('No reverse defined, cannot return grayInTikz')

    grayInTikz = property(__getGrayInTikz, __setGrayInTikz)
    '''
    Plot with gray color and hide all annotations in the TikZ export.

    '''

    def __getIMorphType(self):
        if self.myReverse:
            return self.myReverse.iMorphType
        else:
            _log.error('No reverse defined, cannot return iMorphType')

    def __setIMorphType(self, i):
        if self.myReverse:
            self.myReverse.iMorphType = i
        else:
            _log.error('No reverse defined, cannot return iMorphType')

    iMorphType = property(__getIMorphType, __setIMorphType)
    '''

    '''

# =============================================================================
#    METHODS
# =============================================================================

    def updateGeometry(self):
        '''
        Mark cell to be recomputed before next usage.

        '''
        _log.debug('Called update Geometry in ReversedCell {}'
                          .format(self.infoText))
        if self.myReverse:
            self.myReverse.updateGeometry()


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================
if __name__ == '__main__':
    set_logging_format(logging.DEBUG)
    cc.printBlue('Create reversed cell')
    rc = ReversedCell()
    print(rc)
