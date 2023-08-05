# -*- coding: utf-8 -*-
#==============================================================================
# COMPLEX 2D
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Dec 15 17:58:41 2017


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
from kCells import Node, Edge, Face


#    Complex & Grids
#--------------------------------------------------------------------
from complex.complex import Complex


#    Tools
#--------------------------------------------------------------------
import tools.colorConsole as cc
from tools.tikZPicture.tikZPicture2D import TikZPicture2D
from tools.printTable import Table


#==============================================================================
#    CLASS DEFINITION
#==============================================================================
class Complex2D(Complex):
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__nodes',
                 '__edges',
                 '__faces',
                 '__innerNodes1','__innerNodes2',
                 '__borderNodes1','__borderNodes2',
                 '__additionalBorderNodes1','__additionalBorderNodes2',
                 '__innerEdges1','__innerEdges2',
                 '__borderEdges1','__borderEdges2',
                 '__additionalBorderEdges1','__additionalBorderEdges2',
                 '__innerFaces1','__innerFaces2',
                 '__borderFaces1','__borderFaces2',
                 '__additionalBorderFaces1','__additionalBorderFaces2',
                 '__innerVolumes1','__innerVolumes2',
                 '__borderVolumes1','__borderVolumes2',
                 '__geometricNodes',
                 '__xLim','__xMin','__xMax',
                 '__yLim','__yMin','__yMax',
                 '__changedLimits',
                 '__changedLimits',                 
                 '__incidenceMatrix1ii','__changedIncidenceMatrix1ii',
                 '__incidenceMatrix1ib','__changedIncidenceMatrix1ib',
                 '__incidenceMatrix1iB','__changedIncidenceMatrix1iB',
                 '__incidenceMatrix1bi','__changedIncidenceMatrix1bi',
                 '__incidenceMatrix1bb','__changedIncidenceMatrix1bb',
                 '__incidenceMatrix1bB','__changedIncidenceMatrix1bB',
                 '__incidenceMatrix1Bi','__changedIncidenceMatrix1Bi',
                 '__incidenceMatrix1Bb','__changedIncidenceMatrix1Bb',
                 '__incidenceMatrix1BB','__changedIncidenceMatrix1BB',
                 '__incidenceMatrix2ii','__changedIncidenceMatrix2ii',
                 '__incidenceMatrix2ib','__changedIncidenceMatrix2ib',
                 '__incidenceMatrix2bi','__changedIncidenceMatrix2bi',
                 '__incidenceMatrix2bb','__changedIncidenceMatrix2bb',
                 '__incidenceMatrix2Bi','__changedIncidenceMatrix2Bi',
                 '__incidenceMatrix2Bb','__changedIncidenceMatrix2Bb')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,nodes=[],edges=[],faces=[],loggerName=__name__):
        '''
    
        '''
        
        
        self.__nodes = nodes[:]
        self.__edges = edges[:]
        self.__faces = faces[:]
        self.__innerNodes1 = []
        self.__borderNodes1 = []
        self.__additionalBorderNodes1 = []
        self.__innerEdges1 = []
        self.__borderEdges1 = []
        self.__additionalBorderEdges1 = []
        self.__innerFaces1 = []
        self.__borderFaces1 = []
        self.__innerNodes2 = []
        self.__borderNodes2 = []
        self.__additionalBorderNodes2 = []
        self.__innerEdges2 = []
        self.__borderEdges2 = []
        self.__additionalBorderEdges2 = []
        self.__innerFaces2 = []
        self.__borderFaces2 = []
        self.__geometricNodes = []
        self.__xLim = None
        self.__xMin = None
        self.__xMax = None
        self.__yLim = None
        self.__yMin = None
        self.__yMax = None
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
    
    def __getYLim(self): 
        if self.__changedLimits:
            self.__calcLimits()
        return self.__yLim
    yLim = property(__getYLim)
    '''
    Range of y-coordinates of all nodes in the complex.
    
    '''
    
    
    def __getYMin(self):
        if self.__changedLimits:
            self.__calcLimits()
        return self.__yMin
    yMin = property(__getYMin)
    '''
    Minimal y-coordinate of all nodes in the complex.
    
    '''
    
    def __getYMax(self):
        if self.__changedLimits:
            self.__calcLimits()
        return self.__yMay
    yMax = property(__getYMax)    
    '''
    Maximal y-coordinate of all nodes in the complex.
    
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

      
    def __getNodes(self): 
        if self.changedNumbering:
            self.renumber()
        return self.__nodes
    def __setNodes(self,n): self.__nodes = n[:]
    nodes = property(__getNodes,__setNodes)
    r'''
    All nodes :math:`\Np = \Npi \cup \Npb \cup \NpB` of the complex.
    
    '''

        
    def __getInnerNodes1(self): return self.__innerNodes1
    innerNodes1 = property(__getInnerNodes1)
    r'''
    Inner nodes :math:`\Npi` according to categorization method 1.
    
    '''

    def __getInnerNodes2(self): return self.__innerNodes2
    innerNodes2 = property(__getInnerNodes2)
    r'''
    Inner nodes :math:`\Npi` according to categorization method 2.
    
    '''
    
    def __getInnerNodes(self): return self.pickCategory(self.__innerNodes1,self.__innerNodes2) 
    innerNodes = property(__getInnerNodes)
    r'''
    Inner nodes :math:`\Npi` according to the currently selected categorization
    method.
    
    '''  
    

    def __getBorderNodes1(self): return self.__borderNodes1
    borderNodes1 = property(__getBorderNodes1)
    r'''
    Border nodes :math:`\Npb` according to categorization method 1.
    
    '''

    def __getBorderNodes2(self): return self.__borderNodes2
    borderNodes2 = property(__getBorderNodes2)
    r'''
    Border nodes :math:`\Npb` according to categorization method 2.
    
    '''
    
    def __getBorderNodes(self): return self.pickCategory(self.__borderNodes1,self.__borderNodes2) 
    borderNodes = property(__getBorderNodes)
    r'''
    Border nodes :math:`\Npb` according to the currently selected categorization
    method.
    
    '''  


    def __getAdditionalBorderNodes1(self): return self.__additionalBorderNodes1
    additionalBorderNodes1 = property(__getAdditionalBorderNodes1)
    r'''
    Additional border nodes :math:`\NpB` according to categorization method 1.
    
    '''

    def __getAdditionalBorderNodes2(self): return self.__additionalBorderNodes2
    def __setAdditionalBorderNodes2(self,a): self.__additionalBorderNodes2 = a
    additionalBorderNodes2 = property(__getAdditionalBorderNodes2,__setAdditionalBorderNodes2)
    r'''
    Additional border nodes :math:`\NpB` according to categorization method 2.
    
    '''
    
    def __getAdditionalBorderNodes(self): return self.pickCategory(self.__additionalBorderNodes1,self.__additionalBorderNodes2) 
    additionalBorderNodes = property(__getAdditionalBorderNodes)
    r'''
    Additional border nodes :math:`\NpB` according to the currently selected 
    categorization method.
    
    '''     
    
    def __getGeometricNodes(self): return self.__geometricNodes
    geometricNodes = property(__getGeometricNodes)    
    '''
    Geometric nodes which are not part of the cell complex but are necessary to
    define the geometry of the edges.
    
    '''    
    
#-------------------------------------------------------------------------
#    Edges
#-------------------------------------------------------------------------    
    
    def __getEdges(self): 
        if self.changedNumbering:
            self.renumber()
        return self.__edges
    def __setEdges(self,e): self.__edges = e[:]
    edges = property(__getEdges,__setEdges)
    r'''
    All edges :math:`\Ep = \Epi \cup \Epb \cup \EpB` of the complex.
    
    '''


    def __getInnerEdges1(self): return self.__innerEdges1
    innerEdges1 = property(__getInnerEdges1)
    r'''
    Inner edges :math:`\Epi` according to categorization method 1.
    
    '''

    def __getInnerEdges2(self): return self.__innerEdges2
    innerEdges2 = property(__getInnerEdges2)
    r'''
    Inner edges :math:`\Epi` according to categorization method 2.
    
    '''
    
    def __getInnerEdges(self): return self.pickCategory(self.__innerEdges1,self.__innerEdges2)
    innerEdges = property(__getInnerEdges)
    r'''
    Inner edges :math:`\Epi` according to the currently selected categorization
    method.
    
    '''  

    def __getBorderEdges1(self): return self.__borderEdges1
    borderEdges1 = property(__getBorderEdges1)
    r'''
    Border edges :math:`\Epb` according to categorization method 1.
    
    '''

    def __getBorderEdges2(self): return self.__borderEdges2
    borderEdges2 = property(__getBorderEdges2)
    r'''
    Border edges :math:`\Epb` according to categorization method 2.
    
    '''
    
    def __getBorderEdges(self): return self.pickCategory(self.__borderEdges1,self.__borderEdges2)
    borderEdges = property(__getBorderEdges)
    r'''
    Border edges :math:`\Epb` according to the currently selected categorization
    method.
    
    '''     

    def __getAdditionalBorderEdges1(self): return self.__additionalBorderEdges1
    additionalBorderEdges1 = property(__getAdditionalBorderEdges1)
    r'''
    Additional border edges :math:`\Epb` according to categorization method 1.
    
    '''

    def __getAdditionalBorderEdges2(self): return self.__additionalBorderEdges2
    additionalBorderEdges2 = property(__getAdditionalBorderEdges2)
    r'''
    Additional border edges :math:`\Epb` according to categorization method 2.
    
    '''
    
    def __getAdditionalBorderEdges(self): return self.pickCategory(self.__additionalBorderEdges1,self.__additionalBorderEdges2)
    additionalBorderEdges = property(__getAdditionalBorderEdges)
    r'''
    Additional border edges :math:`\EpB` according to the currently selected 
    categorization method.
    
    '''    
    
#-------------------------------------------------------------------------
#    Faces
#-------------------------------------------------------------------------    
  
    def __getFaces(self): 
        if self.changedNumbering:
            self.renumber()
        return self.__faces
    def __setFaces(self,f): self.__faces = f[:]
    faces = property(__getFaces,__setFaces)
    r'''
    All faces :math:`\Fp = \Fpi \cup \Fpb` of the complex.
    
    '''    
    

    def __getInnerFaces1(self): return self.__innerFaces1
    innerFaces1 = property(__getInnerFaces1)
    r'''
    Inner faces :math:`\Fpi` according to categorization method 1.
    
    '''

    def __getInnerFaces2(self): return self.__innerFaces2
    innerFaces2 = property(__getInnerFaces2)
    r'''
    Inner faces :math:`\Fpi` according to categorization method 2.
    
    '''

    def __getInnerFaces(self): return self.pickCategory(self.__innerFaces1,self.__innerFaces2)
    innerFaces = property(__getInnerFaces)
    r'''
    Inner faces :math:`\Fpi` according to the currently selected categorization
    method.
    
    '''  



    def __getBorderFaces1(self): return self.__borderFaces1
    borderFaces1 = property(__getBorderFaces1)
    r'''
    Border faces :math:`\Fpb` according to categorization method 1.
    
    '''

    def __getBorderFaces2(self): return self.__borderFaces2
    borderFaces2 = property(__getBorderFaces2)
    r'''
    Border faces :math:`\Fpb` according to categorization method 2.
    
    '''

    def __getBorderFaces(self): return self.pickCategory(self.__borderFaces1,self.__borderFaces2)
    borderFaces = property(__getBorderFaces)
    r'''
    Border faces :math:`\Fpb` according to the currently selected categorization
    method.
    
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
    
    def __getIncidenceMatrix1iB(self):
        if self.__changedIncidenceMatrix1iB:
            self.__incidenceMatrix1iB = self.calcIncidence1(self.innerNodes,self.additionalBorderEdges)
            self.__changedIncidenceMatrix1iB = False
        return self.__incidenceMatrix1iB
    incidenceMatrix1iB = property(__getIncidenceMatrix1iB)
    r'''
    Incidence matrix :math:`\incpiB{1} \in \mathbb{R}^{|\Npi|\times|\EpB|}` 
    
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
    
    
    def __getIncidenceMatrix1bB(self):
        if self.__changedIncidenceMatrix1bB:
            self.__incidenceMatrix1bB = self.calcIncidence1(self.borderNodes,self.additionalBorderEdges)
            self.__changedIncidenceMatrix1bB = False
        return self.__incidenceMatrix1bB
    incidenceMatrix1bB = property(__getIncidenceMatrix1bB)
    r'''
    Incidence matrix :math:`\incpbB{1} \in \mathbb{R}^{|\Npb|\times|\EpB|}` 
    
    '''
    
    
    def __getIncidenceMatrix1Bi(self):
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
    
    
    def __getIncidenceMatrix1BB(self):
        if self.__changedIncidenceMatrix1BB:
            self.__incidenceMatrix1BB = self.calcIncidence1(self.additionalBorderNodes,self.additionalBorderEdges)
            self.__changedIncidenceMatrix1BB = False
        return self.__incidenceMatrix1BB
    incidenceMatrix1BB = property(__getIncidenceMatrix1BB)
    r'''
    Incidence matrix :math:`\incpBB{1} \in \mathbb{R}^{|\NpB|\times|\EpB|}` 
    
    '''
        
    
    
   
    def __getIncidenceMatrix1(self):
        incidencematrix1i = np.concatenate((self.incidenceMatrix1ii,self.incidenceMatrix1ib,self.incidenceMatrix1iB),axis=1)
        incidencematrix1b = np.concatenate((self.incidenceMatrix1bi,self.incidenceMatrix1bb,self.incidenceMatrix1bB),axis=1)
        incidencematrix1B = np.concatenate((self.incidenceMatrix1Bi,self.incidenceMatrix1Bb,self.incidenceMatrix1BB),axis=1)
        incidencematrix1 = np.concatenate((incidencematrix1i,incidencematrix1b,incidencematrix1B))
        return incidencematrix1
    incidenceMatrix1 = property(__getIncidenceMatrix1)
    r'''
    
    Complete incidence matrix :math:`\incp{1}` with 
    
    .. math::
        
        \incp{1} &=
        \begin{bmatrix}
            \incpii{1} & \incpib{1} & \incpiB{1} \\
            \incpbi{1} & \incpbb{1} & \incpbB{1} \\
            \incpBi{1} & \incpBb{1} & \incpBB{1}
        \end{bmatrix}.
    
    '''    
    
    

    def __getChangedIncidenceMatrix1ii(self): return self.__changedIncidenceMatrix1ii
    changedIncidenceMatrix1ii = property(__getChangedIncidenceMatrix1ii)

    def __getChangedIncidenceMatrix1ib(self): return self.__changedIncidenceMatrix1ib
    changedIncidenceMatrix1ib = property(__getChangedIncidenceMatrix1ib)

    def __getChangedIncidenceMatrix1iB(self): return self.__changedIncidenceMatrix1iB
    changedIncidenceMatrix1iB = property(__getChangedIncidenceMatrix1iB)

    def __getChangedIncidenceMatrix1bi(self): return self.__changedIncidenceMatrix1bi
    changedIncidenceMatrix1bi = property(__getChangedIncidenceMatrix1bi)

    def __getChangedIncidenceMatrix1bb(self): return self.__changedIncidenceMatrix1bb
    changedIncidenceMatrix1bb = property(__getChangedIncidenceMatrix1bb)

    def __getChangedIncidenceMatrix1bB(self): return self.__changedIncidenceMatrix1bB
    changedIncidenceMatrix1bB = property(__getChangedIncidenceMatrix1bB)

    def __getChangedIncidenceMatrix1Bi(self): return self.__changedIncidenceMatrix1Bi
    changedIncidenceMatrix1Bi = property(__getChangedIncidenceMatrix1Bi)

    def __getChangedIncidenceMatrix1Bb(self): return self.__changedIncidenceMatrix1Bb
    changedIncidenceMatrix1Bb = property(__getChangedIncidenceMatrix1Bb)

    def __getChangedIncidenceMatrix1BB(self): return self.__changedIncidenceMatrix1BB
    changedIncidenceMatrix1BB = property(__getChangedIncidenceMatrix1BB)



#-------------------------------------------------------------------------
#    Incidence matrices 2
#-------------------------------------------------------------------------
    
    def __getIncidenceMatrix2ii(self):
        if self.__changedIncidenceMatrix2ii:
            self.__incidenceMatrix2ii = self.calcIncidence2(self.innerEdges,self.innerFaces)
            self.__changedIncidenceMatrix2ii = False
        return self.__incidenceMatrix2ii
    incidenceMatrix2ii = property(__getIncidenceMatrix2ii)
    r'''
    Incidence matrix :math:`\incpii{2} \in \mathbb{R}^{|\Epi|\times|\Fpi|}` 
    
    '''

    def __getIncidenceMatrix2ib(self):
        if self.__changedIncidenceMatrix2ib:
            self.__incidenceMatrix2ib = self.calcIncidence2(self.innerEdges,self.borderFaces)
            self.__changedIncidenceMatrix2ib = False
        return self.__incidenceMatrix2ib
    incidenceMatrix2ib = property(__getIncidenceMatrix2ib)
    r'''
    Incidence matrix :math:`\incpib{2} \in \mathbb{R}^{|\Epi|\times|\Fpb|}` 
    
    '''
    
    
    def __getIncidenceMatrix2bi(self):
        if self.__changedIncidenceMatrix2bi:
            self.__incidenceMatrix2bi = self.calcIncidence2(self.borderEdges,self.innerFaces)
            self.__changedIncidenceMatrix2bi = False
        return self.__incidenceMatrix2bi
    incidenceMatrix2bi = property(__getIncidenceMatrix2bi)
    r'''
    Incidence matrix :math:`\incpbi{2} \in \mathbb{R}^{|\Epb|\times|\Fpi|}` 
    
    '''

    def __getIncidenceMatrix2bb(self):
        if self.__changedIncidenceMatrix2bb:
            self.__incidenceMatrix2bb = self.calcIncidence2(self.borderEdges,self.borderFaces)
            self.__changedIncidenceMatrix2bb = False
        return self.__incidenceMatrix2bb
    incidenceMatrix2bb = property(__getIncidenceMatrix2bb)
    r'''
    Incidence matrix :math:`\incpbb{2} \in \mathbb{R}^{|\Epb|\times|\Fpb|}` 
    
    '''


    
    
    def __getIncidenceMatrix2Bi(self):#
        if self.__changedIncidenceMatrix2Bi:
            self.__incidenceMatrix2Bi = self.calcIncidence2(self.additionalBorderEdges,self.innerFaces)
            self.__changedIncidenceMatrix2Bi = False
        return self.__incidenceMatrix2Bi
    incidenceMatrix2Bi = property(__getIncidenceMatrix2Bi)
    r'''
    Incidence matrix :math:`\incpBi{2} \in \mathbb{R}^{|\EpB|\times|\Fpi|}` 
    
    '''


    def __getIncidenceMatrix2Bb(self):
        if self.__changedIncidenceMatrix2Bb:
            self.__incidenceMatrix2Bb = self.calcIncidence2(self.additionalBorderEdges,self.borderFaces)
            self.__changedIncidenceMatrix2Bb = False
        return self.__incidenceMatrix2Bb
    incidenceMatrix2Bb = property(__getIncidenceMatrix2Bb)
    r'''
    Incidence matrix :math:`\incpBb{2} \in \mathbb{R}^{|\EpB|\times|\Fpb|}` 
    
    '''
    

    
    def __getIncidenceMatrix2(self):
        incidencematrix2i = np.concatenate((self.incidenceMatrix2ii,self.incidenceMatrix2ib),axis=1)
        incidencematrix2b = np.concatenate((self.incidenceMatrix2bi,self.incidenceMatrix2bb),axis=1)
        incidencematrix2B = np.concatenate((self.incidenceMatrix2Bi,self.incidenceMatrix2Bb),axis=1)
        incidencematrix2 = np.concatenate((incidencematrix2i,incidencematrix2b,incidencematrix2B))
        return incidencematrix2
    incidenceMatrix2 = property(__getIncidenceMatrix2)    
    r'''
    
    Complete incidence matrix :math:`\incp{2}` with 
    
    .. math::
        
        \incp{2} &=
        \begin{bmatrix}
            \incpii{2} & \incpib{2} \\
            \incpbi{2} & \incpbb{2} \\
            \incpBi{2} & \incpBb{2}
        \end{bmatrix}.
    
    '''
   
    def __getChangedIncidenceMatrix2ii(self): return self.__changedIncidenceMatrix2ii
    changedIncidenceMatrix2ii = property(__getChangedIncidenceMatrix2ii)

    def __getChangedIncidenceMatrix2ib(self): return self.__changedIncidenceMatrix2ib
    changedIncidenceMatrix2ib = property(__getChangedIncidenceMatrix2ib)

    def __getChangedIncidenceMatrix2bi(self): return self.__changedIncidenceMatrix2bi
    changedIncidenceMatrix2bi = property(__getChangedIncidenceMatrix2bi)

    def __getChangedIncidenceMatrix2bb(self): return self.__changedIncidenceMatrix2bb
    changedIncidenceMatrix2bb = property(__getChangedIncidenceMatrix2bb)

    def __getChangedIncidenceMatrix2Bi(self): return self.__changedIncidenceMatrix2Bi
    changedIncidenceMatrix2Bi = property(__getChangedIncidenceMatrix2Bi)

    def __getChangedIncidenceMatrix2Bb(self): return self.__changedIncidenceMatrix2Bb
    changedIncidenceMatrix2Bb = property(__getChangedIncidenceMatrix2Bb)

    
    
#==============================================================================
#    METHODS
#==============================================================================

#-------------------------------------------------------------------------
#    Set Up
#-------------------------------------------------------------------------  
    def setUp(self):
        '''
        
        '''
        self.logger.info('Called "Set Up" in Complex2D class')
        self.updateComplex2D()
    

    
    
#-------------------------------------------------------------------------
#    Sort according to category 1
#-------------------------------------------------------------------------     
    def sortPrimal(self):
        '''
        
        '''
        
        self.__innerNodes1 = []
        self.__borderNodes1 = []
        self.__additionalBorderNodes1 = []
        self.__innerEdges1 = []
        self.__borderEdges1 = []
        self.__additionalBorderEdges1 = []
        self.__innerFaces1 = []
        self.__borderFaces1 = []
        self.__geometricNodes = []
        
        # Sort faces
        for f in self.faces:
            if f.category1 == 'inner':
                self.addToList(f,self.innerFaces1)
            elif f.category1 == 'border':
                self.addToList(f,self.borderFaces1)
            else:
                self.logger.error('Unknown category1 {} of face {}'.format(f.category1,f))
                
                
                
        # Sort edges
        for e in self.edges:
            if e.category1 == 'inner':
                self.addToList(e,self.innerEdges1)
            elif e.category1 == 'border':
                self.addToList(e,self.borderEdges1)
            elif e.category1 == 'additionalBorder':
                self.addToList(e,self.additionalBorderEdges1)
            else:
                self.logger.error('Unknown category1 {} of edge {}'.format(e.category1,e))       
                
                
                
        # Sort nodes
        for e in self.edges:
            for n in e.geometricNodes:
                if not n in self.nodes:
                    self.nodes.append(n)
                    
        for n in self.nodes:
            if n.isGeometrical:
                if not n in self.geometricNodes:
                    self.geometricNodes.append(n)
        
        
        for n in self.geometricNodes:
            if n in self.nodes:
                self.nodes.remove(n)
                    
        for n in self.nodes:
            if n.category1 == 'inner':
                self.addToList(n,self.innerNodes1)
            elif n.category1 == 'border':
                self.addToList(n,self.borderNodes1)
            elif n.category1 == 'additionalBorder':
                self.addToList(n,self.additionalBorderNodes1)
            else:
                self.logger.error('Unknown category1 {} of node {}'.format(n.category1,n))       
    

#-------------------------------------------------------------------------
#    Sort according to category 2
#-------------------------------------------------------------------------  

    def sortDual(self):
        '''
        
        '''
        
        self.__innerNodes2 = []
        self.__borderNodes2 = []
        self.__additionalBorderNodes2 = []
        self.__innerEdges2 = []
        self.__borderEdges2 = []
        self.__additionalBorderEdges2 = []
        self.__innerFaces2 = []
        self.__borderFaces2 = []
        
        # Sort faces
        for f in self.faces:
            if f.category2 == 'inner':
                self.addToList(f,self.innerFaces2)
            elif f.category2 == 'border':
                self.addToList(f,self.borderFaces2)
            else:
                self.logger.error('Unknown category2 {} of face {}'.format(f.category2,f))
                
                
                
        # Sort edges
        for e in self.edges:
            if e.category2 == 'inner':
                self.addToList(e,self.innerEdges2)
            elif e.category2 == 'border':
                self.addToList(e,self.borderEdges2)
            elif e.category2 == 'additionalBorder':
                self.addToList(e,self.additionalBorderEdges2)
            else:
                self.logger.error('Unknown category2 {} of edge {}'.format(e.category2,e))       
                
                
                
        # Sort nodes
        for n in self.nodes:
            if n.isGeometrical:
                self.logger.error('Geometrical nodes should not be in the list of nodes anymore')
        
        for n in self.nodes:
            if n.category2 == 'inner':
                self.addToList(n,self.innerNodes2)
            elif n.category2 == 'border':
                self.addToList(n,self.borderNodes2)
            elif n.category2 == 'additionalBorder':
                self.addToList(n,self.additionalBorderNodes2)
            else:
                self.logger.error('Unknown category2 {} of node {}'.format(n.category2,n))      
    
    
    
    
    
    
#-------------------------------------------------------------------------
#    Determine max range for each dimension
#-------------------------------------------------------------------------          
    def __calcLimits(self):
        '''
        
        '''
        self.logger.info('Calculating limits')
        self.__xMax = self.myMax([n.xCoordinate for n in self.nodes])
        self.__yMax = self.myMax([n.yCoordinate for n in self.nodes])
        self.__xMin = self.myMin([n.xCoordinate for n in self.nodes])
        self.__yMin = self.myMin([n.yCoordinate for n in self.nodes])
        self.__xLim = [self.__xMin,self.__xMax]
        self.__yLim = [self.__yMin,self.__yMax]
        self.__changedLimits = False    
        
        
        
#-------------------------------------------------------------------------
#    Update incidence matrices
#-------------------------------------------------------------------------      
    def updateComplex2D(self):
        self.__changedIncidenceMatrix1ii = True
        self.__changedIncidenceMatrix1ib = True
        self.__changedIncidenceMatrix1iB = True
        self.__changedIncidenceMatrix1bi = True
        self.__changedIncidenceMatrix1bb = True
        self.__changedIncidenceMatrix1bB = True
        self.__changedIncidenceMatrix1Bi = True
        self.__changedIncidenceMatrix1Bb = True
        self.__changedIncidenceMatrix1BB = True
        
        self.__changedIncidenceMatrix2ii = True
        self.__changedIncidenceMatrix2ib = True
        self.__changedIncidenceMatrix2bi = True
        self.__changedIncidenceMatrix2bb = True
        self.__changedIncidenceMatrix2Bi = True
        self.__changedIncidenceMatrix2Bb = True   
        
        self.__changedLimits = True
    
    
#-------------------------------------------------------------------------
#    Plot using pyplot
#-------------------------------------------------------------------------      

    def plotComplex(self,ax,*args,**kwargs):
        '''
        
        '''
       
        for f in self.__faces:
            f.plotFace(ax,*args,**kwargs)            
        for e in self.__edges:        
            e.plotEdge(ax,*args,**kwargs)
            
        for n in self.__nodes:        
            n.plotNode(ax,*args,**kwargs)
        ax.view_init(90,-90)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_xlim(self.xLim)
        ax.set_ylim(self.yLim)
        
        
#-------------------------------------------------------------------------
#    Plot using TikZ
#-------------------------------------------------------------------------               
        
    def plotComplexTikZ(self,tikZPicture=None,plotNodes=True,plotEdges=True,plotFaces=True,tikZName=None,**kwargs):
        '''
        
        '''
        if tikZPicture is None:
            tikZPicture = TikZPicture2D(name=tikZName)
            
            
        if tikZPicture.dim != 2:
            self.logger.error('Trying to plot in a 3-dimensional tikZPicture, but a 1-D complex should be plotted in a 2D-picture')
        else:
            
            if plotNodes:
                for n in self.nodes+self.geometricNodes:
                    n.plotNodeTikZ(tikZPicture,dim=2,**kwargs)
            else:
                for n in self.nodes+self.geometricNodes:
                    n.plotNodeTikZ(tikZPicture,dim=2,draw=False)
                    
            if plotEdges:
                for e in self.edges:
                    e.plotEdgeTikZ(tikZPicture,**kwargs)
                    
            if plotFaces:
                for f in self.faces:
                    f.plotFaceTikZ(tikZPicture,**kwargs)   
        return tikZPicture
    
    
    
    def plotNodesTikZ(self,*args,**kwargs):
        '''
        
        '''
        return self.plotComplexTikZ(*args,plotEdges=False,plotFaces=False,**kwargs)
    
    def plotEdgesTikZ(self,*args,**kwargs):
        '''
        
        '''
        return self.plotComplexTikZ(*args,plotNodes=False,plotFaces=False,**kwargs)
    
    def plotFacesTikZ(self,*args,**kwargs):
        '''
        
        '''
        return self.plotComplexTikZ(*args,plotNodes=False,plotEdges=False,**kwargs)
        
 
    
    
    def printCategories(self):
        '''
        
        '''
        self.printHeadline('NODES',cc.printRed)
        
        headlineNodes = ['Node','category1','category2']
        tableContentNodes = [headlineNodes,]
        
        for n in self.nodes:
            tableContentNodes.append([n.infoText,n.category1,n.category2])
            
        tableNodes = Table(tableContentNodes)
        tableNodes.printTable()

        self.printHeadline('EDGES',cc.printBlue)
        
        headlineEdges = ['Edge','category1','category2']
        tableContentEdges = [headlineEdges,]
        
        for e in self.edges:
            tableContentEdges.append([e.infoText,e.category1,e.category2])
            
        tableEdges = Table(tableContentEdges)
        tableEdges.printTable()


        
    def printDualities(self):    
        '''
        
        '''
        self.printHeadline('NODES',cc.printRed)        
        headlineNodes = ['Node','2D dual','1D dual','0D dual']
        tableContentNodes = [headlineNodes,]        
        for n in self.nodes:
            tableContentNodes.append([n.infoText,n.dualCell2D,n.dualCell1D,n.dualCell0D])
        tableNodes = Table(tableContentNodes)
        tableNodes.printTable()
        
        
        self.printHeadline('EDGES',cc.printBlue)    
        headlineEdges = ['Edge','2D dual','1D dual']
        tableContentEdges = [headlineEdges,]        
        for e in self.edges:
            tableContentEdges.append([e.infoText,e.dualCell2D,e.dualCell1D])
        tableEdges = Table(tableContentEdges)
        tableEdges.printTable()
            
            
        self.printHeadline('FACES',cc.printGreen)    
        headlineFaces = ['Face','2D dual']
        tableContentFaces = [headlineFaces,]        
        for f in self.faces:
            tableContentFaces.append([f.infoText,f.dualCell2D])
        tableFaces = Table(tableContentFaces)
        tableFaces.printTable()
                  
    
            
    



               
    
        
    
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
            
if __name__ == '__main__':
    import tools.placeFigures as pf
    from tools.myLogging import MyLogging
    
    with MyLogging('complex2D'):
        
        cc.printBlue('Create nodes')
        n0 = Node(0,0,0)
        n1 = Node(1,0,0)
        n2 = Node(1.5,0,0)
        n3 = Node(0,1,0)
        n4 = Node(1,1,0)
        n5 = Node(0,1.5,0)
        n6 = Node(1.5,1.5,0)
        
        
        
        nodes = [n0,n1,n2,n3,n4,n5,n6]
        
        
        cc.printBlue('Create edges')
        e0 = Edge(n0,n1)
        e1 = Edge(n1,n2)
        e2 = Edge(n3,n4)
        e3 = Edge(n5,n6)
        e4 = Edge(n0,n3)
        e5 = Edge(n1,n4)
        e6 = Edge(n2,n6)
        e7 = Edge(n3,n5)
        e8 = Edge(n4,n6)
        edges = [e0,e1,e2,e3,e4,e5,e6,e7,e8]
        
        
        cc.printBlue('Create faces')
        f0 = Face([e0,e5,-e2,-e4])
        f1 = Face([e1,e6,-e8,-e5])
        f2 = Face([e2,e8,-e3,-e7])
        
        faces = [f0,f1,f2]
        
        
        cc.printBlue('Combine them to a complex')
        c = Complex2D(nodes,edges,faces)

    
    
        
        
#-------------------------------------------------------------------------
#    Plotting
#-------------------------------------------------------------------------    
    
        # Choose plotting method. Possible choices: pyplot, VTK, TikZ, animation, None
        plottingMethod = 'TikZ'   
        
        
#    Disabled
#--------------------------------------------------------------------- 
        if plottingMethod is None or plottingMethod == 'None':
            cc.printBlue('Plotting disabled')
        
#    Pyplot
#---------------------------------------------------------------------         
        elif plottingMethod == 'pyplot':
            cc.printBlue('Plot using pyplot')
            (figs,axes) = pf.getFigures()
            
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
            file = True
            pic.writeLaTeXFile('latex','complex2D',compileFile=file,openFile=file)
            
#    Animation
#--------------------------------------------------------------------- 
        elif plottingMethod == 'animation':
            cc.printBlue('Creating animation')
            cc.printRed('Not implemented')

#    Unknown
#---------------------------------------------------------------------             
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))      
    