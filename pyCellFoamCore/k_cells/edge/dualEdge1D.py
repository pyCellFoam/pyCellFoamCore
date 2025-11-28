# -*- coding: utf-8 -*-
# =============================================================================
# DUAL EDGE 1D
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Dec  7 14:16:21 2017

'''
With Geometric Node
--------------------------------------------------------------------------

The standard procedure is to create a geometric node at the location of
the primal node.

.. image:: ../../../_static/dualEdge1D_1.png
   :width: 400px
   :alt: 1D dual edge with geometric node
   :align: center



Without Geometric Node
--------------------------------------------------------------------------

In the special case that both created simple edges align, the geometric node
is not necessary and can be removed, as well as the simple edges can be
combined.

.. image:: ../../../_static/dualEdge1D_0.png
   :width: 400px
   :alt: 1D dual edge without geometric node
   :align: center

'''

# =============================================================================
#    IMPORTS
# =============================================================================
# ------------------------------------------------------------------------
#    Change to Main Directory
# ------------------------------------------------------------------------
import os
if __name__ == '__main__':
    os.chdir('../../')


# ------------------------------------------------------------------------
#    Standard Libraries
# ------------------------------------------------------------------------
import numpy as np

# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------


#    kCells
# -------------------------------------------------------------------
from k_cells.cell import DualCell
from k_cells.node import Node, DualNode0D, DualNode1D

#    Complex & Grids
# -------------------------------------------------------------------
from k_cells.edge.edge import Edge

#    Tools
# -------------------------------------------------------------------
import tools.colorConsole as cc
import tools.placeFigures as pf
from tools import MyLogging
import tools.tumcolor as tc


# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class DualEdge1D(Edge, DualCell):
    '''
    Create  1D dual edge of a primal node

    '''

# =============================================================================
#    SLOTS
# =============================================================================
#    __slots__ = ()

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self,
                 node,
                 *args,
                 myPrintDebug=None,
                 myPrintError=None,
                 **kwargs):
        '''

        :param Node node: Primal node

        '''
        n1 = Node(0, 0, 0)
        n2 = Node(1, 0, 0)

        super().__init__(n1, n2,
                         *args,
                         num=node.num,
                         **kwargs)

        if myPrintDebug is None:
            myPrintDebug = self.logger.debug
            # myPrintDebug = cc.printYellow
        if myPrintError is None:
            myPrintError = self.logger.error
            # myPrintError = cc.printRed

        error = True

        if node.category1 == 'inner':
            if len(node.edges) == 2:

                newStartNode = node.edges[0].dualCell1D

                if np.allclose(newStartNode.coordinates,
                               self.endNode.coordinates):
                    self.swap()

                self.startNode = newStartNode
                self.endNode = node.edges[1].dualCell1D
                self.category1 = node.category1
                error = False
            else:
                self.logger.error('Can calcute the 1D dual of an inner node ' +
                                  'only if it belongs to exactly 2 edges')

        elif node.category1 == 'border':

            # 1D Case
            if len(node.edges) == 1:

                newStartNode = node.edges[0].dualCell1D

                if np.allclose(newStartNode.coordinates,
                               self.endNode.coordinates):
                    self.swap()
                self.startNode = newStartNode
                self.endNode = node.dualCell0D
                self.category1 = node.category1

                # in 1D edges must always point in positive direction!
                if np.allclose(self.directionVec, np.array([-1, 0, 0])):
                    self.swap()
                error = False

            # 3D case
            else:

                edges = [e for e in node.edges
                         if e.category1 == 'border' or
                         e.category1 == 'additionalBorder']
                if len(edges) == 2:
                    myPrintDebug('Creating dual edge for node {}'.format(node))
                    self.category1 = 'additionalBorder'
                    self.category2 = 'additionalBorder'
                    if not edges[0].dualCell1D:
                        self.logger.error('{} has no 1D '.format(edges[0]) +
                                          'dual, but that is needed')
                    elif not edges[1].dualCell1D:
                        self.logger.error('{} has no 1D '.format(edges[1]) +
                                          'dual, but that is needed')

                    else:
                        self.startNode = edges[0].dualCell1D
                        self.endNode = edges[1].dualCell1D
                        nGeo = DualNode0D(node)
                        self.geometricNodes = nGeo
                        self.setUp()
                        myPrintDebug(self.directionVec)
                        if np.linalg.norm(
                                self.directionVec[0]-self.directionVec[1]) \
                                < self.tolerance:
                            myPrintDebug('Removing geometric node')
                            self.geometricNodes = []
                        error = False
                else:
                    myPrintError('Node {} is border '.format(node.info_text) +
                                 'and should therefor belong to two ' +
                                 'border edges, ' +
                                 'but belongs to {}'.format(len(edges)))
        else:
            myPrintError('Unknown category {} of node {}'
                         .format(node.category1, node.info_text))

        if error:
            self.delete()
            self.logger.error('An error occured during the creation process ' +
                              'of dual Edge --> deleting')
        else:
            self.dualCell1D = node
            node.dualCell1D = self

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

# =============================================================================
#    METHODS
# =============================================================================
# ------------------------------------------------------------------------
#    Plot for Documentation
# ------------------------------------------------------------------------
    @classmethod
    def plotDoc(cls):
        from k_cells.node import DualNode1D
        from k_cells.edge import Edge
        import tools.placeFigures as pf

        n0 = Node(0, 0, 0)
        n1 = Node(1, 0, 0)
        n2 = Node(2, 0, 0)
        n3 = Node(3, 0, 0)
        n4 = Node(4, 0, 0)
        n5 = Node(4, 1, 0)
        nodes = [n0, n1, n2, n3, n4, n5]
        for n in nodes:
            n.category1 = 'border'

        e0 = Edge(n0, n1)
        e1 = Edge(n1, n2)
        e2 = Edge(n3, n4)
        e3 = Edge(n4, n5)
        edges = [e0, e1, e2, e3]
        for e in edges:
            e.category1 = 'border'

        dualNodes = []
        for e in edges:
            dualNodes.append(DualNode1D(e))

        de1 = DualEdge1D(n1)
        de4 = DualEdge1D(n4)

        (figs, axes) = pf.getFigures(numTotal=2)

        for n in [n0, n1, n2]:
            n.plotNode(axes[0])
        for e in [e0, e1]:
            e.plotEdge(axes[0])
        de1.color = tc.TUMLightBlue()
        de1.plotEdge(axes[0])
        for dn in dualNodes[:2]:
            dn.color = tc.TUMRose()
            dn.plotNode(axes[0])

        for n in [n3, n4, n5]:
            n.plotNode(axes[1])
        for e in [e2, e3]:
            e.plotEdge(axes[1])
        de4.color = tc.TUMLightBlue()
        de4.plotEdge(axes[1])
        for dn in dualNodes[2:]:
            dn.color = tc.TUMRose()
            dn.plotNode(axes[1])

        for (i, f) in enumerate(figs):
            pf.exportPNG(f, 'doc/_static/dualEdge1D_'+str(i))


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':

    with MyLogging('dualEdge1D'):

        # ---------------------------------------------------------------------
        #     Create some examples
        # ---------------------------------------------------------------------

        n0 = Node(0, 0, 0)
        n1 = Node(1, 0, 0)
        n2 = Node(2, 0, 0)
        n3 = Node(3, 0, 0)
        n4 = Node(4, 0, 0)
        n5 = Node(4, 1, 0)
        nodes = [n0, n1, n2, n3, n4, n5]
        for n in nodes:
            n.category1 = 'border'

        e0 = Edge(n0, n1)
        e1 = Edge(n1, n2)
        e2 = Edge(n3, n4)
        e3 = Edge(n4, n5)
        edges = [e0, e1, e2, e3]
        for e in edges:
            e.category1 = 'border'

        dualNodes = []
        for e in edges:
            dualNodes.append(DualNode1D(e))

        de1 = DualEdge1D(n1, myPrintDebug=cc.printYellow)
        de4 = DualEdge1D(n4, myPrintDebug=cc.printYellow)
        dualEdges = [de1, de4]

# ------------------------------------------------------------------------
#    Plotting
# ------------------------------------------------------------------------

        # Choose plotting method.
        # Possible choices: pyplot, VTK, TikZ, animation, doc, None
        plottingMethod = 'doc'


#    Disabled
# --------------------------------------------------------------------
        if plottingMethod is None or plottingMethod == 'None':
            cc.printBlue('Plotting disabled')

#    Pyplot
# --------------------------------------------------------------------
        elif plottingMethod == 'pyplot':
            cc.printBlue('Plot using pyplot')
            (figs, axes) = pf.getFigures(numTotal=2)
            for n in [n0, n1, n2]:
                n.plotNode(axes[0])
            for e in [e0, e1]:
                e.plotEdge(axes[0])
            de1.color = tc.TUMLightBlue()
            de1.plotEdge(axes[0])
            for dn in dualNodes[:2]:
                dn.color = tc.TUMRose()
                dn.plotNode(axes[0])

            for n in [n3, n4, n5]:
                n.plotNode(axes[1])
            for e in [e2, e3]:
                e.plotEdge(axes[1])
            de4.color = tc.TUMLightBlue()
            de4.plotEdge(axes[1])
            for dn in dualNodes[2:]:
                dn.color = tc.TUMRose()
                dn.plotNode(axes[1])

#    VTK
# --------------------------------------------------------------------
        elif plottingMethod == 'VTK':
            cc.printBlue('Plot using VTK')
            cc.printRed('Not implemented')

#    TikZ
# --------------------------------------------------------------------
        elif plottingMethod == 'TikZ':
            cc.printBlue('Plot using TikZ')
            cc.printRed('Not implemented')

#    Animation
# --------------------------------------------------------------------
        elif plottingMethod == 'animation':
            cc.printBlue('Creating animation')
            cc.printRed('Not implemented')

#    Documentation
# --------------------------------------------------------------------
        elif plottingMethod == 'doc':
            cc.printBlue('Creating plots for documentation')
            DualEdge1D.plotDoc()

#    Unknown
# --------------------------------------------------------------------
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))
