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

# ------------------------------------------------------------------------
#    Standard Libraries
# ------------------------------------------------------------------------

import logging

from k_cells.face.baseFace import BaseFace
from k_cells.edge import BaseEdge
from k_cells.cell import ReversedCell
from tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


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
        super().__init__(*args, **kwargs)
        _log.debug('Initialized ReversedFace')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getSimpleFaces(self):
        if self.my_reverse:
            return [-x for x in self.my_reverse.simpleFaces]
        else:
            _log.warning('No reverse defined')
            return []

    simpleFaces = property(__getSimpleFaces)

    def __getEdges(self):
        if self.my_reverse:
            return [-x for x in (reversed(self.my_reverse.edges))]
        else:
            _log.warning('No reverse defined')
            return []

    def __setEdges(self, edges):
        if self.my_reverse:
            if isinstance(edges[0], BaseEdge):
                self.my_reverse.edges = [-x for x in (reversed(edges))]
            else:
                allEdges = []
                for e in edges:
                    allEdges.append([-x for x in (reversed(e))])
                self.my_reverse.edges = allEdges
        else:
            _log.error('No reverse defined')

    edges = property(__getEdges, __setEdges)

    def __getRawEdges(self):
        if self.my_reverse:
            if isinstance(self.my_reverse.rawEdges[0], BaseEdge):
                return [-x for x in (reversed(self.my_reverse.rawEdges))]
            else:
                rawEdges = []
                for re in self.my_reverse.rawEdges:
                    rawEdges.append([-x for x in reversed(re)])
                return rawEdges

        else:
            _log.warning('No reverse defined')
            return []

    rawEdges = property(__getRawEdges)

    def __getGeometricEdges(self):
        if self.my_reverse:
            return self.my_reverse.geometricEdges
        else:
            _log.warning('No reverse defined')
            return []

    geometricEdges = property(__getGeometricEdges)

    def __getGeometricNodes(self):
        if self.my_reverse:
            return self.my_reverse.geometricNodes
        else:
            _log.warning('No reverse defined')
            return []

    geometricNodes = property(__getGeometricNodes)

    def __getShowNormalVec(self):
        if self.my_reverse:
            return self.my_reverse.showNormalVec
        else:
            _log.warning('No reverse defined')
            return True

    def __setShowNormalVec(self, s):
        if self.my_reverse:
            self.my_reverse.showNormalVec = s
        else:
            _log.error(
                'Cannot set showNormalVec because the reversed edge ' +
                'does not belong to an edge')

    showNormalVec = property(__getShowNormalVec, __setShowNormalVec)

    def __getShowBarycenter(self):
        if self.my_reverse:
            return self.my_reverse.showBarycenter
        else:
            _log.warning('No reverse defined')
            return True

    def __setShowBarycenter(self, s):
        if self.my_reverse:
            self.my_reverse.showBarycenter = s
        else:
            _log.error(
                'Cannot set showBarycenter because the reversed edge ' +
                'does not belong to an edge')

    showBarycenter = property(__getShowBarycenter, __setShowBarycenter)

    def __getPolygons(self):
        if self.my_reverse:
            return self.my_reverse.polygons
        else:
            _log.warning('No reverse defined')
            return None
    polygons = property(__getPolygons)

    def __getVolumes(self):
        if self.my_reverse:
            return self.my_reverse.volumes
        else:
            _log.warning('No reverse defined')
            return None
    volumes = property(__getVolumes)

# =============================================================================
#    METHODS
# =============================================================================

    def simplifyFace(self):
        if self.my_reverse:
            self.my_reverse.simplifyFace()
        else:
            _log.error('No reverse defined')

# ------------------------------------------------------------------------
#    Add a volume that uses this face
# ------------------------------------------------------------------------
    def addVolume(self, volume):
        if self.my_reverse:
            self.my_reverse.addVolume(volume)
        else:
            _log.error(
                'Cannot add volume {}'.format(volume.infoText) +
                ' to reversed face {} '.format(self.info_text) +
                'because it does not belong to a face')

# ------------------------------------------------------------------------
#    Delete a volume that uses this face
# ------------------------------------------------------------------------
    def delVolume(self, volume):
        if self.my_reverse:
            self.my_reverse.delVolume(volume)
        else:
            _log.error(
                'Cannot delete volume {} '.format(volume.infoText) +
                'from reversed face {} '.format(self.info_text) +
                'because it does not belong to a face')

    def setUp(self):
        self.my_reverse.setUp()


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':
    set_logging_format(logging.DEBUG)
    rf = ReversedFace()
