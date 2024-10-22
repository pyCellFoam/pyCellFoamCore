# -*- coding: utf-8 -*-
#==============================================================================
# TIKZ ELEMENT
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Feb  7 16:11:44 2020

'''


'''
#==============================================================================
#    IMPORTS
#==============================================================================
import os
if __name__ == '__main__':
    os.chdir('../../')
import tools.myLogging as ml
import tools.colorConsole as cc

#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class TikZElement:
    '''

    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__tikZEnvironment',
                 '__logger',                 
                 '__show',
                 '__tikZPrefix')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,tikZEnvironment):
        '''
        
        '''
        self.__logger = ml.getLogger(__name__)
        self.__tikZEnvironment = tikZEnvironment
        self.__show = True
        self.__tikZPrefix = '\t'
        self.__logger.info('Created TikZElement')        
        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getLogger(self): return self.__logger
    logger = property(__getLogger)

    def __getTikZEnvironment(self): return self.__tikZEnvironment
    tikZEnvironment = property(__getTikZEnvironment)


    
    def __getShow(self): return self.__show
    def __setShow(self,s): self.__show = s
    show = property(__getShow,__setShow)


    def __getTikZPrefix(self): return self.tikZEnvironment.tikZPrefix + self.__tikZPrefix
    def __setTikZPrefix(self,t): self.__tikZPrefix = t
    tikZPrefix = property(__getTikZPrefix,__setTikZPrefix)
    
    
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    
    import logging
    from tools.tikZPicture.tikZEnvironment import TikZEnvironment
    
    with ml.MyLogging('TikZElement',shLevel=logging.DEBUG):
        cc.printBlue('Create an environment')
        env = TikZEnvironment()
        
        cc.printBlue('Create an element')
        element = TikZElement(env)

