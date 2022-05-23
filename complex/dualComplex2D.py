# -*- coding: utf-8 -*-
#==============================================================================
# DUAL COMPLEX 2D
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Mon Mar 30 13:25:39 2020

'''

'''
#==============================================================================
#    IMPORTS
#==============================================================================
import os
if __name__ == '__main__':
    os.chdir('../')

from kCells import Node, DualNode2D, DualNode1D
from kCells import Edge, DualEdge2D, DualEdge1D
from kCells import Face, DualFace2D

from complex.primalComplex2D import PrimalComplex2D
from complex.complex2D import Complex2D
import tools.colorConsole as cc
#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class DualComplex2D(Complex2D):
    '''
    This is the explanation of this class.
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__primalComplex',
                 '__createNodes',
                 '__createEdges',
                 '__createFaces')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,primalComplex,createNodes=True,createEdges=True,createFaces=True):
        '''
        :param PrimalComplex2D primalComplex: 
        
        '''
        self.__primalComplex = primalComplex
        primalComplex.dualComplex = self
        self.__createNodes = createNodes
        self.__createEdges = createEdges
        self.__createFaces = createFaces
        super().__init__(loggerName=__name__)
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getPrimalComplex(self): return self.__primalComplex
    primalComplex = property(__getPrimalComplex)
    '''
    
    '''
    
    
    def __getUseCategory(self): 
        if self.primalComplex:
            return self.primalComplex.useCategory
        else:
            self.logger.error('Cannot get useCategory: no primalComplex defined')
            return None
    def __setUseCategory(self,u): 
        if self.primalComplex:
            self.primalComplex.useCategory = u
        else:
            self.logger.error('Cannot set useCategory: no primalComplex defined')
    useCategory = property(__getUseCategory,__setUseCategory)
    '''
    
    '''

    def __getChangedNumbering(self): 
        if self.primalComplex:
            return self.primalComplex.changedNumbering
        else:
            self.logger.error('Cannot get changedNumbering: no primalComplex defined')
            return False
    changedNumbering = property(__getChangedNumbering)
    '''
    
    '''


    

    
#==============================================================================
#    METHODS
#==============================================================================
    
#-------------------------------------------------------------------------
#    Method 1
#-------------------------------------------------------------------------
    def setUp(self):
        '''
        
        '''
        self.logger.info('Called "Set Up" in DualComplex2D class')
        self.__construct()
        self.sortPrimal()
        self.sortDual()
        self.renumberList(self.geometricNodes)
        cc.printRed()
        cc.printRed('Geometric Nodes:')
        cc.printRed(self.geometricNodes)
        cc.printRed()
        super().setUp()
        
        
        
        
       
    
  
    
#-------------------------------------------------------------------------
#    Method 1
#-------------------------------------------------------------------------    
    def __construct(self):
        '''
        
        '''
        dualNodes = []
        dualEdges = []
        dualFaces = []
        
        # Dual nodes
        if self.__createNodes:
            for f in self.__primalComplex.faces:
                dualNodes.append(DualNode2D(f))
            for e in self.__primalComplex.borderEdges1:
                dualNodes.append(DualNode1D(e))
        else:
            self.logger.warning('Creation of nodes has been disabled')
            
        
        # Dual edges
        if self.__createEdges and self.__createNodes:
            for e in self.__primalComplex.innerEdges1 + self.__primalComplex.borderEdges1:
                dualEdges.append(DualEdge2D(e))
            for n in self.__primalComplex.borderNodes1:
                dualEdges.append(DualEdge1D(n))
        else:
            self.logger.warning('Creation of edges has been disabled')                
            
            
        # Dual faces
        if self.__createFaces and self.__createEdges and self.__createNodes:
            for n in self.__primalComplex.innerNodes1 +  self.__primalComplex.borderNodes1:
                dualFaces.append(DualFace2D(n))
        else:
            self.logger.warning('Creation of faces has been disabled')     
        
        self.nodes = dualNodes
        self.edges = dualEdges
        self.faces = dualFaces
    
    
#-------------------------------------------------------------------------
#    Method 1
#-------------------------------------------------------------------------    

    def renumber(self):
        '''
        
        '''
        if self.primalComplex:
            self.primalComplex.renumber()
        else:
            self.logger.error('Cannot renumber: no primalComplex defined')
    
    
    
#-------------------------------------------------------------------------
#    Method 1
#-------------------------------------------------------------------------    
    def checkAllIncidenceMatrices(self,doPrints=True):
        '''
        
        '''
        checks = []
        
        self.useCategory = 1
        if doPrints:
            cc.printBlue()
            cc.printBlue('Checking incidence matrix dualities')
            cc.printBlue('='*35)
            cc.printBlue()
            cc.printBlue('Using category 1')
            cc.printBlue('-'*15)
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2ii,-self.__primalComplex.incidenceMatrix1ii,'d̂2ii','-d1ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2ib,-self.__primalComplex.incidenceMatrix1bi,'d̂2ib','-d1bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2bi,-self.__primalComplex.incidenceMatrix1ib,'d̂2bi','-d1ib',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2bb,-self.__primalComplex.incidenceMatrix1bb,'d̂2bb','-d1bb',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1ii,self.__primalComplex.incidenceMatrix2ii,'d̂1ii','d2ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1ib,self.__primalComplex.incidenceMatrix2bi,'d̂1ib','d2bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1bi,self.__primalComplex.incidenceMatrix2ib,'d̂1bi','d2ib',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1bb,self.__primalComplex.incidenceMatrix2bb,'d̂1bb','d2bb',doPrints))
        
#        checks.append(self.checkIncidenceMatrixZero(self.incidenceMatrix1bb,'d̂1bb',doPrints))
#        checks.append(self.checkIncidenceMatrixZero(self.__primalComplex.incidenceMatrix1bb,'d1bb',doPrints))
        
        
        if doPrints:
            cc.printBlue()
            cc.printBlue('Using category 2')
            cc.printBlue('-'*15)
        
        self.useCategory = 2
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2ii,-self.__primalComplex.incidenceMatrix1ii,'d̂2ii','-d1ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2ib,-self.__primalComplex.incidenceMatrix1bi,'d̂2ib','-d1bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2bi,-self.__primalComplex.incidenceMatrix1ib,'d̂2bi','-d1ib',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2bb,-self.__primalComplex.incidenceMatrix1bb,'d̂2bb','-d1bb',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1ii,self.__primalComplex.incidenceMatrix2ii,'d̂1ii','d2ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1ib,self.__primalComplex.incidenceMatrix2bi,'d̂1ib','d2bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1bi,self.__primalComplex.incidenceMatrix2ib,'d̂1bi','d2ib',doPrints))


        
        if doPrints:
            cc.printGreen()
            
            if all(checks):
                cc.printGreen('-'*50)
                cc.printGreen('All incidence matrix dualities are correct')
                cc.printGreen('-'*50)
            else:
                cc.printRed('-'*50)
                cc.printRed('Not all incidence matrix dualities are correct')
                cc.printRed('-'*50)
            cc.printGreen()
        return checks


    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    import tools.placeFigures as pf
    
    from tools.myLogging import MyLogging
    
    with MyLogging('DualComplex2D',debug=False):
       
        
        
#-------------------------------------------------------------------------
#    Example 1
#-------------------------------------------------------------------------        
        
        n0 = Node(0,0,0)
        n1 = Node(1,0,0)
        n2 = Node(1.5,1,0)
        n3 = Node(0,1,0)
        n4 = Node(1,1,0)
        n5 = Node(0,-0.5,0)
        n6 = Node(1.5,-0.5,0)
        nodes = [n0,n1,n2,n3,n4,n5,n6]
        
        
        
        e0 = Edge(n0,n1)
        e1 = Edge(n1,n4)
        e2 = Edge(n3,n4)
        e3 = Edge(n0,n3)
        e4 = Edge(n0,n6,geometricNodes=n5)
        e5 = Edge(n6,n4,geometricNodes=n2)
        e6 = Edge(n6,n1)
        
        edges = [e0,e1,e2,e3,e4,e5,e6]
        
        fi0 = Face([e0,e1,-e2,-e3])
        fi0.category1 = 'inner'
        fb0 = Face([e4,e6,-e0])
        fb0.category1 = 'border'
        fb1 = Face([e5,-e1,-e6])
        fb1.category1 = 'border'
        faces = [fi0,fb0,fb1]
        
        pc = PrimalComplex2D(nodes,edges,faces)
        dc = DualComplex2D(pc)
        
        dc.checkAllIncidenceMatrices()
        
        
        pc.useCategory = 2
        
        
        pc.printDualities()
        
        print(dc.useCategory)
        
#        for e in dc.edges:
#            print(e.useCategory)
        
#        print(pc.borderFaces)
#        print(pc.innerEdges)
#        
#        print(dc.borderNodes)
#        print(dc.innerEdges)
#        print(pc.incidenceMatrix1)
#        print(pc.incidenceMatrix2)
#        print(dc.incidenceMatrix1)
#        print(dc.incidenceMatrix2)
#        
#        
#        pc.useCategory = 2
#        print(pc.incidenceMatrix1)
#        print(pc.incidenceMatrix2)
#        print(dc.incidenceMatrix1)
#        print(dc.incidenceMatrix2)        
#        
#        pc.useCategory = 1
#        print(pc.incidenceMatrix1ii.shape,dc.incidenceMatrix2ii.shape)
#        print(pc.incidenceMatrix1ib.shape,dc.incidenceMatrix2bi.shape)
#        print(dc.incidenceMatrix1bi.shape,pc.incidenceMatrix2ib.shape)
#  
#


        

        
    

#-------------------------------------------------------------------------
#    Example 2: Automatic combination of additional border edges
#------------------------------------------------------------------------- 
        
        
        n100 = Node(0,0,0,num=0)
        n101 = Node(1,0,0,num=1)
        n102 = Node(1.5,1,0,num=2)
        n103 = Node(0,1,0,num=3)
        n104 = Node(1,1,0,num=4)
        n105 = Node(0,-0.5,0,num=5)
        n106 = Node(1.5,-0.5,0,num=6)
        nodes100 = [n100,n101,n102,n103,n104,n105,n106]
        
        
        e100 = Edge(n100,n101,num=0)
        e101 = Edge(n101,n104,num=1)
        e102 = Edge(n103,n104,num=2)
        e103 = Edge(n100,n103,num=3)
        e104 = Edge(n100,n105,num=4)
        e107 = Edge(n105,n106,num=7)
        e105 = Edge(n106,n102,num=5)
        e108 = Edge(n102,n104,num=8)
        e106 = Edge(n106,n101,num=6)
        
        edges100 = [e100,e101,e102,e103,e104,e105,e106,e107,e108]
        
        
        f100 = Face([e100,e101,-e102,-e103])
        f101 = Face([e104,e107,e106,-e100])
        f102 = Face([e105,e108,-e101,-e106])
        
        f101.category1 = 'border'
        f102.category1 = 'border'
        
        faces100 = [f100,f101,f102]
        
        c100 = PrimalComplex2D(nodes100,edges100,faces100)
        dc100 = DualComplex2D(c100)

        
        
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
            
            pc.useCategory = 1
            pc.plotComplex(axes[0])
            axes[0].view_init(90,180)
            axes[0].set_title('Category 1 primal')
            axes[0].axis('off')
            
            dc.plotComplex(axes[1])
            axes[1].view_init(90,180)
            axes[1].set_title('Category 1 dual')
            axes[1].axis('off')
            pc.useCategory = 2
            pc.plotComplex(axes[2])
            axes[2].view_init(90,180)
            axes[2].set_title('Primal')
            axes[2].axis('off')
            # figs[2].set_size_inches(4,4)
            figs[2].savefig('img/2D_primal.png',dpi=150)
            dc.plotComplex(axes[3])  
            axes[3].view_init(90,180)
            axes[3].set_title('Dual')
            axes[3].axis('off')
            # figs[3].set_size_inches(4,4)
            figs[3].savefig('img/2D_dual.png',dpi=150)            
#            c100.plotComplex(axes[2])
#            dc100.plotComplex(axes[3])

#    VTK
#--------------------------------------------------------------------- 
        elif plottingMethod == 'VTK' :
            cc.printBlue('Plot using VTK')
            cc.printRed('Not implemented')


#    TikZ
#--------------------------------------------------------------------- 
        elif plottingMethod == 'TikZ' :
            cc.printBlue('Plot using TikZ')            
            pic = dc.plotComplexTikZ()
            pic.scale=2
            pic.writeTikZFile(filename='Complex2DDual')
            
#    Animation
#--------------------------------------------------------------------- 
        elif plottingMethod == 'animation':
            cc.printBlue('Creating animation')
            cc.printRed('Not implemented')

#    Unknown
#---------------------------------------------------------------------             
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))         
        
