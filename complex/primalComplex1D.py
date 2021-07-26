# -*- coding: utf-8 -*-
#==============================================================================
# PRIMAL COMPLEX 1D
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Mon Mar 23 09:24:59 2020

'''

'''
#==============================================================================
#    IMPORTS
#==============================================================================

import os
if __name__ == '__main__':
    os.chdir('../')


from kCells import Node,Edge
from complex.complex1D import Complex1D

#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class PrimalComplex1D(Complex1D):
    '''
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ()

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,*args,**kwargs):
        '''
        :param Node nodes: List of all nodes
        :param Edge edges: List of all edges
        :param str loggerName: Optional name of the logger. Standard value 
            is `__name__`
        
        '''
        
        super().__init__(*args,**kwargs,loggerName=__name__)
        
        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    
#==============================================================================
#    METHODS
#==============================================================================

#-------------------------------------------------------------------------
#    Set Up
#-------------------------------------------------------------------------
        
    def setUp(self):
        '''
        Setting up the primal 1D complex with the following steps:
        
        1.  Categorize all k-cells (nodes and edges).
        2.  Sort all k-cells into lists according to their category.
        3.  Renumber k-cells to get the correct category numbering.
        
        '''
        self.logger.info('Called "Set Up" in PrimalComplex1D class')
        self.__categorize()
        self.sort()
        self.renumberList(self.innerNodes)
        self.renumberList(self.borderNodes)
        self.renumberList(self.additionalBorderNodes)
        self.renumberList(self.innerEdges)
        self.renumberList(self.borderEdges)
    
#-------------------------------------------------------------------------
#    Categorize
#-------------------------------------------------------------------------
    def __categorize(self):
        '''
        
        '''
        for e in self.edges:
            if e.category1 == 'undefined':
                e.category1 = 'inner'
        for n in self.nodes:
            if len(n.edges) == 0:
                self.logger.error('Unconnected node {} cannot be categorized'.format(n))
            elif len(n.edges) == 1:
                if n.edges[0].category1 == 'inner':
                    n.category1 = 'border'
                    self.logger.debug('Found border node')
                if n.edges[0].category1 ==  'border':
                    n.category1 = 'additionalBorder'
                    self.logger.debug('Found additional border node')
            elif len(n.edges) == 2:
                self.logger.debug('Found inner node')
                n.category1 = 'inner'
            else:
                self.logger.error('A node in a 1D-complex can have 2 edges at maximum, but {} has {}: {}'.format(n,len(n.edges),n.edges))
                
                

                
                
        
    
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    from tools import MyLogging
    import tools.colorConsole as cc
    import tools.placeFigures as pf
    
    
    with MyLogging('PrimalComplex1D',debug=False):
        
        cc.printBlue('Prepare plots')
        (figs,axes) = pf.getFigures(numTotal=4)
        
        cc.printBlue('Create some nodes')
        n0 = Node(0,0,0)
        n1 = Node(1,0,0)
        n2 = Node(2,0,0)
        n3 = Node(3.5,0,0)
        n4 = Node(4,0,0)
        nodes = [n0,n1,n2,n3,n4]
        
        
        cc.printBlue('Create some edges')
        e0 = Edge(n0,n1)
        e1 = Edge(n1,n2)
        e2 = Edge(n2,n3)
        e3 = Edge(n3,n4)
        edges = [e0,e1,e2,e3]
        
        e0.category1 = 'border'
        
        
        cc.printBlue('Combine them to a complex')
        c = PrimalComplex1D(nodes,edges)
        
#        cc.printBlue('Plot')
        c.plotComplex(axes[0])
        
        print(c.incidenceMatrix1ii)
        print(c.incidenceMatrix1ib)
        print(c.incidenceMatrix1bi)
        print(c.incidenceMatrix1bb)
        print(c.incidenceMatrix1Bi)
        print(c.incidenceMatrix1Bb)
#        
#        
#        pic = c.plotComplexTikZ()
#        pic.scale = 3
#        file = True
#        pic.writeLaTeXFile('latex','primalComplex1D',compileFile=file,openFile=file)
    

