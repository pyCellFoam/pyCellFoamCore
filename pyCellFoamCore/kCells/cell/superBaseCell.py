# -*- coding: utf-8 -*-
# =============================================================================
# SUPER BASE CELL
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Sat Oct  6 09:48:45 2018

'''
Top parent class that contains the most basic properties of all k-cells.

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

#    Tools
# -------------------------------------------------------------------

from pyCellFoamCore import set_logging_format

# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


# =============================================================================
#    CLASS DEFINITION
# =============================================================================

class SuperBaseCell:
    '''
    This class does not inherit from any other class.

    '''

    # =========================================================================
    #    CLASS VARIABLES
    # =========================================================================

    allCells = []

    # =========================================================================
    #    INITIALIZATION
    # =========================================================================
    def __init__(
        self,
        *args,
        my_reverse=None,
        **kwargs
    ):

        self.__my_reverse = my_reverse

        # prepare text changed variables
        self.__label_text_changed = True
        self.__info_text = ''
        self.__info_text_changed = True

        # Check if there are any non-used positional arguments
        if args:
            _log.warning(
                'Unused positional arguments %s were passed',
                args,
            )

        if kwargs:
            _log.warning(
                'Unused keyword arguments %s were passed',
                kwargs,
            )

        if self in SuperBaseCell.allCells:
            _log.error(
                'Multiple call of SuperBaseCell for %s',
                self,
            )

        else:
            SuperBaseCell.allCells.append(self)

        _log.debug('Initialized SuperBaseCell')

    # =========================================================================
    #    SETTER AND GETTER
    # =========================================================================

    def __get_info_text(self):
        if self.__info_text_changed:
            self.__create_info_text()
        return self.__info_text
    info_text = property(__get_info_text)
    '''
    This text is used to be displayed in the console to identify the cell in a
    readable way.

    '''

    def __getLabelText(self):
        if self.__label_text_changed:
            self.__create_label_text()
        return self.__labelText
    labelText = property(__getLabelText)
    '''
    This text ist used in plots.

    '''

    def __getLabelTextShort(self):
        if self.__label_text_changed:
            self.__create_label_text()
        return self.__labelTextShort
    labelTextShort = property(__getLabelTextShort)
    '''
    Short version of the label text, mostly for TikZ export

    '''

    def __getTikZName(self):
        name = self.label.replace('\\', '') \
            + self.categoryText + str(self.num) \
            + str(self.labelSuffix.replace('(', '').replace(')', ''))
        if self.isDual:
            name = 'd' + name
        name = name.replace(',', '_')
        return name
    tikZName = property(__getTikZName)
    '''
    Name of the k-cell in the TikZ-plot.

    '''

    def __getMyReverse(self): return self.__my_reverse
    myReverse = property(__getMyReverse)
    '''
    Returns the reverse of this cell, can also be accesed by using the - symbol

    '''

    def __getLabelTextChanged(self): return self.__label_text_changed
    labelTextChanged = property(__getLabelTextChanged)
    '''
    This is set to true if some element of the the label text has changed since
    the last time that the text was compiled.

    '''

    def __getInfoTextChanged(self): return self.__info_text_changed
    infoTextChanged = property(__getInfoTextChanged)
    '''
    This is set to true if some element of the the info text has changed since
    the last time that the text was compiled.

    '''

    def __getTolerance(self): return 1E-4
    tolerance = property(__getTolerance)
    '''
    Tolerance used to check for parallelity and perpendicularity.

    '''

    # --------------------------------------------------------------------
    #    Standard values for properties that will be defined in child classes
    #    but that are needed for methods in this class
    # --------------------------------------------------------------------

    def __getLabel(self):
        _log.warning('Using standard value for label')
        return 'SUPBC'
    label = property(__getLabel)
    '''
    The label is typically just one letter describing the type of the k-cell.
    This should be implemented in child classes. Using standard value here.

    '''

    def __getNum(self):
        _log.warning('Using standard value for num')
        return -1
    num = property(__getNum)

    '''
    The k-cells need to be numbered.
    This should be implemented in child classes. Using standard value here.

    '''

    def __getLabelPrefix(self):
        _log.warning('Using standard value for labelPrefix')
        return 'x'
    labelPrefix = property(__getLabelPrefix)
    '''
    A prefix (typically the sign) can be added to the label.
    This should be implemented in child classes. Using standard value here.

    '''

    def __getIsDual(self):
        _log.warning('Using standard value for isDual')
        return False
    isDual = property(__getIsDual)
    '''
    This can be used to easily check if a k-cell belongs to the dual complex.
    This should be implemented in child classes. Using standard value here.

    '''

    def __getCategory(self):
        _log.warning('Using standard value for category')
        return 'NO_CATEGORY'
    category = property(__getCategory)
    '''
    The category of a k-cell can either be "inner", "border" or
    "additionalBorder".
    This should be implemented in child classes. Using standard value here.

    '''

    def __getCategoryText(self):
        _log.warning('Using standard value for categoryText')
        return 'NC'
    categoryText = property(__getCategoryText)
    '''
    The category is indicated in the label by a shortcut.
    This should be implemented in child classes. Using standard value here.

    '''

    def __getLabelSuffix(self):
        _log.warning('Using standard value for labelSuffix')
        return ''
    labelSuffix = property(__getLabelSuffix)
    '''
    A suffix can be added to the label. This is typically a letter indicating
    the simple k-cell used in a k-cell.
    This should be implemented in child classes. Using standard value here.

    '''

    def __getIsDeleted(self):
        _log.warning('Using standard value for isDeleted')
        return False
    isDeleted = property(__getIsDeleted)
    '''
    Instead of deleting an instance completely, the delete function is called
    on a k-cell that is not needed anymore. This makes it possible to keep
    track of deleted items.

    This should be implemented in child classes. Using standard value here.

    '''

    # =========================================================================
    #    MAGIC METHODS
    # =========================================================================

    def __neg__(self):
        '''
        Simply Use " - " sign to get the reversed kCell

        '''
        return self.__my_reverse

    def __repr__(self):
        '''
        Show infoText in console

        '''
        return self.info_text

    # =========================================================================
    #    METHODS
    # =========================================================================

    # --------------------------------------------------------------------
    #    Create info text
    # --------------------------------------------------------------------
    def __create_info_text(self):
        '''
        Parse the text that is displayed in the console. This should be called
        if the infoText is needed and has been changed since the last use.

        '''
        if self.isDual:
            label = self.label+'^'
        else:
            label = self.label
        self.__info_text = r'' + self.labelPrefix+label + '_' + \
            self.categoryText+str(self.num)+self.labelSuffix
        if self.isDeleted:
            self.__info_text = self.__info_text + '***deleted***'

        self.__info_text_changed = False
        _log.debug('Update infoText %s', self.__info_text)

    def __create_label_text(self):
        '''
        Parse the text that is displayed in the plot. This should be called
        if the label text is needed and has been changed since the last use.

        '''

        if self.isDual:
            label = r'\hat{'+self.label+'}'
        else:
            label = self.label

        if self.categoryText:
            categoryText = r'\mathrm{'+self.categoryText+'}'
        else:
            categoryText = ''

        self.__labelText = r'$' + self.labelPrefix+label + '_{'+categoryText \
            + str(self.num)+self.labelSuffix+'}$'
        self.__labelTextShort = r'$' + self.labelPrefix + label \
            + '_{'+categoryText + str(self.num)+'}$'
        self.__label_text_changed = False
        _log.debug('Update labelText {}'.format(self.__labelText))

    def updateText(self):
        '''
        Call this to update all texts if some part of it has changed in a child
        class.

        '''
        self.__label_text_changed = True
        self.__info_text_changed = True

    def tikZCoords(self, v, precission=3):
        '''
        Transform given coordinates from a vector into a string that is used
        in the TikZ plot.

        '''
        # Give a template for the format of the coordinate.
        # Example: '{:.3}'
        # In the later join function, the braces are replaced by the number
        coordFormat = r'{:.' + str(precission) + r'}'

        # Use join function to concatenate all coordinates in the wanted format
        return ','.join([coordFormat.format(x) for x in v])

    def checkIfDuplicates(self, listOfElems):
        '''
        Check if given list contains any duplicates

        '''
        setOfElems = set()
        for elem in listOfElems:
            if elem in setOfElems:
                return True
            else:
                setOfElems.add(elem)
        return False


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================
if __name__ == "__main__":

    set_logging_format(logging.DEBUG)

    test_supbc1 = SuperBaseCell()
    test_supbc2 = SuperBaseCell(my_reverse=test_supbc1)

    logging.debug("%s", test_supbc1)
    logging.debug("%s", test_supbc2)
    logging.debug("%s", -test_supbc1)
    logging.debug("%s", -test_supbc2)
