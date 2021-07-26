# -*- coding: utf-8 -*-
#==============================================================================
# COMPLEX 1D
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Jul 17 09:51:59 2019


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
import numpy as np


#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------


#    kCells
#--------------------------------------------------------------------
from kCells import Node,Edge

#    Complex & Grids
#--------------------------------------------------------------------
from complex.complex import Complex

#    Tools
#--------------------------------------------------------------------

from tools.tikZPicture.tikZPicture2D import TikZPicture2D



#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class Complex1D(Complex):
    '''
    
    A class to represent a 1D cell complex. 
    Serves as parent class for primal and dual 1D complex.
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__nodes',
                 '__edges',
                 '__innerNodes',
                 '__borderNodes',
                 '__additionalBorderNodes',
                 '__innerEdges',
                 '__borderEdges',
                 '__xLim','__xMin','__xMax',
                 '__changedLimits',
                 '__changedLimits',                 
                 '__incidenceMatrix1ii','__changedIncidenceMatrix1ii',
                 '__incidenceMatrix1ib','__changedIncidenceMatrix1ib',
                 '__incidenceMatrix1bi','__changedIncidenceMatrix1bi',
                 '__incidenceMatrix1bb','__changedIncidenceMatrix1bb',
                 '__incidenceMatrix1Bi','__changedIncidenceMatrix1Bi',
                 '__incidenceMatrix1Bb','__changedIncidenceMatrix1Bb')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,nodes=None,edges=None,loggerName = __name__):
        '''
        :param Node nodes: List of all nodes
        :param Edge edges: List of all edges
        :param str loggerName: Optional name of the logger. Standard value 
            is `__name__`
        
        
        '''
        self.__nodes = nodes
        self.__edges = edges
        self.__innerNodes = []
        self.__borderNodes = []
        self.__additionalBorderNodes = []
        self.__innerEdges = []
        self.__borderEdges = []
        self.__changedIncidenceMatrix1ii = True
        self.__changedIncidenceMatrix1ib = True
        self.__changedIncidenceMatrix1bi = True
        self.__changedIncidenceMatrix1bb = True
        self.__changedIncidenceMatrix1Bi = True
        self.__changedIncidenceMatrix1Bb = True
        self.__xLim = None
        self.__xMin = None
        self.__xMax = None
        self.__changedLimits = True         
        super().__init__(loggerName)
        
        
        
        
        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================

#-------------------------------------------------------------------------
#    Limits
#-------------------------------------------------------------------------        
        
    def __getXLim(self): 
        if self.__changedLimits:
            self.__calcLimits()
        return self.__xLim
    xLim = property(__getXLim)
    '''
    Range of x-coordinates of all nodes in the complex.
    
    '''
    
    
    def __getXMin(self):
        if self.__changedLimits:
            self.__calcLimits()
        return self.__xMin
    xMin = property(__getXMin)
    '''
    Minimal x-coordinate of all nodes in the complex.
    
    '''
    
    def __getXMax(self):
        if self.__changedLimits:
            self.__calcLimits()
        return self.__xMax
    xMax = property(__getXMax)    
    '''
    Maximal x-coordinate of all nodes in the complex.
    
    '''



    def __getChangedLimits(self): return self.__changedLimits
    changedLimits = property(__getChangedLimits)
    '''
    Bool variable that is set when the nodes or the coordinates of the nodes 
    have changed and therefor the limits must be recalculated.
    
    '''


    
    
#-------------------------------------------------------------------------
#    Nodes
#-------------------------------------------------------------------------
    
    def __getNodes(self): return self.__nodes
    def __setNodes(self,nodes):
        error = False
        for n in nodes:
            if not (n.yCoordinate == 0 and n.zCoordinate == 0):
                self.logger.error('y- and z-coordinate must be 0, but node {} has coordinates {}'.format(n,n.coordinates))
                error = True
        if not error:
            self.__nodes = nodes[:]
    nodes = property(__getNodes,__setNodes)
    r'''
    All nodes :math:`\Np = \Npi \cup \Npb \cup \NpB` of the complex.
    
    '''
    
    
    
    def __getInnerNodes(self): return self.__innerNodes
    innerNodes = property(__getInnerNodes)
    r'''
    Inner nodes :math:`\Npi` of the complex.
    
    '''

    def __getBorderNodes(self): return self.__borderNodes
    borderNodes = property(__getBorderNodes)
    r'''
    Border nodes :math:`\Npb` of the complex.
    
    '''

    def __getAdditionalBorderNodes(self): return self.__additionalBorderNodes
    additionalBorderNodes = property(__getAdditionalBorderNodes)
    r'''
    Additional border nodes :math:`\NpB` of the complex.
    
    '''


#-------------------------------------------------------------------------
#    Edges
#-------------------------------------------------------------------------

    def __getEdges(self): return self.__edges
    def __setEdges(self,edges):
        error = False
        for e in edges:
            if not all([n in self.nodes for n in e.topologicNodes]):
                unknownNodes = []
                for n in e.topologicNodes:
                    if not n in self.nodes:
                        unknownNodes.append(n)
                self.logger.error('Edge {} contains {} that does not belong to the complex'.format(e,unknownNodes))
                error = True
        if not error:
            self.__edges = edges[:]
    edges = property(__getEdges,__setEdges)
    r'''
    All edges :math:`\Ep = \Epi \cup \Epb` of the complex.
    
    '''


    def __getInnerEdges(self): return self.__innerEdges
    innerEdges = property(__getInnerEdges)
    r'''
    Inner edges :math:`\Epi` of the complex.
    
    '''

    def __getBorderEdges(self): return self.__borderEdges
    borderEdges = property(__getBorderEdges)
    r'''
    Border edges :math:`\Epb` of the complex.
    
    '''


#-------------------------------------------------------------------------
#    Incidence matrices 1
#-------------------------------------------------------------------------


    def __getIncidenceMatrix1ii(self):
        if self.__changedIncidenceMatrix1ii:
            self.__incidenceMatrix1ii = self.calcIncidence1(self.innerNodes,self.innerEdges)
            self.__changedIncidenceMatrix1ii = False
        return self.__incidenceMatrix1ii
    incidenceMatrix1ii = property(__getIncidenceMatrix1ii)
    r'''
    Incidence matrix :math:`\incpii{1} \in \mathbb{R}^{|\Npi|\times|\Epi|}` 
    
    '''
    
    
    def __getIncidenceMatrix1ib(self):
        if self.__changedIncidenceMatrix1ib:
            self.__incidenceMatrix1ib = self.calcIncidence1(self.innerNodes,self.borderEdges)
            self.__changedIncidenceMatrix1ib = False
        return self.__incidenceMatrix1ib
    incidenceMatrix1ib = property(__getIncidenceMatrix1ib)
    r'''
    Incidence matrix :math:`\incpib{1} \in \mathbb{R}^{|\Npi|\times|\Epb|}` 
    
    '''
    
    
    def __getIncidenceMatrix1bi(self):
        if self.__changedIncidenceMatrix1bi:
            self.__incidenceMatrix1bi = self.calcIncidence1(self.borderNodes,self.innerEdges)
            self.__changedIncidenceMatrix1bi = False
        return self.__incidenceMatrix1bi
    incidenceMatrix1bi = property(__getIncidenceMatrix1bi)
    r'''
    Incidence matrix :math:`\incpbi{1} \in \mathbb{R}^{|\Npb|\times|\Epi|}` 
    
    '''


    def __getIncidenceMatrix1bb(self):
        if self.__changedIncidenceMatrix1bb:
            self.__incidenceMatrix1bb = self.calcIncidence1(self.borderNodes,self.borderEdges)
            self.__changedIncidenceMatrix1bb = False
        return self.__incidenceMatrix1bb
    incidenceMatrix1bb = property(__getIncidenceMatrix1bb)
    r'''
    Incidence matrix :math:`\incpbb{1} \in \mathbb{R}^{|\Npb|\times|\Epb|}` 
    
    '''
    
    def __getIncidenceMatrix1Bi(self):#
        if self.__changedIncidenceMatrix1Bi:
            self.__incidenceMatrix1Bi = self.calcIncidence1(self.additionalBorderNodes,self.innerEdges)
            self.__changedIncidenceMatrix1Bi = False
        return self.__incidenceMatrix1Bi
    incidenceMatrix1Bi = property(__getIncidenceMatrix1Bi)
    r'''
    Incidence matrix :math:`\incpBi{1} \in \mathbb{R}^{|\NpB|\times|\Epi|}` 
    
    '''

    def __getIncidenceMatrix1Bb(self):
        if self.__changedIncidenceMatrix1Bb:
            self.__incidenceMatrix1Bb = self.calcIncidence1(self.additionalBorderNodes,self.borderEdges)
            self.__changedIncidenceMatrix1Bb = False
        return self.__incidenceMatrix1Bb
    incidenceMatrix1Bb = property(__getIncidenceMatrix1Bb)
    r'''
    Incidence matrix :math:`\incpBb{1} \in \mathbb{R}^{|\NpB|\times|\Epb|}` 
    
    '''
   
    def __getIncidenceMatrix1(self):
        incidencematrix1i = np.concatenate((self.incidenceMatrix1ii,self.incidenceMatrix1ib),axis=1)
        incidencematrix1b = np.concatenate((self.incidenceMatrix1bi,self.incidenceMatrix1bb),axis=1)
        incidencematrix1B = np.concatenate((self.incidenceMatrix1Bi,self.incidenceMatrix1Bb),axis=1)
        incidencematrix1 = np.concatenate((incidencematrix1i,incidencematrix1b,incidencematrix1B))
        return incidencematrix1
    incidenceMatrix1 = property(__getIncidenceMatrix1)
    r'''
    
    Complete incidence matrix :math:`\incp{1}` with 
    
    .. math::
        
        \incp{1} &=
        \begin{bmatrix}
            \incpii{1} & \incpib{1} \\
            \incpbi{1} & \incpbb{1} \\
            \incpBi{1} & \incpBb{1}
        \end{bmatrix}.
    
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
        self.logger.info('Called "Set Up" in Complex1D class')


   
    
    
#-------------------------------------------------------------------------
#    Sort 
#-------------------------------------------------------------------------    
    def sort(self):
        '''
        
        '''
        for n in self.nodes:
            if n.category == 'inner':
                self.addToList(n,self.innerNodes)
            elif n.category == 'border':
                self.addToList(n,self.borderNodes)
            elif n.category == 'additionalBorder':
                self.addToList(n,self.additionalBorderNodes)
            else:
                self.logger.error('Unknown category of {}'.format(n))
                
        for e in self.edges:
            if e.category == 'inner':
                self.addToList(e,self.innerEdges)
            elif e.category == 'border':
                self.addToList(e,self.borderEdges)
            else:
                self.logger.error('Unknown category of {}'.format(e))
                
                
    
#-------------------------------------------------------------------------
#    Determine max range for each dimension
#-------------------------------------------------------------------------          
    def __calcLimits(self):    
        '''
        
        '''
        self.logger.info('Calculating limits')
        self.__xMax = self.myMax([n.xCoordinate for n in self.nodes])
        self.__xMin = self.myMin([n.xCoordinate for n in self.nodes])
        self.__xLim = [self.__xMin,self.__xMax]
        self.__changedLimits = False    
    
    
    
    
#-------------------------------------------------------------------------
#    Plot
#-------------------------------------------------------------------------
    def plotComplex(self,ax,**kwargs):
        '''
        Plot all nodes and edges in this 1D complex.
        
        :param ax: Axis where this complex is plotted.        
        
        '''
        for n in self.__nodes:
            n.plotNode(ax,**kwargs)
        for e in self.__edges:
            e.plotEdge(ax,**kwargs)
            

#-------------------------------------------------------------------------
#    Plot TikZ
#-------------------------------------------------------------------------            
    def plotComplexTikZ(self,tikZPicture=None):
        '''
        
        '''
        if tikZPicture is None:
            tikZPicture = TikZPicture2D()
            
            
        if tikZPicture.dim != 2:
            self.logger.error('Trying to plot in a 3-dimensional tikZPicture, but a 1-D complex should be plotted in a 2D-picture')
        else:
            for n in self.nodes:
                n.plotNodeTikZ(tikZPicture,dim=2)
                
            for e in self.edges:
                e.plotEdgeTikZ(tikZPicture)
            
        return tikZPicture

        

    
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    
    from tools import MyLogging
    import tools.colorConsole as cc
    import tools.placeFigures as pf
    
    with MyLogging('Complex1D',debug=False):
        
        
        cc.printBlue('Prepare plots')
        
        
        cc.printBlue('Create some nodes')
        n0 = Node(0,0,0)
        n1 = Node(1,0,0)
        n2 = Node(1.5,0,0)
        nodes = [n0,n1,n2]
        
        
        cc.printBlue('Create some edges')
        e0 = Edge(n0,n1)
        e1 = Edge(n1,n2)
        edges = [e0,e1]
        
        
        cc.printBlue('Combine them to a complex')
        c = Complex1D(nodes,edges)
        
        
        
        

            
#-------------------------------------------------------------------------
#    Plotting
#-------------------------------------------------------------------------    
    
        # Choose plotting method. Possible choices: pyplot, VTK, TikZ, animation, None
        plottingMethod = 'pyplot'   
        
        
#    Disabled
#--------------------------------------------------------------------- 
        if plottingMethod is None or plottingMethod == 'None':
            cc.printBlue('Plotting disabled')
        
#    Pyplot
#---------------------------------------------------------------------         
        elif plottingMethod == 'pyplot':
            cc.printBlue('Plot using pyplot')
            (figs,axes) = pf.getFigures(numTotal=4)
            c.plotComplex(axes[0])

#    VTK
#--------------------------------------------------------------------- 
        elif plottingMethod == 'VTK' :
            cc.printBlue('Plot using VTK')
            cc.printRed('Not implemented')

#    TikZ
#--------------------------------------------------------------------- 
        elif plottingMethod == 'TikZ' :
            cc.printBlue('Plot using TikZ')  
            pic = c.plotComplexTikZ()
            pic.scale = 3
            file = False
            pic.writeLaTeXFile('latex','complex1D',compileFile=file,openFile=file)
            
#    Animation
#--------------------------------------------------------------------- 
        elif plottingMethod == 'animation':
            cc.printBlue('Creating animation')
            cc.printRed('Not implemented')

#    Unknown
#---------------------------------------------------------------------             
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))   
