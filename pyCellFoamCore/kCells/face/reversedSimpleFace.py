# -*- coding: utf-8 -*-
# =============================================================================
# REVERSED SIMPLE FACE
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue May 22 18:15:43 2018

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


from kCells.face.baseSimpleFace import BaseSimpleFace
from kCells.cell import ReversedSimpleCell
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


class ReversedSimpleFace(BaseSimpleFace, ReversedSimpleCell):
    '''

    '''

# =============================================================================
#    SLOTS
# =============================================================================
#    __slots__ = ('__coordinates',
#                 '__nodes',
#                 '__normalVec',
#                 '__area')
#

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.__coordinates = None
        self.__area = None
        self.__normalVec = None
        self.__nodes = None
        _log.debug('Initialized ReversedSimpleFace')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================
    def __getCoordinates(self):
        if self.__coordinates is None:
            if self.myReverse:
                self.__coordinates = np.flipud(self.myReverse.coordinates)
            else:
                _log.error(
                    'No reverse defined, cannot give coordinates')
        return self.__coordinates

    coordinates = property(__getCoordinates)

    def __getNodes(self):
        if self.__nodes is None:
            if self.myReverse:
                self.__nodes = list(reversed(self.myReverse.nodes))
            else:
                _log.error('No reverse defined, cannot give nodes')
        return self.__nodes

    nodes = property(__getNodes)

    def __getArea(self):
        if self.__area is None:
            if self.myReverse:
                self.__area = [[a for a in reversed(self.myReverse.area[0])],
                               self.myReverse.area[1]]
            else:
                _log.error('No reverse defined, cannot give area')
        return self.__area

    area = property(__getArea)

    def __getNormalVec(self):
        if self.__normalVec is None:
            if self.myReverse:
                self.__normalVec = -self.myReverse.normalVec
            else:
                _log.error('No reverse defined, cannot give normalVec')
        return self.__normalVec

    normalVec = property(__getNormalVec)

    def __getBarycenter(self):
        if self.myReverse:
            return self.myReverse.barycenter
        else:
            _log.error('Reversed simple face does not belong to a ' +
                              'simple face, cannot return barycenter')
            return np.array([0, 0, 0])

    barycenter = property(__getBarycenter)

    def __getSimpleEdges(self):
        if self.myReverse:
            return [se.myReverse for se in
                    reversed(self.myReverse.simpleEdges)]
        else:
            _log.error(
                'Reversed simple face does not belong to a simple face, ' +
                'cannot return simpleEdges')
            return []
    simpleEdges = property(__getSimpleEdges)

#    def __getEdges(self):
#        edges = []
#        for e in self.data.edges:
#            edges.append(-e)
#        return list(reversed(edges))
#    def __setEdges(self, edges):
#        newedges = []
#        for e in edges:
#            newedges.append(-e)
#        newedges = list(reversed(newedges))
#        if self.checkContinuity(newedges):
#            # TODO check if edges form a plane!!!
#            for e in self.__data.edges:
#                e.delFace(self)
#            self.__data.edges = newedges
#            for e in self.__data.edges:
#                e.addFace(self)
#            self.createCoordinates()
#            self.calcBarycenter()
#    edges = property(__getEdges)
#
#    def __getNormalVec(self): return -self.data.normalVec
#    normalVec = property(__getNormalVec)


if __name__ == '__main__':
    import tools.colorConsole as cc

    set_logging_format(logging.DEBUG)
    rsf = ReversedSimpleFace()
    cc.printRed(rsf.coordinates)
    cc.printRed(rsf.area)
    cc.printRed(rsf.barycenter)
