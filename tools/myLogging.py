# -*- coding: utf-8 -*-
#==============================================================================
# MY LOGGING
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri May  4 15:15:59 2018

'''
Creates a logger with two handlers, one that prints to the console and one that
prints to a given file.

'''
#==============================================================================
#    IMPORTS
#==============================================================================

import os
if __name__== '__main__':
    os.chdir('../')

import logging

error = logging.ERROR
debug = logging.DEBUG
warning = logging.WARNING
info = logging.INFO


#==============================================================================
#    CLASS DEFINITION
#==============================================================================
class MyLogging:
    '''
    
    '''
    
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__logger',
                 '__fh',
                 '__sh')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,filename,debug=False,fhLevel=info,shLevel=warning):
        '''
        
        
        '''
        # create logger
        self.__logger = logging.getLogger('log')
        self.__logger.setLevel(logging.DEBUG)
        
        if not os.path.isdir('log'):
            os.mkdir('log')
        
        
        # determine location to save the logfile
        path = 'log/'+filename+'.log'
        
        # create file handler which logs even debug messages
        self.__fh = logging.FileHandler(path, mode='w')
        if debug:
            self.__fh.setLevel(logging.DEBUG)
        else:
            self.__fh.setLevel(fhLevel)
            
        
        # create console handler with a higher log level
        self.__sh = logging.StreamHandler()
        if debug:
            self.__sh.setLevel(logging.DEBUG)
        else:
            self.__sh.setLevel(shLevel)
            
        
        # create formatter and add it to the handlers
        formatterFile = logging.Formatter('[%(asctime)s] %(levelname)8s : %(module)16s : %(lineno)5s : %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        
        formatterConsole = logging.Formatter('%(levelname)8s : %(module)18s : %(lineno)5s : %(message)s')
        
        self.__fh.setFormatter(formatterFile)
        self.__sh.setFormatter(formatterConsole)
        
        # add the handlers to the logger
        self.__logger.addHandler(self.__sh)
        self.__logger.addHandler(self.__fh)
        

#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getLogger(self): return self.__logger
    logger = property(__getLogger)
    '''
    
    '''
       
        
#==============================================================================
#    MAGIC METHODS
#==============================================================================
#-------------------------------------------------------------------------
#    Enter
#-------------------------------------------------------------------------
    def __enter__(self):
        '''
        
        '''
        return self
    
#-------------------------------------------------------------------------
#    Exit
#-------------------------------------------------------------------------
    
    def __exit__(self, exc_type, exc_value, traceback):
        '''
        
        '''
        self.__fh.close()
        self.__logger.removeHandler(self.__sh)
        self.__logger.removeHandler(self.__fh)

#==============================================================================
#    METHODS
#==============================================================================
        

#==============================================================================
#    FUNCTIONS
#==============================================================================
def getLogger(name):
    '''
    
    
    '''
    logger = logging.getLogger('log.'+name)
    if not logger.parent.handlers:
        logging.basicConfig(
            level = logging.INFO,
            style = '%',
            format = 'BASIC LOGGER: %(levelname)8s : %(module)18s : %(lineno)5s : %(message)s')
    else:
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
    return logger


def setStreamLevel(logger,level=logging.WARNING):
    '''
    
    '''
    logger.parent.handlers[0].setLevel(level)

        

#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    logger = getLogger(__name__)
    logger.error('This is an error')
    logger.warning('This is a warning')
    logger.info('This is an information')
    logger.debug('This is only for debugging')
    with MyLogging('MyLogging1'):
        logger = getLogger(__name__)
        logger.error('This is an error')
        logger.warning('This is a warning')
        logger.info('This is an information')
        logger.debug('This is only for debugging')
    with MyLogging('MyLogging2',True):
        logger = getLogger(__name__)
        logger.error('This is an error')
        logger.warning('This is a warning')
        logger.info('This is an information')
        logger.debug('This is only for debugging')
        
        
        
    with MyLogging('MyLogging3'):
        logger = getLogger('Test')
        logger.debug('Hello 1')
        logger.parent.handlers[0].setLevel(logging.DEBUG)
        logger.debug('Hello 2')
        logger.parent.handlers[0].setLevel(logging.WARNING)
        logger.debug('Hello 3')

    
