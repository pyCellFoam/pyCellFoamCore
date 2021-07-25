# -*- coding: utf-8 -*-
#==============================================================================
# TIKZ POLYGON
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue Feb  4 16:21:14 2020

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

class TikZPolygon(TikZElement):
    '''
    
    '''

#==============================================================================
#    CLASS VARIABLES
#==============================================================================    
    commandList = ['draw','fill','filldraw']
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__command',
                 '__coordinates',
                 '__options',
                 '__cycle')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,coordinates,command='draw',options=None,cycle=False,**kwargs):
        '''
        
        '''
        super().__init__(**kwargs)
        self.__command = None
        self.command = command
        self.__coordinates = coordinates
        self.__options = options
        self.__cycle = cycle
        self.logger.info('Created TikZPolygon')
        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getCommand(self): return self.__command
    def __setCommand(self,c): 
        if c in self.commandList:
            self.__command = c
        else:
            self.logger.error('Unknown command {} - Possible commands: {}'.format(c,self.commandList))
    command = property(__getCommand,__setCommand)

    def __getTikZText(self):
        if self.__options is None:
            optionsText = ''
        else:
            optionsText = '['+','.join(self.__options)+']'
        
        
        text = self.tikZPrefix + '\\{}{} {}'.format(self.command,optionsText,' -- '.join(['('+x.name+'.center)' for x in self.__coordinates]))
        if self.__cycle:
            text += ' -- cycle'
        text += ';\n'
        return text
    tikZText = property(__getTikZText)   

    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    
    
    import logging
    
    from tools import MyLogging
    from tools.tikZPicture.tikZPicture3D import TikZPicture3D
    
    with MyLogging('TikZPicture3D',shLevel=logging.DEBUG):
        
        tikzpic3D = TikZPicture3D()
        
        a = 5
        
        
        # Creat some coordinates
        c1 = tikzpic3D.addTikZCoordinate('c1',np.array([0,0,0]))
        c2 = tikzpic3D.addTikZCoordinate('c2',np.array([0,0,a]))
        c3 = tikzpic3D.addTikZCoordinate('c3',np.array([0,a,a]))
        c4 = tikzpic3D.addTikZCoordinate('c4',np.array([0,a,0]))
        c5 = tikzpic3D.addTikZCoordinate('c5',np.array([a,0,0]))
        c6 = tikzpic3D.addTikZCoordinate('c6',np.array([a,0,a]))
        c7 = tikzpic3D.addTikZCoordinate('c7',np.array([a,a,a]))
        c8 = tikzpic3D.addTikZCoordinate('c8',np.array([a,a,0]))
    
        
        # Create a polygon, with all possible parameters
        tikzpic3D.addTikZPolygon(coordinates = [c1,c2,c3,c4],
                                      command = 'filldraw',
                                      options = ['fill=TUMBlue','draw=TUMOrange','ultra thick'],
                                      cycle = True)
        # Create another polygon
        tikzpic3D.addTikZPolygon([c1,c2,c5],'draw',['dashed','TUMGreen'],True)
        
        
        # Create another polygon with minimal number of parameters
        tikzpic3D.addTikZPolygon([c5,c6,c7,c8])
    #    p3 = tikzpic3D.addTikZPolygon(coordinates = [c5,c6,c7,c8],
    #                                  cycle = True)
        
        
        # Create LaTeX file
        tikzpic3D.writeLaTeXFile('latex','tikZPolygon',compileFile=True,openFile=True)
    

