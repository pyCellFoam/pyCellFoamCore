# -*- coding: utf-8 -*-
#==============================================================================
# 2-DIMENSIONAL RECTANGULAR GRID
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Dec  7 14:16:21 2017

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
from k_cells import Node,Edge,Face

#    Complex & Grids
#--------------------------------------------------------------------
from complex import PrimalComplex2D,DualComplex2D


#    Tools
#--------------------------------------------------------------------
import tools.colorConsole as cc
import tools.placeFigures as pf
from tools import MyLogging





#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class Grid2DRectangular(PrimalComplex2D):
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__xNum',
                 '__yNum',
                 '__xLen',
                 '__yLen',
                 '__deltaX',
                 '__deltaY',
                 '__borderFacesLeft',
                 '__borderFacesRight',
                 '__borderFacesTop',
                 '__borderFacesBottom',
                 '__boundaryNodesLeft',
                 '__boundaryNodesRight',
                 '__boundaryNodesTop',
                 '__boundaryNodesBottom')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,xNum=3,yNum=None,xLen=1,yLen=1,
                 borderFacesLeft=False,
                 borderFacesRight=False,
                 borderFacesTop=False,
                 borderFacesBottom=False):
        '''
        This is the explanation of the __init__ method.

        All parameters should be listed:

        :param int a: Some Number
        :param str b: Some String

        '''
        self.__xNum = xNum
        if yNum is None:
            self.__yNum = xNum
        else:
            self.__yNum = yNum
        self.__xLen = xLen
        self.__yLen = yLen
        self.__deltaX = xLen/(self.__xNum-1)
        self.__deltaY = yLen/(self.__yNum-1)

        self.__borderFacesLeft = borderFacesLeft
        self.__borderFacesRight = borderFacesRight
        self.__borderFacesTop = borderFacesTop
        self.__borderFacesBottom = borderFacesBottom

        self.__boundaryNodesLeft = []
        self.__boundaryNodesRight = []
        self.__boundaryNodesTop = []
        self.__boundaryNodesBottom = []

        super().__init__()






#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getXNum(self): return self.__xNum
    xNum = property(__getXNum)

    def __getYNum(self): return self.__yNum
    yNum = property(__getYNum)

    def __getXLen(self): return self.__xLen
    xLen = property(__getXLen)

    def __getYLen(self): return self.__yLen
    yLen = property(__getYLen)

    def __getDeltaX(self): return self.__deltaX
    deltaX = property(__getDeltaX)

    def __getDeltaY(self): return self.__deltaY
    deltaY = property(__getDeltaY)

    def __getBoundaryNodesLeft(self): return self.__boundaryNodesLeft
    boundaryNodesLeft = property(__getBoundaryNodesLeft)

    def __getBoundaryNodesRight(self): return self.__boundaryNodesRight
    boundaryNodesRight = property(__getBoundaryNodesRight)

    def __getBoundaryNodesTop(self): return self.__boundaryNodesTop
    boundaryNodesTop = property(__getBoundaryNodesTop)

    def __getBoundaryNodesBottom(self): return self.__boundaryNodesBottom
    boundaryNodesBottom = property(__getBoundaryNodesBottom)





#==============================================================================
#    METHODS
#==============================================================================


#-------------------------------------------------------------------------
#    Set Up
#-------------------------------------------------------------------------

    def setUp(self):

        #    Create Nodes
        #---------------------------------------------------------------

        nodes = []
        nodeNum = 0
        for x in range(self.__xNum):
            for y in range(self.__yNum):
                nodes.append(Node(x*self.deltaX,y*self.deltaY,0,num=nodeNum))

                if y == 0:
                    self.__boundaryNodesBottom.append(nodes[-1])
                if y == self.__yNum-1:
                    self.__boundaryNodesTop.append(nodes[-1])

                if x == 0:
                    self.__boundaryNodesLeft.append(nodes[-1])


                if x == self.__xNum-1:
                    self.__boundaryNodesRight.append(nodes[-1])


                nodeNum += 1

        #    Create Edges
        #---------------------------------------------------------------
        edges = []
        edge_num = 0
        node_num = 0
        for x in range(self.__xNum):
            for y in range(self.__yNum-1):
                edges.append(Edge(nodes[node_num],nodes[node_num + 1],num=edge_num))
                edge_num += 1
                node_num += 1
            node_num += 1

        for y in range(self.__yNum):
            node_num = y
            for x in range(self.__xNum - 1):
                edges.append(Edge(nodes[node_num],nodes[node_num + self.__yNum],num=edge_num))
                edge_num += 1
                node_num += self.__yNum


        #    Create Faces
        #---------------------------------------------------------------
        faces = []
        face_num = 0
        edgeNumBottom = self.__xNum*(self.__yNum-1)
        edgeNumRight = 0
        edgeNumTop = 0
        edgeNumLeft = 0
        for x in range(self.__xNum-1):
            edgeNumBottom = x+self.__xNum*(self.__yNum-1)
            for y in range(self.__yNum-1):
                edgeNumTop = edgeNumBottom + self.__xNum-1
                edgeNumRight = edgeNumLeft + self.__yNum-1
                faces.append(Face([edges[edgeNumBottom],edges [edgeNumRight],-edges[edgeNumTop],-edges[edgeNumLeft]],num=face_num))
                edgeNumLeft += 1
                edgeNumBottom += self.__xNum - 1
                face_num += 1


        for f in faces:
            if f.num < self.__yNum-1 and self.__borderFacesLeft:
                if f.category1 == 'undefined':
                    f.category1 = 'border'

            if f.num >= (self.__xNum-2)*(self.__yNum-1) and self.__borderFacesRight:
                if f.category1 == 'undefined':
                    f.category1 = 'border'

            if f.num % (self.__yNum-1) == 0 and self.__borderFacesBottom:
                if f.category1 == 'undefined':
                    f.category1 = 'border'

            if f.num % (self.__yNum-1) == self.__yNum-2 and self.__borderFacesTop:
                if f.category1 == 'undefined':
                    f.category1 = 'border'



        #    Set Up Primal Complex
        #---------------------------------------------------------------
        self.nodes = nodes
        self.edges = edges
        self.faces = faces
        super().setUp()


#-------------------------------------------------------------------------
#    Plot for Documentation
#-------------------------------------------------------------------------
    @classmethod
    def plotDoc(cls):
        pc = Grid2DRectangular(3,4)
        dc = DualComplex2D(pc)


        (figs,axes) = pf.getFigures(numTotal=2)

        pc.plotComplex(axes[0])
        dc.plotComplex(axes[1])

        pf.exportPNG(figs[0],'doc/_static/grid2DRectangular1')
        pf.exportPNG(figs[1],'doc/_static/grid2DRectangular2')


#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    with MyLogging('grid2DRectangular'):

        pc0 = Grid2DRectangular(4,6)
        pc1 = Grid2DRectangular(4,6,borderFacesLeft=True)
        pc2 = Grid2DRectangular(4,6,borderFacesRight=True)
        pc3 = Grid2DRectangular(4,6,borderFacesBottom=True)
        pc4 = Grid2DRectangular(4,6,borderFacesTop=True)
        pc5 = Grid2DRectangular(4,6,borderFacesLeft=True,borderFacesRight=True)
        pc6 = Grid2DRectangular(4,6,borderFacesLeft=True,borderFacesTop=True)
        pc7 = Grid2DRectangular(4,6,borderFacesLeft=True,borderFacesRight=True,borderFacesTop=True,borderFacesBottom=True)



        dc0 = DualComplex2D(pc0)
        dc1 = DualComplex2D(pc1)
        dc2 = DualComplex2D(pc2)
        dc3 = DualComplex2D(pc3)
        dc4 = DualComplex2D(pc4)
        dc5 = DualComplex2D(pc5)
        dc6 = DualComplex2D(pc6)
        dc7 = DualComplex2D(pc7)


        dc0.checkAllIncidenceMatrices()
        dc1.checkAllIncidenceMatrices()
        dc2.checkAllIncidenceMatrices()
        dc3.checkAllIncidenceMatrices()
        dc4.checkAllIncidenceMatrices()
        dc5.checkAllIncidenceMatrices()
        dc6.checkAllIncidenceMatrices()
        dc7.checkAllIncidenceMatrices()


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
            pc0.plotComplex(axes[0],showLabel=False)
            pc1.plotComplex(axes[1],showLabel=False)
            pc5.plotComplex(axes[2],showLabel=False)
            dc0.plotComplex(axes[3],showLabel=False)
            dc1.plotComplex(axes[4],showLabel=False)
            dc5.plotComplex(axes[5],showLabel=False)

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
            Grid2DRectangular.plotDoc()

#    Unknown
#---------------------------------------------------------------------
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))
#