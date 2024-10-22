# -*- coding: utf-8 -*-
#==============================================================================
# GRID 1D EQUIDISTANT
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue Mar 24 17:35:22 2020

'''

Create a 1-dimensional grid with nodes spread equidistantly over the domain:

.. image:: ../../../_static/grid1DEquidistant1.png
       :width: 90%
       :alt: 1D equidistant grid - primal complex
       :align: center
       
       

It's dual:       
       
.. image:: ../../../_static/grid1DEquidistant2.png
       :width: 90%
       :alt: 1D equidistant grid - dual complex
       :align: center       


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
import numpy as np

#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------


#    kCells
#--------------------------------------------------------------------
from kCells import Node,Edge

#    Complex & Grids
#--------------------------------------------------------------------
from complex.primalComplex1D import PrimalComplex1D
from complex.dualComplex1D import DualComplex1D

#    Tools
#--------------------------------------------------------------------
import tools.colorConsole as cc
import tools.placeFigures as pf
from tools import MyLogging


    




#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class Grid1DEquidistant(PrimalComplex1D):
    '''
    This is the explanation of this class.
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__xMin',
                 '__xMax',
                 '__numberOfNodes',
                 '__categoryOfFirstEdge',
                 '__categoryOfLastEdge')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,xMin,xMax,numberOfNodes,categoryOfFirstEdge='inner',categoryOfLastEdge='inner',**kwargs):
        '''
        This is the explanation of the __init__ method. 
        
        All parameters should be listed:
        
        :param int a: Some Number
        :param str b: Some String
        
        '''
        self.__xMin = xMin
        self.__xMax = xMax
        self.__numberOfNodes = numberOfNodes
        self.__categoryOfFirstEdge = categoryOfFirstEdge
        self.__categoryOfLastEdge = categoryOfLastEdge
        super().__init__()
        
        
        

        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getXMin(self): return self.__xMin
    xMin = property(__getXMin)
    '''
    
    '''

    def __getXMax(self): return self.__xMax
    xMax = property(__getXMax)
    '''
    
    '''

    def __getNumberOfNodes(self): return self.__numberOfNodes
    numberOfNodes = property(__getNumberOfNodes)
    '''
    
    '''

    def __getCategoryOfFirstEdge(self): return self.__categoryOfFirstEdge
    categoryOfFirstEdge = property(__getCategoryOfFirstEdge)
    '''
    
    '''

    def __getCategoryOfLastEdge(self): return self.__categoryOfLastEdge
    categoryOfLastEdge = property(__getCategoryOfLastEdge)
    '''
    
    '''


    
#==============================================================================
#    METHODS
#==============================================================================
    
#-------------------------------------------------------------------------
#    Set Up
#-------------------------------------------------------------------------
    def setUp(self):
        '''
    
        '''
        
        step = (self.xMax-self.xMin)/(self.numberOfNodes-1)
        
        nodes = []
        edges = []
        for x in np.arange(self.xMin,self.xMax+step,step):
            nodes.append(Node(x,0,0))
        
        
        for (start,end) in zip(nodes[:-1],nodes[1:]):
            edges.append(Edge(start,end))
            
        
        edges[0].category1 = self.categoryOfFirstEdge
        edges[-1].category1 = self.categoryOfLastEdge
        
        
        self.nodes = nodes
        self.edges = edges
        super().setUp()
        
        
        
#-------------------------------------------------------------------------
#    Plot for Documentation
#-------------------------------------------------------------------------         
    @classmethod
    def plotDoc(cls):
        pc = Grid1DEquidistant(0,1,4)      
        dc = DualComplex1D(pc)
        
        
        (figs,axes) = pf.getFigures(numTotal=2)
        
        pc.plotComplex(axes[0])
        dc.plotComplex(axes[1])        
        
        pf.exportPNG(figs[0],'doc/_static/grid1DEquidistant1')
        pf.exportPNG(figs[1],'doc/_static/grid1DEquidistant2')
        
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    
    with MyLogging('Grid1DEquidistant',debug=False):


#-------------------------------------------------------------------------
#    Create some grids
#-------------------------------------------------------------------------          
        
        
        pc0 = Grid1DEquidistant(0,10,6)
        pc1 = Grid1DEquidistant(0,10,6,categoryOfFirstEdge='border')
        pc2 = Grid1DEquidistant(0,10,6,categoryOfFirstEdge='border',categoryOfLastEdge='border')
        
        
        dc0 = DualComplex1D(pc0)
        dc1 = DualComplex1D(pc1)
        dc2 = DualComplex1D(pc2)
        
        
        
        
        dc0.checkAllIncidenceMatrices()
        dc1.checkAllIncidenceMatrices()
        dc2.checkAllIncidenceMatrices()
        
        
        
        
        
        
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
            
            pc0.plotComplex(axes[0])
            pc1.plotComplex(axes[1])
            pc2.plotComplex(axes[2])            
            
            dc0.plotComplex(axes[3])
            dc1.plotComplex(axes[4])
            dc2.plotComplex(axes[5])

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
            Grid1DEquidistant.plotDoc()

#    Unknown
#---------------------------------------------------------------------             
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))               
        
        
