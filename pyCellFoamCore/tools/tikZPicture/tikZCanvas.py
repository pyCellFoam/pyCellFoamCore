# -*- coding: utf-8 -*-
#==============================================================================
# TIKZ CANVAS
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue Feb 11 15:50:58 2020

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
from pyCellFoamCore.tools.tikZPicture.tikZEnvironment import TikZEnvironment


#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class TikZCanvas(TikZEnvironment):
    '''

    '''

#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__center',
                 '__directionVecX',
                 '__directionVecY',
                 '__tikZPicture3D')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,center,directionVecX,directionVecY,tikZPicture3D):
        '''

        '''
        super().__init__()
        self.__center = center
        self.__directionVecX = directionVecX
        self.__directionVecY = directionVecY
        self.__tikZPicture3D = tikZPicture3D
        self.tikZPrefix = '\t'
        self.logger.info('Created TikZCanvas')



#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getCenter(self): return self.__center
    center = property(__getCenter)

    def __getDirectionVecX(self): return self.__directionVecX
    directionVecX = property(__getDirectionVecX)

    def __getDirectionVecY(self): return self.__directionVecY
    directionVecY = property(__getDirectionVecY)




    def __getEnvironmentName(self): return 'scope'
    environmentName = property(__getEnvironmentName)

    def __getTikZText(self):
        text = self.tikZPrefix + '\\begin{{scope}}[canvas is plane={{O({})x({})y({})}}]\n'.format(self.numpy2TikZ(self.center),self.numpy2TikZ(self.directionVecX+self.center),self.numpy2TikZ(self.directionVecY+self.center))
        text += super().tikZText
        text += self.tikZPrefix + '\\end{scope}\n'
        return text
    tikZText = property(__getTikZText)



    def __getTikZPrefix(self): return self.__tikZPicture3D.tikZPrefix + super().tikZPrefix
    def __setTikZPrefix(self,t): TikZEnvironment.tikZPrefix.fset(self,t)
    tikZPrefix = property(__getTikZPrefix,__setTikZPrefix)


#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    import logging

    from tools import MyLogging
    from tools.tikZPicture.tikZPicture3D import TikZPicture3D

    with MyLogging('TikZPicture3D',shLevel=logging.WARNING):
        cc.printBlue('Create picture')
        pic = TikZPicture3D(scale=2)

        cc.printBlue('Create canvas')


        n1 = pic.addTikZNode('n1',np.array([0,0,0]),options=['inner sep = 0pt','fill=TUMOrange','circle','minimum size = 3mm'])
        cosy1 = pic.addTikZCoSy3D(n1)


        canv1 = pic.addTikZCanvas(center = np.array([3,0,0]),
                          directionVecX = np.array([0,1,0]),
                          directionVecY = np.array([0,0,1]))

        n2 = canv1.addTikZNode('n2',np.array([0,0]),options=['inner sep = 0pt','fill=TUMOrange','circle','minimum size = 3mm'])
        cosy2 = canv1.addTikZCoSy2D(n2)
        canv1.addTikZCircledArrow(n2,1,['TUMBlue',])


        canv2 = pic.addTikZCanvas(center = np.array([2,0,0]),
                          directionVecX = np.array([np.sqrt(2)/2,np.sqrt(2)/2,0]),
                          directionVecY = np.array([-np.sqrt(2)/2,np.sqrt(2)/2,0]))

        n3 = canv2.addTikZNode('n3',np.array([0,0]),options=['inner sep = 0pt','fill=TUMOrange','circle','minimum size = 3mm'])
        cosy3 = canv2.addTikZCoSy2D(n3)
        canv2.addTikZCircledArrow(n3,1,['TUMBlue',])






        cc.printGreen('CoSys in picture:')
        cc.printYellow(pic.tikZCoSys)



        pic.writeLaTeXFile('latex','tikZCanvas',compileFile=True,openFile=True)
