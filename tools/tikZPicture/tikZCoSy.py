# -*- coding: utf-8 -*-
#==============================================================================
# TIKZ COSY
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Feb  5 15:03:21 2020

'''
'''
#==============================================================================
#    IMPORTS
#==============================================================================
import os
if __name__ == '__main__':
    os.chdir('../../')
import numpy as np
import tools.colorConsole as cc
from tools.tikZPicture.tikZElement import TikZElement

#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class TikZCoSy(TikZElement):
    '''
    
    '''
    
#==============================================================================
#    CLASS VARIABLES
#==============================================================================
    totalNumCoSy = 0
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__center',
                 '__arrowLength',
                 '__num')


#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,center,arrowLength=1,**kwargs):
        '''
        
        '''
        super().__init__(**kwargs)
        self.__center = center
        self.__arrowLength = arrowLength
        self.__num = TikZCoSy.totalNumCoSy
        TikZCoSy.totalNumCoSy += 1
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getCenter(self): return self.__center
    def __setCenter(self,c): self.__center = c
    center = property(__getCenter,__setCenter)

    def __getArrowLength(self): return self.__arrowLength
    def __setArrowLength(self,a): self.__arrowLength = a
    arrowLength = property(__getArrowLength,__setArrowLength)
    
    
    def __getArrowLengthText(self): 
        if self.arrowLength == 1:
            return ''
        else:
            return '[{}]'.format(self.arrowLength)
    arrowLengthText = property(__getArrowLengthText)
    
    
    def __getNum(self): return self.__num
    num = property(__getNum)



    
#==============================================================================
#    METHODS
#==============================================================================
    
#-------------------------------------------------------------------------
#    Print
#-------------------------------------------------------------------------
    
    def printTikZCoSy(self):
        print('Coordinate system at {} with arrow length {}'.format(self.center,self.arrowLength))

#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    
    import logging
    
    from tools import MyLogging
    from tools.tikZPicture.tikZPicture3D import TikZPicture3D
    
    with MyLogging('TikZCircledArrow',shLevel=logging.DEBUG):    
    
        tikzpic3D = TikZPicture3D()
        c1 = tikzpic3D.addTikZCoordinate('c1',np.array([0,0,0]))
        cosy = TikZCoSy(c1,tikZEnvironment = tikzpic3D)
        cosy.printTikZCoSy()
        
        
    
