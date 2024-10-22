# -*- coding: utf-8 -*-
#==============================================================================
# TIKZ PICTURE 3D
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue Feb 11 15:39:42 2020

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
from tools.tikZPicture.tikZPicture import TikZPicture
from tools.tikZPicture.tikZCoSy2D import TikZCoSy2D
from tools.tikZPicture.tikZCoSy3D import TikZCoSy3D
from tools.tikZPicture.tikZCanvas import TikZCanvas


#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class TikZPicture3D(TikZPicture):
    '''
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__tikZCanvases',
                 '__tikZPerspective')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,tikZPerspective=None,**kwargs):
        '''
        :param TikZPerspective tikZPerspective: optional perspective
        :param float scale: scale of the tikzpicture
        :param str name: A name for the tikzpicture  
        
        '''
        super().__init__(**kwargs)
        self.__tikZCanvases = []
        self.__tikZPerspective = None
        if tikZPerspective:
            self.tikZPerspective = tikZPerspective
#        self.__tikZPerspective = tikZPerspective
#        if self.__tikZPerspective:
#            self.__tikZPerspective.tikZEnvironment.append(self)
        self.logger.info('Created TikZPicture3D')
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getTikZPerspective(self): return self.__tikZPerspective
    def __setTikZPerspective(self,t):
        if self.__tikZPerspective is not None:
            self.__tikZPerspective.tikZEnvironment.remove(self)
        self.__tikZPerspective = t
        self.__tikZPerspective.tikZEnvironment.append(self)
    tikZPerspective = property(__getTikZPerspective,__setTikZPerspective)
    
    def __getLibraryOptions(self): return super().libraryOptions + ['3d',]
    libraryOptions = property(__getLibraryOptions)
    
#    def __getTikZCoSys(self): 
#        cosys = super().tikZCoSys
#        for c in self.tikZCanvases:
#            cosys.extend(c.tikZCoSys)
#        return cosys
#    tikZCoSys = property(__getTikZCoSys)    
    
    def __getPictureOptions(self):
        options = super().pictureOptions
        if self.__tikZPerspective:
            options.append(self.__tikZPerspective.name)
        return options
    pictureOptions = property(__getPictureOptions)    
    
    
    def __getNewcommands(self):
        newcommandsTemp = super().newcommands
        if self.tikZCoSy3DUsed:
            newcommandsTemp.append('''\\newcommand{\\CoSyThreeD}[2][1]{% #1 Arrow length, #2 Center
    \\draw[TUMOrange,-stealth] (#2) -- +(#1,0,0);
    \\draw[TUMGreen,-stealth] (#2) -- +(0,#1,0);
    \\draw[TUMBlue,-stealth] (#2) -- +(0,0,#1);
}
''')
        if self.tikZCanvases:
            newcommandsTemp.append('''\\makeatletter
\\tikzoption{canvas is plane}[]{\\@setOxy#1}
\\def\\@setOxy O(#1,#2,#3)x(#4,#5,#6)y(#7,#8,#9)%
{\\def\\tikz@plane@origin{\\pgfpointxyz{#1}{#2}{#3}}%
	\\def\\tikz@plane@x{\\pgfpointxyz{#4}{#5}{#6}}%
	\\def\\tikz@plane@y{\\pgfpointxyz{#7}{#8}{#9}}%
	\\tikz@canvas@is@plane
}
\\makeatother  
''')
        return newcommandsTemp
    newcommands = property(__getNewcommands)
    
    
    def __getTikZCanvases(self): return self.__tikZCanvases
    tikZCanvases = property(__getTikZCanvases)    
    

    def __getTikZNames(self):
        names = super().tikZNames
        for c in self.tikZCanvases:
            names.extend(c.tikZNames)
        return names
    tikZNames = property(__getTikZNames)
    
    
    
    def __getTikzsets(self):
        sets = super().tikzsets
        if self.__tikZPerspective:
            sets.append(self.__tikZPerspective.tikzset)
        return sets
    tikzsets = property(__getTikzsets)
    
    def __getTikZText(self):
        text = self.tikZPrefix + '\\begin{tikzpicture}'
        if self.pictureOptions:
            text += ('['+','.join(self.pictureOptions)+']')
        text += '\n'
        text += super().tikZText
        for c in self.tikZCanvases:
            text  += c.tikZText        
        text += self.tikZPrefix + '\\end{tikzpicture}\n'
        return text
    tikZText = property(__getTikZText)        
    
            
    def __getTikZCoSy2DUsed(self): 
        cosys = super().tikZCoSys[:]
        for c in self.tikZCanvases:
            cosys.extend(c.tikZCoSys)        
        return any([type(x) == TikZCoSy2D for x in cosys])
    tikZCoSy2DUsed = property(__getTikZCoSy2DUsed)

    def __getTikZCoSy3DUsed(self): return any([type(x) == TikZCoSy3D for x in self.tikZCoSys])
    tikZCoSy3DUsed = property(__getTikZCoSy3DUsed)
    
    def __getCircledArrowsUsed(self): 
        circledArrows = self.tikZCircledArrows[:]
        for c in self.tikZCanvases:
            circledArrows.extend(c.tikZCircledArrows)
        return any(circledArrows)
    circledArrowsUsed = property(__getCircledArrowsUsed)    
 
    
    def __getDim(self): return 3
    dim = property(__getDim)    
 
#==============================================================================
#    MAGIC METHODS
#==============================================================================   
    def  __repr__(self):
        '''
        Show infoText in console
        
        '''
        return 'TikZPicture3D "{}" '.format(self.name)    
#==============================================================================
#    METHODS
#==============================================================================
    
#-------------------------------------------------------------------------
#    Add TikZ coordinate system
#-------------------------------------------------------------------------
    def addTikZCoSy3D(self,center,*args,**kwargs):
        coSy = TikZCoSy3D(center,*args,tikZEnvironment=self,**kwargs)
        if center in self.tikZCoordinates+self.tikZNodes:
            self.tikZCoSys.append(coSy)
            return coSy
        else:
            self.logger.error('{} is not a coordinate in this TikZPicture'.format(center))    
    

#-------------------------------------------------------------------------
#    Add TikZ canvas
#-------------------------------------------------------------------------      
    def addTikZCanvas(self,*args,**kwargs):
        self.logger.info('Adding TikZCanvas')
        canvas = TikZCanvas(*args,tikZPicture3D = self,**kwargs)
        self.__tikZCanvases.append(canvas)
        return canvas    
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    
    import logging
    
    from tools import MyLogging
    
    with MyLogging('TikZPicture3D',shLevel=logging.DEBUG):
        
        cc.printBlue('Create picture')
        tikzpic3D = TikZPicture3D()
        
        
        
        cc.printBlue('Create coordinates')
        a = 5
        c1 = tikzpic3D.addTikZCoordinate('c1',np.array([0,0,0]))
        c2 = tikzpic3D.addTikZCoordinate('c2',np.array([0,0,a]))
        c3 = tikzpic3D.addTikZCoordinate('c3',np.array([0,a,a]))
        c4 = tikzpic3D.addTikZCoordinate('c4',np.array([0,a,0]))
        c5 = tikzpic3D.addTikZCoordinate('c5',np.array([a,0,0]))
        c6 = tikzpic3D.addTikZCoordinate('c6',np.array([a,0,a]))
        c7 = tikzpic3D.addTikZCoordinate('c7',np.array([a,a,a]))
        c8 = tikzpic3D.addTikZCoordinate('c8',np.array([a,a,0]))
        c9 = tikzpic3D.addTikZCoordinate('c9',np.array([2*a,0.5*a,0.5*a]))

        
        cc.printBlue('Create node')
        n1 = tikzpic3D.addTikZNode('n1',np.array([a,0.5*a,0.5*a]),options=['inner sep = 0pt','fill=TUMOrange','circle','minimum size = 3mm'])
        
        cc.printBlue('Create polygons')
        
        p1 = tikzpic3D.addTikZPolygon(coordinates = [c1,c2,c3,c4],
                                      command = 'filldraw',
                                      options = ['fill=TUMBlue','draw=TUMOrange','ultra thick'],
                                      cycle = True)
        
        p2 = tikzpic3D.addTikZPolygon(coordinates = [c5,c6,c7,c8],
                                      cycle = True)
        
        cc.printBlue('Create coordinate system')
        tikzpic3D.addTikZCoSy3D(c9)
        
        cc.printGreen('Preamble:')
        print(tikzpic3D.latexPreamble)
        
        
            
        
        cc.printBlue('Export LaTeX file')
        tikzpic3D.writeLaTeXFile('latex','tikz3D',compileFile=True,openFile=True)
        
