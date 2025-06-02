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

#    Tools
# -------------------------------------------------------------------

import tools.myLogging as myLogging
from tools.logging_formatter import set_logging_format

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

# =============================================================================
#    CLASS VARIABLES
# =============================================================================

    allCells = []

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self,
                 *args,
                 myReverse=None,
                 loggerName='MISSING_LOGGER_NAME',
                 **kwargs):
        '''


        :param SuperBaseCell myReverse:
        :param str loggerName: The logger name needs to be passed from the
            class at the lowest level by loggerName = __name__

        '''
        # Check if a loger name was passed to this class from child classes
        if loggerName == 'MISSING_LOGGER_NAME':
            self.__logger = _log
            self.logger.warning('Logger name is not set')
        
        else:
            # Create logger
            self.__logger = myLogging.getLogger(loggerName)
        

        self.__myReverse = myReverse

        # prepare text changed variables
        self.__labelTextChanged = True
        self.__infoTextChanged = True


        # Check if there are any non-used positional arguments
        if args:
            self.logger.warning('Unused positional arguments {} were passed'
                                .format(args))

        if kwargs:
            self.logger.warning('Unused keyword arguments {} were passed'
                                .format(kwargs))

        if self in SuperBaseCell.allCells:
            self.logger.error('Multiple call of SuperBaseCell for {}'
                              .format(self.infoText))
        else:
            SuperBaseCell.allCells.append(self)

        self.logger.debug('Initialized SuperBaseCell')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getLogger(self): return self.__logger
    logger = property(__getLogger)
    '''
    Logger from the logging package to keep track of everything.

    '''

    def __getInfoText(self):
        if self.__infoTextChanged:
            self.__createInfoText()
        return self.__infoText
    infoText = property(__getInfoText)
    '''
    This text is used to be displayed in the console to identify the cell in a
    readable way.

    '''

    def __getLabelText(self):
        if self.__labelTextChanged:
            self.__createLabelText()
        return self.__labelText
    labelText = property(__getLabelText)
    '''
    This text ist used in plots.

    '''

    def __getLabelTextShort(self):
        if self.__labelTextChanged:
            self.__createLabelText()
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

    def __getMyReverse(self): return self.__myReverse
    myReverse = property(__getMyReverse)
    '''
    Returns the reverse of this cell, can also be accesed by using the - symbol

    '''

    def __getLabelTextChanged(self): return self.__labelTextChanged
    labelTextChanged = property(__getLabelTextChanged)
    '''
    This is set to true if some element of the the label text has changed since
    the last time that the text was compiled.

    '''

    def __getInfoTextChanged(self): return self.__infoTextChanged
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

# ------------------------------------------------------------------------
#    Standard values for properties that will be defined in child classes
#    but that are needed for methods in this class
# ------------------------------------------------------------------------

    def __getLabel(self):
        self.logger.warning('Using standard value for label')
        return 'SUPBC'
    label = property(__getLabel)
    '''
    The label is typically just one letter describing the type of the k-cell.
    This should be implemented in child classes. Using standard value here.

    '''

    def __getNum(self):
        self.logger.warning('Using standard value for num')
        return -1
    num = property(__getNum)

    '''
    The k-cells need to be numbered.
    This should be implemented in child classes. Using standard value here.

    '''

    def __getLabelPrefix(self):
        self.logger.warning('Using standard value for labelPrefix')
        return 'x'
    labelPrefix = property(__getLabelPrefix)
    '''
    A prefix (typically the sign) can be added to the label.
    This should be implemented in child classes. Using standard value here.

    '''

    def __getIsDual(self):
        self.logger.warning('Using standard value for isDual')
        return False
    isDual = property(__getIsDual)
    '''
    This can be used to easily check if a k-cell belongs to the dual complex.
    This should be implemented in child classes. Using standard value here.

    '''

    def __getCategory(self):
        self.logger.warning('Using standard value for category')
        return 'NO_CATEGORY'
    category = property(__getCategory)
    '''
    The category of a k-cell can either be "inner", "border" or
    "additionalBorder".
    This should be implemented in child classes. Using standard value here.

    '''

    def __getCategoryText(self):
        self.logger.warning('Using standard value for categoryText')
        return 'NC'
    categoryText = property(__getCategoryText)
    '''
    The category is indicated in the label by a shortcut.
    This should be implemented in child classes. Using standard value here.

    '''

    def __getLabelSuffix(self):
        self.logger.warning('Using standard value for labelSuffix')
        return ''
    labelSuffix = property(__getLabelSuffix)
    '''
    A suffix can be added to the label. This is typically a letter indicating
    the simple k-cell used in a k-cell.
    This should be implemented in child classes. Using standard value here.

    '''

    def __getIsDeleted(self):
        self.logger.warning('Using standard value for isDeleted')
        return False
    isDeleted = property(__getIsDeleted)
    '''
    Instead of deleting an instance completely, the delete function is called
    on a k-cell that is not needed anymore. This makes it possible to keep
    track of deleted items.

    This should be implemented in child classes. Using standard value here.

    '''

# =============================================================================
#    MAGIC METHODS
# =============================================================================

    def __neg__(self):
        '''
        Simply Use " - " sign to get the reversed kCell

        '''
        return self.__myReverse

    def __repr__(self):
        '''
        Show infoText in console

        '''
        return self.infoText

# =============================================================================
#    METHODS
# =============================================================================

# ------------------------------------------------------------------------
#    Create info text
# ------------------------------------------------------------------------
    def __createInfoText(self):
        '''
        Parse the text that is displayed in the console. This should be called
        if the infoText is needed and has been changed since the last use.

        '''
        if self.isDual:
            label = self.label+'^'
        else:
            label = self.label
        self.__infoText = r'' + self.labelPrefix+label + '_' + \
                          self.categoryText+str(self.num)+self.labelSuffix
        if self.isDeleted:
            self.__infoText = self.__infoText + '***deleted***'

        self.__infoTextChanged = False
        self.logger.debug('Update infoText {}'.format(self.__infoText))

    def __createLabelText(self):
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
        self.__labelTextChanged = False
        self.logger.debug('Update labelText {}'.format(self.__labelText))

    def updateText(self):
        '''
        Call this to update all texts if some part of it has changed in a child
        class.

        '''
        self.__labelTextChanged = True
        self.__infoTextChanged = True

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
    test_supbc2 = SuperBaseCell(myReverse=test_supbc1)
    
    logging.debug("%s", test_supbc1)
    logging.debug("%s", test_supbc2)
    logging.debug("%s", -test_supbc1)
    logging.debug("%s", -test_supbc2)
