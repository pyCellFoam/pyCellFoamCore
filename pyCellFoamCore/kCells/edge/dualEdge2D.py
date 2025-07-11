# -*- coding: utf-8 -*-
# =============================================================================
# DUAL EDGE 2D
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Jul  6 15:38:54 2018

'''
.. todo::
    * Describe the different cases
    * Add a class method to create plot for documenation


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

from kCells.cell import DualCell


from kCells.edge.edge import Edge
from kCells.node import Node, DualNode1D, DualNode2D
import tools.colorConsole as cc
import tools.tumcolor as tc
import numpy as np
from tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class DualEdge2D(Edge, DualCell):
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
                 edge,
                 *args,
                 simplifySimpleEdges=True,
                 **kwargs):
        '''
        This is the explanation of the __init__ method.

        All parameters should be listed:

        :param int a: Some Number
        :param str b: Some String

        '''

        n1 = Node(0, 0, 0)
        n2 = Node(1.168, 0, 0)

        super().__init__(n1, n2,
                         *args,
                         num=edge.num,
                         **kwargs)

        if not simplifySimpleEdges:
            _log.debug('Do not simplify simple edges')


        error = True

        if edge.dualCell2D is not None:
            _log.error('Edge {} already has a dual edge!'.format(edge))

        if edge.dualCell1D is None:
            _log.debug('{} has no dual yet --> calculating it'.format(edge))
            dn = DualNode1D(edge)
            _log.debug('New node: {}'.format(dn))

        if edge.dualCell1D is None:
            _log.error('Something went wrong with the calculation ' +
                         'of the 1D dual of {}. '.format(edge) +
                         'The duals are: 0D: {} - '.format(edge.dualCell0D) +
                         '1D: {} - '.format(edge.dualCell1D) +
                         '2D: {}'.format(edge.dualCell2D))

        if edge.category1 == 'border':
            if len(edge.faces) == 1:
                _log.debug('Assuming 2D complex border edge')

                self.category1 = edge.category1
                self.category2 = edge.category2
                self.startNode = edge.dualCell1D
                self.endNode = edge.faces[0].dualCell2D
                self.setUp()

                v = np.cross(edge.directionVec[0], self.directionVec[0])
                normv = np.linalg.norm(v)
                if normv > self.tolerance:
                    v = v/normv
                    _log.debug(v)
                    if v[2] < -0.5:
                        _log.debug('Edge was in the wrong direction, ' +
                                     'turning around')
                        self.startNode = n1
                        self.endNode = edge.dualCell1D
                        self.startNode = edge.faces[0].dualCell2D
                        self.setUp()
                        v = np.cross(edge.directionVec[0],
                                     self.directionVec[0])
                        v = v/np.linalg.norm(v)

                    if v[2] < -0.5:
                        _log.error('Edge {} is still in the '.format(self) +
                                     'wrong direction')
                    else:
                        _log.debug('Edge is ok')
                        error = False

                else:
                    _log.error('Direction vector of ' +
                                 'primal edge {}'.format(edge) +
                                 ': {} and '.format(edge.directionVec) +
                                 'dual edge {}:'.format(self) +
                                 ' {} are close'.format(self.directionVec) +
                                 ' to parallel')

            else:

                faces = [f for f in edge.faces
                         if f.category == 'border'
                         or f.category == 'additionalBorder']
                for f in faces:

                    if f.dualCell2D is None:
                        DualNode2D(f)

                if len(faces) == 2:
                    _log.debug('Assuming 3D complex')
                    self.category1 = 'additionalBorder'
                    self.category2 = 'additionalBorder'

                    self.startNode = faces[0].dualCell2D
                    self.endNode = faces[1].dualCell2D

                    nGeo = edge.dualCell1D
                    if nGeo is None:
                        _log.error('{} should have'.format(edge) +
                                     ' a 1D dual but has not')

                    else:
                        self.geometricNodes = nGeo
                        self.setUp()
                        _log.debug(self.directionVec)
                        if np.linalg.norm(
                                self.directionVec[0]-self.directionVec[1]) \
                                < 1e-4 and simplifySimpleEdges:
                            self.geometricNodes = []
                            self.setUp()
                        error = False
                else:
                    _log.error('Edge {} is border '.format(edge.infoText) +
                                 'and should therefor belong to ' +
                                 'two border faces, ' +
                                 'but belongs to {}: {}'.format(len(faces), faces))

        elif edge.category1 == 'inner':
            _log.debug('Assuming 2D complex inner edge')
            if len(edge.faces) == 2:
                self.category1 = edge.category1
                self.category2 = edge.category2
                _log.debug('Creating 2D dual edge')

                self.startNode = edge.faces[0].dualCell2D
                self.endNode = edge.faces[1].dualCell2D
                nGeo = edge.dualCell1D
                self.geometricNodes = nGeo
                self.setUp()
                _log.debug(self.directionVec)

                v = np.cross(edge.directionVec, self.directionVec)

                v1 = v[0]/np.linalg.norm(v[0])
                v2 = v[1]/np.linalg.norm(v[1])

                _log.debug(v1, v2)

                if v1[2] < -0.5 or v2[2] < -0.5:
                    _log.debug('Dual edge was in the wrong direction, ' +
                                 'swapping start and end')
                    self.endNode = n1
                    self.startNode = edge.faces[1].dualCell2D
                    self.endNode = edge.faces[0].dualCell2D

                if np.linalg.norm(
                        self.directionVec[0]-self.directionVec[1]) \
                        < self.tolerance and simplifySimpleEdges:
                    self.geometricNodes = []
                    self.setUp()

                error = False

            else:
                _log.error('An inner edge in a 2D complex needs ' +
                                  'two faces')

        else:
            _log.error('Unknown category {}'.format(edge.category) +
                         ' of edge {}'.format(edge.infoText))

        if error:
            self.delete()
            _log.error('An error occured during the creation process ' +
                              'of dual Edge --> deleting')
        else:
            if edge.isReverse:
                self.dualCell2D = -edge
                edge.dualCell2D = -self
            else:
                self.dualCell2D = edge
                edge.dualCell2D = self

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

# =============================================================================
#    METHODS
# =============================================================================

    def calcHeatFlow(self):

        if len(self.simpleEdges) == 1:
            _log.debug('1 simple edge in dual edge {}'.format(self))
            se = self.simpleEdges[0]
            v = se.connectionVec
            _log.debug('Start node dual: {} | end node dual: {}'
                         .format(se.startNode, se.endNode))
            if se.startNode.category == 'inner' \
                    and se.endNode.category != 'inner':
                _log.debug('Using {} for interpolation'
                             .format(se.startNode.dualCell2D))
                entry = (se.startNode.num, -v[1], v[0])
            elif se.startNode.category != 'inner' \
                    and se.endNode.category == 'inner':
                _log.debug('Using {} for interpolation'
                             .format(se.endNode.dualCell2D))
                entry = (se.endNode.num, -v[1], v[0])
            else:
                _log.error('Cannot find the correct primal face ' +
                             'for interpolation')
                return None
            entries = [entry, ]
        elif len(self.simpleEdges) == 2:
            _log.debug('2 simple edges in dual edge {}'.format(self))
            se1 = self.simpleEdges[0]
            se2 = self.simpleEdges[1]
            v1 = se1.connectionVec
            v2 = se2.connectionVec

            _log.debug('Evaluating {} for simple edge {}'
                         .format(se1.startNode.dualCell2D, se1))
            _log.debug('Evaluating {} for simple edge {}'
                         .format(se2.endNode.dualCell2D, se2))
            entry1 = (se1.startNode.num, -v1[1], v1[0])
            entry2 = (se2.endNode.num, -v2[1], v2[0])
            entries = [entry1, entry2]

        else:
            return None
            _log.error('{} simple edges in dual edge {} cannot be handled!'
                         .format(len(self.simpleEdges), self))
        return entries


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================
if __name__ == "__main__":
    from kCells.node import DualNode3D
    from kCells.face import Face
    from kCells.volume.volume import Volume
    import tools.placeFigures as pf
    from tools import MyLogging
    set_logging_format(logging.DEBUG)
    n0 = Node(0, 0, 0)
    n1 = Node(1, 0, 0)
    n2 = Node(0, 1, 0)
    n3 = Node(0, 0, 1)
    n4 = Node(1, 1, 1)
    nodes = [n0, n1, n2, n3, n4]

    e0 = Edge(n0, n1)
    e1 = Edge(n0, n2)
    e2 = Edge(n0, n3)
    e3 = Edge(n1, n2)
    e4 = Edge(n1, n3)
    e5 = Edge(n2, n3)
    e6 = Edge(n1, n4)
    e7 = Edge(n2, n4)
    e8 = Edge(n3, n4)

    edges = [e0, e1, e2, e3, e4, e5, e6, e7, e8]

    for e in edges:
        e.category1 = 'border'

    f0 = Face([e0, e3, -e1])
    f1 = Face([e1, e5, -e2])
    f2 = Face([e0, e4, -e2])
    f3 = Face([e3, e5, -e4])
    f4 = Face([e4, e8, -e6])
    f5 = Face([e5, e8, -e7])
    f6 = Face([e3, e7, -e6])

    faces = [f0, f1, f2, f3, f4, f5, f6]
    for f in faces:
        f.useCategory = 1
        if f == f3:
            f.category = 'inner'
        else:
            f.category = 'border'

    v1 = Volume([-f0, -f1, f2, f3])
    v2 = Volume([f6, f5, -f4, -f3])
    volumes = [v1, v2]
    for v in volumes:
        v.useCategory = 1
        v.category = 'inner'

    (figs, ax) = pf.getFigures(2, 2)
    for e in edges:
        e.plotEdge(ax[0])
    for f in faces:
        f.plotFace(ax[0])

    for v in volumes:
        v.plotVolume(ax[1])

    dualNodes = []
    for v in volumes:
        dualNodes.append(DualNode3D(v))

    de1 = DualEdge2D(e3)

    for v in volumes:
        v.showLabel = False
        v.plotVolume(ax[2])
    for n in dualNodes:
        n.plotNode(ax[2])

    de1.plotEdge(ax[2])

    n100 = Node(0, 0, 0, num=100)
    n101 = Node(1, 0, 0, num=101)
    n102 = Node(1, 1, 0, num=102)
    n103 = Node(0, 1, 0, num=103)
    n104 = Node(2, 0, 0, num=104)
    n105 = Node(2, 1, 0, num=105)
    n106 = Node(0, 2, 0, num=106)
    n107 = Node(2, 2, 0, num=107)
    n108 = Node(1, 1.5, 0, num=108)
    nodes = [n100, n101, n102, n103, n104, n105, n106, n107, n108]

    e100 = Edge(n100, n101, num=100)
    e101 = Edge(n101, n102, num=101)
    e102 = Edge(n102, n103, num=102)
    e103 = Edge(n103, n100, num=103)
    e104 = Edge(n101, n104, num=104)
    e105 = Edge(n104, n105, num=105)
    e106 = Edge(n105, n102, num=106)
    e107 = Edge(n101, n105, num=107)
    e108 = Edge(n103, n106, num=108)
    e109 = Edge(n102, n108, num=109)
    e110 = Edge(n108, n106, num=110)
    e111 = Edge(n105, n107, num=111)
    e112 = Edge(n107, n108, num=112)
    e113 = Edge(n107, n106, num=113)
    edges = [e100, e101, e102, e103, e104, e105, e106, e107, e108, e109,
             e110, e111, e112, e113]

    borderEdges = [e100, e104, e105, e111, e113, e108, e103]
    innerEdges = [e for e in edges if e not in borderEdges]

    for e in borderEdges:
        e.category1 = 'border'
    for e in innerEdges:
        e.category1 = 'inner'

    f100 = Face([e100, e101, e102, e103])
    f101 = Face([e104, e105, -e107])
    f102 = Face([e107, e106, -e101])
    f103 = Face([e109, e110, -e108, -e102])
    f104 = Face([e113, -e110, -e112])
    f105 = Face([e111, e112, -e109, -e106])
    faces = [f100, f101, f102, f103, f104, f105]

    dualNodes = []
    for f in faces:
        f.category1 = 'inner'
        dualNodes.append(DualNode2D(f))

    for e in edges:
        e.plotEdge(ax[3])
    for f in faces:
        f.plotFace(ax[3])

    ax[3].view_init(90, -90)
    ax[3].set_xlabel('x')
    ax[3].set_ylabel('y')

    dualEdges = []
    for e in edges:
        dualEdges.append(DualEdge2D(e))

    for e in dualEdges:
        e.color = tc.TUMOrange()
        e.plotEdge(ax[3])
