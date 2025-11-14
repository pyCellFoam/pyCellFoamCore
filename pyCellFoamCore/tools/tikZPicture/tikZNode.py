# -*- coding: utf-8 -*-
#==============================================================================
# TIKZ NODE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue Feb  4 15:20:20 2020

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
from pyCellFoamCore.tools.tikZPicture.tikZCoordinate import TikZCoordinate

#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class TikZNode(TikZCoordinate):
    '''

    '''

#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__content',
                 '__options')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,name,coordinates,content='',options=None,**kwargs):
        '''

        '''
        super().__init__(name,coordinates,**kwargs)
        self.__content = content
        self.__options = options
        self.logger.info('Created TikZNode')




#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getTikZText(self):
        if self.show:
            if self.__options is None:
                optionsText = ''
            else:
                optionsText = '['+','.join(self.__options)+']'
            return self.tikZPrefix + '\\node{} ({}) at ({}){{{}}};\n'.format(optionsText,self.name,self.coordinatesTikZ,self.__content)
        else:
            return ''
    tikZText = property(__getTikZText)

#==============================================================================
#    MAGIC METHODS
#==============================================================================
    def  __repr__(self):
        '''
        Show infoText in console

        '''
        return 'TikZNode ({}) at ({}) {{{}}}'.format(self.name,self.coordinatesTikZ,self.__content)

#==============================================================================
#    METHODS
#==============================================================================

#-------------------------------------------------------------------------
#    Print
#-------------------------------------------------------------------------
    def printTikZNode(self):
        print('TikZNode ({}) at ({}) - Text: {} - Options: {}'.format(self.name,self.coordinatesTikZ,self.__content,self.__options))



#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    import logging

    from tools import MyLogging
    from tools.tikZPicture.tikZPicture3D import TikZPicture3D

    with MyLogging('TikZCircledArrow',shLevel=logging.DEBUG):
        pic = TikZPicture3D()

        # Create a node, with all possible parameters
        cc.printBlue('Create node')
        n1 = pic.addTikZNode(name = 'n1',
                                   coordinates = np.array([0,0,0]),
                                   content = '$n_1$',
                                   options = ['draw=TUMBlue','fill=TUMGreen','text=TUMOrange'])

        # Print the node
        n1.printTikZNode()

        # Create another node
        cc.printBlue('Create another node')
        n2 = pic.addTikZNode('n2',np.array([3,0,0]),'$n_2$',['draw','TUMBlue'])

        cc.printBlue('Create another node')
        n3 = pic.addTikZNode('n3',np.array([6,0,0]),options=['circle','fill','inner sep = 0pt','minimum size=2mm','label={below right: $n_3$}'])

        # Create LaTeX file
        cc.printBlue('Create first LaTeX file')
        pic.writeLaTeXFile('latex','tikzNode1',compileFile=True,openFile=True)

        # Change coordinates
        cc.printBlue('Change coordinates of a TikZCoordinate')
        n3.coordinates = np.array([0,6,0])

        cc.printBlue('Create second LaTeX file')
        pic.writeLaTeXFile('latex','tikzNode2',compileFile=True,openFile=True)
