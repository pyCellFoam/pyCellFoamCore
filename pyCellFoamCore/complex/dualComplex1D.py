# -*- coding: utf-8 -*-
#==============================================================================
# DUAL COMPLEX 1D
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue Mar 24 13:50:01 2020

'''

'''
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
from kCells import Node,DualNode1D,DualNode0D
from kCells import Edge,DualEdge1D

#    Complex & Grids
#--------------------------------------------------------------------
from complex.complex1D import Complex1D
from complex.primalComplex1D import PrimalComplex1D

#    Tools
#--------------------------------------------------------------------
import tools.colorConsole as cc
import tools.placeFigures as pf
from tools import MyLogging





#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class DualComplex1D(Complex1D):
    '''
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__primalComplex')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,primalComplex):
        '''
        
        :param PrimalComplex1D primalComplex: Primal complex of which the dual
            is constructed.
        
        '''
        self.__primalComplex = primalComplex
        super().__init__(loggerName=__name__)
        

        
                
            
        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================

    
#==============================================================================
#    METHODS
#==============================================================================
        
        
    def setUp(self):
        '''
        
        '''
        self.logger.info('Called "Set Up" in DualComplex1D class')
        self.__construct()
        self.sort()
        
        
    def __construct(self):
        '''
        
        '''
        error = False
        
        
        if not isinstance(self.__primalComplex,PrimalComplex1D):
            error = True
            self.logger.error('Need primal 1D complex as input, but got {}'.format(self.__primalComplex))
            
            
            
        dualNodes = []
        dualEdges = []
        if not error:
            for e in self.__primalComplex.edges:
                dualNodes.append(DualNode1D(e))
                
            for n in self.__primalComplex.borderNodes:
                dualNodes.append(DualNode0D(n))
                
                
            for n in self.__primalComplex.innerNodes+self.__primalComplex.borderNodes:
                dualEdges.append(DualEdge1D(n))
                
        self.nodes = dualNodes 
        self.edges = dualEdges        
    
#-------------------------------------------------------------------------
#    Method 1
#-------------------------------------------------------------------------
    
    def checkAllIncidenceMatrices(self,doPrints=True):
        '''
        
        '''
        checks = []
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1ii,-self.__primalComplex.incidenceMatrix1ii,'d̂1ii','-d1ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1ib,-self.__primalComplex.incidenceMatrix1bi,'d̂1ib','-d1bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1bi,-self.__primalComplex.incidenceMatrix1ib,'d̂1bi','-d1ib',doPrints))
        checks.append(self.checkIncidenceMatrixZero(self.incidenceMatrix1bb,'d̂1bb',doPrints))
        checks.append(self.checkIncidenceMatrixZero(self.__primalComplex.incidenceMatrix1bb,'d1bb',doPrints))
        
        if doPrints:
            if all(checks):
                cc.printGreen('All incidence matrix dualities are correct')
            else:
                cc.printRed('Not all incidence matrix dualities are correct')
        return checks
        
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    from tools import MyLogging
    
    import tools.placeFigures as pf
    import tools.tumcolor as tc
    
    
    with MyLogging('Complex1D'):
        
        cc.printBlue('Prepare plots')
        (figs,axes) = pf.getFigures(numTotal=4)
        
        cc.printBlue('Create some nodes')
        n0 = Node(0,0,0)
        n1 = Node(1,0,0)
        n2 = Node(2,0,0)
        # n3 = Node(3.5,0,0)
        # n4 = Node(4,0,0)
        # nodes = [n0,n1,n2,n3,n4]
        nodes = [n0,n1,n2]
        
        
        cc.printBlue('Create some edges')
        e0 = Edge(n0,n1)
        e1 = Edge(n1,n2)
        # e2 = Edge(n2,n3)
        # e3 = Edge(n3,n4)
        # edges = [e0,e1,e2,e3]
        edges = [e0,e1]
        
        e0.category1 = 'border'
        
        cc.printBlue('Combine them to a complex')
        pc = PrimalComplex1D(nodes,edges)
        
        cc.printBlue('Plot')
        pc.plotComplex(axes[0])
        axes[0].view_init(90,-90)
        axes[0].set_title('primal')
        axes[0].axis('off')
        figs[0].set_size_inches(4,4)
        figs[0].savefig('img/1D_primal.png',dpi=150)
        
        
        dc = DualComplex1D(pc)
        
        for n in dc.nodes:
            n.color = tc.TUMRose()
        
        dc.plotComplex(axes[1])
        
        axes[1].view_init(90,-90)
        axes[1].set_title('primal')
        axes[1].axis('off')
        figs[1].set_size_inches(4,4)    
        figs[1].savefig('img/1D_dual.png',dpi=150)
        
        
        cc.printBlue()
        cc.printBlue()
        cc.printBlue()
        dc.checkAllIncidenceMatrices()
        
        pc.printDualities()
        
        

