# -*- coding: utf-8 -*-
#==============================================================================
# TIKZCOORDINATE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue Feb  4 14:40:21 2020

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

class TikZCoordinate(TikZElement):
    '''
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__name',
                 '__coordinates')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,name,coordinates,tikZPicture):
        '''
        
        '''
        super().__init__(tikZPicture)
        self.__name = name
        self.__coordinates = coordinates
        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getName(self): return self.__name
    name = property(__getName)
    
    
    def __getCoordinates(self): return self.__coordinates
    def __setCoordinates(self,c):
#        self.__tikZTextChanged = True
        self.__coordinates = c
    coordinates = property(__getCoordinates,__setCoordinates)
    
    ##################
    # TODO: Use function to transform coordinates!!!
    #############
    def __getCoordinatesTikZ(self): return ','.join([str(c) for c in self.coordinates])
    coordinatesTikZ = property(__getCoordinatesTikZ)
        
    
    
    def __getTikZText(self):
        return self.tikZPrefix + '\\coordinate ({}) at ({});\n'.format(self.name,self.coordinatesTikZ)
    tikZText = property(__getTikZText)


#==============================================================================
#    MAGIC METHODS
#==============================================================================   
    def  __repr__(self):
        '''
        Show infoText in console
        
        '''
        return 'TikZCoordinate ({}) at ({})'.format(self.name,self.coordinatesTikZ)
    
    
#==============================================================================
#    METHODS
#==============================================================================
     
#-------------------------------------------------------------------------
#    Method 1
#-------------------------------------------------------------------------
    def printTikZCoordinate(self):
        print('TikZCoordinate ({}) at ({})'.format(self.name,self.coordinatesTikZ))   
    
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    
    
    from tools import MyLogging
    from tools.tikZPicture.tikZPicture3D import TikZPicture3D
    
    with MyLogging('TikZCircledArrow',debug=True):    
        pic = TikZPicture3D()
        
        # Create a coordinate, with all possible parameters
        c1 = pic.addTikZCoordinate(name = 'c1',
                                         coordinates = np.array([0,0,0]))
        
        # Print the coordinate
        c1.printTikZCoordinate()
        
        # Create another coordinate
        c2 = pic.addTikZCoordinate('c2',np.array([0,0,1]))
        
        c3 = pic.addTikZCoordinate('c3',np.array([1,2,3,4]))
        c4 = pic.addTikZCoordinate('c4','a')
        
        cc.printBlue('TikZ Preamble')
        print(pic.latexPreamble)
        
        cc.printBlue('TikZ Text')
        print(pic.tikZText)
        
        cc.printBlue('Create pdf')
        file = False
        pic.writeLaTeXFile('latex','TikZCoordinate',compileFile=file,openFile=file)
        
    
    
    
    





        
        

    
    
    

