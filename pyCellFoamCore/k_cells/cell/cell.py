# -*- coding: utf-8 -*-
# =============================================================================
# CELL
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Dec  7 14:16:21 2017

'''
Parent class for all positive k-Cells

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
from pyCellFoamCore.k_cells.cell.base_cell import BaseCell
from k_cells.cell.superCell import SuperCell
from k_cells.cell.reversedCell import ReversedCell

#    Tools
# -------------------------------------------------------------------
import tools.tumcolor as tc
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


class Cell(BaseCell, SuperCell):
    '''
    This class inherits from the BaseCell and the SuperCell classes.

    '''

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self,
                 *args,
                 num=-2,
                 label='c',
                 showLabel=True,
                 color=tc.TUMBlue(),
                 myReverse=None,
                 category='undefined',
                 isGeometrical=False,
                 **kwargs):
        '''

        :param int num: number of this k-cell
        :param str label: label of this k-cell
        :param bool showLabel: Should the label be shown in the plot?
        :param TUMColor color: The color of this cell in the plot.
        :param SuperBaseCell myReverse:
        :param str category: The category (inner, border, additonal border),
            that this k-cell belongs to.
        :param bool isGeometrical: Set, if the k-cell is not part of the
            topology of the complex.
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__

        '''

        if myReverse is None:
            myReverse = ReversedCell(myReverse=self, **kwargs)

        self.__label = label
        self.__num = num
        self.__category1 = category
        self.__category2 = category
        self.__categoryText = ''
        self.__categoryTextChanged = True
        super().__init__(*args, myReverse=myReverse, **kwargs)
        self.__showLabel = showLabel
        self.color = color
        self.__dualCell3D = None
        self.__dualCell2D = None
        self.__dualCell1D = None
        self.__dualCell0D = None
        self.__isGeometrical = isGeometrical
        self.__useCategory = 1
        self.__geometryChanged = True
        self.__showInPlot = True
        self.__grayInTikz = False
        self.__iMorphType = None
        _log.debug('Initialized Cell')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __get_num(self): return self.__num

    def __setNum(self, n):
        self.__num = n
        if not self.isDual:
            if self.dualCell3D:
                self.dualCell3D.updateNum()
            if self.dualCell2D:
                self.dualCell2D.updateNum()
            if self.dualCell1D:
                self.dualCell1D.updateNum()
            if self.dualCell0D:
                self.dualCell0D.updateNum()
        self.update_text()

    num = property(__get_num, __setNum)
    '''
    Number of this k-cell.

    '''

    def __get_label(self): return self.__label

    def __setLabel(self, s):
        self.__label = s
        self.update_text()

    label = property(__get_label, __setLabel)
    '''
    Label (typically one letter) of this k-cell.

    '''

    def __getCategory1(self): return self.__category1

    def __setCategory1(self, t):
        if self.__category1 == 'undefined' or t == 'undefined':
            if t in ['inner', 'border', 'additionalBorder', 'undefined']:
                self.__category1 = t
                self.__categoryTextChanged = True
                self.update_text()
            else:
                _log.error('Unknwon category {}'.format(str(t)))
        else:
            _log.error('Attempting to change type of {} from {} to {}'
                              .format(self.info_text, self.category1, t))
    category1 = property(__getCategory1, __setCategory1)

    '''
    Category 1 is used if the volums in the primal complex are used as control
    volumes.

    '''

    def __getCategory2(self): return self.__category2

    def __setCategory2(self, t):
        if self.__category2 == 'undefined' or t == 'undefined':
            if t in ['inner', 'border', 'additionalBorder', 'undefined']:
                self.__category2 = t
                self.__categoryTextChanged = True
                self.update_text()
            else:
                _log.error('Unknwon category {}'.format(str(t)))
        else:
            _log.error('Attempting to change type of {} from {} to {}'
                              .format(self.info_text, self.category2,
                                      t))

    category2 = property(__getCategory2, __setCategory2)
    '''
    Category 2 is used if the volums in the dual complex are used as control
    volumes.

    '''

    def __get_category(self):
        if self.useCategory == 0:
            return ''
        elif self.useCategory == 1:
            return self.__category1
        elif self.useCategory == 2:
            return self.__category2
        else:
            _log.error('useCategory is set to '
                              + '{}'.format(self.useCategory)
                              + ' - this is not ok: only 1 and 2 is allowed')
            return self.__category1

    def __setCategory(self, c):
        _log.warning('Setting general category of {}'.format(self)
                            + ' - better use category1 or category2')
        if self.useCategory == 1:
            self.category1 = c
        elif self.useCategory == 2:
            self.category2 = c
        else:
            _log.error('useCategory of {}'.format(self)
                              + ' is set to {}'.format(self.useCategory)
                              + ' - Please choose 1 or 2 '
                              + 'before assigning a category')

    category = property(__get_category, __setCategory)
    '''
    Returns either category 1 or 2, depending on the useCategory variable.

    '''

    def __getUseCategory(self): return self.__useCategory

    def __setUseCategory(self, u):
        if u in [1, 2]:
            self.__useCategory = u
            self.__categoryTextChanged = True
            self.update_text()
        else:
            _log.error('Cannot set useCategory of {}'.format(self)
                              + ' to {} - It must be either 1 or 2'.format(u))

    useCategory = property(__getUseCategory, __setUseCategory)
    '''
    Determines which category should be used.

    '''

    def __get_category_text(self):
        if self.__categoryTextChanged:
            self.__createCategoryText()
        return self.__categoryText

    categoryText = property(__get_category_text)
    '''
    Shortcut for the category of this k-cell.

    '''

    def __getCategoryTextChanged(self): return self.__categoryTextChanged

    categoryTextChanged = property(__getCategoryTextChanged)
    '''
    If the category has changed, its shortcut needs to be changed, too.

    '''

    def __getGeometryChanged(self): return self.__geometryChanged

    def __setGeometryChanged(self, g): self.__geometryChanged = g

    geometryChanged = property(__getGeometryChanged, __setGeometryChanged)
    '''
    If the geometry of the k-cell has changed, it needs to be recalculated
    before beeing used the next time.

    '''

    def __getDualCell3D(self):
        return self.__dualCell3D

    def __setDualCell3D(self, d):
        if self.__dualCell3D is None:
            self.__dualCell3D = d
        else:
            _log.error('{} already has a 3D dual'.format(self.info_text))

    dualCell3D = property(__getDualCell3D, __setDualCell3D)
    '''
    3D dual of this k-cell

    '''

    def __getDualCell2D(self):
        return self.__dualCell2D

    def __setDualCell2D(self, d):
        if self.__dualCell2D is None:
            self.__dualCell2D = d
        else:
            _log.error('{} already has a 2D dual'.format(self.info_text))

    dualCell2D = property(__getDualCell2D, __setDualCell2D)
    '''
    2D dual of this k-cell

    '''

    def __getDualCell1D(self):
        return self.__dualCell1D

    def __setDualCell1D(self, d):
        if self.__dualCell1D is None:
            self.__dualCell1D = d
        else:
            _log.error('{} already has a 1D dual'.format(self.info_text))

    dualCell1D = property(__getDualCell1D, __setDualCell1D)
    '''
    1D dual of this k-cell

    '''

    def __getDualCell0D(self): return self.__dualCell0D

    def __setDualCell0D(self, d):
        if self.__dualCell0D is None:
            self.__dualCell0D = d
        else:
            _log.error('{} already has a 0D dual'.format(self.info_text))

    dualCell0D = property(__getDualCell0D, __setDualCell0D)
    '''
    0D dual of this k-cell

    '''

    def __getColor(self): return self.__color

    def __setColor(self, c):
        if isinstance(c, tc.TUMcolor):
            self.__color = c
        else:
            _log.error('Cannot set color of {}: '.format(self) +
                              '{} is not an instance of TUMcolor()'.format(c))

    color = property(__getColor, __setColor)
    '''
    Color in the plots

    '''

    def __getShowLabel(self): return self.__showLabel

    def __setShowLabel(self, show): self.__showLabel = show

    showLabel = property(__getShowLabel, __setShowLabel)
    '''
    Show or hide label in the plot.

    '''

    def __getIsGeometrical(self): return self.__isGeometrical

    def __setIsGeometrical(self, i):
        self.__isGeometrical = i
        if i:
            self.category1 = 'undefined'
            self.category2 = 'undefined'

    isGeometrical = property(__getIsGeometrical, __setIsGeometrical)
    '''
    True, if the k-cell is not part of the topology of the complex.

    '''

    def __get_is_dual(self): return False

    isDual = property(__get_is_dual)
    '''
    Cells are by standard not dual. This function is overwritten in the
    DualCell parent class that all

    '''

    def __getShowInPlot(self): return self.__showInPlot

    def __setShowInPlot(self, s): self.__showInPlot = s

    showInPlot = property(__getShowInPlot, __setShowInPlot)
    '''
    Hide the cell in a plot.
    This function can be useful when k-cells are stored in large lists an some
    k-cells need to be excluded from the plotting but should stay in the list.

    '''

    def __getGrayInTikz(self): return self.__grayInTikz

    def __setGrayInTikz(self, g): self.__grayInTikz = g

    grayInTikz = property(__getGrayInTikz, __setGrayInTikz)
    '''
    Plot with gray color and hide all annotations in the TikZ export.

    '''

    def __getIMorphType(self): return self.__iMorphType

    def __setIMorphType(self, i): self.__iMorphType = i

    iMorphType = property(__getIMorphType, __setIMorphType)
    '''

    '''

# =============================================================================
#    METHODS
# =============================================================================

    def __createCategoryText(self):
        '''
        Give the shortcut for the category that this cell belongs to.

        '''
        if self.category == 'inner':
            self.__categoryText = 'i'
        elif self.category == 'border':
            self.__categoryText = 'b'
        elif self.category == 'additionalBorder':
            self.__categoryText = 'B'
        else:
            self.__categoryText = ''
        self.__categoryTextChanged = False
        _log.debug('Created category text')

    def updateGeometry(self):
        '''
        Mark cell to be recomputed before next usage.

        '''
        _log.debug('Called update Geometry in Cell {}'
                          .format(self.info_text))
        self.__geometryChanged = True


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':
    set_logging_format(logging.DEBUG)

    cc.printBlue('Create a cell')
    testC = Cell(loggerName='test')

    cc.printBlue('Set some attributes of the cell')
    testC.num = 12
    testC.label = 'a'
    testC.isGeometrical = False
    testC.category1 = 'inner'
    testC.category2 = 'border'

    cc.printBlue('Get reversed cell')
    mTestC = -testC

    cc.printBlue('Check that changed variables have been set')
    print(testC.info_text_changed)
    print(mTestC.infoTextChanged)

    cc.printBlue('Check label')
    print(testC.label_text)

    cc.printBlue('Check info text')
    print(testC.info_text)

    cc.printBlue('Check category1 of cell and reversed cell')
    print(testC.category, mTestC.category)

    cc.printBlue('Check category2 of cell and reversed cell')
    testC.useCategory = 2
    print(testC.category, mTestC.category)
