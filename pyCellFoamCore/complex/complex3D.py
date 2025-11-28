# -*- coding: utf-8 -*-
#==============================================================================
# COMPLEX 3D
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Dec 15 17:58:41 2017

r'''
On incidence matrices:
--------------------------------------------------------------------------

:math:`\partial^1`:  Primal nodes and edges

:math:`\partial^2`:  Primal edges and faces

:math:`\partial^2`:  Primal faces and volumes

.. math::

   \hat{\partial}_{ii}^1 &= - (\partial_{ii}^3)^\mathrm{T} \\
   \hat{\partial}_{ib}^1 &= - (\partial_{bi}^3)^\mathrm{T} \\
   \hat{\partial}_{bi}^1 &= - (\partial_{ib}^3)^\mathrm{T} \\
   \hat{\partial}_{bb}^1 &= - (\partial_{bb}^3)^\mathrm{T} = 0






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
import logging
import numpy as np
import matplotlib.pyplot as plt

from itertools import chain,islice
from tabulate import tabulate
import pathlib

#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------


#    kCells
#--------------------------------------------------------------------
from pyCellFoamCore.k_cells.node.node import Node
from pyCellFoamCore.k_cells.edge.edge import Edge
from pyCellFoamCore.k_cells.face.face import Face
from pyCellFoamCore.k_cells.volume.volume import Volume

#    Complex & Grids
#--------------------------------------------------------------------
from pyCellFoamCore.complex.complex import Complex

#    Tools
#--------------------------------------------------------------------
import pyCellFoamCore.tools.placeFigures as pf
import pyCellFoamCore.tools.colorConsole as cc
import pyCellFoamCore.tools.myVTK as myv
import pyCellFoamCore.tools.tumcolor as tc

from pyCellFoamCore.tools.tikZPicture.tikZPicture3D import TikZPicture3D
from pyCellFoamCore.tools.printTable import Table


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)



#==============================================================================
#    CLASS DEFINITION
#==============================================================================
class Complex3D(Complex):
    '''
    Description

    '''

#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__nodes',
                 '__edges',
                 '__faces',
                 '__volumes',
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
                 '__geometricEdges',
                 '__xLim','__xMin','__xMax',
                 '__yLim','__yMin','__yMax',
                 '__zLim','__zMin','__zMax',
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
                 '__incidenceMatrix2iB','__changedIncidenceMatrix2iB',
                 '__incidenceMatrix2bi','__changedIncidenceMatrix2bi',
                 '__incidenceMatrix2bb','__changedIncidenceMatrix2bb',
                 '__incidenceMatrix2bB','__changedIncidenceMatrix2bB',
                 '__incidenceMatrix2Bi','__changedIncidenceMatrix2Bi',
                 '__incidenceMatrix2Bb','__changedIncidenceMatrix2Bb',
                 '__incidenceMatrix2BB','__changedIncidenceMatrix2BB',
                 '__incidenceMatrix3ii','__changedIncidenceMatrix3ii',
                 '__incidenceMatrix3ib','__changedIncidenceMatrix3ib',
                 '__incidenceMatrix3bi','__changedIncidenceMatrix3bi',
                 '__incidenceMatrix3bb','__changedIncidenceMatrix3bb',
                 '__incidenceMatrix3Bi','__changedIncidenceMatrix3Bi',
                 '__incidenceMatrix3Bb','__changedIncidenceMatrix3Bb',
                 '__errorCells')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,
                 nodes=[],
                 edges=[],
                 faces=[],
                 volumes=[]):

        '''
        Description

        '''

        _log.info("Initialize Complex3D")


#        self.__myDual = myDual

        self.__nodes = nodes
        self.__edges = edges
        self.__faces = faces
        self.__volumes = volumes



        # Initialize lists for nodes
        self.__innerNodes1 = []
        self.__borderNodes1 = []
        self.__additionalBorderNodes1 = []
        self.__innerNodes2 = []
        self.__borderNodes2 = []
        self.__additionalBorderNodes2 = []
        self.__geometricNodes = []


        # Initialize lists for edges
        self.__innerEdges1 = []
        self.__borderEdges1 = []
        self.__additionalBorderEdges1 = []
        self.__innerEdges2 = []
        self.__borderEdges2 = []
        self.__additionalBorderEdges2 = []
        self.__geometricEdges = []


        # Initialize lists for faces
        self.__borderFaces1 = []
        self.__innerFaces1 = []
        self.__additionalBorderFaces1 = []
        self.__borderFaces2 = []
        self.__innerFaces2 = []
        self.__additionalBorderFaces2 = []

        # Initialize lists for volumes
        self.__innerVolumes1 = []
        self.__borderVolumes1 = []
        self.__innerVolumes2 = []
        self.__borderVolumes2 = []



        self.__errorCells = []

        self.__xLim = None
        self.__xMin = None
        self.__xMax = None
        self.__yLim = None
        self.__yMin = None
        self.__yMax = None
        self.__zLim = None
        self.__zMin = None
        self.__zMax = None
        self.__changedLimits = True



        super().__init__()










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
        return self.__yMax
    yMax = property(__getYMax)
    '''
    Maximal y-coordinate of all nodes in the complex.

    '''

    def __getZLim(self):
        if self.__changedLimits:
            self.__calcLimits()
        return self.__zLim
    zLim = property(__getZLim)
    '''
    Range of z-coordinates of all nodes in the complex.

    '''


    def __getZMin(self):
        if self.__changedLimits:
            self.__calcLimits()
        return self.__zMin
    zMin = property(__getZMin)
    '''
    Minimal z-coordinate of all nodes in the complex.

    '''

    def __getZMax(self):
        if self.__changedLimits:
            self.__calcLimits()
        return self.__zMax
    zMax = property(__getZMax)
    '''
    Maximal z-coordinate of all nodes in the complex.

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


    def __getGeometricNodes(self):
#        if self.changedNumbering:
#            self.renumber()
        return self.__geometricNodes
    def __setGeometricNodes(self,n): self.__geometricNodes = n[:]
    geometricNodes = property(__getGeometricNodes,__setGeometricNodes)
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


    def __getGeometricEdges(self):
#        if self.changedNumbering:
#            self.renumber()
        return self.__geometricEdges
    def __setGeometricEdges(self,e): self.__geometricEdges = e[:]
    geometricEdges = property(__getGeometricEdges,__setGeometricEdges)

#-------------------------------------------------------------------------
#    Faces
#-------------------------------------------------------------------------

    def __getFaces(self):
        if self.changedNumbering:
            self.renumber()
        return self.__faces
    def __setFaces(self,e): self.__faces = e[:]
    faces = property(__getFaces,__setFaces)
    r'''
    All faces :math:`\Fp = \Fpi \cup \Fpb \cup \FpB` of the complex.

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

    def __getAdditionalBorderFaces1(self): return self.__additionalBorderFaces1
    additionalBorderFaces1 = property(__getAdditionalBorderFaces1)
    r'''
    Additional border faces :math:`\Fpb` according to categorization method 1.

    '''

    def __getAdditionalBorderFaces2(self): return self.__additionalBorderFaces2
    additionalBorderFaces2 = property(__getAdditionalBorderFaces2)
    r'''
    Additional border faces :math:`\Fpb` according to categorization method 2.

    '''

    def __getAdditionalBorderFaces(self): return self.pickCategory(self.__additionalBorderFaces1,self.__additionalBorderFaces2)
    additionalBorderFaces = property(__getAdditionalBorderFaces)
    r'''
    Additional border faces :math:`\FpB` according to the currently selected
    categorization method.

    '''








    def __getInnerVolumes1(self): return self.__innerVolumes1
    def __setInnerVolumes1(self,i): self.__innerVolumes1 = i
    innerVolumes1 = property(__getInnerVolumes1,__setInnerVolumes1)
    '''

    '''

    def __getInnerVolumes2(self): return self.__innerVolumes2
    def __setInnerVolumes2(self,i): self.__innerVolumes2 = i
    innerVolumes2 = property(__getInnerVolumes2,__setInnerVolumes2)
    '''

    '''

    def __getBorderVolumes1(self): return self.__borderVolumes1
    def __setBorderVolumes1(self,b): self.__borderVolumes1 = b
    borderVolumes1 = property(__getBorderVolumes1,__setBorderVolumes1)
    '''

    '''

    def __getBorderVolumes2(self): return self.__borderVolumes2
    def __setBorderVolumes2(self,b): self.__borderVolumes2 = b
    borderVolumes2 = property(__getBorderVolumes2,__setBorderVolumes2)
    '''

    '''





    def __getVolumes(self): return self.__volumes
    def __setVolumes(self,v): self.__volumes = v[:]
    volumes = property(__getVolumes,__setVolumes)
    '''

    '''






    def __getInnerVolumes(self): return self.pickCategory(self.__innerVolumes1,self.__innerVolumes2)
    innerVolumes = property(__getInnerVolumes)
    '''

    '''

    def __getBorderVolumes(self): return self.pickCategory(self.__borderVolumes1,self.__borderVolumes2)
    borderVolumes = property(__getBorderVolumes)
    '''

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

    def __getIncidenceMatrix2iB(self):
        if self.__changedIncidenceMatrix2iB:
            self.__incidenceMatrix2iB = self.calcIncidence2(self.innerEdges,self.additionalBorderFaces)
            self.__changedIncidenceMatrix2iB = False
        return self.__incidenceMatrix2iB
    incidenceMatrix2iB = property(__getIncidenceMatrix2iB)
    r'''
    Incidence matrix :math:`\incpiB{2} \in \mathbb{R}^{|\Epi|\times|\FpB|}`

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


    def __getIncidenceMatrix2bB(self):
        if self.__changedIncidenceMatrix2bB:
            self.__incidenceMatrix2bB = self.calcIncidence2(self.borderEdges,self.additionalBorderFaces)
            self.__changedIncidenceMatrix2bB = False
        return self.__incidenceMatrix2bB
    incidenceMatrix2bB = property(__getIncidenceMatrix2bB)
    r'''
    Incidence matrix :math:`\incpbB{2} \in \mathbb{R}^{|\Epb|\times|\FpB|}`

    '''


    def __getIncidenceMatrix2Bi(self):
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


    def __getIncidenceMatrix2BB(self):
        if self.__changedIncidenceMatrix2BB:
            self.__incidenceMatrix2BB = self.calcIncidence2(self.additionalBorderEdges,self.additionalBorderFaces)
            self.__changedIncidenceMatrix2BB = False
        return self.__incidenceMatrix2BB
    incidenceMatrix2BB = property(__getIncidenceMatrix2BB)
    r'''
    Incidence matrix :math:`\incpBB{2} \in \mathbb{R}^{|\EpB|\times|\FpB|}`

    '''




    def __getIncidenceMatrix2(self):
        incidencematrix2i = np.concatenate((self.incidenceMatrix2ii,self.incidenceMatrix2ib,self.incidenceMatrix2iB),axis=1)
        incidencematrix2b = np.concatenate((self.incidenceMatrix2bi,self.incidenceMatrix2bb,self.incidenceMatrix2bB),axis=1)
        incidencematrix2B = np.concatenate((self.incidenceMatrix2Bi,self.incidenceMatrix2Bb,self.incidenceMatrix2BB),axis=1)
        incidencematrix2 = np.concatenate((incidencematrix2i,incidencematrix2b,incidencematrix2B))
        return incidencematrix2
    incidenceMatrix2 = property(__getIncidenceMatrix2)
    r'''

    Complete incidence matrix :math:`\incp{2}` with

    .. math::

        \incp{2} &=
        \begin{bmatrix}
            \incpii{2} & \incpib{2} & \incpiB{2} \\
            \incpbi{2} & \incpbb{2} & \incpbB{2} \\
            \incpBi{2} & \incpBb{2} & \incpBB{2}
        \end{bmatrix}.

    '''



    def __getChangedIncidenceMatrix2ii(self): return self.__changedIncidenceMatrix2ii
    changedIncidenceMatrix2ii = property(__getChangedIncidenceMatrix2ii)

    def __getChangedIncidenceMatrix2ib(self): return self.__changedIncidenceMatrix2ib
    changedIncidenceMatrix2ib = property(__getChangedIncidenceMatrix2ib)

    def __getChangedIncidenceMatrix2iB(self): return self.__changedIncidenceMatrix2iB
    changedIncidenceMatrix2iB = property(__getChangedIncidenceMatrix2iB)

    def __getChangedIncidenceMatrix2bi(self): return self.__changedIncidenceMatrix2bi
    changedIncidenceMatrix2bi = property(__getChangedIncidenceMatrix2bi)

    def __getChangedIncidenceMatrix2bb(self): return self.__changedIncidenceMatrix2bb
    changedIncidenceMatrix2bb = property(__getChangedIncidenceMatrix2bb)

    def __getChangedIncidenceMatrix2bB(self): return self.__changedIncidenceMatrix2bB
    changedIncidenceMatrix2bB = property(__getChangedIncidenceMatrix2bB)

    def __getChangedIncidenceMatrix2Bi(self): return self.__changedIncidenceMatrix2Bi
    changedIncidenceMatrix2Bi = property(__getChangedIncidenceMatrix2Bi)

    def __getChangedIncidenceMatrix2Bb(self): return self.__changedIncidenceMatrix2Bb
    changedIncidenceMatrix2Bb = property(__getChangedIncidenceMatrix2Bb)

    def __getChangedIncidenceMatrix2BB(self): return self.__changedIncidenceMatrix2BB
    changedIncidenceMatrix2BB = property(__getChangedIncidenceMatrix2BB)





#-------------------------------------------------------------------------
#    Incidence matrices 3
#-------------------------------------------------------------------------

    def __getIncidenceMatrix3ii(self):
        if self.__changedIncidenceMatrix3ii:
            self.__incidenceMatrix3ii = self.calcIncidence3(self.innerFaces,self.innerVolumes)
            self.__changedIncidenceMatrix3ii = False
        return self.__incidenceMatrix3ii
    incidenceMatrix3ii = property(__getIncidenceMatrix3ii)
    r'''
    Incidence matrix :math:`\incpii{3} \in \mathbb{R}^{|\Fpi|\times|\Vpi|}`

    '''

    def __getIncidenceMatrix3ib(self):
        if self.__changedIncidenceMatrix3ib:
            self.__incidenceMatrix3ib = self.calcIncidence3(self.innerFaces,self.borderVolumes)
            self.__changedIncidenceMatrix3ib = False
        return self.__incidenceMatrix3ib
    incidenceMatrix3ib = property(__getIncidenceMatrix3ib)
    r'''
    Incidence matrix :math:`\incpib{3} \in \mathbb{R}^{|\Fpi|\times|\Vpb|}`

    '''


    def __getIncidenceMatrix3bi(self):
        if self.__changedIncidenceMatrix3bi:
            self.__incidenceMatrix3bi = self.calcIncidence3(self.borderFaces,self.innerVolumes)
            self.__changedIncidenceMatrix3bi = False
        return self.__incidenceMatrix3bi
    incidenceMatrix3bi = property(__getIncidenceMatrix3bi)
    r'''
    Incidence matrix :math:`\incpbi{3} \in \mathbb{R}^{|\Fpb|\times|\Vpi|}`

    '''

    def __getIncidenceMatrix3bb(self):
        if self.__changedIncidenceMatrix3bb:
            self.__incidenceMatrix3bb = self.calcIncidence3(self.borderFaces,self.borderVolumes)
            self.__changedIncidenceMatrix3bb = False
        return self.__incidenceMatrix3bb
    incidenceMatrix3bb = property(__getIncidenceMatrix3bb)
    r'''
    Incidence matrix :math:`\incpbb{3} \in \mathbb{R}^{|\Fpb|\times|\Vpb|}`

    '''




    def __getIncidenceMatrix3Bi(self):#
        if self.__changedIncidenceMatrix3Bi:
            self.__incidenceMatrix3Bi = self.calcIncidence3(self.additionalBorderFaces,self.innerVolumes)
            self.__changedIncidenceMatrix3Bi = False
        return self.__incidenceMatrix3Bi
    incidenceMatrix3Bi = property(__getIncidenceMatrix3Bi)
    r'''
    Incidence matrix :math:`\incpBi{3} \in \mathbb{R}^{|\FpB|\times|\Vpi|}`

    '''


    def __getIncidenceMatrix3Bb(self):
        if self.__changedIncidenceMatrix3Bb:
            self.__incidenceMatrix3Bb = self.calcIncidence3(self.additionalBorderFaces,self.borderVolumes)
            self.__changedIncidenceMatrix3Bb = False
        return self.__incidenceMatrix3Bb
    incidenceMatrix3Bb = property(__getIncidenceMatrix3Bb)
    r'''
    Incidence matrix :math:`\incpBb{3} \in \mathbb{R}^{|\FpB|\times|\Vpb|}`

    '''



    def __getIncidenceMatrix3(self):
        incidencematrix3i = np.concatenate((self.incidenceMatrix3ii,self.incidenceMatrix3ib),axis=1)
        incidencematrix3b = np.concatenate((self.incidenceMatrix3bi,self.incidenceMatrix3bb),axis=1)
        incidencematrix3B = np.concatenate((self.incidenceMatrix3Bi,self.incidenceMatrix3Bb),axis=1)
        incidencematrix3 = np.concatenate((incidencematrix3i,incidencematrix3b,incidencematrix3B))
        return incidencematrix3
    incidenceMatrix3 = property(__getIncidenceMatrix3)
    r'''

    Complete incidence matrix :math:`\incp{3}` with

    .. math::

        \incp{3} &=
        \begin{bmatrix}
            \incpii{3} & \incpib{3} \\
            \incpbi{3} & \incpbb{3} \\
            \incpBi{3} & \incpBb{3}
        \end{bmatrix}.

    '''

    def __getChangedIncidenceMatrix3ii(self): return self.__changedIncidenceMatrix3ii
    changedIncidenceMatrix3ii = property(__getChangedIncidenceMatrix3ii)

    def __getChangedIncidenceMatrix3ib(self): return self.__changedIncidenceMatrix3ib
    changedIncidenceMatrix3ib = property(__getChangedIncidenceMatrix3ib)

    def __getChangedIncidenceMatrix3bi(self): return self.__changedIncidenceMatrix3bi
    changedIncidenceMatrix3bi = property(__getChangedIncidenceMatrix3bi)

    def __getChangedIncidenceMatrix3bb(self): return self.__changedIncidenceMatrix3bb
    changedIncidenceMatrix3bb = property(__getChangedIncidenceMatrix3bb)

    def __getChangedIncidenceMatrix3Bi(self): return self.__changedIncidenceMatrix3Bi
    changedIncidenceMatrix3Bi = property(__getChangedIncidenceMatrix3Bi)

    def __getChangedIncidenceMatrix3Bb(self): return self.__changedIncidenceMatrix3Bb
    changedIncidenceMatrix3Bb = property(__getChangedIncidenceMatrix3Bb)












    def __getErrorCells(self): return self.__errorCells
    errorCells = property(__getErrorCells)



    def __getLatexPreamble(self):
        _log.error('Deprecated - Do not use')
        return ''
    latexPreamble=property(__getLatexPreamble)


#==============================================================================
#    MAGIC METHODS
#==============================================================================
    def  __repr__(self):
        return 'Complex3D with {} nodes, {} edges, {} faces and {} volumes'.format(len(self.nodes),len(self.edges),len(self.faces),len(self.volumes))


#==============================================================================
#    METHODS
#==============================================================================


    def setUp(self):
        '''

        '''
        _log.info('Called "Set Up" in Complex3D class')
        self.updateComplex3D()






#-------------------------------------------------------------------------
#    Determine max range for each dimension
#-------------------------------------------------------------------------
    def __calcLimits(self):
        '''

        '''
        _log.info('Calculating limits')
        self.__xMax = self.myMax([n.xCoordinate for n in self.nodes])
        self.__yMax = self.myMax([n.yCoordinate for n in self.nodes])
        self.__zMax = self.myMax([n.zCoordinate for n in self.nodes])
        self.__xMin = self.myMin([n.xCoordinate for n in self.nodes])
        self.__yMin = self.myMin([n.yCoordinate for n in self.nodes])
        self.__zMin = self.myMin([n.zCoordinate for n in self.nodes])
        self.__xLim = [self.__xMin,self.__xMax]
        self.__yLim = [self.__yMin,self.__yMax]
        self.__zLim = [self.__zMin,self.__zMax]
        self.__changedLimits = False







    def sortPrimal(self):
        '''

        '''

        self.__innerNodes1 = []
        self.__borderNodes1 = []
        self.__additionalBorderNodes1 = []
        self.__innerEdges1 = []
        self.__borderEdges1 = []
        self.__additionalBorderEdges1 = []
        self.__borderFaces1 = []
        self.__innerFaces1 = []
        self.__additionalBorderFaces1 = []
        self.__innerVolumes1 = []
        self.__borderVolumes1 = []


        if True:
            for n in self.__nodes:
                if n.category1 == 'inner':
                    self.addToList(n,self.__innerNodes1)
                elif n.category1 == 'border':
                    self.addToList(n,self.__borderNodes1)
                elif n.category1 == 'additionalBorder':
                    self.addToList(n,self.__additionalBorderNodes1)
                else:
                    _log.error('Unknown category1 {} of {}'.format(n.category1,n))
                    self.errorCells.append(n)

            for e in self.__edges:
                if e.category1 == 'inner':
                    self.addToList(e,self.__innerEdges1)
                elif e.category1 == 'border':
                    self.addToList(e,self.__borderEdges1)
                elif e.category1 == 'additionalBorder':
                    self.addToList(e,self.__additionalBorderEdges1)
                else:
                    _log.error('Unknown category1 {} of {}'.format(e.category1,e))


            for f in self.__faces:
                if f.category1 == 'inner':
                    self.addToList(f,self.__innerFaces1)
                elif f.category1 == 'border':
                    self.addToList(f,self.__borderFaces1)
                elif f.category1 == 'additionalBorder':
                    self.addToList(f,self.__additionalBorderFaces1)
                else:
                    _log.error('Unknown category1 {} of {}'.format(f.category1,f))



            for v in self.__volumes:
                if v.category1 == 'inner':
                    self.addToList(v,self.__innerVolumes1)
                elif v.category1 == 'border':
                    self.addToList(v,self.__borderVolumes1)
                else:
                    _log.error('Unknown category1 {} of {}'.format(v.category1,v))



    def sortDual(self):
        '''

        '''

        self.__innerNodes2 = []
        self.__borderNodes2 = []
        self.__additionalBorderNodes2 = []
        self.__innerEdges2 = []
        self.__borderEdges2 = []
        self.__additionalBorderEdges2 = []
        self.__borderFaces2 = []
        self.__innerFaces2 = []
        self.__additionalBorderFaces2 = []
        self.__innerVolumes2 = []
        self.__borderVolumes2 = []

        if True:
            for n in self.__nodes:
                if n.category2 == 'inner':
                    self.addToList(n,self.__innerNodes2)
                elif n.category2 == 'border':
                    self.addToList(n,self.__borderNodes2)
                elif n.category2 == 'additionalBorder':
                    self.addToList(n,self.__additionalBorderNodes2)
                else:
                    _log.error('Unknown category2 {} of {}'.format(n.category2,n))


            for e in self.__edges:
                if e.category2 == 'inner':
                    self.addToList(e,self.__innerEdges2)
                elif e.category2 == 'border':
                    self.addToList(e,self.__borderEdges2)
                elif e.category2 == 'additionalBorder':
                    self.addToList(e,self.__additionalBorderEdges2)
                else:
                    _log.error('Unknown category2 {} of {}'.format(e.category2,e))


            for f in self.__faces:
                if f.category2 == 'inner':
                    self.addToList(f,self.__innerFaces2)
                elif f.category2 == 'border':
                    self.addToList(f,self.__borderFaces2)
                elif f.category2 == 'additionalBorder':
                    self.addToList(f,self.__additionalBorderFaces2)
                else:
                    _log.error('Unknown category2 {} of {}'.format(f.category2,f))


            for v in self.__volumes:
                if v.category2 == 'inner':
                    self.addToList(v,self.__innerVolumes2)
                elif v.category2 == 'border':
                    self.addToList(v,self.__borderVolumes2)
                else:
                    _log.error('Unknown category2 {} of {}'.format(v.category2,v))








#-------------------------------------------------------------------------
#    Renumbering
#-------------------------------------------------------------------------
#    def _renumber(self,cells):

#
#    def pickCategory(self,opt1,opt2):
#        if self.useCategory == 1:
#            return opt1
#        elif self.useCategory == 2:
#            return opt2
#        else:
#            _log.error('useCategory is set to {} - this is not ok: only 1 and 2 is allowed')
#            return None

#-------------------------------------------------------------------------
#    Update
#-------------------------------------------------------------------------
    def updateComplex3D(self):
        '''

        '''
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
        self.__changedIncidenceMatrix2iB = True
        self.__changedIncidenceMatrix2bi = True
        self.__changedIncidenceMatrix2bb = True
        self.__changedIncidenceMatrix2bB = True
        self.__changedIncidenceMatrix2Bi = True
        self.__changedIncidenceMatrix2Bb = True
        self.__changedIncidenceMatrix2BB = True

        self.__changedIncidenceMatrix3ii = True
        self.__changedIncidenceMatrix3ib = True
        self.__changedIncidenceMatrix3bi = True
        self.__changedIncidenceMatrix3bb = True
        self.__changedIncidenceMatrix3Bi = True
        self.__changedIncidenceMatrix3Bb = True

        self.__changedLimits = True







#-------------------------------------------------------------------------
#    Plot using pyplot
#-------------------------------------------------------------------------



    def plotComplex(self,ax,plotNodes=True,plotEdges=True,plotFaces=False,plotVolumes=False,plotGeometric=True,axisEqual=True,**kwargs):
        '''

        '''
        if plotNodes:
            for n in self.nodes:
                n.plotNode(ax,**kwargs)
            if plotGeometric:
                for n in self.geometricNodes:
                    n.plotNode(ax,**kwargs)
        if plotEdges:
            for e in self.edges:
                e.plotEdge(ax,**kwargs)
            if plotGeometric:
                for e in self.geometricEdges:
                    e.plotEdge(ax,**kwargs)
        if plotFaces:
            for f in self.faces:
                f.plotFace(ax,**kwargs)

        if plotVolumes:
            for v in self.volumes:
                v.plotVolume(ax,**kwargs)


        ax.set_xlim(self.__xLim)
        ax.set_ylim(self.__yLim)
        ax.set_zlim(self.__zLim)

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        if axisEqual:
            pf.setAxesEqual(ax)




    def plotNodes(self,ax,**kwargs):
        '''

        '''
        self.plotComplex(ax,plotNodes=True,plotEdges=False,plotFaces=False,plotVolumes=False,**kwargs)
    def plotEdges(self,ax,**kwargs):
        '''

        '''
        self.plotComplex(ax,plotNodes=False,plotEdges=True,plotFaces=False,plotVolumes=False,**kwargs)
    def plotFaces(self,ax,**kwargs):
        '''

        '''
        self.plotComplex(ax,plotNodes=False,plotEdges=False,plotFaces=True,plotVolumes=False,**kwargs)
    def plotVolumes(self,ax,**kwargs):
        '''

        '''
        self.plotComplex(ax,plotNodes=False,plotEdges=False,plotFaces=False,plotVolumes=True,**kwargs)








#-------------------------------------------------------------------------
#    Plot using VTK
#-------------------------------------------------------------------------
    def plotComplexVTK(self,plotNodes = True,
                     plotEdges = True,
                     plotFaces = False,
                     oldVTK = None,
                     showLabel=False,
                     edgeColor=None,
                     pointSize = None,
                     backgroundColor = None,
                     **kwargs):

        if backgroundColor is None:
            backgroundColor = tc.TUMBlack()

        if oldVTK == None:
            myVTK = myv.MyVTK(pointSize = pointSize,backgroundColor = backgroundColor.rgb01)
        else:
            myVTK = oldVTK

        if plotNodes:
            for n in self.nodes:
                n.plotNodeVtk(myVTK,showLabel=showLabel,**kwargs)

        if plotEdges:
            for e in self.edges:
                e.plotEdgeVtk(myVTK,showLabel=showLabel,color=edgeColor,**kwargs)

        if plotFaces:
            for f in self.faces:
                f.plotFaceVtk(myVTK,showLabel=showLabel,**kwargs)
#            for e in chain(self.innerEdges,self.borderEdges):
#                for c in e.cylinders:
#                    myVTK.addActor(c.vtkActor)
#
#        if plotFaces:
#            for f in self.innerFaces:
#                for p in f.polygons:
#                    myVTK.addActor(p.vtkActor)
#
#
        return myVTK





    def plotFacesVTK(self,**kwargs):
        return self.plotComplexVTK(plotNodes=False,plotEdges=False,plotFaces=True,**kwargs)



    def plotVtkVoxels(self,resolution=100,
                           plotNodes=True,
                           plotEdges=True,
                           oldVTK=None,
                           showOutline=True):
        if oldVTK == None:
            myVTK = myv.MyVTK()
        else:
            myVTK = oldVTK

        minX = min([n.xCoordinate-n.radius for n in self.nodes])
        maxX = max([n.xCoordinate+n.radius for n in self.nodes])
        minY = min([n.yCoordinate-n.radius for n in self.nodes])
        maxY = max([n.yCoordinate+n.radius for n in self.nodes])
        minZ = min([n.zCoordinate-n.radius for n in self.nodes])
        maxZ = max([n.zCoordinate+n.radius for n in self.nodes])

        myVTK.createSampleFunction(resolution,[minX,maxX,minY,maxY,minZ,maxZ])


        if plotNodes:
#            print('complex3D: vtkvoxels')
#            print(self.nodes[1].sphere.radius)
#            myVTK.addActor(self.nodes[1].sphere.vtkActorVoxels)
            for n in self.nodes: #chain(self.innerNodes,self.borderNodes):
                myVTK.addBooleanFunction(n.sphere.vtkImplicitFunction)
#                myVTK.addActor(n.sphere.vtkActorVoxels)

        if plotEdges:
#            for e in chain(self.innerEdges,self.borderEdges):
            for e in self.edges:
                for se in e.simpleEdges:
                    myVTK.addBooleanFunction(se.cylinder.vtkImplicitFunction)


        myVTK.plotSampleFunction(showOutline)


        return myVTK





#-------------------------------------------------------------------------
#    Plot using TikZ
#-------------------------------------------------------------------------
    def plotComplexTikZ(self,tikZPicture=None,plotNodes=True,plotEdges=True,plotFaces=True,name=None,**kwargs):
        '''

        '''
        if tikZPicture is None:
            tikZPicture = TikZPicture3D(name=name)


        if tikZPicture.dim != 3:
            _log.error('Trying to plot in a 2-dimensional tikZPicture, but a 3-D complex should be plotted in a 3D-picture')
        else:

            if plotNodes:
                for n in self.nodes+self.geometricNodes:
                    n.plotNodeTikZ(tikZPicture,**kwargs)
            else:
                for n in self.nodes+self.geometricNodes:
                    n.plotNodeTikZ(tikZPicture,draw=False)

            if plotEdges:
                for e in self.edges:
                    e.plotEdgeTikZ(tikZPicture,**kwargs)

            if plotFaces:
                for f in self.faces:
                    f.plotFaceTikZ(tikZPicture,**kwargs)
        return tikZPicture



    def plotNodesTikZ(self,*args,**kwargs):
        return self.plotComplexTikZ(*args,plotEdges=False,plotFaces=False,**kwargs)

    def plotEdgesTikZ(self,*args,**kwargs):
        return self.plotComplexTikZ(*args,plotNodes=False,plotFaces=False,**kwargs)

    def plotFacesTikZ(self,*args,**kwargs):
        return self.plotComplexTikZ(*args,plotNodes=False,plotEdges=False,**kwargs)









#
#    def plotIncidence1(self,fig):
#        plt.figure(fig.number)
#        plt.clf()
#        titles = [['d_1_ii','d_1_ib','d_1_iB'],['d_1_bi','d_1_bb','d_1_bB'],['d_1_Bi','d_1_Bb','d_1_BB']]
#        incidenceMatrices = [[self.incidenceMatrix1ii,self.incidenceMatrix1ib,self.incidenceMatrix1iB],
#                             [self.incidenceMatrix1bi,self.incidenceMatrix1bb,self.incidenceMatrix1bB],
#                             [self.incidenceMatrix1Bi,self.incidenceMatrix1Bb,self.incidenceMatrix1BB]]
#        self.__plotIncidence(fig,titles,incidenceMatrices)


    def plotIncidence1(self,fig):
        plt.figure(fig.number)
        plt.clf()
#        titles = [['d_1_ii','d_1_ib','d_1_iB'],['d_1_bi','d_1_bb','d_1_bB'],['d_1_Bi','d_1_Bb','d_1_BB']]
#        incidenceMatrices = [[self.incidenceMatrix1ii,self.incidenceMatrix1ib,self.incidenceMatrix1iB],
#                             [self.incidenceMatrix1bi,self.incidenceMatrix1bb,self.incidenceMatrix1bB],
#                             [self.incidenceMatrix1Bi,self.incidenceMatrix1Bb,self.incidenceMatrix1BB]]
#        self.__plotIncidence(fig,titles,incidenceMatrices)
        plt.imshow(self.incidenceMatrix1)
#        plt.plot([0,100],[30,30])
        plt.plot([-0.5,len(self.edges)-0.5],[len(self.innerNodes)-0.5,len(self.innerNodes)-0.5],color='w')
        plt.plot([-0.5,len(self.edges)-0.5],[len(self.innerNodes)+len(self.borderNodes)-0.5,len(self.innerNodes)+len(self.borderNodes)-0.5],color='w')
        plt.plot([len(self.innerEdges)-0.5,len(self.innerEdges)-0.5],[-0.5,len(self.nodes)-0.5],color='w')
        plt.plot([len(self.innerEdges)+len(self.borderEdges)-0.5,len(self.innerEdges)+len(self.borderEdges)-0.5],[-0.5,len(self.nodes)-0.5],color='w')
        plt.grid(False)


    def plotIncidence2(self,fig):
        plt.figure(fig.number)
        plt.clf()
        plt.imshow(self.incidenceMatrix2)
        plt.plot([-0.5,len(self.__faces)-0.5],[len(self._innerEdges1)-0.5,len(self._innerEdges1)-0.5],color='w')
        plt.plot([-0.5,len(self.__faces)-0.5],[len(self._innerEdges1)+len(self._borderEdges1)-0.5,len(self._innerEdges1)+len(self._borderEdges1)-0.5],color='w')
        plt.plot([len(self._innerFaces1)-0.5,len(self._innerFaces1)-0.5],[-0.5,len(self.__edges)-0.5],color='w')
        plt.plot([len(self._innerFaces1)+len(self._borderFaces1)-0.5,len(self._innerFaces1)+len(self._borderFaces1)-0.5],[-0.5,len(self.__edges)-0.5],color='w')
        plt.grid(False)


    def plotIncidence3(self,fig):
        plt.figure(fig.number)
        plt.clf()
        plt.imshow(self.incidenceMatrix3)
        plt.plot([-0.5,len(self.__volumes)-0.5],[len(self._innerFaces1)-0.5,len(self._innerFaces1)-0.5],color='w')
        plt.plot([-0.5,len(self.__volumes)-0.5],[len(self._innerFaces1)+len(self._borderFaces1)-0.5,len(self._innerFaces1)+len(self._borderFaces1)-0.5],color='w')
        plt.plot([len(self._innerVolumes1)-0.5,len(self._innerVolumes1)-0.5],[-0.5,len(self.__faces)-0.5],color='w')
#        plt.plot([len(self._innerVolumes1)+len(self._borderFaces1)-0.5,len(self._innerFaces1)+len(self._borderFaces1)-0.5],[-0.5,len(self.__edges)-0.5],color='w')
        plt.grid(False)







    def writeTikZ(self,filename='tikz',
                       additionalText = '',
                       plotNodes=True,
                       plotEdges=True,
                       plotFaces=True,
                       plotVolumes=False,
                       color=None,
                       draw=None,
                       **kwargs):
        _log.error('Deprecated - Do not use')


    def setTikZGray(self,setValue=True):
        '''

        '''
        for c in self.nodes+self.edges+self.faces+self.volumes+self.geometricNodes+self.geometricEdges:
            c.grayInTikz = setValue




#    def __plotIncidence(self,fig,titles,incidenceMatrices):
#        for (i,line) in enumerate(incidenceMatrices):
#            for (j,incidence) in enumerate(line):
#                plt.subplot(3,3,3*i+j+1)
#                plt.title(titles[i][j])
#                # do not plot if matrix has either no lines or no rows
#                if all(incidence.shape):
#                    plt.imshow(incidence,vmin=-1,vmax=1,aspect='auto')

##-------------------------------------------------------------------------
##    Calculation of dual complex
##-------------------------------------------------------------------------
#    def calcDualComplex(self):
#
#
##    prepare lists
##....................................................................
#        dualInnerNodes = []
#        dualBorderNodes = []
#        dualAdditionalBorderNodes = []
#
#        dualInnerEdges = []
#        dualBorderEdges = []
#        dualAdditionalBorderEdges = []
#
#        dualInnerFaces = []
#        dualBorderFaces = []
#        dualAdditionalBorderFaces = []
#
#        dualInnerVolumes = []
#        dualBorderVolumes = []
#
#
#        for v in self.innerVolumes:
#            dualInnerNodes.append(DualNode3D(v))
#
#        for v in self.borderVolumes:
#            dualBorderNodes.append(DualNode3D(v))
#
#        for f in self.borderFaces:
#            dualAdditionalBorderNodes.append(DualNode2D(f))
#
#
#
#        for f in self.innerFaces:
#            dualInnerEdges.append(DualEdge3D(f))
#
#
#        for f in self.borderFaces:
#            dualBorderEdges.append(DualEdge3D(f))
#
#        for e in self.borderEdges:
#            dualAdditionalBorderEdges.append(DualEdge2D(e))
#
#        for e in self.innerEdges:
#            dualInnerFaces.append(DualFace3D(e))
#
#        for e in self.borderEdges:
#            dualBorderFaces.append(DualFace3D(e))
#
#
#        for n in self.borderNodes:
#            dualAdditionalBorderFaces.append(DualFace2D(n))
#
#        for n in self.innerNodes:
#            dualInnerVolumes.append(DualVolume3D(n))
#
#        for n in self.borderNodes:
#            dualBorderVolumes.append(DualVolume3D(n))
#
#
#
#
#        dualNodes = [n for n in chain(dualInnerNodes,dualBorderNodes,dualAdditionalBorderNodes)]
#        dualEdges = [e for e in chain(dualInnerEdges,dualBorderEdges,dualAdditionalBorderEdges)]
#        dualFaces = [f for f in chain(dualInnerFaces,dualBorderFaces,dualAdditionalBorderFaces)]
#        dualVolumes = [v for v in chain(dualInnerVolumes,dualBorderVolumes)]
#        dualComplex = Complex3D(dualNodes,
#                                dualEdges,
#                                dualFaces,
#                                dualVolumes,
#                                myDual=self)
#
#        return dualComplex
#


#-------------------------------------------------------------------------
#    Printing categories
#-------------------------------------------------------------------------
    def printCategories(self,myPrint=print,maxNumEntries = 100):
        '''

        '''
        lineWidth = len(str(self))
        myPrint()
        myPrint()
        myPrint('='*lineWidth)
        myPrint(self)
        myPrint('='*lineWidth)
        myPrint()


        myPrint('-'*lineWidth)
        myPrint('Nodes')
        myPrint('-'*lineWidth)
        myPrint()
        tableNodes = []
        for n in islice(chain(self.innerNodes,self.borderNodes,self.additionalBorderNodes),maxNumEntries):
            tableNodes.append([str(n),n.category1,n.category2])
        print(tabulate(tableNodes,headers=['Node','Category 1','Category 2'],tablefmt='psql'))
        myPrint()
        myPrint()


        myPrint('-'*lineWidth)
        myPrint('Edges')
        myPrint('-'*lineWidth)
        myPrint()
        tableEdges = []
        for e in islice(chain(self.innerEdges,self.borderEdges,self.additionalBorderEdges),maxNumEntries):
            tableEdges.append([str(e),e.category1,e.category2])
        print(tabulate(tableEdges,headers=['Edge','Category 1','Category 2'],tablefmt='psql'))
        myPrint()
        myPrint()


        myPrint('-'*lineWidth)
        myPrint('Faces')
        myPrint('-'*lineWidth)
        myPrint()
        tableFaces = []
        for f in islice(chain(self.innerFaces,self.borderFaces,self.additionalBorderFaces),maxNumEntries):
            tableFaces.append([str(f),f.category1,f.category2])
        print(tabulate(tableFaces,headers=['Face','Category 1','Category 2'],tablefmt='psql'))
        myPrint()
        myPrint()


        myPrint('-'*lineWidth)
        myPrint('Volumes')
        myPrint('-'*lineWidth)
        myPrint()
        tableVolumes = []
        for v in islice(chain(self.innerVolumes,self.borderVolumes),maxNumEntries):
            tableVolumes.append([str(v),v.category1,v.category2])
        print(tabulate(tableVolumes,headers=['Volume','Category 1','Category 2'],tablefmt='psql'))

#-------------------------------------------------------------------------
#    Printing dualities
#-------------------------------------------------------------------------
    def printDualities(self):
        '''

        '''
        self.printHeadline('NODES',cc.printRed)
        headlineNodes = ['Node','3D dual','2D dual','1D dual','0D dual']
        tableContentNodes = [headlineNodes,]
        for n in self.nodes:
            tableContentNodes.append([n.info_text,n.dualCell3D,n.dualCell2D,n.dualCell1D,n.dualCell0D])
        tableNodes = Table(tableContentNodes)
        tableNodes.printTable()


        self.printHeadline('EDGES',cc.printBlue)
        headlineEdges = ['Edge','3D dual','2D dual','1D dual']
        tableContentEdges = [headlineEdges,]
        for e in self.edges:
            tableContentEdges.append([e.info_text,e.dualCell3D,e.dualCell2D,e.dualCell1D])
        tableEdges = Table(tableContentEdges)
        tableEdges.printTable()


        self.printHeadline('FACES',cc.printGreen)
        headlineFaces = ['Face','3D dual','2D dual']
        tableContentFaces = [headlineFaces,]
        for f in self.faces:
            tableContentFaces.append([f.info_text,f.dualCell3D,f.dualCell2D])
        tableFaces = Table(tableContentFaces)
        tableFaces.printTable()

        self.printHeadline('VOLUMES',cc.printMagenta)
        headlineFaces = ['Volume','3D dual']
        tableContentFaces = [headlineFaces,]
        for v in self.volumes:
            tableContentFaces.append([v.info_text,v.dualCell3D])
        tableFaces = Table(tableContentFaces)
        tableFaces.printTable()


    def printDuals(self,myPrint=print,maxNumEntries = 100):
        lineWidth = len(str(self))
        myPrint()
        myPrint()
        myPrint('='*lineWidth)
        myPrint(self)
        myPrint('='*lineWidth)
        myPrint()


        myPrint('-'*lineWidth)
        myPrint('Nodes')
        myPrint('-'*lineWidth)
        myPrint()
        tableNodes = []
        for n in islice(chain(self.innerNodes,self.borderNodes,self.additionalBorderNodes),maxNumEntries):
            tableNodes.append([str(n),n.dualCell3D,n.dualCell2D,n.dualCell1D,n.dualCell0D])
        print(tabulate(tableNodes,headers=['Node','3D dual','2D dual','1D dual','0D dual'],tablefmt='psql'))
        myPrint()
        myPrint()


        myPrint('-'*lineWidth)
        myPrint('Edges')
        myPrint('-'*lineWidth)
        myPrint()
        tableEdges = []
        for e in islice(chain(self.innerEdges,self.borderEdges,self.additionalBorderEdges),maxNumEntries):
            tableEdges.append([str(e),e.dualCell3D,e.dualCell2D,e.dualCell1D,])
        print(tabulate(tableEdges,headers=['Edge','3D dual','2D dual','1D dual'],tablefmt='psql'))
        myPrint()
        myPrint()


        myPrint('-'*lineWidth)
        myPrint('Faces')
        myPrint('-'*lineWidth)
        myPrint()
        tableFaces = []
        for f in islice(chain(self.innerFaces,self.borderFaces,self.additionalBorderFaces),maxNumEntries):
            tableFaces.append([str(f),f.dualCell3D,f.dualCell2D])
        print(tabulate(tableFaces,headers=['Face','3D dual','2D dual'],tablefmt='psql'))
        myPrint()
        myPrint()


        myPrint('-'*lineWidth)
        myPrint('Volumes')
        myPrint('-'*lineWidth)
        myPrint()
        tableVolumes = []
        for v in islice(chain(self.innerVolumes,self.borderVolumes),maxNumEntries):
            tableVolumes.append([str(v),v.dualCell3D,])
        print(tabulate(tableVolumes,headers=['Volume','3D dual'],tablefmt='psql'))


    def code_generator(self, filename):
        '''

        '''
        export_folder = pathlib.Path(__file__).parent.parent.parent / "export"
        _log.critical("Generating code in folder: %s", export_folder)

        export_file = export_folder / filename
        _log.critical("Generating code in file: %s", export_file)

        with export_file.open("w") as file:
            file.write("# Auto-generated code for Complex3D\n")
            file.write("import logging\n")
            file.write("from pyCellFoamCore.k_cells.node.node import Node\n")
            file.write("from pyCellFoamCore.k_cells.node.node import NodePlotly\n")
            file.write("from pyCellFoamCore.k_cells.edge.edge import Edge\n")
            file.write("from pyCellFoamCore.k_cells.edge.baseEdge import EdgePlotly\n")
            file.write("from pyCellFoamCore.k_cells.face.face import Face\n")
            file.write("from pyCellFoamCore.k_cells.face.baseFace import FacePlotly\n")
            file.write("from pyCellFoamCore.k_cells.volume.volume import Volume\n")
            file.write("from pyCellFoamCore.k_cells.volume.volume import VolumePlotly\n")
            file.write("from pyCellFoamCore.tools.logging_formatter import set_logging_format\n\n")
            file.write("set_logging_format(logging.INFO)\n\n")

            geometric_edges = []
            for f in self.faces:
                for ge in f.geometricEdges:
                    if ge not in geometric_edges:
                        geometric_edges.append(ge)
            geometric_nodes = []
            for e in geometric_edges:
                if e.startNode.is_geometrical and e.startNode not in geometric_nodes:
                    geometric_nodes.append(e.startNode)
                if e.endNode.is_geometrical and e.endNode not in geometric_nodes:
                    geometric_nodes.append(e.endNode)

            _log.critical("Generating code for %d nodes", len(self.nodes))
            for n in self.nodes:
                file.write(f"n{n.num} = Node({n.xCoordinate}, {n.yCoordinate}, {n.zCoordinate}, num={n.num})\n")
            for n in geometric_nodes:
                file.write(f"gn{n.num} = Node({n.xCoordinate}, {n.yCoordinate}, {n.zCoordinate}, num={n.num})\n")

            file.write("nodes = [")
            file.write(", ".join([f"n{n.num}" for n in self.nodes]))
            file.write("]\n\n")


            edge_nums = []
            _log.critical("Generating code for %d edges", len(self.edges))
            for e in self.edges:
                file.write(f"e{e.num} = Edge(n{e.startNode.num}, n{e.endNode.num}, num={e.num})\n")
                if e.num in edge_nums:
                    _log.error("Duplicate edge number found: %d", e.num)
                edge_nums.append(e.num)
            for e in geometric_edges:
                file.write(f"ge{e.num} = Edge({'gn' if e.startNode.is_geometrical else 'n'}{e.startNode.num}, {'gn' if e.endNode.is_geometrical else 'n'}{e.endNode.num}, num={e.num})  # Geometric edge\n")

            file.write("edges = [")
            file.write(", ".join([f"e{e.num}" for e in self.edges]))
            file.write("]\n\n")


            file.write("geometric_edges = [")
            file.write(", ".join([f"ge{e.num}" for e in geometric_edges]))
            file.write("]\n\n")

            _log.critical("Generating code for %d faces", len(self.faces))
            for f in self.faces:
                _log.critical("geometric edges in face %s: %s", f, f.geometricEdges)
                edge_list = []
                for sf in f.simpleFaces:
                    simple_edge_list = ", ".join([f"{'-' if edge.is_reverse else ''}{'ge' if edge.is_geometrical else 'e'}{edge.num}" for edge in sf.simpleEdges])
                    edge_list.append(f"[{simple_edge_list}]")
                edge_list = ", ".join(edge_list)
                file.write(f"f{f.num} = Face([{edge_list}], num={f.num})\n")
            file.write("faces = [")
            file.write(", ".join([f"f{f.num}" for f in self.faces]))
            file.write("]\n\n")

            if True:

                for v in self.volumes:
                    face_list = ", ".join([f"{'-' if face.is_reverse else ''}f{face.num}" for face in v.faces])
                    file.write(f"v{v.num} = Volume([{face_list}], num={v.num}, accept_incomplete_geometry=True)\n")
                file.write("volumes = [")
                file.write(", ".join([f"v{v.num}" for v in self.volumes]))
                file.write("]\n\n")

            else:
                file.write("volumes = []  # Volume generation is skipped\n\n")

            file.write("plotly_nodes = NodePlotly(nodes)\n")
            file.write("plotly_fig_nodes = plotly_nodes.plot_nodes_plotly()\n")
            file.write("plotly_fig_nodes.show()\n\n")
            file.write("plotly_edges = EdgePlotly(edges+geometric_edges)\n")
            file.write("plotly_fig_edges = plotly_edges.plot_edges_plotly()\n")
            file.write("plotly_fig_edges.show()\n\n")
            file.write("plotly_faces = FacePlotly(faces)\n")
            file.write("plotly_fig_faces = plotly_faces.plot_faces_plotly()\n")
            file.write("plotly_fig_faces.show()\n\n")
            file.write("plotly_volumes = VolumePlotly(volumes)\n")
            file.write("plotly_fig_volumes = plotly_volumes.plot_volumes_plotly()\n")
            file.write("plotly_fig_volumes.show()\n\n")








#-------------------------------------------------------------------------
#    Plot for Documentation
#-------------------------------------------------------------------------

    @classmethod
    def plotDoc(cls):
        '''
        Create the plots used in documentation.

        '''

        # Create nodes
        n0 = Node(0,0,0)
        n1 = Node(1,0,0)
        n2 = Node(1.5,0,0)
        n3 = Node(0,1,0)
        n4 = Node(1,1,0)
        n5 = Node(0,1.5,0)
        n6 = Node(1.5,1.5,0)
        n7 = Node(0,0,1)
        n8 = Node(1,0,1)
        n9 = Node(0,1,1)
        n10 = Node(1,1,1)
        n11 = Node(0,0,1.5)
        n12 = Node(1.5,0,1.5)
        n13 = Node(0,1.5,1.5)
        n14 = Node(1.5,1.5,1.5)

        nodes = [n0,n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14]


        # Create edges
        e0 = Edge(n0,n1)
        e1 = Edge(n1,n2)
        e2 = Edge(n3,n4)
        e3 = Edge(n5,n6)
        e4 = Edge(n0,n3)
        e5 = Edge(n1,n4)
        e6 = Edge(n2,n6)
        e7 = Edge(n3,n5)
        e8 = Edge(n4,n6)
        e9 = Edge(n7,n8)
        e10 = Edge(n8,n10)
        e11 = Edge(n10,n9)
        e12 = Edge(n9,n7)
        e13 = Edge(n11,n12)
        e14 = Edge(n12,n14)
        e15 = Edge(n14,n13)
        e16 = Edge(n13,n11)
        e17 = Edge(n0,n7)
        e18 = Edge(n1,n8)
        e19 = Edge(n4,n10)
        e20 = Edge(n3,n9)
        e21 = Edge(n2,n12)
        e22 = Edge(n6,n14)
        e23 = Edge(n5,n13)
        e24 = Edge(n7,n11)
        e25 = Edge(n8,n12)
        e26 = Edge(n10,n14)
        e27 = Edge(n9,n13)

        edges = [e0,e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13,e14,e15,e16,e17,e18,e19,e20,e21,e22,e23,e24,e25,e26,e27]


        # Create faces
        f0 = Face([e0,e5,-e2,-e4])
        f1 = Face([e1,e6,-e8,-e5])
        f2 = Face([e2,e8,-e3,-e7])
        f3 = Face([e0,e18,-e9,-e17])
        f4 = Face([e5,e19,-e10,-e18])
        f5 = Face([e2,e19,e11,-e20])
        f6 = Face([e4,e20,e12,-e17])
        f7 = Face([e9,e10,e11,e12])
        f8 = Face([e9,e25,-e13,-e24])
        f9 = Face([e1,e21,-e25,-e18])
        f10 = Face([e6,e22,-e14,-e21])
        f11 = Face([e25,e14,-e26,-e10])
        f12 = Face([e8,e22,-e26,-e19])
        f13 = Face([e3,e22,e15,-e23])
        f14 = Face([e26,e15,-e27,-e11])
        f15 = Face([e7,e23,-e27,-e20])
        f16 = Face([e27,e16,-e24,-e12])
        f17 = Face([e13,e14,e15,e16])

        faces = [f0,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17]


        # Create volumes
        v0 = Volume([-f0,f3,f4,-f5,-f6,f7])
        v1 = Volume([-f1,-f4,f9,f10,f11,-f12])
        v2 = Volume([-f2,f5,f12,-f13,f14,-f15])
        v3 = Volume([-f7,f8,-f11,-f14,-f16,f17])

        volumes = [v0,v1,v2,v3]


        # Create complex

        c = Complex3D(nodes,edges,faces,volumes)

        # Plot
        (figs,axes) = pf.getFigures()
        c.plotComplex(axes[0],plotFaces=True,showNormalVec=False)

        # Create image files
        pf.exportPNG(figs[0],'doc/_static/complex3D.png')


#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':

    from tools import MyLogging
    with MyLogging('Complex3D',debug=False):


#-------------------------------------------------------------------------
#    Create some examples
#-------------------------------------------------------------------------


        cc.printBlue('Create nodes')
        n0 = Node(0,0,0)
        n1 = Node(1,0,0)
        n2 = Node(1.5,0,0)
        n3 = Node(0,1,0)
        n4 = Node(1,1,0)
        n5 = Node(0,1.5,0)
        n6 = Node(1.5,1.5,0)
        n7 = Node(0,0,1)
        n8 = Node(1,0,1)
        n9 = Node(0,1,1)
        n10 = Node(1,1,1)
        n11 = Node(0,0,1.5)
        n12 = Node(1.5,0,1.5)
        n13 = Node(0,1.5,1.5)
        n14 = Node(1.5,1.5,1.5)


        nodes = [n0,n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14]


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
        e9 = Edge(n7,n8)
        e10 = Edge(n8,n10)
        e11 = Edge(n10,n9)
        e12 = Edge(n9,n7)
        e13 = Edge(n11,n12)
        e14 = Edge(n12,n14)
        e15 = Edge(n14,n13)
        e16 = Edge(n13,n11)
        e17 = Edge(n0,n7)
        e18 = Edge(n1,n8)
        e19 = Edge(n4,n10)
        e20 = Edge(n3,n9)
        e21 = Edge(n2,n12)
        e22 = Edge(n6,n14)
        e23 = Edge(n5,n13)
        e24 = Edge(n7,n11)
        e25 = Edge(n8,n12)
        e26 = Edge(n10,n14)
        e27 = Edge(n9,n13)

        edges = [e0,e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13,e14,e15,e16,e17,e18,e19,e20,e21,e22,e23,e24,e25,e26,e27]

        cc.printBlue('Create faces')
        f0 = Face([e0,e5,-e2,-e4])
        f1 = Face([e1,e6,-e8,-e5])
        f2 = Face([e2,e8,-e3,-e7])
        f3 = Face([e0,e18,-e9,-e17])
        f4 = Face([e5,e19,-e10,-e18])
        f5 = Face([e2,e19,e11,-e20])
        f6 = Face([e4,e20,e12,-e17])
        f7 = Face([e9,e10,e11,e12])
        f8 = Face([e9,e25,-e13,-e24])
        f9 = Face([e1,e21,-e25,-e18])
        f10 = Face([e6,e22,-e14,-e21])
        f11 = Face([e25,e14,-e26,-e10])
        f12 = Face([e8,e22,-e26,-e19])
        f13 = Face([e3,e22,e15,-e23])
        f14 = Face([e26,e15,-e27,-e11])
        f15 = Face([e7,e23,-e27,-e20])
        f16 = Face([e27,e16,-e24,-e12])
        f17 = Face([e13,e14,e15,e16])


        faces = [f0,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17]


        cc.printBlue('Create volumes')

        v0 = Volume([-f0,f3,f4,-f5,-f6,f7])
        v1 = Volume([-f1,-f4,f9,f10,f11,-f12])
        v2 = Volume([-f2,f5,f12,-f13,f14,-f15])
        v3 = Volume([-f7,f8,-f11,-f14,-f16,f17])

        facesForVolume = [-f7,f8,-f11,-f14,-f16,f17]

        volumes = [v0,v1,v2,v3]

        c = Complex3D(nodes,edges,faces,volumes)



#-------------------------------------------------------------------------
#    Plotting
#-------------------------------------------------------------------------

        # Choose plotting method. Possible choices: pyplot, VTK, TikZ, animation, doc, None
        plottingMethod = 'doc'


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
            c.plotFaces(axes[1])
            c.plotVolumes(axes[2])

#    VTK
#---------------------------------------------------------------------
        elif plottingMethod == 'VTK' :
            cc.printBlue('Plot using VTK')
            myvtk = c.plotComplexVTK()
            myvtk.start()

#    TikZ
#---------------------------------------------------------------------
        elif plottingMethod == 'TikZ' :
            cc.printBlue('Plot using TikZ')
            pic = c.plotComplexTikZ()
            pic.scale = 5
            origin = pic.addTikZCoordinate('O',np.array([0,0,0]))
            pic.addTikZCoSy3D(origin,arrowLength=1.3)
            pic.writeLaTeXFile('latex','complex3D',True,True)

#    Animation
#---------------------------------------------------------------------
        elif plottingMethod == 'animation':
            cc.printBlue('Creating animation')
            cc.printRed('Not implemented')

#    Documentation
#---------------------------------------------------------------------
        elif plottingMethod == 'doc':
            cc.printBlue('Creating plots for documentation')
            Complex3D.plotDoc()

#    Unknown
#---------------------------------------------------------------------
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))
