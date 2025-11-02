# -*- coding: utf-8 -*-
# =============================================================================
# EDGE
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Dec  7 14:16:21 2017

'''


'''
# =============================================================================
#    IMPORTS
# =============================================================================
if __name__ == '__main__':
    import os
    os.chdir('../../')

# ------------------------------------------------------------------------
#    Standard Libraries
# ------------------------------------------------------------------------

import logging

from kCells.cell import Cell
from kCells.node import Node
from kCells.edge.baseEdge import BaseEdge
from kCells.edge.simpleEdge import SimpleEdge
from kCells.edge.reversedEdge import ReversedEdge
import tools.colorConsole as cc
import tools.alphaNum as an

from tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)

# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class Edge(BaseEdge, Cell):
    '''

    Primal edge in positive direction.

    '''
    edgeCount = 0

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self,
                 start,
                 end,
                 *args,
                 num=None,
                 label='e',
                 geometricNodes=[],
                 **kwargs):
        '''
        This is the explanation of the __init__ method.

        All parameters should be listed:

        :param Node start: Start node
        :param Node end: End node
        :param int num: Number of the node. Leave empty for automatic numbering
        :param list geometricNodes: list of geometric nodes in correct order.

        '''
        if num is None:
            num = Edge.edgeCount
            Edge.edgeCount += 1

        super().__init__(*args,
                         label=label,
                         num=num,
                         myReverse=ReversedEdge(myReverse=self),
                         **kwargs)
        self.__geometricNodes = geometricNodes
        self.__startNode = start
        self.__endNode = end
        self.__showArrow = True
        self.__faces = []
        self.__simpleEdges = []

        self.setUp()
        if self.__simpleEdges:
            self.startNode.addEdge(self)
            self.endNode.addEdge(self)

            _log.info('Created edge {}'.format(self.infoText))

        _log.debug('Initialized Edge')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getShowArrow(self): return self.__showArrow

    def __setShowArrow(self, s): self.__showArrow = s

    showArrow = property(__getShowArrow, __setShowArrow)
    '''
    Show or hide the arrows in the plot.

    '''

    def __getFaces(self): return self.__faces

    faces = property(__getFaces)

    def __getStartNode(self):
        if self.geometryChanged:
            self.setUp()
        return self.__startNode

    def __setStartNode(self, s):
        _log.debug('Setting start node in edge %s', self)

        # Remove this edge from both nodes, to get connections right
        self.__startNode.delEdge(self)
        self.__endNode.delEdge(self)

        # set startNode
        self.__startNode = s

        # Add this edge to both (new) nodes
        self.__startNode.addEdge(self)
        self.__endNode.addEdge(self)
        self.updateGeometry()
    startNode = property(__getStartNode, __setStartNode)

    def __getEndNode(self):
        if self.geometryChanged:
            self.setUp()
        return self.__endNode

    def __setEndNode(self, s):
        _log.debug('Setting end node in edge %s', self)
        # Remove this edge from both nodes, to get connections right
        self.__endNode.delEdge(self)
        self.__startNode.delEdge(self)

        # set endNode
        self.__endNode = s

        # Add this edge to both (new) nodes
        self.__startNode.addEdge(self)
        self.__endNode.addEdge(self)
        self.updateGeometry()

    endNode = property(__getEndNode, __setEndNode)

    def __getTopologicNodes(self): return [self.startNode, self.endNode]

    topologicNodes = property(__getTopologicNodes)

    def __getAllNodes(self):
        return [self.startNode, *self.geometricNodes, self.endNode]

    allNodes = property(__getAllNodes)

    def __getGeometricNodes(self): return self.__geometricNodes

    def __setGeometricNodes(self, g):
        for n in self.__geometricNodes:
            if self in n.edges:
                n.delEdge(self)
        if isinstance(g, Cell):
            g = [g, ]
        self.__geometricNodes = g
        for n in self.__geometricNodes:
            n.isGeometrical = True
        self.updateGeometry()

    geometricNodes = property(__getGeometricNodes, __setGeometricNodes)

    def __getRadius(self):
        if len(self.simpleEdges) == 1:
            return self.simpleEdges[0].radius
        else:
            return [se.radius for se in self.simpleEdges]

    def __setRadius(self, r):
        for se in self.simpleEdges:
            se.radius = r

    radius = property(__getRadius, __setRadius)

    def __getSimpleEdges(self):
        if self.geometryChanged:
            self.setUp()
        return self.__simpleEdges

    simpleEdges = property(__getSimpleEdges)

    def __getCylinders(self):
        if self.geometryChanged:
            self.setUp()
        return [se.cylinder for se in self.simpleEdges]

    cylinders = property(__getCylinders)

    def __getProjectionFace(self): return self.__projectionFace

    def __setProjectionFace(self, p): self.__projectionFace = p

    projectionFace = property(__getProjectionFace, __setProjectionFace)

    def __getProjectedEdge(self): return self.__projectedEdge

    def __setProjectedEdge(self, p): self.__projectedEdge = p

    projectedEdge = property(__getProjectedEdge, __setProjectedEdge)

# =============================================================================
#    METHODS
# =============================================================================

# ------------------------------------------------------------------------
#    Set up edge
# ------------------------------------------------------------------------

    def setUp(self):
        _log.debug('Setting up edge {}'.format(self))
        for se in self.__simpleEdges:
            se.delete()
        self.__simpleEdges = []

        if isinstance(self.geometricNodes, Node):
            self.__geometricNodes = [self.__geometricNodes, ]

        allNodes = [self.__startNode, *self.__geometricNodes, self.__endNode]
        if self.checkIfDuplicates(allNodes):
            _log.error('Duplicate nodes in definition of {}: {}'
                              .format(self, allNodes))

        else:
            if all(allNodes):

                for n in self.__geometricNodes:
                    if self in n.edges:
                        n.delEdge(self)

                num = 0

                if len(self.__geometricNodes) == 0:
                    self.__simpleEdges.append(
                        SimpleEdge(start=self.__startNode,
                                   end=self.__endNode,
                                   belongsTo=self,
                                   labelSuffix='('+an.alphaNum(num)+')'))
                else:
                    for n in self.__geometricNodes:
                        n.isGeometrical = True
                        n.addEdge(self)
                    self.__simpleEdges.append(
                        SimpleEdge(start=self.__startNode,
                                   end=self.__geometricNodes[0],
                                   belongsTo=self,
                                   labelSuffix='('+an.alphaNum(num)+')'))
                    num += 1
                    if num > 25:
                        num = 0
                    for (n1, n2) in zip(self.__geometricNodes[:-1],
                                        self.__geometricNodes[1:]):
                        self.__simpleEdges.append(
                            SimpleEdge(start=n1,
                                       end=n2,
                                       belongsTo=self,
                                       labelSuffix='('+an.alphaNum(num)+')'))
                        num += 1
                        if num > 25:
                            num = 0
                    self.__simpleEdges.append(
                        SimpleEdge(start=self.__geometricNodes[-1],
                                   end=self.__endNode,
                                   belongsTo=self,
                                   labelSuffix='('+an.alphaNum(num)+')'))

            else:
                _log.debug('This edge is not completely defined, ' +
                                  'maybe its deleted')

            if len(self.__simpleEdges) == 1:
                self.__simpleEdges[0].labelSuffix = ''
        self.geometryChanged = False

# ------------------------------------------------------------------------
#    Add a face that uses this edge
# ------------------------------------------------------------------------
    def addFace(self, face):
        '''

        This method adds a face to the list of faces that this edge belongs to.
        This method is called from the Face class when the face is set up.

        '''
        if face in self.__faces:
            _log.error('Face {} already belongs to edge {}!'
                              .format(face.infoText, self.infoText))
        else:
            self.__faces.append(face)

# ------------------------------------------------------------------------
#    Delete a face that uses this edge
# ------------------------------------------------------------------------
    def delFace(self, face):
        '''

        This method deletes a face from the list of faces that this edge
        belongs to. This method is called from the Face class when the face
        is beeing deleted.

        '''
        if face in self.__faces:
            self.__faces.remove(face)
            _log.debug('Removed simple face {} from simple edge {}'
                             .format(face.infoText, self.infoText))
        else:
            _log.error('Cannot remove simple face {}'
                              .format(face.infoText) +
                              ' from simple edge {}!'.format(self.infoText))

# ------------------------------------------------------------------------
#
# ------------------------------------------------------------------------
    def updateGeometry(self):
        super().updateGeometry()
        for f in self.faces:
            f.updateGeometry()

# ------------------------------------------------------------------------
#    Invert the direction of the edge
# ------------------------------------------------------------------------
    def swap(self):
        '''

        Swap start and end node as well as the order of the geometric nodes.

        '''
        endNode = self.__startNode
        self.__startNode = self.__endNode
        self.__endNode = endNode
        self.__geometricNodes = list(reversed(self.__geometricNodes))
        self.updateGeometry()

# ------------------------------------------------------------------------
#    Delete the entire edge
# ------------------------------------------------------------------------
    def delete(self):
        if self.faces:
            _log.error('Cannot delete {} because it belongs to a face'
                              .format(self))
        else:
            for n in [self.__startNode, self.__endNode, *self.geometricNodes]:
                n.delEdge(self)
            self.__startNode = None
            self.__endNode = None
            self.__geometricNodes = []
            super().delete()

# ------------------------------------------------------------------------
#    Update text
# ------------------------------------------------------------------------
    def updateText(self):
        for se in self.__simpleEdges:
            se.updateText()
        super().updateText()

# ------------------------------------------------------------------------
#    Plot for Documentation
# ------------------------------------------------------------------------
    @classmethod
    def plotDoc(cls):
        '''
        Create all plots needed for the documentation.

        '''

        import tools.placeFigures as pf
        (figs, ax) = pf.getFigures(numTotal=1)
        n101 = Node(0, 0, 0, num=0)
        n102 = Node(1, 1, 1, num=1)
        e101 = Edge(n101, n102, num=0)
        n101.plotNode(ax[0])
        n102.plotNode(ax[0])
        e101.plotEdge(ax[0])
        pf.exportPNG(figs[0], 'doc/_static/edge1')


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == "__main__":
    import tools.placeFigures as pf
#    import matplotlib.pyplot as plt
    # from tools import MyLogging
#    from kCells import Node

    set_logging_format(logging.DEBUG)

    # Create some figures on second screen
    (fig, ax) = pf.getFigures(numTotal=6)

    n0 = Node(0, 0, 0)
    n1 = Node(0, 1, 0)
    n2 = Node(1, 0, 0)
    n3 = Node(1, 1, 0)
    n4 = Node(1.2, 2, 0)
    n5 = Node(2, 0, 0)
    n6 = Node(2, 1, 0)
    n7 = Node(2.2, 2, 0)
    n8 = Node(2, 3, 0)
    nodes = [n0, n1, n2, n3, n4, n5, n6, n7, n8]

    # ml.logger.info('')

    e0 = Edge(n0, n1)

    e1 = Edge(n2, n4, geometricNodes=[n3, ])
    e2 = Edge(n5, n8, geometricNodes=[n6, n7])

    print(e1.simpleEdges)

    edges = [e0, e1, e2]

    for n in nodes:
        n.plotNode(ax[0])
        n.plotNode(ax[1])

    for e in edges:
        e.plotEdge(ax[0])
        me = -e
        me.plotEdge(ax[1])
        print(me.simpleEdges[0].directionVec)

    cc.printBlue('change coordinate')
    cc.printWhite()
    n1.zCoordinate = 3

    n10 = Node(1, 0, 1, num=10)
    n14 = Node(1.2, 2, -1, num=14)
    nodes.append(n10)
    nodes.append(n14)
    cc.printBlue('Check before changing node:')
    cc.printWhite('start:', e1.startNode,
                  'end:', e1.endNode,
                  'n2 is connected to', n2.connectedNodes,
                  'n4 is connected to', n4.connectedNodes)
    cc.printWhite()
    cc.printBlue('Change start node of', e2)
    print('Edges of n2:', n2.edges)
    e1.startNode = n10
    cc.printWhite('start:', e1.startNode,
                  'end:', e1.endNode,
                  'n2 is connected to', n2.connectedNodes,
                  'n4 is connected to', n4.connectedNodes,
                  'n10 is connected to:', n10.connectedNodes)
    cc.printWhite()
    e1.endNode = n14

    n11 = Node(2, 1, 0.5, num=11)
    n12 = Node(2.2, 2, 0.8, num=12)
    n13 = Node(2.2, 2.3, 0.8, num=13)
    nodes.append(n11)
    nodes.append(n12)
    nodes.append(n13)
    e2.geometricNodes = [n11, n12, n13]

    for n in nodes:
        n.plotNode(ax[2])

    for e in edges:
        e.plotEdge(ax[2])

    cc.printBlue('barycenter:')
    for b in e2.barycenter:
        cc.printGreen('\t', b)
    cc.printBlue('directionVec:')
    for d in e2.directionVec:
        cc.printGreen('\t', d)

    e2.swap()
    for n in nodes:
        n.plotNode(ax[3])

    for e in edges:
        e.plotEdge(ax[3])

# =============================================================================
#    IMAGES FOR DOCUMENTATION
# =============================================================================
    if False:
        Edge.plotDoc()
