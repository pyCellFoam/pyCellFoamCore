# -*- coding: utf-8 -*-
#==============================================================================
# TIKZ PERSPECTIVE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Feb 13 15:26:17 2020

'''

'''
#==============================================================================
#    IMPORTS
#==============================================================================
import os
if __name__ == '__main__':
    os.chdir('../../')

import numpy as np

import pyCellFoamCore.tools.colorConsole as cc
from pyCellFoamCore.tools.tikZPicture.tikZElement import TikZElement

#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class TikZPerspective(TikZElement):
    '''
    This is the explanation of this class.

    '''
#==============================================================================
#    CLASS VARIABLES
#==============================================================================
    allNames = []

#==============================================================================
#    RESET NAMES
#==============================================================================
    @classmethod
    def resetNames(cls):
       TikZPerspective.allNames = []

#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__projectionX',
                 '__projectionY',
                 '__projectionZ',
                 '__name')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,name,projectionX=np.array([1,0]),projectionY=np.array([0,1]),projectionZ=np.array([-np.sqrt(2)/2,-np.sqrt(2)/2])):
        '''

        '''
        super().__init__([])
        self.__name = name
        if self.__name in TikZPerspective.allNames:
            self.logger.error('Name "{}" of the TikZPerspective is already in use'.format(name))
        else:
            TikZPerspective.allNames.append(name)
        self.__projectionX = projectionX
        self.__projectionY = projectionY
        self.__projectionZ = projectionZ
        self.logger.info('Created TikZPerspective')




#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getName(self): return self.__name
    name = property(__getName)

    def __getProjectionX(self): return self.__projectionX
    def __setProjectionX(self,p): self.__projectionX = p
    projectionX = property(__getProjectionX,__setProjectionX)

    def __getProjectionY(self): return self.__projectionY
    def __setProjectionY(self,p): self.__projectionY = p
    projectionY = property(__getProjectionY,__setProjectionY)

    def __getProjectionZ(self): return self.__projectionZ
    def __setProjectionZ(self,p): self.__projectionZ = p
    projectionZ = property(__getProjectionZ,__setProjectionZ)


    def __getTikzset(self):
        text = '\t{}/.style = {{\n'.format(self.name)
        text += '\t\tx = {{({}cm, {}cm)}},\n'.format(self.projectionX[0],self.projectionX[1])
        text += '\t\ty = {{({}cm, {}cm)}},\n'.format(self.projectionY[0],self.projectionY[1])
        text += '\t\tz = {{({}cm, {}cm)}}\n'.format(self.projectionZ[0],self.projectionZ[1])
        text += '\t}'
        return text

    tikzset = property(__getTikzset)




#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    import logging

    from tools import MyLogging
    from tools.tikZPicture.tikZPicture3D import TikZPicture3D

    with MyLogging('TikZPerspective',shLevel=logging.DEBUG):
        cc.printBlue('Create perspective')
        TikZPerspective.resetNames()
        perspective = TikZPerspective('bla',
                                      np.array([-0.9,0.3]),
                                      np.array([-0.8,-0.4]),
                                      np.array([0,1]))

        cc.printBlue('Create picture')
        pic = TikZPicture3D(perspective,scale=2)

        cc.printBlue('Create node')
        n1 = pic.addTikZNode('n1',np.array([0,0,0]),'A',options=['draw','circle'])

        cc.printBlue('Create coordinate system')
        pic.addTikZCoSy3D(n1)

        cc.printBlue('Create LaTeX file')
        # pic.writeLaTeXFile('latex','tikZPerspective',compileFile=True,openFile=True)
