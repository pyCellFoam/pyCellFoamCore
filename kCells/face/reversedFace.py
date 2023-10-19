# -*- coding: utf-8 -*-
# =============================================================================
# REVERSED FACE
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Dec 13 15:19:20 2017


'''

'''


# =============================================================================
#    IMPORTS
# =============================================================================

if __name__ == '__main__':
    import os
    os.chdir('../../')

from kCells.face.baseFace import BaseFace
from kCells.edge import BaseEdge
from kCells.cell import ReversedCell


# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class ReversedFace(BaseFace, ReversedCell):
    '''
    Defines the face and prepares further properties.

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

        '''
        super().__init__(*args, loggerName=__name__, **kwargs)
        self.logger.debug('Initialized ReversedFace')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getSimpleFaces(self):
        if self.myReverse:
            return [-x for x in self.myReverse.simpleFaces]
        else:
            self.logger.warning('No reverse defined')
            return []

    simpleFaces = property(__getSimpleFaces)

    def __getEdges(self):
        if self.myReverse:
            return [-x for x in (reversed(self.myReverse.edges))]
        else:
            self.logger.warning('No reverse defined')
            return []

    def __setEdges(self, edges):
        if self.myReverse:
            if isinstance(edges[0], BaseEdge):
                self.myReverse.edges = [-x for x in (reversed(edges))]
            else:
                allEdges = []
                for e in edges:
                    allEdges.append([-x for x in (reversed(e))])
                self.myReverse.edges = allEdges
        else:
            self.logger.error('No reverse defined')

    edges = property(__getEdges, __setEdges)

    def __getRawEdges(self):
        if self.myReverse:
            if isinstance(self.myReverse.rawEdges[0], BaseEdge):
                return [-x for x in (reversed(self.myReverse.rawEdges))]
            else:
                rawEdges = []
                for re in self.myReverse.rawEdges:
                    rawEdges.append([-x for x in reversed(re)])
                return rawEdges

        else:
            self.logger.warning('No reverse defined')
            return []

    rawEdges = property(__getRawEdges)

    def __getGeometricEdges(self):
        if self.myReverse:
            return self.myReverse.geometricEdges
        else:
            self.logger.warning('No reverse defined')
            return []

    geometricEdges = property(__getGeometricEdges)

    def __getGeometricNodes(self):
        if self.myReverse:
            return self.myReverse.geometricNodes
        else:
            self.logger.warning('No reverse defined')
            return []

    geometricNodes = property(__getGeometricNodes)

    def __getShowNormalVec(self):
        if self.myReverse:
            return self.myReverse.showNormalVec
        else:
            self.logger.warning('No reverse defined')
            return True

    def __setShowNormalVec(self, s):
        if self.myReverse:
            self.myReverse.showNormalVec = s
        else:
            self.logger.error(
                'Cannot set showNormalVec because the reversed edge ' +
                'does not belong to an edge')

    showNormalVec = property(__getShowNormalVec, __setShowNormalVec)

    def __getShowBarycenter(self):
        if self.myReverse:
            return self.myReverse.showBarycenter
        else:
            self.logger.warning('No reverse defined')
            return True

    def __setShowBarycenter(self, s):
        if self.myReverse:
            self.myReverse.showBarycenter = s
        else:
            self.logger.error(
                'Cannot set showBarycenter because the reversed edge ' +
                'does not belong to an edge')

    showBarycenter = property(__getShowBarycenter, __setShowBarycenter)

    def __getPolygons(self):
        if self.myReverse:
            return self.myReverse.polygons
        else:
            self.logger.warning('No reverse defined')
            return None
    polygons = property(__getPolygons)

    def __getVolumes(self):
        if self.myReverse:
            return self.myReverse.volumes
        else:
            self.logger.warning('No reverse defined')
            return None
    volumes = property(__getVolumes)

# =============================================================================
#    METHODS
# =============================================================================

    def simplifyFace(self):
        if self.myReverse:
            self.myReverse.simplifyFace()
        else:
            self.logger.error('No reverse defined')

# ------------------------------------------------------------------------
#    Add a volume that uses this face
# ------------------------------------------------------------------------
    def addVolume(self, volume):
        if self.myReverse:
            self.myReverse.addVolume(volume)
        else:
            self.logger.error(
                'Cannot add volume {}'.format(volume.infoText) +
                ' to reversed face {} '.format(self.infoText) +
                'because it does not belong to a face')

# ------------------------------------------------------------------------
#    Delete a volume that uses this face
# ------------------------------------------------------------------------
    def delVolume(self, volume):
        if self.myReverse:
            self.myReverse.delVolume(volume)
        else:
            self.logger.error(
                'Cannot delete volume {} '.format(volume.infoText) +
                'from reversed face {} '.format(self.infoText) +
                'because it does not belong to a face')

    def setUp(self):
        self.myReverse.setUp()


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':
    rf = ReversedFace()
