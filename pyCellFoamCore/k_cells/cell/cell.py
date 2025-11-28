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
#    Standard Libraries
# ------------------------------------------------------------------------
import logging

# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------

#    kCells
# -------------------------------------------------------------------
from pyCellFoamCore.k_cells.cell.base_cell import BaseCell
from pyCellFoamCore.k_cells.cell.super_cell import SuperCell
from pyCellFoamCore.k_cells.cell.reversed_cell import ReversedCell

#    Tools
# -------------------------------------------------------------------
import pyCellFoamCore.tools.tumcolor as tc
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


class Cell(BaseCell, SuperCell):
    '''
    This class inherits from the BaseCell and the SuperCell classes.

    '''

    # =========================================================================
    #    INITIALIZATION
    # =========================================================================
    def __init__(self,
                 *args,
                 num=-2,
                 label='c',
                 show_label=True,
                 color=tc.TUMBlue(),
                 my_reverse=None,
                 category='undefined',
                 is_geometrical=False,
                 **kwargs):
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

        if my_reverse is None:
            my_reverse = ReversedCell(my_reverse=self, **kwargs)

        self.__label = label
        self.__num = num
        self.__category1 = category
        self.__category2 = category
        self.__category_text = ''
        self.__category_text_changed = True
        super().__init__(*args, my_reverse=my_reverse, **kwargs)
        self.__show_label = show_label
        self.color = color
        self.__dual_cell_3d = None
        self.__dual_cell_2d = None
        self.__dual_cell_1d = None
        self.__dual_cell_0d = None
        self.__is_geometrical = is_geometrical
        self.__use_category = 1
        self.__geometry_changed = True
        self.__show_in_plot = True
        self.__gray_in_tikz = False
        self.__imorph_type = None
        _log.debug('Initialized Cell')

    # =========================================================================
    #    SETTER AND GETTER
    # =========================================================================

    def __get_num(self): return self.__num

    def __set_num(self, n):
        self.__num = n
        if not self.is_dual:
            if self.dualCell3D:
                self.dualCell3D.updateNum()
            if self.dualCell2D:
                self.dualCell2D.updateNum()
            if self.dualCell1D:
                self.dualCell1D.updateNum()
            if self.dualCell0D:
                self.dualCell0D.updateNum()
        self.update_text()

    num = property(__get_num, __set_num)
    '''
    Number of this k-cell.

    '''

    def __get_label(self):
        return self.__label

    def __set_label(self, s):
        self.__label = s
        self.update_text()

    label = property(__get_label, __set_label)
    '''
    Label (typically one letter) of this k-cell.

    '''

    def __get_category1(self): return self.__category1

    def __set_category1(self, t):
        if self.__category1 == 'undefined' or t == 'undefined':
            if t in ['inner', 'border', 'additionalBorder', 'undefined']:
                self.__category1 = t
                self.__category_text_changed = True
                self.update_text()
            else:
                _log.error('Unknwon category %s', t)
        else:
            _log.error(
                'Attempting to change type of %s from %s to %s',
                self,
                self.category1,
                t,
            )
    category1 = property(__get_category1, __set_category1)

    '''
    Category 1 is used if the volums in the primal complex are used as control
    volumes.

    '''

    def __get_category2(self):
        return self.__category2

    def __set_category2(self, t):
        if self.__category2 == 'undefined' or t == 'undefined':
            if t in ['inner', 'border', 'additionalBorder', 'undefined']:
                self.__category2 = t
                self.__category_text_changed = True
                self.update_text()
            else:
                _log.error('Unknwon category %s', t)
        else:
            _log.error('Attempting to change type of {} from {} to {}'
                              .format(self.info_text, self.category2,
                                      t))

    category2 = property(__get_category2, __set_category2)
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

    def __getUseCategory(self): return self.__use_category

    def __setUseCategory(self, u):
        if u in [1, 2]:
            self.__use_category = u
            self.__category_text_changed = True
            self.update_text()
        else:
            _log.error('Cannot set useCategory of {}'.format(self)
                              + ' to {} - It must be either 1 or 2'.format(u))

    useCategory = property(__getUseCategory, __setUseCategory)
    '''
    Determines which category should be used.

    '''

    def __get_category_text(self):
        if self.__category_text_changed:
            self.__createcategory_text()
        return self.__category_text

    category_text = property(__get_category_text)
    '''
    Shortcut for the category of this k-cell.

    '''

    def __getcategory_textChanged(self): return self.__category_text_changed

    category_text_changed = property(__getcategory_textChanged)
    '''
    If the category has changed, its shortcut needs to be changed, too.

    '''

    def __getGeometryChanged(self): return self.__geometry_changed

    def __setGeometryChanged(self, g): self.__geometry_changed = g

    geometryChanged = property(__getGeometryChanged, __setGeometryChanged)
    '''
    If the geometry of the k-cell has changed, it needs to be recalculated
    before beeing used the next time.

    '''

    def __getDualCell3D(self):
        return self.__dual_cell_3d

    def __setDualCell3D(self, d):
        if self.__dual_cell_3d is None:
            self.__dual_cell_3d = d
        else:
            _log.error('{} already has a 3D dual'.format(self.info_text))

    dualCell3D = property(__getDualCell3D, __setDualCell3D)
    '''
    3D dual of this k-cell

    '''

    def __getDualCell2D(self):
        return self.__dual_cell_2d

    def __setDualCell2D(self, d):
        if self.__dual_cell_2d is None:
            self.__dual_cell_2d = d
        else:
            _log.error('{} already has a 2D dual'.format(self.info_text))

    dualCell2D = property(__getDualCell2D, __setDualCell2D)
    '''
    2D dual of this k-cell

    '''

    def __getDualCell1D(self):
        return self.__dual_cell_1d

    def __setDualCell1D(self, d):
        if self.__dual_cell_1d is None:
            self.__dual_cell_1d = d
        else:
            _log.error('{} already has a 1D dual'.format(self.info_text))

    dualCell1D = property(__getDualCell1D, __setDualCell1D)
    '''
    1D dual of this k-cell

    '''

    def __getDualCell0D(self): return self.__dual_cell_0d

    def __setDualCell0D(self, d):
        if self.__dual_cell_0d is None:
            self.__dual_cell_0d = d
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

    def __getShowLabel(self): return self.__show_label

    def __setShowLabel(self, show): self.__show_label = show

    showLabel = property(__getShowLabel, __setShowLabel)
    '''
    Show or hide label in the plot.

    '''

    def __get_is_geometrical(self): return self.__is_geometrical

    def __set_is_geometrical(self, i):
        self.__is_geometrical = i
        if i:
            self.category1 = 'undefined'
            self.category2 = 'undefined'

    is_geometrical = property(__get_is_geometrical, __set_is_geometrical)
    '''
    True, if the k-cell is not part of the topology of the complex.

    '''

    def __get_is_dual(self): return False

    is_dual = property(__get_is_dual)
    '''
    Cells are by standard not dual. This function is overwritten in the
    DualCell parent class that all

    '''

    def __getShowInPlot(self): return self.__show_in_plot

    def __setShowInPlot(self, s): self.__show_in_plot = s

    showInPlot = property(__getShowInPlot, __setShowInPlot)
    '''
    Hide the cell in a plot.
    This function can be useful when k-cells are stored in large lists an some
    k-cells need to be excluded from the plotting but should stay in the list.

    '''

    def __get_gray_in_tikz(self): return self.__gray_in_tikz

    def __set_gray_in_tikz(self, g): self.__gray_in_tikz = g

    gray_in_tikz = property(__get_gray_in_tikz, __set_gray_in_tikz)
    '''
    Plot with gray color and hide all annotations in the TikZ export.

    '''

    def __getIMorphType(self): return self.__imorph_type

    def __setIMorphType(self, i): self.__imorph_type = i

    iMorphType = property(__getIMorphType, __setIMorphType)
    '''

    '''

    # =========================================================================
    #    METHODS
    # =========================================================================

    def __createcategory_text(self):
        '''
        Give the shortcut for the category that this cell belongs to.

        '''
        if self.category == 'inner':
            self.__category_text = 'i'
        elif self.category == 'border':
            self.__category_text = 'b'
        elif self.category == 'additionalBorder':
            self.__category_text = 'B'
        else:
            self.__category_text = ''
        self.__category_text_changed = False
        _log.debug('Created category text')

    def updateGeometry(self):
        '''
        Mark cell to be recomputed before next usage.

        '''
        _log.debug('Called update Geometry in Cell {}'
                          .format(self.info_text))
        self.__geometry_changed = True


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':
    set_logging_format(logging.DEBUG)

    cc.printBlue('Create a cell')
    testC = Cell()

    cc.printBlue('Set some attributes of the cell')
    testC.num = 12
    testC.label = 'a'
    testC.is_geometrical = False
    testC.category1 = 'inner'
    testC.category2 = 'border'

    cc.printBlue('Get reversed cell')
    mTestC = -testC

    cc.printBlue('Check that changed variables have been set')
    print(testC.info_text_changed)
    print(mTestC.info_text_changed)

    cc.printBlue('Check label')
    print(testC.label_text)

    cc.printBlue('Check info text')
    print(testC.info_text)

    cc.printBlue('Check category1 of cell and reversed cell')
    print(testC.category, mTestC.category)

    cc.printBlue('Check category2 of cell and reversed cell')
    testC.useCategory = 2
    print(testC.category, mTestC.category)
