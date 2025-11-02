# -*- coding: utf-8 -*-
# =============================================================================
# TITLE
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Dec  7 14:16:21 2017

'''
This is the explanation of the whole module and will be printed at the very
beginning


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


from kCells.cell import ReversedCell
from kCells.edge.baseEdge import BaseEdge
from tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)

# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class ReversedEdge(BaseEdge, ReversedCell):
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
    def __init__(self, *args, **kwargs):
        '''
        This is the explanation of the __init__ method.

        All parameters should be listed:

        :param int a: Some Number
        :param str b: Some String

        '''
        super().__init__(*args, **kwargs)
        _log.debug('Initialized ReversedEdge')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getFaces(self):
        if self.myReverse:
            return [-f for f in reversed(self.myReverse.faces)]
        else:
            _log.warning('No reverse defined')
            return True

    faces = property(__getFaces)

    def __getShowArrow(self):
        if self.myReverse:
            return self.myReverse.showArrow
        else:
            _log.warning('No reverse defined')
            return True

    def __setShowArrow(self, s):
        if self.myReverse:
            self.myReverse.showArrow = s
        else:
            _log.error(
                'Cannot set showArrow because the reversed edge ' +
                'does not belong to an edge')

    showArrow = property(__getShowArrow, __setShowArrow)

    def __getStartNode(self):
        if self.myReverse.geometryChanged:
            self.myReverse.setUp()
        return self.myReverse.endNode

    def __setStartNode(self, s):
        _log.debug('Setting start node in edge %s', self)
        self.myReverse.endNode = s

    startNode = property(__getStartNode, __setStartNode)

    def __getEndNode(self):
        if self.myReverse.geometryChanged:
            self.myReverse.setUp()
        return self.myReverse.startNode

    def __setEndNode(self, s):
        _log.debug('Setting end node in edge %s', self)
        self.myReverse.startNode = s

    endNode = property(__getEndNode, __setEndNode)

    def __getGeometricNodes(self):
        return list(reversed(self.myReverse.geometricNodes))

    def __setGeometricNodes(self, g):
        self.myReverse.geometricNodes = list(reversed(g))

    geometricNodes = property(__getGeometricNodes, __setGeometricNodes)

    def __getSimpleEdges(self):
        if self.myReverse:
            return [-se for se in reversed(self.myReverse.simpleEdges)]
        else:
            _log.error('No reverse defined')

    simpleEdges = property(__getSimpleEdges)

    def __getTopologicNodes(self):
        if self.myReverse:
            return list(reversed(self.myReverse.topologicNodes))
        else:
            _log.error('No reverse defined')

    topologicNodes = property(__getTopologicNodes)

    def __getProjectedEdge(self):
        if self.myReverse:
            return -self.myReverse.projectedEdge
        else:
            _log.error('No reverse defined')
    projectedEdge = property(__getProjectedEdge)

    def __getProjectionFace(self):
        if self.myReverse:
            return self.myReverse.projectionFace
        else:
            _log.error('No reverse defined')
    projectionFace = property(__getProjectionFace)

# =============================================================================
#    METHODS
# =============================================================================
# ------------------------------------------------------------------------
#    Add a face that uses this edge
# ------------------------------------------------------------------------
    def addFace(self, face):
        if self.myReverse:
            self.myReverse.addFace(-face)
        else:
            _log.error(
                'Cannot add face {}'.format(face.infoText) +
                ' to reversed edge {} '.format(self.infoText) +
                'because it does not belong to an edge')

# ------------------------------------------------------------------------
#    Delete a face that uses this edge
# ------------------------------------------------------------------------
    def delFace(self, face):
        if self.myReverse:
            self.myReverse.delFace(-face)
        else:
            _log.error(
                'Cannot delete face {}'.format(face.infoText) +
                ' from reversed edge {} '.format(self.infoText) +
                'because it does not belong to an edge')


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================

if __name__ == "__main__":
    set_logging_format(logging.DEBUG)
    re = ReversedEdge()
#    import tools.placeFigures as pf
#    from face import Face
#    from tools import MyLogging
#    from node import Node
#
#
#    with MyLogging('Edge'):
#
#        # Create some figures on second screen
#        (fig, ax) = pf.getFigures(numTotal=4)
#
#        n1 = Node(0  , 0, 0, 1)
#        n2 = Node(0  , 1, 0, 2)
#        n3 = Node(1  , 0, 0, 3)
#        n4 = Node(1  , 1, 0, 4)
#        n5 = Node(1.2, 2, 0, 5)
#        n6 = Node(2  , 0, 0, 6)
#        n7 = Node(2  , 1, 0, 7)
#        n8 = Node(2.2, 2, 0, 8)
#        n9 = Node(2  , 3, 0, 9)
#        nodes = [n1, n2, n3, n4, n5, n6, n7, n8, n9]
#
#
#        e1 = Edge(n1, n2, 1)
#        e2 = Edge(n3, n5, 2, geometricNodes=[n4, ])
#        e3 = Edge(n6, n9, 3, geometricNodes=[n7, n8])
#
#        edges = [e1, e2, e3]
#
#        for n in nodes:
#            n.plotNode(ax[0])
#
#        for e in edges:
#            e.plotEdge(ax[0])
