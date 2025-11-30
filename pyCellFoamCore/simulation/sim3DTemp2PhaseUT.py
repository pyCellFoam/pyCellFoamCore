# -*- coding: utf-8 -*-
#==============================================================================
# TITLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Sat Jun  6 17:09:56 2020

'''

'''
#==============================================================================
#    IMPORTS
#==============================================================================
#-------------------------------------------------------------------------
#    Change to Main Directory
#-------------------------------------------------------------------------
import os
if __name__ == '__main__':
    os.chdir('../')


#-------------------------------------------------------------------------
#    Standard Libraries
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------


#    kCells
#--------------------------------------------------------------------


#    Complex & Grids
#--------------------------------------------------------------------
from grids import Grid3DKelvin
from complex import DualComplex3D


#    Simulation
#--------------------------------------------------------------------
from simulations.simulation import Simulation

#    Tools
#--------------------------------------------------------------------
import tools.colorConsole as cc
import tools.placeFigures as pf
from tools import MyLogging


#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class Sim3DTemp2PhaseUT(Simulation):
    '''
    This is the explanation of this class.
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__doPrints',)

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,doPrints=True):
        '''
        This is the explanation of the __init__ method. 
        
        All parameters should be listed:
        
        :param int a: Some Number
        :param str b: Some String
        
        '''
        self.doPrints = doPrints
        
        super().__init__()
        
        
        # Primal complex
        
        if self.doPrints:
            cc.printBlue('Creating primal complex')
        self.primalComplex = Grid3DKelvin(0)
        
        
        
        
        # Dual complex
        
        if self.doPrints:
            cc.printBlue('Creating dual complex')
            
        self.dualComplex = DualComplex3D(self.primalComplex)
        
        
        
        # Finalize
        
        self.primalComplex.useCategory = 2
        
        if self.doPrints:
            cc.printBlue('Finished initialization')
        
        
        
        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getDoPrints(self): return self.__doPrints
    def __setDoPrints(self,d): self.__doPrints = d
    doPrints = property(__getDoPrints,__setDoPrints)



    
#==============================================================================
#    METHODS
#==============================================================================
    
#-------------------------------------------------------------------------
#    Method 1
#-------------------------------------------------------------------------



#-------------------------------------------------------------------------
#    Plot for Documentation
#-------------------------------------------------------------------------         
    @classmethod
    def plotDoc(cls):    
        cc.printRed('Not implemented')
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    
    with MyLogging('Sim3DTemp2PhaseUT'):

#-------------------------------------------------------------------------
#    Create some examples
#-------------------------------------------------------------------------
        
        
        sim = Sim3DTemp2PhaseUT()
        
        sim.simulate()
        
        print(sim.timeVector)


#-------------------------------------------------------------------------
#    Plotting
#-------------------------------------------------------------------------    
    
        # Choose plotting method. Possible choices: pyplot, VTK, TikZ, animation, doc, None
        plottingMethod = 'pyplot'   
        
        
#    Disabled
#--------------------------------------------------------------------- 
        if plottingMethod is None or plottingMethod == 'None':
            cc.printBlue('Plotting disabled')
        
#    Pyplot
#---------------------------------------------------------------------         
        elif plottingMethod == 'pyplot':
            cc.printBlue('Plot using pyplot')
            (figs,axes) = pf.getFigures()
            
            sim.primalComplex.plotComplex(axes[0],showLabel=False)
            sim.dualComplex.plotComplex(axes[1],showLabel=False)

#    VTK
#--------------------------------------------------------------------- 
        elif plottingMethod == 'VTK' :
            cc.printBlue('Plot using VTK')
            cc.printRed('Not implemented')

#    TikZ
#--------------------------------------------------------------------- 
        elif plottingMethod == 'TikZ' :
            cc.printBlue('Plot using TikZ')            
            cc.printRed('Not implemented')
            
#    Animation
#--------------------------------------------------------------------- 
        elif plottingMethod == 'animation':
            cc.printBlue('Creating animation')
            cc.printRed('Not implemented')
            
#    Documentation
#--------------------------------------------------------------------- 
        elif plottingMethod == 'doc':
            cc.printBlue('Creating plots for documentation')
            test.plotDoc()
            
#    Unknown
#---------------------------------------------------------------------             
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))        
        
    

