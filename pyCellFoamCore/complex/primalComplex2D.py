# -*- coding: utf-8 -*-
#==============================================================================
# PRIMAL COMPLEX 2D
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Oct 30 15:56:53 2019

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
from k_cells import Node, Edge, Face


#    Complex & Grids
#--------------------------------------------------------------------
from complex.complex2D import Complex2D


#    Tools
#--------------------------------------------------------------------
import tools.colorConsole as cc


#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class PrimalComplex2D(Complex2D):
    '''

    '''

#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__dualComplex',
                 '__useCategory',
                 '__changedNumbering')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,nodes=[],edges=[],faces=[]):
        '''
        :param list nodes:
        :param list edges:
        :param list faces:

        '''
        self.__dualComplex = None
        self.__useCategory = 1
        self.__changedNumbering = False
        super().__init__(nodes,edges,faces,loggerName = __name__)



    def setUp(self):
        '''
        Setting up the primal 2D complex with the following steps:

        1.  Categorize all k-cells (nodes, edges and faces) with categorization
            method 1 (balance equations on primal faces).
        2.  Sort all k-cells into lists according to their category 1.
        3.  Combine additional border edges so that a border face has a maximum
            of one additoinal border edge.
        4.  Sort all k-cells again into lists according to their category 1.
        5.  Categorize all k-cells (nodes, edges and faces) with categorization
            method 2 (balance equations on dual faces)
        6.  Sort all k-cells into lists according to their category 2.

        '''
        self.__categorizePrimal()
        self.sortPrimal()
        self.__combineAdditionalBorderEdges()
        self.sortPrimal()
        self.__categorizeDual()
        self.sortDual()
        self.__changedNumbering = True
        super().setUp()



#==============================================================================
#    SETTER AND GETTER
#==============================================================================

    def __getUseCategory(self): return self.__useCategory
    def __setUseCategory(self,u):
        if u in [1,2]:
            self.__changedNumbering = True
            self.updateComplex2D()
            if self.__dualComplex:
                self.__dualComplex.updateComplex2D()
            self.__useCategory = u
            for c in self.nodes+self.edges+self.faces:
                c.useCategory = u

            if self.__dualComplex:
                for c in self.__dualComplex.nodes+self.__dualComplex.edges+self.__dualComplex.faces:
                    c.useCategory = u
        else:
            self.logger.error('Cannot set useCategory of to {} - It must be either 1 or 2'.format(u))
    useCategory = property(__getUseCategory,__setUseCategory)
    '''

    '''


    def __getChangedNumbering(self): return self.__changedNumbering
    changedNumbering = property(__getChangedNumbering)
    '''

    '''


    def __getDualComplex(self): return self.__dualComplex
    def __setDualComplex(self,d):
        if self.__dualComplex is None:
            self.__dualComplex = d
        else:
            self.logger.error('Dual complex is already set')
    dualComplex = property(__getDualComplex,__setDualComplex)
    '''

    '''



#==============================================================================
#    METHODS
#==============================================================================








#-------------------------------------------------------------------------
#    Categorize k-cells (balance equations on primal complex)
#-------------------------------------------------------------------------
    def __categorizePrimal(self):
        '''

        '''

        # Categorize faces
        for f in self.faces:
            if f.category1 == 'undefined':
                f.category1 = 'inner'


        # Categorize edges
        for e in self.edges:
            if e.category1 == 'undefined':
                if len(e.faces) == 0:
                    self.logger.warning('Edge {} does not belong to a face'.format(e))
                elif len(e.faces) == 1:
                    if e.faces[0].category1 == 'inner':
                        e.category1 = 'border'
                    elif e.faces[0].category1 == 'border':
                        e.category1 = 'additionalBorder'
                    else:
                        self.logger.error('Unknown category1 {} of face {}'.format(e.faces[0].category1,e.faces[0]))
                elif len(e.faces) == 2:
                    e.category1 = 'inner'
                else:
                    self.logger.error('Edge {} has {} faces, this is too much'.format(e,len(e.faces)))
            else:
                self.logger.error('Edge {} was already categorized'.format(e))


        # Categorize nodes
        for n in self.nodes:

            if n.is_geometrical:
                if not n in self.geometricNodes:
                    self.geometricNodes.append(n)

            else:
                if n.category1 == 'undefined':
                    inner = True
                    border = False
                    for e in n.edges:
                        if e.category1 == 'border':
                            inner = False
                            border = True
                        elif e.category1 == 'additionalBorder':
                            inner = False
                    if inner:
                        n.category1 = 'inner'
                    elif border:
                        n.category1 = 'border'
                    else:
                        n.category1 = 'additionalBorder'

                else:
                    self.logger.error('Node {} was already categorized'.format(n))






#-------------------------------------------------------------------------
#    Categorize k-cells (balance equations on dual complex)
#-------------------------------------------------------------------------
    def __categorizeDual(self):
        '''

        '''

        # Categorize faces
        for f in self.faces:
            if f.category2 == 'undefined':
                f.category2 = f.category1


        # Categorize edges
        for e in self.edges:
            if e.category2 == 'undefined':
                if len(e.faces) == 0:
                    self.logger.warning('Edge {} does not belong to a face'.format(e))
                elif len(e.faces) == 1:
                    if e.faces[0].category2 == 'inner':
                        e.category2 = 'inner'
                    elif e.faces[0].category2 == 'border':
                        e.category2 = 'additionalBorder'
                    else:
                        self.logger.error('Unknown category2 {} of face {}'.format(e.faces[0].category2,e.faces[0]))
                elif len(e.faces) == 2:
                    if e.faces[0].category2 == 'inner' or e.faces[1].category2 == 'inner':
                        e.category2 = 'inner'
                    elif all([x.category2 in ['inner','border'] for x in e.faces]):
                        e.category2 = 'border'
                    else:
                        for f in e.faces:
                            if f.category2 not in ['inner','border']:
                                self.logger.error('Unknown category2 {} of face {}'.format(f.category2,f))


                else:
                    self.logger.error('Edge {} has {} faces, this is too much'.format(e,len(e.faces)))
            else:
                self.logger.error('Edge {} was already categorized'.format(e))



        # Categorize nodes
        for n in self.nodes:

            if n.is_geometrical:
                if not n in self.geometricNodes:
                    self.geometricNodes.append(n)

            else:
                if n.category2 == 'undefined':
                    border = False
                    additionalBorder = True
                    for e in n.edges:
                        connectedFaces = []
                        for f in e.faces:
                            if not f in connectedFaces:
                                connectedFaces.append(f)
                        if len(connectedFaces) == 1:
                            border = True
                        if any([f.category2 == 'inner' for f in e.faces]):
                            additionalBorder = False

                    if border:
                        if additionalBorder:
                            n.category2 = 'additionalBorder'
                        else:
                            n.category2 = 'border'

                    else:
                        n.category2 = 'inner'
                else:
                    self.logger.error('Node {} was already categorized'.format(n))





    def __combineAdditionalBorderEdges(self,myPrintDebug=None,myPrintError=None,myPrintInfo=None):
        '''

        '''
        if myPrintDebug == None:
            myPrintDebug = self.logger.debug
        if myPrintError == None:
            myPrintError = self.logger.error
        if myPrintInfo == None:
            myPrintInfo = self.logger.info

        for f in self.borderFaces1:
            myPrintDebug('Checking  border face {}'.format(f))

            edges = [e for e in f.edges if e.category1 == 'additionalBorder']

            myPrintDebug('The face belongs to additional border edges {}'.format(edges))

            if len(edges) == 0:
                myPrintError('Border face {} should belong to at least 1 additional border edges, but it has none'.format(f))
            elif len(edges) == 1:
                myPrintDebug('Border face {} has exactly 1 additional border edge, this is ok'.format(f))
            elif len(edges) == 2:
                myPrintInfo('Border face {} has exactly 2 additional border edges, trying to combine them'.format(f))
                error = False
                if edges[0].endNode == edges[1].startNode:
                    myPrintDebug('Combine  0 & 1')
                    newEdge = Edge(edges[0].startNode,edges[1].endNode,geometricNodes=[edges[0].endNode,])
                elif edges[0].startNode == edges[1].endNode:
                    myPrintDebug('Combine  1 & 0')
                    newEdge = Edge(edges[1].startNode,edges[0].endNode,geometricNodes=[edges[1].endNode,])
                elif edges[0].startNode == edges[1].startNode:
                    myPrintDebug('Combine  -0 & 1')
                    newEdge = Edge(edges[0].endNode,edges[1].endNode,geometricNodes=[edges[0].startNode,])
                elif edges[0].endNode == edges[1].endNode:
                    myPrintDebug('Combine  0 & -1')
                    newEdge = Edge(edges[0].startNode,edges[1].startNode,geometricNodes=[edges[0].endNode,])
                else:
                    myPrintError('Edges {} are not connected'.format(edges))
                    error = True

                if not error:
                    newEdges = f.edges[:]
                    for e in edges:
                        newEdges.remove(e)
                        if e.is_reverse:
                            e = -e
                        self.edges.remove(e)
                    newEdges.append(newEdge)
                    self.edges.append(newEdge)
                    newEdge.category1 = 'additionalBorder'
                    f.sortEdges = True
                    f.edges = newEdges
                    f.setUp()
                    for e in edges:
                        e.delete()



            else:
                myPrintError('Border face {} has {} additional border edges, combination of them is not implemented'.format(f,len(edges)))


#-------------------------------------------------------------------------
#    Renumber according to current category in use
#-------------------------------------------------------------------------

    def renumber(self):
        '''

        '''
        self.renumberList(self.geometricNodes)
        if self.useCategory == 1:
            self.renumberList(self.innerNodes1)
            self.renumberList(self.borderNodes1)
            self.renumberList(self.additionalBorderNodes1)
            self.renumberList(self.innerEdges1)
            self.renumberList(self.borderEdges1)
            self.renumberList(self.additionalBorderEdges1)
            self.renumberList(self.innerFaces1)
            self.renumberList(self.borderFaces1)
            self.__changedNumbering = False

        elif self.useCategory == 2:
            self.renumberList(self.innerNodes2)
            self.renumberList(self.borderNodes2)
            self.renumberList(self.additionalBorderNodes2)
            self.renumberList(self.innerEdges2)
            self.renumberList(self.borderEdges2)
            self.renumberList(self.additionalBorderEdges2)
            self.renumberList(self.innerFaces2)
            self.renumberList(self.borderFaces2)
            self.__changedNumbering = False

        else:
            self.logger.error('Unknown useCategory {}'.format(self.useCategory))



#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    import tools.placeFigures as pf

    from tools.myLogging import MyLogging


#-------------------------------------------------------------------------
#    Check categorization
#-------------------------------------------------------------------------
    def printCategories(c):
        cc.printMagenta('======================================')
        cc.printMagenta('NODES')
        cc.printMagenta('======================================')

        cc.printMagenta()
        cc.printMagenta('Inner nodes')
        cc.printMagenta('-----------------------------------')
        cc.printWhite(c.innerNodes)

        cc.printMagenta()
        cc.printMagenta('Border nodes')
        cc.printMagenta('-----------------------------------')
        cc.printWhite(c.borderNodes)

        cc.printMagenta()
        cc.printMagenta('Additional border nodes')
        cc.printMagenta('-----------------------------------')
        cc.printWhite(c.additionalBorderNodes)

        cc.printBlue()
        cc.printBlue()
        cc.printBlue('======================================')
        cc.printBlue('EDGES')
        cc.printBlue('======================================')


        cc.printBlue()
        cc.printBlue('Inner edges')
        cc.printBlue('-----------------------------------')
        cc.printWhite(c.innerEdges)

        cc.printBlue()
        cc.printBlue('Border edges')
        cc.printBlue('-----------------------------------')
        cc.printWhite(c.borderEdges)

        cc.printBlue()
        cc.printBlue('Additional border edges')
        cc.printBlue('-----------------------------------')
        cc.printWhite(c.additionalBorderEdges)


        cc.printGreen()
        cc.printGreen()
        cc.printGreen('======================================')
        cc.printGreen('FACES')
        cc.printGreen('======================================')

        cc.printGreen()
        cc.printGreen('Inner faces')
        cc.printGreen('-----------------------------------')
        cc.printWhite(c.innerFaces)

        cc.printGreen()
        cc.printGreen('Border faces')
        cc.printGreen('-----------------------------------')
        cc.printWhite(c.borderFaces)




    with MyLogging('PrimalComplex2D'):


#-------------------------------------------------------------------------
#    Example 1
#-------------------------------------------------------------------------
        n0 = Node(0,0,0)
        n1 = Node(1,0,0)
        n2 = Node(1.5,0,0)
        n3 = Node(0,1,0)
        n4 = Node(1,1,0)
        n5 = Node(0,1.5,0)
        n6 = Node(1.5,1.5,0)



        nodes = [n0,n1,n2,n3,n4,n5,n6]


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


        f0 = Face([e0,e5,-e2,-e4])
        f1 = Face([e1,e6,-e8,-e5])
        f2 = Face([e2,e8,-e3,-e7])

        f1.category1 = 'border'
        f2.category1 = 'border'

        faces = [f0,f1,f2]


        pc = PrimalComplex2D(nodes,edges,faces)









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
            pc.useCategory = 1
            pc.plotComplex(axes[0])
            pc.useCategory = 2
            pc.plotComplex(axes[1])


#    VTK
#---------------------------------------------------------------------
        elif plottingMethod == 'VTK' :
            cc.printBlue('Plot using VTK')
            cc.printRed('Not implemented')

#    TikZ
#---------------------------------------------------------------------
        elif plottingMethod == 'TikZ' :
            cc.printBlue('Plot using TikZ')
            pic = pc.plotComplexTikZ(plotEdges=False,plotFaces=False)
            pic.scale = 2
            file = False

            picNodes = pc.plotNodesTikZ()
            picNodes.scale = 2
            picNodes.writeTikZFile(filename='Complex2D0Nodes')

            picEdges = pc.plotEdgesTikZ()
            picEdges.scale = 2
            picEdges.writeTikZFile(filename='Complex2D1Edges')

            picFaces = pc.plotFacesTikZ()
            picFaces.scale = 2
            picFaces.writeTikZFile(filename='Complex2D2Faces')


            print(pc.incidenceMatrix1)
            print(pc.incidenceMatrix2)


            pic.writeLaTeXFile('latex','primalComplex2D',compileFile=file,openFile=file)

#    Animation
#---------------------------------------------------------------------
        elif plottingMethod == 'animation':
            cc.printBlue('Creating animation')
            cc.printRed('Not implemented')

#    Unknown
#---------------------------------------------------------------------
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))
