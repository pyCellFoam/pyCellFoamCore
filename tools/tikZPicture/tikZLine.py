# -*- coding: utf-8 -*-
#==============================================================================
# TIKZ LINE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Mon Mar 23 11:01:25 2020

'''
This is the explanation of the whole module and will be printed at the very 
beginning

Use - signs to declare a headline
--------------------------------------------------------------------------

* this is an item
* this is another one

#. numbered lists
#. are also possible


Maths
--------------------------------------------------------------------------

Math can be inline :math:`a^2 + b^2 = c^2` or displayed

.. math::

   (a + b)^2 = a^2 + 2ab + b^2

   (a - b)^2 = a^2 - 2ab + b^2

Always remember that the last line has to be blank

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

class TikZLine(TikZElement):
    '''
    This is the explanation of this class.
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__start',
                 '__end',
                 '__options',
                 '__intermediateText',
                 '__intermediatePosition')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,start,end,options=None,intermediateText=None,intermediatePosition='above',**kwargs):
        '''
        This is the explanation of the __init__ method. 
        
        All parameters should be listed:
        
        :param int a: Some Number
        :param str b: Some String
        
        '''
        super().__init__(**kwargs)
        self.__start = start
        self.__end = end
        self.__options = options
        self.__intermediateText = intermediateText
        self.__intermediatePosition = intermediatePosition
        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getStart(self): return self.__start
    start = property(__getStart)

    def __getEnd(self): return self.__end
    end = property(__getEnd)


    def __getTikZText(self):
        if self.__options is None:
            optionsText = ''
        else:
            optionsText = '['+','.join(self.__options)+']'
            
        if self.intermediateText is None:
            intermediateTikZText = ''
        else:
            intermediateTikZText = 'node[{}]{{{}}}'.format(self.intermediatePosition,self.intermediateText)
        text = self.tikZPrefix + '\\draw{} ({}.center) -- {}({}.center);\n'.format(optionsText,self.start.name,intermediateTikZText,self.end.name)
        return text
    tikZText = property(__getTikZText)   


    def __getIntermediateText(self): return self.__intermediateText
    intermediateText = property(__getIntermediateText)

    def __getIntermediatePosition(self): return self.__intermediatePosition
    intermediatePosition = property(__getIntermediatePosition)


    
#==============================================================================
#    METHODS
#==============================================================================
    
#-------------------------------------------------------------------------
#    Method 1
#-------------------------------------------------------------------------
    
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
   
    
    
    from tools import MyLogging
    from tools.tikZPicture.tikZPicture3D import TikZPicture3D
    
    with MyLogging('TikZPicture3D',debug=True):
        
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
        
        
        
        tikzpic3D.addTikZLine(c1,c2,options=['TUMBlue','->-'],intermediate='X')
    
        
#        # Create a polygon, with all possible parameters
#        p1 = tikzpic3D.addTikZPolygon(coordinates = [c1,c2,c3,c4],
#                                      command = 'filldraw',
#                                      options = ['fill=TUMBlue','draw=TUMOrange','ultra thick'],
#                                      cycle = True)
#        # Create another polygon
#        p2 = tikzpic3D.addTikZPolygon([c1,c2,c5],'draw',['dashed','TUMGreen'],True)
#        
#        
#        # Create another polygon with minimal number of parameters
#        p3 = tikzpic3D.addTikZPolygon([c5,c6,c7,c8])
#    #    p3 = tikzpic3D.addTikZPolygon(coordinates = [c5,c6,c7,c8],
#    #                                  cycle = True)
#        
        
        # Create LaTeX file
        tikzpic3D.writeLaTeXFile('latex','tikZLine',compileFile=True,openFile=True)
        print(tikzpic3D.tikZText)
        
        
