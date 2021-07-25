# -*- coding: utf-8 -*-
#==============================================================================
# TIKZ CIRCLED ARROW
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Feb 14 11:41:57 2020

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

class TikZCircledArrow(TikZElement):
    '''
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__center',
                 '__radius',
                 '__options')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,center,radius,options = [],**kwargs):
        '''
        
        '''
        super().__init__(**kwargs)
        
        self.__center = center
        self.__radius = radius
        self.__options = options
        
        self.logger.info('Created TikZCircledArrow')
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
        
    def __getOptionsText(self):
        if self.options:
            return '[' + ','.join(self.options) + ']'
        else:
            return ''
        
    optionsText = property(__getOptionsText)
    
    def __getTikZText(self):
        return self.tikZPrefix + '\\circledarrow{}{{{}}}{{{}}}\n'.format(self.optionsText,self.center.name,self.radius)
    tikZText = property(__getTikZText)

    def __getCenter(self): return self.__center
    def __setCenter(self,c): self.__center = c
    center = property(__getCenter,__setCenter)

    def __getRadius(self): return self.__radius
    def __setRadius(self,r): self.__radius = r
    radius = property(__getRadius,__setRadius)

    def __getOptions(self): return self.__options
    def __setOptions(self,o): self.__options = o
    options = property(__getOptions,__setOptions)



    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    
    import logging
    
    from tools import MyLogging
    from tools.tikZPicture.tikZPicture2D import TikZPicture2D
    
    with MyLogging('TikZCircledArrow',shLevel=logging.DEBUG):
        
        cc.printBlue('Create picture')
        tikzpic2D = TikZPicture2D()
        
        cc.printBlue('Add node')
        n1 = tikzpic2D.addTikZNode('n1',np.array([0,0]),options=['inner sep = 0pt','fill=TUMOrange','circle','minimum size = 3mm'])  
        
        
        cc.printBlue('Add circled arrow')
        tikzpic2D.addTikZCircledArrow(center = n1,
                                      radius = 2,
                                      options = ['TUMBlue',])
        
        tikzpic2D.addTikZCircledArrow(n1,3)
        
        
        cc.printBlue('Create LaTeX file')
        tikzpic2D.writeLaTeXFile('latex','TikZCircledArrow',compileFile=True,openFile=True)
        

