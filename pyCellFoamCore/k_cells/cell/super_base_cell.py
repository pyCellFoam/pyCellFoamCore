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

from pyCellFoamCore.tools import set_logging_format

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
        self.__label_text = ''
        self.__label_text_short = ''
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
            _log.critical(
                'Unused keyword arguments %s were passed',
                list(kwargs.keys()),
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

    def __get_label_text(self):
        if self.__label_text_changed:
            self.__create_label_text()
        return self.__label_text
    label_text = property(__get_label_text)
    '''
    This text ist used in plots.

    '''

    def __get_label_text_short(self):
        if self.__label_text_changed:
            self.__create_label_text()
        return self.__label_text_short
    label_text_short = property(__get_label_text_short)
    '''
    Short version of the label text, mostly for TikZ export

    '''

    def __get_tikz_name(self):
        name = self.label.replace('\\', '') \
            + self.category_text + str(self.num) \
            + str(self.label_suffix.replace('(', '').replace(')', ''))
        if self.is_dual:
            name = 'd' + name
        name = name.replace(',', '_')
        return name
    tikz_name = property(__get_tikz_name)
    '''
    Name of the k-cell in the TikZ-plot.

    '''

    def __get_my_reverse(self):
        return self.__my_reverse
    my_reverse = property(__get_my_reverse)
    '''
    Returns the reverse of this cell, can also be accesed by using the - symbol

    '''

    def __get_label_text_changed(self):
        return self.__label_text_changed
    label_text_changed = property(__get_label_text_changed)
    '''
    This is set to true if some element of the the label text has changed since
    the last time that the text was compiled.

    '''

    def __get_info_text_changed(self):
        return self.__info_text_changed
    info_text_changed = property(__get_info_text_changed)
    '''
    This is set to true if some element of the the info text has changed since
    the last time that the text was compiled.

    '''

    def __get_tolerance(self):
        return 1E-4
    tolerance = property(__get_tolerance)
    '''
    Tolerance used to check for parallelity and perpendicularity.

    '''

    # --------------------------------------------------------------------
    #    Standard values for properties that will be defined in child classes
    #    but that are needed for methods in this class
    # --------------------------------------------------------------------

    def __get_label(self):
        _log.warning('Using standard value for label')
        return 'SUPBC'
    label = property(__get_label)
    '''
    The label is typically just one letter describing the type of the k-cell.
    This should be implemented in child classes. Using standard value here.

    '''

    def __get_num(self):
        _log.warning('Using standard value for num')
        return -1
    num = property(__get_num)

    '''
    The k-cells need to be numbered.
    This should be implemented in child classes. Using standard value here.

    '''

    def __get_label_prefix(self):
        _log.warning('Using standard value for labelPrefix')
        return 'x'
    label_prefix = property(__get_label_prefix)
    '''
    A prefix (typically the sign) can be added to the label.
    This should be implemented in child classes. Using standard value here.

    '''

    def __get_is_dual(self):
        _log.warning('Using standard value for isDual')
        return False
    is_dual = property(__get_is_dual)
    '''
    This can be used to easily check if a k-cell belongs to the dual complex.
    This should be implemented in child classes. Using standard value here.

    '''

    def __get_category(self):
        _log.warning('Using standard value for category')
        return 'NO_CATEGORY'
    category = property(__get_category)
    '''
    The category of a k-cell can either be "inner", "border" or
    "additionalBorder".
    This should be implemented in child classes. Using standard value here.

    '''

    def __get_category_text(self):
        _log.warning('Using standard value for categoryText')
        return 'NC'
    category_text = property(__get_category_text)
    '''
    The category is indicated in the label by a shortcut.
    This should be implemented in child classes. Using standard value here.

    '''

    def __get_label_suffix(self):
        _log.warning('Using standard value for label_suffix')
        return ''
    label_suffix = property(__get_label_suffix)
    '''
    A suffix can be added to the label. This is typically a letter indicating
    the simple k-cell used in a k-cell.
    This should be implemented in child classes. Using standard value here.

    '''

    def __get_is_deleted(self):
        _log.warning('Using standard value for isDeleted')
        return False
    is_deleted = property(__get_is_deleted)
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
        if self.is_dual:
            label = self.label+'^'
        else:
            label = self.label
        self.__info_text = r'' + self.label_prefix+label + '_' + \
            self.category_text+str(self.num)+self.label_suffix
        if self.is_deleted:
            self.__info_text = self.__info_text + '***deleted***'

        self.__info_text_changed = False
        _log.debug('Update infoText %s', self.__info_text)

    def __create_label_text(self):
        '''
        Parse the text that is displayed in the plot. This should be called
        if the label text is needed and has been changed since the last use.

        '''

        if self.is_dual:
            label = r'\hat{'+self.label+'}'
        else:
            label = self.label

        if self.category_text:
            category_text = r'\mathrm{'+self.category_text+'}'
        else:
            category_text = ''

        self.__label_text = r'$' + self.label_prefix+label \
            + '_{'+category_text \
            + str(self.num)+self.label_suffix+'}$'
        self.__label_text_short = r'$' + self.label_prefix + label \
            + '_{'+category_text + str(self.num)+'}$'
        self.__label_text_changed = False
        _log.debug('Update labelText %s', self.__label_text)

    def update_text(self):
        '''
        Call this to update all texts if some part of it has changed in a child
        class.

        '''
        self.__label_text_changed = True
        self.__info_text_changed = True

    def tikz_coords(self, v, precission=3):
        '''
        Transform given coordinates from a vector into a string that is used
        in the TikZ plot.

        '''
        # Give a template for the format of the coordinate.
        # Example: '{:.3}'
        # In the later join function, the braces are replaced by the number
        coord_format = r'{:.' + str(precission) + r'}'

        # Use join function to concatenate all coordinates in the wanted format
        return ','.join([coord_format.format(x) for x in v])

    def check_if_duplicates(self, list_of_elems):
        '''
        Check if given list contains any duplicates

        '''
        set_of_elems = set()
        for elem in list_of_elems:
            if elem in set_of_elems:
                return True
            set_of_elems.add(elem)
        return False


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================
if __name__ == "__main__":

    set_logging_format(logging.DEBUG)

    test_supbc1 = SuperBaseCell(bla='blub')
    test_supbc2 = SuperBaseCell(my_reverse=test_supbc1)

    logging.debug("%s", test_supbc1)
    logging.debug("%s", test_supbc2)
    logging.debug("%s", -test_supbc1)
    logging.debug("%s", -test_supbc2)
