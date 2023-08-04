# -*- coding: utf-8 -*-
#==============================================================================
# 2-DIMENSIONAL TRIANGULAR GRID
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
from kCells import Node,Edge,Face

#    Complex & Grids
#--------------------------------------------------------------------
from complex import PrimalComplex2D, DualComplex2D

#    Tools
#--------------------------------------------------------------------
import tools.colorConsole as cc
import tools.placeFigures as pf







#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class Grid2DTriangular(PrimalComplex2D):
    '''
    This is the explanation of this class.
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__xNum',
                 '__yNum',
                 '__xLen',
                 '__yLen')
#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,xNum=3,yNum=None,xLen=1,yLen=1):
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
        for x in range(self.xNum):
            for y in range(self.yNum):            
                nodes.append(Node(x*self.xLen,y*self.yLen,0))
                
       
        #    Create Edges
        #---------------------------------------------------------------
        edges = []
        node_num = 0
        for x in range(self.xNum):
            for y in range(self.yNum-1):            
                edges.append(Edge(nodes[node_num],nodes[node_num + 1]))
                node_num += 1
            node_num += 1       
        
            
        
        for y in range(self.yNum):
            node_num = y
            for x in range(self.xNum - 1):
                edges.append(Edge(nodes[node_num],nodes[node_num + self.yNum]))
                node_num += self.yNum
                
                
        for y in range(self.yNum-1):
            node_num = y
            for x in range(self.xNum - 1):
                edges.append(Edge(nodes[node_num],nodes[node_num + self.yNum + 1]))
                node_num += self.yNum
                
        
                
    
        #    Create Faces
        #---------------------------------------------------------------
        faces = []
        edgeNumRight = 0
        edgeNumTop = 0
        edgeNumLeft = 0
        
        for x in range(self.xNum-1):
            edgeNumBottom = x+self.xNum*(self.yNum-1)
            for y in range(self.yNum-1):
                edgeNumTop = edgeNumBottom + self.xNum-1
                edgeNumRight = edgeNumLeft + self.yNum-1
                
                edgeNumDiagonal = edgeNumBottom + (self.xNum-1)*self.yNum
                faces.append(Face([edges[edgeNumBottom],edges [edgeNumRight],-edges[edgeNumDiagonal]]))
                faces.append(Face([edges[edgeNumDiagonal],-edges[edgeNumTop],-edges[edgeNumLeft]]))
                edgeNumLeft += 1
                edgeNumBottom += self.xNum - 1            
                
                
        #    Set Up Primal Complex
        #---------------------------------------------------------------        
        self.nodes = nodes
        self.edges = edges
        self.faces = faces
        
        super().setUp()





#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    from tools.myLogging import MyLogging
    
    with MyLogging('grid2DQuadratic'):
        (figs,axes) = pf.getFigures()
        
        cc.printBlue('Create triangular grid')
        pc = Grid2DTriangular()
        
        cc.printBlue('Construct dual complex')
        dc = DualComplex2D(pc)
        
        cc.printBlue('Plot both complexes')
        pc.plotComplex(axes[0])
        dc.plotComplex(axes[1])
        
        

    

