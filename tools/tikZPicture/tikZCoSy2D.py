# -*- coding: utf-8 -*-
#==============================================================================
# TIKZ COSY 2D
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Mon Feb 10 16:48:03 2020

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
from tools.tikZPicture.tikZCoSy import TikZCoSy

#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class TikZCoSy2D(TikZCoSy):
    '''
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__tikZNodeX',
                 '__tikZNodeY')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,*args,**kwargs):
        '''
        
        '''
        super().__init__(*args,**kwargs)
        
        nodeNameBase = 'CoSy'+str(self.num)
        self.__tikZNodeX = self.tikZEnvironment.addTikZNode(coordinates = self.center.coordinates+np.array([self.arrowLength,0]),
                                                        name = nodeNameBase+'X',
                                                        options = ['label = {[TUMOrange] below: $x$}',])
        
        self.__tikZNodeY = self.tikZEnvironment.addTikZNode(coordinates = self.center.coordinates+np.array([0,self.arrowLength]),
                                                        name = nodeNameBase+'Y',
                                                        options = ['label = {[TUMGreen] above: $y$}',])
        
        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
        
    def __getTikZText(self):
        return self.tikZPrefix + '\\CoSyTwoD{}{{{}}}\n'.format(self.arrowLengthText,self.center.name)
    tikZText = property(__getTikZText)

    
    def __getShowCoordinateLabels(self):
        return (self.__tikZNodeX.show,self.__tikZNodeY.show)
    def __setShowCoordinateLabels(self,s):
        self.__tikZNodeX.show = s
        self.__tikZNodeY.show = s
    showCoordinateLabels = property(__getShowCoordinateLabels,__setShowCoordinateLabels)    
    
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    import logging
    
    from tools import MyLogging
    from tools.tikZPicture.tikZPicture2D import TikZPicture2D
    
    with MyLogging('TikZCircledArrow',shLevel=logging.DEBUG):
        cc.printBlue('Create TikZPicture')
        pic = TikZPicture2D()
        
        cc.printBlue('Add coordinate')
        c1 = pic.addTikZCoordinate('c1',np.array([0,0]))
        
        cc.printBlue('Add coordinate system')
        cosy1 = pic.addTikZCoSy2D(c1,arrowLength=5)
        
        cc.printBlue('Add another coordinate')
        c2 = pic.addTikZCoordinate('c2',np.array([8,2]))
        
        cc.printBlue('Add another coordinate system')
        cosy2 = pic.addTikZCoSy2D(c2,arrowLength=1)
#        
        
        cc.printBlue('Disable plotting of axis labels for first coordinate system')
        cosy1.showCoordinateLabels = True
#    
        cc.printBlue('Create LaTeX file')
        pic.writeLaTeXFile('latex','TikZCoSy2D',compileFile=True,openFile=True)
#

