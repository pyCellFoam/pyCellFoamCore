# -*- coding: utf-8 -*-
#==============================================================================
# TIKZ COSY 3D
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Feb  7 11:52:47 2020

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

class TikZCoSy3D(TikZCoSy):
    '''
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__tikZNodeX',
                 '__tikZNodeY',
                 '__tikZNodeZ')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,*args,addLabels=False,**kwargs):
        '''
        
        '''
        super().__init__(*args,**kwargs)
        
        nodeNameBase = 'CoSy'+str(self.num)
        self.__tikZNodeX = self.tikZEnvironment.addTikZNode(coordinates = self.center.coordinates+np.array([self.arrowLength,0,0]),
                                                        name = nodeNameBase+'X',
                                                        options = ['label = {[TUMOrange] below: $x$}',])
        
        self.__tikZNodeY = self.tikZEnvironment.addTikZNode(coordinates = self.center.coordinates+np.array([0,self.arrowLength,0]),
                                                        name = nodeNameBase+'Y',
                                                        options = ['label = {[TUMGreen] above: $y$}',])
        
        self.__tikZNodeZ = self.tikZEnvironment.addTikZNode(coordinates = self.center.coordinates+np.array([0,0,self.arrowLength]),
                                                        name = nodeNameBase+'Z',
                                                        options = ['label = {[TUMBlue] below: $z$}',])        
        
        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getTikZText(self):
        return self.tikZPrefix + '\\CoSyThreeD{}{{{}}}\n'.format(self.arrowLengthText,self.center.name)
    tikZText = property(__getTikZText)        
    
    
    
    def __getShowCoordinateLabels(self):
        return (self.__tikZNodeX.show,self.__tikZNodeY.show,self.__tikZNodeZ.show)
    def __setShowCoordinateLabels(self,s):
        self.__tikZNodeX.show = s
        self.__tikZNodeY.show = s
        self.__tikZNodeZ.show = s
    showCoordinateLabels = property(__getShowCoordinateLabels,__setShowCoordinateLabels)
        
            

    
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    import logging
    
    from tools import MyLogging
    from tools.tikZPicture.tikZPicture3D import TikZPicture3D
    
    with MyLogging('TikZCircledArrow',shLevel=logging.DEBUG):
        cc.printBlue('Create TikZPicture')
        tikzpic3D = TikZPicture3D()
        
        cc.printBlue('Add coordinate')
        c1 = tikzpic3D.addTikZCoordinate('c1',np.array([0,0,0]))
        
        cc.printBlue('Add coordinate system')
        cosy1 = tikzpic3D.addTikZCoSy3D(c1,arrowLength=5)
        
        cc.printBlue('Add another coordinate')
        c2 = tikzpic3D.addTikZCoordinate('c2',np.array([8,2,3]))
        
        cc.printBlue('Add another coordinate system')
        cosy2 = tikzpic3D.addTikZCoSy3D(c2,arrowLength=1)
        
        cc.printBlue('Disable plotting of axis labels for first coordinate system')
        cosy1.showCoordinateLabels = False
    
        cc.printBlue('Create LaTeX file')
        tikzpic3D.writeLaTeXFile('latex','TikZCoSy3D',compileFile=True,openFile=True)
