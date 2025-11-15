# -*- coding: utf-8 -*-
# =============================================================================
# DUAL FACE 3D
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Mon Jul  9 16:49:21 2018

'''

'''



# =============================================================================
#    IMPORTS
# =============================================================================

# ------------------------------------------------------------------------
#    Change to Main Directory
# ------------------------------------------------------------------------
if __name__ == '__main__':
    import os
    os.chdir('../../')

# ------------------------------------------------------------------------
#    Standard Libraries
# ------------------------------------------------------------------------
import logging

# ------------------------------------------------------------------------
#    Third Party Libraries
# ------------------------------------------------------------------------
import numpy as np

# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------

#    kCells
# -------------------------------------------------------------------
from pyCellFoamCore.k_cells.cell.dual_cell import DualCell
from k_cells.edge import Edge, DualEdge3D
from k_cells.face import Face
from k_cells import DualNode1D
from k_cells import Node
from k_cells import DualNode3D, DualNode2D
from k_cells import DualEdge2D
from k_cells.volume.volume import Volume


#    Tools
# -------------------------------------------------------------------

from tools.logging_formatter import set_logging_format
import tools.placeFigures as pf

# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


# =============================================================================
#    CLASS DEFINITION
# =============================================================================

class DualFace3D(Face, DualCell):
    '''

    '''

# =============================================================================
#    SLOTS
# =============================================================================
#    __slots__ = ('___log.debug', '___log.error')

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self,
                 edge,
                 *args,
                 **kwargs):
        '''
        :param edge Edge: Primal edge

        '''

        super().__init__([],
                         *args,
                         num=edge.num,
                         **kwargs)

        _log.info("Create dual face of {}".format(edge))

        if edge.category1 == 'inner':
            _log.info('Dual Face of inner edge')
            # Find center node
            _log.debug('Creating dual of edge {} that belongs to faces {}'
                         .format(edge.infoText, edge.faces))
            if edge.dualCell1D is None:
                centerNode = DualNode1D(edge)
            else:
                centerNode = edge.dualCell1D
            _log.debug('Center for dual face: {}'
                         .format(centerNode.info_text))

            # Find all edges that define the dual face
            dualEdges = []
            for f in edge.faces:
                if f.dualCell3D is None:
                    _log.error('Dual edge of {}: {}'.format(f, f.dualCell3D))
                else:
                    dualEdges.append(f.dualCell3D)
                    _log.debug('Dual edge of {}: {}'.format(f, f.dualCell3D))

            dualEdgesSorted = self.__sortEdges(dualEdges)
            _log.debug('Sorted dual Edges: {}'.format(dualEdgesSorted))

            # Find all simple edges that define a closed circle around the
            # dual face
            simpleEdgesForFaces = []
            for e in dualEdgesSorted:
                for se in e.simpleEdges:
                    simpleEdgesForFaces.append(se)
            _log.debug(simpleEdgesForFaces)

            # Find edges to define simple faces
            edgesForFaces = []
            sem = simpleEdgesForFaces[0]
            em = sem.belongs_to
            e1 = Edge(centerNode, sem.startNode)
            e2 = Edge(sem.endNode, centerNode)
            _log.debug('Creating first triangle with dual edges {}'
                         .format([e1.info_text, sem.infoText, e2.info_text]))
            edgesForFaces.append([e1, em, e2])

            _log.debug('Nodes that should define the simple face: ' +
                         '{} {} {} {} {} {}'
                         .format(e1.startNode,
                                 e1.endNode,
                                 sem.startNode,
                                 sem.endNode,
                                 e2.startNode,
                                 e2.endNode))

            for sem in simpleEdgesForFaces[1:-1]:
                e1 = -e2
                em = sem.belongs_to
                e2 = Edge(sem.endNode, centerNode)
                _log.debug('Creating triangle with dual edge {}'
                             .format([e1.infoText, em.infoText, e2.info_text]))
                edgesForFaces.append([e1, em, e2])
                _log.debug('Nodes that should define the simple face: ' +
                             '{} {} {} {} {} {}'
                             .format(e1.startNode,
                                     e1.endNode,
                                     sem.startNode,
                                     sem.endNode,
                                     e2.startNode,
                                     e2.endNode))

            e1 = -e2
            e2 = -edgesForFaces[0][0]
            em = simpleEdgesForFaces[-1].belongs_to
            _log.debug('Creating last triangle with dual edge {}'
                         .format([e1.infoText, em.infoText, e2.infoText]))
            _log.debug('Nodes that should define the simple face: ' +
                         '{} {} {} {} {} {}'
                         .format(e1.startNode,
                                 e1.endNode,
                                 sem.startNode,
                                 sem.endNode,
                                 e2.startNode,
                                 e2.endNode))
            edgesForFaces.append([e1, em, e2])

            self.category1 = 'inner'
            self.category2 = edge.category2
            self.edges = edgesForFaces
            self.setUp()

        elif edge.category1 == 'border':
            edge.dualCell2D.setUp()
            if len(edge.dualCell2D.simpleEdges) == 2:
                _log.debug('Dual Face of border edge with 2 simple edges')
                # Find center node
                _log.debug('Creating dual of edge {}'.format(edge.infoText) +
                             ' that belongs to faces {}'.format(edge.faces))
                if edge.dualCell1D is None:
                    centerNode = DualNode1D(edge)
                else:
                    centerNode = edge.dualCell1D
                _log.debug('Center for dual face: {}'
                             .format(centerNode.info_text))

                # Find all edges that define the dual face
                dualEdges = []
                if edge.dualCell2D is None:
                    DualEdge2D(edge)
                dualEdges.append(edge.dualCell2D)
                if edge.dualCell2D is None:
                    _log.error('Cannot calculate 2D dual of edge')
                for f in edge.faces:
                    if f.category != 'additionalBorder':
                        if f.dualCell3D is None:
                            DualEdge3D(f)
                        dualEdges.append(f.dualCell3D)

                _log.debug('Edges before sorting: {}'.format(dualEdges))
                _log.debug('Nodes of edges: {}'
                             .format([(e.startNode, e.endNode)
                                      for e in dualEdges]))

                dualEdgesSorted = self.__sortEdges(dualEdges)
                _log.debug('Sorted dual Edges: {}'.format(dualEdgesSorted))

                if dualEdgesSorted:

                    _log.debug('Sorted dual Edges: {}'
                                 .format(dualEdgesSorted))

                    # Find all simple edges that define a closed circle
                    # around the dual face
                    simpleEdgesForFaces = []
                    for e in dualEdgesSorted:
                        for se in e.simpleEdges:
                            simpleEdgesForFaces.append(se)
                    _log.debug(simpleEdgesForFaces)

                    # Find edges to define simple faces
                    edgesForFaces = []
                    sem = simpleEdgesForFaces[2]
                    em = sem.belongs_to
                    e1 = edge.dualCell2D
                    e2 = Edge(sem.endNode, centerNode)
                    _log.debug('Creating first triangle with dual edges {}'
                                 .format([e1.infoText,
                                          sem.infoText,
                                          e2.info_text]))
                    edgesForFaces.append([e1, em, e2])
                    _log.debug('Nodes that should define the simple face: ' +
                                 '{} {} {} {} {} {}'
                                 .format(e1.startNode,
                                         e1.endNode,
                                         sem.startNode,
                                         sem.endNode,
                                         e2.startNode,
                                         e2.endNode))
                    for sem in simpleEdgesForFaces[3:-1]:
                        e1 = -e2
                        em = sem.belongs_to
                        e2 = Edge(sem.endNode, centerNode)
                        _log.debug('Creating triangle with dual edge {}'
                                     .format([e1.infoText,
                                              em.infoText,
                                              e2.info_text]))
                        edgesForFaces.append([e1, em, e2])
                        _log.debug('Nodes that should define the simple ' +
                                     'face: {} {} {} {} {} {}'
                                     .format(e1.startNode,
                                             e1.endNode,
                                             sem.startNode,
                                             sem.endNode,
                                             e2.startNode,
                                             e2.endNode))

                    e1 = -e2
                    e2 = edge.dualCell2D
                    em = simpleEdgesForFaces[-1].belongs_to
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
                    edgesForFaces.append([e1, em, e2])

                    self.category1 = 'border'
                    self.category2 = edge.category2
                    self.edges = edgesForFaces
                    self.setUp()

            elif len(edge.dualCell2D.simpleEdges) == 1:
                _log.info('Dual Face of border edge with 1 simple edge')

                # Find all edges that define the dual face
                dualEdges = []
                if edge.dualCell2D is None:
                    DualEdge2D(edge)
                dualEdges.append(edge.dualCell2D)
                if edge.dualCell2D is None:
                    _log.error('Cannot calculate 2D dual of edge')
                for f in edge.faces:
                    if f.category != 'additionalBorder':
                        if f.dualCell3D is None:
                            DualEdge3D(f)
                        dualEdges.append(f.dualCell3D)

                _log.debug('Edges before sorting: {}'.format(dualEdges))
                _log.debug('Nodes of edges: {}'
                             .format([(e.startNode, e.endNode)
                                      for e in dualEdges]))

                dualEdgesSorted = self.__sortEdges(dualEdges)
                _log.debug('Sorted dual Edges: {}'.format(dualEdgesSorted))

                if dualEdgesSorted:
                    _log.debug('{}: length of dual edges to define face: {}'
                                 .format(self.info_text, len(dualEdgesSorted)))

                    if len(dualEdgesSorted) < 3:
                        _log.error('{}: A face '.format(self.info_text) +
                                     'with less than 3 edges is not possible')
                    elif len(dualEdgesSorted) == 3:
                        edgesForFaces = [dualEdgesSorted, ]
                    else:

                        _log.debug('Sorted dual Edges: {}'
                                     .format(dualEdgesSorted))

                        # Find all simple edges that define a closed circle
                        # around the dual face
                        simpleEdgesForFaces = []
                        for e in dualEdgesSorted:
                            for se in e.simpleEdges:
                                simpleEdgesForFaces.append(se)
                        _log.debug(simpleEdgesForFaces)

                        # Find edges to define simple faces
                        edgesForFaces = []
                        sem = simpleEdgesForFaces[1]
                        centerNode = edge.dualCell2D.startNode
                        em = sem.belongs_to
                        e1 = edge.dualCell2D
                        e2 = Edge(sem.endNode, centerNode)
                        _log.debug('Creating first triangle with dual ' +
                                     'edges {}'.format([e1.infoText,
                                                        sem.infoText,
                                                        e2.info_text]))
                        edgesForFaces.append([e1, em, e2])
                        _log.debug('Nodes that should define the simple ' +
                                     'face: {} {} {} {} {} {}'
                                     .format(e1.startNode,
                                             e1.endNode,
                                             sem.startNode,
                                             sem.endNode,
                                             e2.startNode,
                                             e2.endNode))
                        for sem in simpleEdgesForFaces[2:-2]:
                            e1 = -e2
                            em = sem.belongs_to
                            e2 = Edge(sem.endNode, centerNode)
                            _log.debug(
                                'Creating triangle with dual edge {}'
                                .format([e1.infoText,
                                         em.infoText,
                                         e2.info_text]))
                            edgesForFaces.append([e1, em, e2])
                            _log.debug(
                                'Nodes that should define the simple face: ' +
                                '{} {} {} {} {} {}'
                                .format(e1.startNode,
                                        e1.endNode,
                                        sem.startNode,
                                        sem.endNode,
                                        e2.startNode,
                                        e2.endNode))

                        #  TODO: !!!! ATTENTION: WHAT HAPPENS IF THE LAST TWO
                        # SIMPLE EDGES BELONG TO THE SAME EDGE???
                        e1 = -e2
                        em = simpleEdgesForFaces[-2].belongs_to
                        e2 = simpleEdgesForFaces[-1].belongs_to
                        edgesForFaces.append([e1, em, e2])

                    self.category1 = 'border'
                    self.category2 = edge.category2
                    self.edges = edgesForFaces
                    self.setUp()

            else:
                _log.error('2D dual of edge {} does not have 2 simple edges'
                             .format(self.info_text))

        else:
            _log.error('Unknwon cateogry {}. '.format(edge.category) +
                         'Cannot create dual face for edge {}'
                         .format(edge.infoText))

        # Change direction if it does not fit with the primal edge
        if self.normalVec:
            if self.normalVec[0] is not None:
                if np.inner(self.normalVec[0], edge.directionVec[0]) < 0:
                    _log.debug('Old edges: {}'.format(edgesForFaces))
                    newEdges = []
                    for es in edgesForFaces:
                        newEdges.append([-e for e in es[::-1]])
                    _log.debug('New edges: {}'.format(newEdges))
                    self.edges = newEdges
                    self.setUp()

                # Check direction
                if np.inner(self.normalVec[0], edge.directionVec[0]) > 0:
                    _log.debug('{}: direction ok'
                                      .format(self.info_text))
                else:
                    _log.error('{}: direction not ok'
                                      .format(self.info_text))
        else:
            _log.error('Cannot check normal vec because face ' +
                              '{} is empty'.format(self))

        self.dualCell3D = edge
        edge.dualCell3D = self

        for e in self.edges:
            if e.dualCell3D is None and e.dualCell2D is None:
                _log.error('Dual face {} of {}: edge {} has no dual'
                             .format(self, self.dualCell3D, e))

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

# =============================================================================
#    METHODS
# =============================================================================
    def __sortEdges(self, edges):
        edgesSorted = [edges[0], ]
        edges.pop(0)

        _log.debug("Sorting edges {}".format(edges))

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


    set_logging_format(logging.DEBUG)


    # with MyLogging('dualFace3D'):
    n0 = Node(0, 0, 0)
    n1 = Node(1, 0, 0)
    n2 = Node(0, 1, 0)
    n3 = Node(0, 0, 1)
    n4 = Node(1, 1, 1)
    n5 = Node(0.8, 1.5, -2)
    n6 = Node(1, 0, 4)

    nodes = [n0, n1, n2, n3, n4, n5, n6]
    for n in nodes:
        n.useCategory = 1

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
    for e in edges:
        e.useCategory = 1

    e3.category = 'inner'
    for e in edges:
        if e.category == 'undefined':
            e.category = 'border'

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
        v.useCategory = 1
        v.category = 'inner'

    for f in faces:
        f.useCategory = 1
        if len(f.volumes) == 2:
            f.category = 'inner'
        else:
            f.category = 'border'

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

    for v in volumes:
        v.showLabel = False
        v.plotVolume(ax[2])
    for n in dualNodes:
        n.plotNode(ax[2])

    for de in dualEdges:
        de.plotEdge(ax[2])

    df = DualFace3D(e3)

    df2 = DualFace3D(e6)

    df.plotFace(ax[3])
    df2.color = 'r'
    df2.plotFace(ax[3])

    for e in edges:
        e.showArrow = False
        e.showLabel = False
        e.plotEdge(ax[3])
