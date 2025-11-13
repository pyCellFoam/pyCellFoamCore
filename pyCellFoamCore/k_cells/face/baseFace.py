# -*- coding: utf-8 -*-
# =============================================================================
# BASE FACE
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

from k_cells.cell import BaseCell
from tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)

# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class BaseFace(BaseCell):
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

        '''
        super().__init__(*args, **kwargs)
        _log.debug('Initialized BaseFace')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getSimpleEdges(self):
        simpleEdges = []
        for e in self.edges:
            for se in e.simpleEdges:
                simpleEdges.append(se)
        return simpleEdges

    simpleEdges = property(__getSimpleEdges)

    def __getBarycenter(self):
        return [sf.barycenter for sf in self.simpleFaces]

    barycenter = property(__getBarycenter)

    def __getNormalVec(self): return [sf.normalVec for sf in self.simpleFaces]

    normalVec = property(__getNormalVec)

    def __getArea(self):
        areas = []
        totalArea = 0
        for sf in self.simpleFaces:
            areas.append(sf.area)
            totalArea += sf.area[1]
        area = [areas, totalArea]
        return area
    area = property(__getArea)

# =============================================================================
#    METHODS
# =============================================================================
    def plotFace(self, *arg, **kwarg):
        if self.geometryChanged:
            self.setUp()

        if self.showInPlot:

            if not self.simpleFaces:
                _log.warning(
                    'Face {} has no simple faces, maybe it was deleted'
                    .format(self))
            for sf in self.simpleFaces:
                sf.plotFace(*arg, **kwarg)
        else:
            _log.warning('Plotting of face {} is disabled'.format(self))

    def plotFaceVtk(self, *arg, **kwarg):
        if self.geometryChanged:
            self.setUp()

        if not self.simpleFaces:
            _log.warning(
                'Face {} has no simple faces, maybe it was deleted'
                .format(self))
        for sf in self.simpleFaces:
            sf.plotFaceVtk(*arg, **kwarg)

    def plotFlowVtk(self, *arg, **kwarg):
        if self.geometryChanged:
            self.setUp()
        if not self.simpleFaces:
            _log.warning(
                'Face {} has no simple faces, maybe it was deleted'
                .format(self))
        for sf in self.simpleFaces:
            sf.plotFlowVtk(*arg, **kwarg)

    def plotFaceTikZ(self, *args, **kwargs):
        if self.showInPlot:
            for sf in self.simpleFaces:
                sf.plotFaceTikZ(*args, **kwargs)

    def isIdenticalTo(self, other):
        '''
        Two faces are seen as identical, if they consist of the same edges.
        The orientation is neglected.

        Remark: It is of course not possible that only some of the edges are
        flipped, because then one of the faces would not be defined correctly.

        '''
        return (all([e in other.edges for e in self.edges])
                and all([e in self.edges for e in other.edges])) \
            or (all([-e in other.edges for e in self.edges])
                and all([-e in self.edges for e in other.edges]))


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == "__main__":
    set_logging_format(logging.DEBUG)
    bf = BaseFace()
