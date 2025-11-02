# -*- coding: utf-8 -*-
#==============================================================================
# BOUNDING BOX ELEMENT
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Mon Feb 24 11:18:53 2020

'''


'''
#==============================================================================
#    IMPORTS
#==============================================================================
import os
if __name__ == '__main__':
    os.chdir('../')

import logging

#==============================================================================
#    LOGGING
#==============================================================================

_log = logging.getLogger(__name__)

#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class BoundingBoxElement:
    '''


    '''

#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__logger',
                 '__identifier')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,identifier,loggerName):
        '''
        :param str identifier: A name for the element
        :param str loggerName: A name for the logger instance

        '''
        self.__identifier = identifier
        _log.info('Created BoundingBoxElement')




#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getLogger(self): return self.__logger
    logger = property(__getLogger)
    '''

    '''

    def __getIdentifier(self): return self.__identifier
    identifier = property(__getIdentifier)
    '''

    '''


#==============================================================================
#    MAGIC METHODS
#==============================================================================

    def  __repr__(self):
        '''
        Show infoText in console

        '''
        return self.identifier





#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    from tools import MyLogging
    import tools.colorConsole as cc
    with MyLogging('BoundingBoxCorner',debug=True):
        cc.printBlue('Create bbElement')
        ele = BoundingBoxElement('testElement',__name__)
        cc.printBlue('Check resulut')
        print(ele)

