# -*- coding: utf-8 -*-
#==============================================================================
# TIKZ PICTURE 2D
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue Feb 11 15:56:05 2020

'''

'''
#==============================================================================
#    IMPORTS
#==============================================================================
import os
if __name__ == '__main__':
    os.chdir('../../')
    

import tools.colorConsole as cc
from tools.tikZPicture.tikZPicture import TikZPicture

#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class TikZPicture2D(TikZPicture):
    '''
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ()

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,*args,**kwargs):
        '''
        :param float scale: scale of the tikzpicture
        :param str name: A name for the tikzpicture  
        
        '''
        super().__init__(*args,**kwargs)
        self.logger.info('Created TikZPicture2D')
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getTikZText(self):
        text = self.tikZPrefix + '\\begin{tikzpicture}'
        if self.pictureOptions:
            text += ('['+','.join(self.pictureOptions)+']')
        text += '\n'
        text += super().tikZText
        text += self.tikZPrefix + '\\end{tikzpicture}\n'
        return text
    tikZText = property(__getTikZText)    

    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
        
    
    import numpy as np
    import logging
    
    from tools import MyLogging
    
    with MyLogging('TikZPicture2D',shLevel=logging.DEBUG):
        
        cc.printBlue('Creat picture')
        tikzpicture = TikZPicture2D()
        
        cc.printBlue('Create coordinates')
        c1 = tikzpicture.addTikZCoordinate('c1',np.array([0,0]))
        c2 = tikzpicture.addTikZCoordinate('c2',np.array([1,0]))
        
        cc.printBlue('Create node')
        n1 = tikzpicture.addTikZNode('n1',np.array([0,1]))
        
        cc.printBlue('Create polygon')
        tikzpicture.addTikZPolygon([c1,c2,n1])
        
        cc.printBlue('Create coordinate system')
        tikzpicture.addTikZCoSy2D(c2)
        
        cc.printGreen('Preamble:')
        print(tikzpicture.latexPreamble)
        
        cc.printGreen('TikZ text:')
        print(tikzpicture.tikZText)
        
        cc.printBlue('Create LaTeX file')
        tikzpicture.writeLaTeXFile()
        tikzpicture.writeLaTeXFile('latex','tikz2D',compileFile=True,openFile=True)
        
        
        
        
        
