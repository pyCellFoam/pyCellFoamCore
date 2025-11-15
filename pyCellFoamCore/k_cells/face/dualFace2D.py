# -*- coding: utf-8 -*-
# =============================================================================
# TITLE
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Mon Jul 23 17:29:19 2018

'''
This is the explanation of the whole module and will be printed at the very
beginning

Use - signs to declare a headline
--------------------------------------------------------------------------

* this is an item
* this is another one

#. numbered lists
#. are also possible


Maths
--------------------------------------------------------------------------

Math can be inline :math:`a^2 + b^2 = c^2` or displayed

.. math::

   (a + b)^2 = a^2 + 2ab + b^2

   (a - b)^2 = a^2 - 2ab + b^2

Always remember that the last line has to be blank

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

from k_cells.cell import DualCell
from k_cells import Edge, DualEdge3D, DualEdge2D, BaseEdge
from k_cells.face.face import Face
from k_cells import DualNode0D
import numpy as np
import tools.colorConsole as cc
from tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)

# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class DualFace2D(Face, DualCell):
    '''
    This is the explanation of this class.

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
                 **kwargs):
        '''
        :param Node node: Primal node

        '''
        super().__init__([],
                         *args,
                         num=node.num,
                         **kwargs)


        error = True
        if node.category1 == 'inner':
            self.category1 = 'inner'
            self.category2 = node.category2
            _log.debug('Assuming 2D complex')
            _log.debug('Creating 2D dual of inner node {}'
                         .format(node.infoText))
            dualEdges = [e.dualCell2D for e in node.edges]
            dualSortedEdges = self.__sortEdges(dualEdges,
                                               _log.debug,
                                               _log.error)
            _log.debug(dualSortedEdges)
            self.edges = dualSortedEdges
            self.setUp()

            if np.linalg.norm(self.normalVec-np.array([0, 0, 1])) \
                    > self.tolerance:
                _log.debug('Face pointed in the wrong direction')
                self.edges = [e.my_reverse for e in reversed(dualSortedEdges)]
                self.setUp()

            error = False

        elif node.category1 == 'border':

            _log.debug('Creating 2D dual of border node {}'
                         .format(node.infoText))

            primEdges = []
            for e in node.edges:
                if e.category1 not in ['inner', 'undefined']:
                    primEdges.append(e)

            if len(primEdges) == 2 and len(primEdges[0].faces) == 1:
                _log.debug('Assuming 2D complex')

                self.category1 = 'border'
                self.category2 = 'border'
                dualEdges = []
                for e in node.edges:
                    if e.dualCell2D:
                        dualEdges.append(e.dualCell2D)
                dualEdges.append(node.dualCell1D)
                dualSortedEdges = self.__sortEdges(dualEdges,
                                                   _log.debug,
                                                   _log.error)
                _log.debug(dualSortedEdges)

                if dualSortedEdges:
                    self.edges = dualSortedEdges
                    self.setUp()
                    error = False
                    if np.linalg.norm(self.normalVec-np.array([0, 0, 1])) \
                            > self.tolerance:
                        _log.debug('Face pointed in the wrong direction')
                        self.edges = [e.my_reverse
                                      for e in reversed(dualSortedEdges)]
                        self.setUp()
                else:
                    _log.error('Cannot build face with the edges {}'
                                      .format(dualSortedEdges))

            else:
                self.category1 = 'additionalBorder'
                self.category2 = 'additionalBorder'

                _log.info('Dual face of border node in 3D complex')
                _log.debug('Primal (additional) border edges that' +
                             ' belong to the node {}'.format(primEdges))

                dualEdges = []
                for e in primEdges:
                    if e.category1 == 'additionalBorder':
                        if e.dualCell2D:
                            dualEdges.append(e.dualCell2D)
                    else:
                        if not e.dualCell2D:
                            DualEdge2D(e)
                        dualEdges.append(e.dualCell2D)

                dualEdgesSorted = self.__sortEdges(dualEdges)

                if dualEdgesSorted:
                    _log.debug('Dual (additional) border edges that ' +
                                 'belong to the node {}'
                                 .format(dualEdgesSorted))

                    dualSimpleEdges = []
                    for e in dualEdgesSorted:
                        simpleEdges = e.simpleEdges
                        for se in simpleEdges:
                            dualSimpleEdges.append(se)
                    _log.debug('Simple edges around the dual face: {}'
                                 .format(dualSimpleEdges))

                    if node.dualCell0D is None:
                        DualNode0D(node)
                    centerNode = node.dualCell0D

                    edgesForFaces = []

                    e1 = Edge(centerNode, dualSimpleEdges[0].startNode)
                    sem = dualSimpleEdges[0]
                    em = sem.belongs_to
                    e2 = Edge(dualSimpleEdges[0].endNode, centerNode)
                    edgesForFaces.append([e1, em, e2])
                    _log.debug('Creating first triangle with dual edges {}'
                                 .format([e1.info_text,
                                          sem.infoText,
                                          e2.info_text]))
                    _log.debug('Nodes that should define the simple face: ' +
                                 '{} {} {} {} {} {}'
                                 .format(e1.startNode,
                                         e1.endNode,
                                         sem.startNode,
                                         sem.endNode,
                                         e2.startNode,
                                         e2.endNode))

                    for sem in dualSimpleEdges[1:-1]:
                        e1 = -e2
                        em = sem.belongs_to
                        e2 = Edge(sem.endNode, centerNode)
                        edgesForFaces.append([e1, em, e2])
                        _log.debug('Creating triangle with dual edge {}'
                                     .format([e1.infoText,
                                              sem.infoText,
                                              e2.info_text]))
                        _log.debug('Nodes that should define the simple ' +
                                     'face: {} {} {} {} {} {}'
                                     .format(e1.startNode,
                                             e1.endNode,
                                             sem.startNode,
                                             sem.endNode,
                                             e2.startNode,
                                             e2.endNode))

                    e1 = -e2
                    sem = dualSimpleEdges[-1]
                    em = sem.belongs_to
                    e2 = -edgesForFaces[0][0]
                    edgesForFaces.append([e1, em, e2])
                    _log.debug('Creating last triangle with dual edge {}'
                                 .format([e1.infoText,
                                          em.infoText,
                                          e2.infoText]))
                    _log.debug('Nodes that should define the simple face: ' +
                                 '{} {} {} {} {} {}'
                                 .format(e1.startNode,
                                         e1.endNode,
                                         sem.startNode,
                                         sem.endNode,
                                         e2.startNode,
                                         e2.endNode))

                    self.edges = edgesForFaces
                    self.setUp()
                    error = False

                else:
                    error = True

        if error:
            self.delete()
            _log.error('An error occured during the creation process ' +
                         'of dual face --> deleting')
        else:
            self.dualCell2D = node
            node.dualCell2D = self

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

# =============================================================================
#    METHODS
# =============================================================================

    def __sortEdges(self, edges):

        if not all([isinstance(e, BaseEdge) for e in edges]):
            _log.error('Need list of edges, but got {}'.format(edges))
            return False

        edgesSorted = [edges[0], ]
        edges.pop(0)

        counter = 0
        maxCounter = 50
        while len(edges) > 0 and counter < maxCounter:
            counter += 1
            for e in edges:
                if e.startNode == edgesSorted[-1].endNode:
                    edgesSorted.append(e)
                    edges.remove(e)
                elif e.endNode == edgesSorted[-1].endNode:
                    edgesSorted.append(-e)
                    edges.remove(e)

        if counter >= maxCounter:
            _log.error('Cannot find closed circle to define dual Face {}'
                         .format(self.info_text))
            return False

        return edgesSorted


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == "__main__":

    from k_cells.node import Node
    from k_cells.node import DualNode3D, DualNode2D
#    from edge import Edge
    from k_cells.face import Face
    from k_cells.volume.volume import Volume
    import tools.placeFigures as pf
#    import tools.colorConsole as cc
#    from tools import MyLogging
    import tools.myLogging as ml
    import tools.tumcolor as tc
    set_logging_format(logging.DEBUG)
    n0 = Node(0, 0, 0)
    n1 = Node(1, 0, 0)
    n2 = Node(0, 1, 0)
    n3 = Node(0, 0, 1)
    n4 = Node(1, 1, 1)
    n5 = Node(0.8, 1.5, -2)
    n6 = Node(1, 0, 4)
    nodes = [n0, n1, n2, n3, n4, n5, n6]

    for n in nodes:
        n.useCategory1 = 1

    e0 = Edge(n0, n1)
    e1 = Edge(n0, n2)
    e2 = Edge(n0, n3)
    e3 = Edge(n1, n2)
    e4 = Edge(n1, n3)
    e5 = Edge(n2, n3)
    e6 = Edge(n1, n4)
    e7 = Edge(n2, n4)
    e8 = Edge(n3, n4)
    e9 = Edge(n5, n1)
    e10 = Edge(n5, n4)
    e11 = Edge(n5, n2)
    e12 = Edge(n0, n5)
    e13 = Edge(n1, n6)
    e14 = Edge(n3, n6)
    e15 = Edge(n4, n6)

    edges = [e0, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10,
             e11, e12, e13, e14, e15]

    e3.category1 = 'inner'
    for e in edges:
        if e.category1 == 'undefined':
            e.category1 = 'border'

    f0 = Face([e0, e3, -e1])
    f1 = Face([e1, e5, -e2])
    f2 = Face([e0, e4, -e2])
    f3 = Face([e3, e5, -e4])
    f4 = Face([e4, e8, -e6])
    f5 = Face([e5, e8, -e7])
    f6 = Face([e3, e7, -e6])
    f7 = Face([e9, e6, -e10])
    f8 = Face([e11, e7, -e10])
    f9 = Face([e9, e3, -e11])
    f10 = Face([e12, e9, -e0])
    f11 = Face([e12, e11, -e1])
    f12 = Face([e4, e14, -e13])
    f13 = Face([e14, -e15, -e8])
    f14 = Face([e13, -e15, -e6])

    faces = [f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10,
             f11, f12, f13, f14]

    v0 = Volume([-f0, -f1, f2, f3])
    v1 = Volume([f6, f5, -f4, -f3])
    v2 = Volume([f9, f8, -f7, -f6])
    v3 = Volume([f10, -f11, -f9, f0])
    v4 = Volume([-f14, -f12, f13, f4])
    volumes = [v0, v1, v2, v3, v4]
    for v in volumes:
        v.category = 'inner'

    for f in faces:
        if len(f.volumes) == 2:
            f.category1 = 'inner'
        else:
            f.category1 = 'border'

    (figs, ax) = pf.getFigures(2, 2)
    for n in nodes:
        n.plotNode(ax[0])
    for e in edges:
        e.plotEdge(ax[0])
    for f in faces:
        f.plotFace(ax[0])

    for v in volumes:
        v.plotVolume(ax[1])

    dualNodes = []
    for v in volumes:
        dualNodes.append(DualNode3D(v))

    for f in faces:
        DualNode2D(f)

    dualEdges = []
    for f in faces:
        dualEdges.append(DualEdge3D(f))
    for e in edges:
        if e.category == 'border':
            dualEdges.append(DualEdge2D(e))

    n6.category1 = 'border'
    df1 = DualFace2D(n6)

    df1.plotFace(ax[3])

    red = tc.TUMcolor([255, 0, 0], 'red')
    for e in n6.edges:
        de = e.dualCell2D
        de.color = red
        de.plotEdge(ax[3])

    for v in volumes:
        v.showLabel = False
        v.plotVolume(ax[2])
    for n in dualNodes:
        n.plotNode(ax[2])

    for de in dualEdges:
        de.plotEdge(ax[2])

    for e in edges:
        e.showArrow = False
        e.showLabel = False
        e.plotEdge(ax[3])
