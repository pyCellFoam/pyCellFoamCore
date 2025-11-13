# -*- coding: utf-8 -*-
# =============================================================================
# SIMPLE FACE
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Dec 13 15:19:20 2017


'''

* edges:        list with all Edge objects that define the area
* coordinates:  all coordinates (including additonal coordinates)
* area:         list with two elements
    - element 1:  another list with all sub-areas
    - element 2:  value of total area

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

# ------------------------------------------------------------------------
#    Third Party Libraries
# ------------------------------------------------------------------------

import numpy as np

# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------

#    kCells
# -------------------------------------------------------------------

from k_cells.face.reversedSimpleFace import ReversedSimpleFace
from k_cells.face.baseSimpleFace import BaseSimpleFace
from k_cells.cell import SimpleCell
import tools.colorConsole as cc
import math
from scipy.spatial import ConvexHull

from k_cells.node import Node
from k_cells.edge import Edge

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


class SimpleFace(BaseSimpleFace, SimpleCell):
    '''
    Defines the face and prepares further properties.

    '''

# =============================================================================
#    SLOTS
# =============================================================================
#    __slots__ = ('__simpleEdges',
#                 '__coordinates',
#                 '__barycenter',
#                 '__normalVec',
#                 '__polygon',
#                 '__area',
#                 '__nodes')

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self, simpleEdges, *args, belongsTo=None, **kwargs):
        '''

        '''
        if belongsTo is None:
            belongsToRev = None
        else:
            belongsToRev = belongsTo.myReverse
        super().__init__(*args,
                         myReverse=ReversedSimpleFace(myReverse=self,
                                                      belongsTo=belongsToRev),
                         belongsTo=belongsTo,
                         **kwargs)
        self.__simpleEdges = simpleEdges
        self.__normalVec = None
        if len(self.__simpleEdges) > 2:
            if self.__checkContinuity(self.__simpleEdges):
                self.__createCoordinates()
                self.__checkPlane()
                self.__calcArea()
                self.__calcBarycenter()

                for se in self.simpleEdges:
                    se.addSimpleFace(self)

            else:
                _log.error('Continuity check failed')
                self.__coordinates = []
        else:
            _log.error(
                'Simple face must consist of more than 2 simple edges! {}'
                .format(self.__simpleEdges))
            self.__coordinates = []

#        self.__polygon = None

        _log.debug('Initialized SimpleFace')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getSimpleEdges(self): return self.__simpleEdges

    simpleEdges = property(__getSimpleEdges)

    def __getCoordinates(self): return self.__coordinates

    coordinates = property(__getCoordinates)

    def __getNodes(self): return self.__nodes

    nodes = property(__getNodes)

    def __getNormalVec(self): return self.__normalVec

    normalVec = property(__getNormalVec)

    def __getArea(self): return self.__area

    area = property(__getArea)

    def __getBarycenter(self): return self.__barycenter

    barycenter = property(__getBarycenter)

#    def __getPolygon(self):
#        if not self.__polygon:
#            self.__polygon = Polygon(self.coordinates)
#        return self.__polygon
#    polygon = property(__getPolygon)

# =============================================================================
#    METHODS
# =============================================================================

# ------------------------------------------------------------------------
#    Check if the given edges form a closed cycle
# ------------------------------------------------------------------------
    def __checkContinuity(self, edges):
        ok = True

        # loop over all inner connections
        for e1, e2 in zip(edges[:-1], edges[1:]):
            if e1.endNode != e2.startNode:
                _log.error(
                    'Error when building simple face {}: '.format(self) +
                    'simple edge {} '.format(e1) +
                    'and simple edge {} '.format(e2) +
                    'do not connect correctly')
                _log.error(
                    'End node of {}: {}, '.format(e1, e1.endNode) +
                    'start node of {}: {}, '.format(e2, e2.startNode) +
                    'they should be the same')
                ok = False

        # check connection from last edge to first edge
        if edges[-1].endNode != edges[0].startNode:
            _log.error('Error when building Face {}: '.format(self) +
                              'Edge {} '.format(edges[-1]) +
                              'and Edge {} '.format(edges[0]) +
                              'do not connect correctly')
            ok = False

        if not ok:
            _log.error('Simple face {} is not well defined'
                              .format(self.info_text))

        _log.debug('Continuity ok')
        return ok

# ------------------------------------------------------------------------
#    Calculate all coordinates
# ------------------------------------------------------------------------
    def __createCoordinates(self):
        coordinates = []
        nodes = []
        for se in self.__simpleEdges:
            nodes.append(se.startNode)
            coordinates.append(se.startNode.coordinates)

        self.__nodes = nodes
        self.__coordinates = np.vstack((tuple(coordinates)))
        _log.debug('Created Coordinates')

# ------------------------------------------------------------------------
#    Check if the given nodes lay in the same plane
# ------------------------------------------------------------------------
    def __checkPlane(self):
        inPlane = True
        tol = 1E-4
        o = self.__coordinates[0]
        x = self.__coordinates[1]

        # If first three coordinates are in one line, choose another coordinate
        # to calculate the normal vector. Keep searching, when its still the
        # case
        count = 0
        vec0 = np.array([0, 0, 0])
        while count < len(self.__coordinates) - 2 and \
                np.linalg.norm(vec0) < tol:
            y = self.__coordinates[count+2]
            vec0 = np.cross(x-o, y-o)
            _log.debug('vec1: {} x vec2: {} = vec0: {}'
                              .format(x-o, y-o, vec0))
            count += 1

        if np.linalg.norm(vec0) > tol:
            vec0 = vec0/np.linalg.norm(vec0)
            self.__normalVec = vec0
        else:
            self.__normalVec = np.array([0, 0, 0])
            _log.error('Could not find a valid normal vector for {}'
                              .format(self))

        # Go through all triangles
        for x, y in zip(self.__coordinates[1:-1], self.__coordinates[2:]):
            vec = np.cross(x-o, y-o)
            # If vec is close to zero, the two vectors are close to beeing
            # parallel thereofore they also must lie in the same plane
            if np.linalg.norm(vec) > tol:
                vec = vec/np.linalg.norm(vec)
                if np.linalg.norm(vec-vec0) > tol \
                        and np.linalg.norm(vec+vec0) > tol:
                    inPlane = False
                    _log.error('Simple face {} is not a plane'
                                      .format(self))

        # return result
        _log.debug('Checked planarity')

        _log.debug('SimpleFace: Checking for convexity')
        v1 = np.array([0, 0, 1])
        v2 = self.__normalVec
        angle = np.arccos(np.dot(v1, v2) /
                          (np.linalg.norm(v1) * np.linalg.norm(v2)))
        _log.debug('Angle between normal vector and z direction: {}'
                          .format(360*angle/math.tau))
        axis = np.cross(v1, v2)
        _log.debug('Axis for rotation: {}'.format(axis))
        if np.linalg.norm(axis) < self.tolerance:
            rot = np.eye(3)
            _log.debug('No rotation needed')
        else:
            rot = self.__rotationMatrix(-angle, axis)
            _log.debug('Rotating with rotation matrix:\r\n {}'
                              .format(rot))

        localCoordinates3D = (rot @ self.__coordinates.transpose()).transpose()
#        cc.printYellow('Local coordinates with 3rd dimension:')
#        cc.printYellow(localCoordinates3D)
        localCoordiantes2D = localCoordinates3D[:, 0:2]
#        cc.printYellow('Local coordiantes in 2D:')
#        cc.printYellow(localCoordiantes2D)
        try:
            hull = ConvexHull(localCoordiantes2D)
        except Exception as e:
            _log.error(
                'Cannot caculate convex hull for simpleface {} in face {}.'
                .format(self, self.belongsTo) +
                'Error: {}'.format(e))
            hull = False

        if hull:
            hull.vertices.sort()
            convexHullPoints = localCoordinates3D[hull.vertices]
            o = convexHullPoints[0]
            x = convexHullPoints[1]

            count = 0
            vec0 = np.array([0, 0, 0])
            while count < len(convexHullPoints)-2 and \
                    np.linalg.norm(vec0) < tol:
                y = convexHullPoints[count+2]
                vec0 = np.cross(x-o, y-o)
                _log.debug('vec1: {} x vec2: {} = vec0: {}'
                                  .format(x-o, y-o, vec0))
                count += 1

            if np.linalg.norm(vec0) > tol:
                vec0 = vec0/np.linalg.norm(vec0)
                comparisonNormalVec = vec0
            else:
                comparisonNormalVec = np.array([0, 0, 0])
                _log.error(
                    'Could not find a valid normal vector of the convex  ' +
                    'hull for {}'.format(self))

            comparisonNormalVec = rot.transpose() @ comparisonNormalVec
            if np.linalg.norm(self.__normalVec - comparisonNormalVec) > \
                    self.tolerance:
                self.__normalVec = -self.__normalVec
                _log.debug('Turning normal vector around')

            if np.linalg.norm(self.__normalVec - comparisonNormalVec) > \
                    self.tolerance:
                _log.error('Cannot find correct normal vector')
            else:
                _log.debug('Found hopefully correct normal vector')

        return inPlane

# ------------------------------------------------------------------------
#    Calculate area
# ------------------------------------------------------------------------
    def __calcArea(self):
        o = self.__coordinates[0]
        areas = []
        totalArea = 0
        for x, y in zip(self.coordinates[1:-1], self.coordinates[2:]):
            area = 1/2*np.linalg.norm(np.cross(x-o, y-o))
            totalArea += area
            areas.append(area)

        self.__area = [areas, totalArea]
        if totalArea < self.tolerance:
            _log.error('{}: area is close to zero or negative: {}'
                              .format(self.info_text, totalArea))
        _log.debug('Calculated area')

# ------------------------------------------------------------------------
#    Calculate barycenter
# ------------------------------------------------------------------------
    def __calcBarycenter(self):
        if self.area[1] > self.tolerance:
            o = self.__coordinates[0]
            barycenter = np.array([0., 0., 0.])
            for x, y, a in zip(self.__coordinates[1:-1],
                               self.__coordinates[2:],
                               self.__area[0]):
                barycenter += (o+x+y)/3*a

            self.__barycenter = barycenter/self.area[1]
            _log.debug('Calculated barycenter')
        else:
            self.__barycenter = np.array([0, 0, 0])
            _log.error('Cannot calculate barycenter ' +
                              'of {} because the area is too small, '
                              .format(self) +
                              'it is only {}'.format(self.area[1]))

# ------------------------------------------------------------------------
#    Delete the entire simple face
# ------------------------------------------------------------------------
    def delete(self):
        for se in self.__simpleEdges:
            se.delSimpleFace(self)
        super().delete()

    def __rotationMatrix(self, angle, axis):
        a = angle
        n = axis
        cos = math.cos
        sin = math.sin
        if np.linalg.norm(n) < self.tolerance:
            _log.error('Cannot find rotation matrix')
            return np.eye(3)
        else:
            n = n/np.linalg.norm(n)
            n1 = n[0]
            n2 = n[1]
            n3 = n[2]
            return np.array([
                    [
                        n1**2*(1-cos(a))+cos(a),
                        n1*n2*(1-cos(a))-n3*sin(a),
                        n1*n3*(1-cos(a))+n2*sin(a)
                    ],
                    [
                        n2*n1*(1-cos(a))+n3*sin(a),
                        n2**2*(1-cos(a))+cos(a),
                        n2*n3*(1-cos(a))-n1*sin(a)
                    ],
                    [
                        n3*n1*(1-cos(a))-n2*sin(a),
                        n3*n2*(1-cos(a))+n1*sin(a),
                        n3**2*(1-cos(a))+cos(a)
                    ]])


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================
if __name__ == '__main__':

    set_logging_format(logging.DEBUG)

    n0 = Node(0, 0, 0)
    n1 = Node(5, 0, 0)
    n2 = Node(0, 5, 0)
    nodes = [n0, n1, n2]

    e0 = Edge(n0, n1)
    e1 = Edge(n1, n2)
    e2 = Edge(n2, n0)
    edges = [e0, e1, e2]

    sf = SimpleFace([e0.simpleEdges[0],
                     e1.simpleEdges[0],
                     e2.simpleEdges[0]])

# ------------------------------------------------------------------------
#    Plotting
# ------------------------------------------------------------------------

    # Choose plotting method.
    # Possible choices: pyplot, VTK, TikZ, animation, doc, None
    plottingMethod = 'pyplot'


#    Disabled
# --------------------------------------------------------------------
    if plottingMethod is None or plottingMethod == 'None':
        cc.printBlue('Plotting disabled')

#    Pyplot
# --------------------------------------------------------------------
    elif plottingMethod == 'pyplot':
        cc.printBlue('Plot using pyplot')
        (figs, axes) = pf.getFigures()

        for n in nodes:
            n.plotNode(axes[0])

        for e in edges:
            e.plotEdge(axes[0])

        sf.plotFace(axes[0])

#    VTK
# --------------------------------------------------------------------
    elif plottingMethod == 'VTK':
        cc.printBlue('Plot using VTK')
        cc.printRed('Not implemented')

#    TikZ
# --------------------------------------------------------------------
    elif plottingMethod == 'TikZ':
        cc.printBlue('Plot using TikZ')
        pf.closeFigures()
        from tools.tikZPicture.tikZPicture3D import TikZPicture3D
        tikZPic = TikZPicture3D()
        origin = tikZPic.addTikZCoordinate('origin', np.array([0, 0, 0]))
        tikZPic.addTikZCoSy3D(origin)
        for n in nodes:
            n.plotNodeTikZ(tikZPic)
        sf.plotFaceTikZ(tikZPic, showNormalVec=True)
        tikZPic.writeLaTeXFile('latex',
                               'simpleFace',
                               compileFile=True,
                               openFile=True)

#    Animation
# --------------------------------------------------------------------
    elif plottingMethod == 'animation':
        cc.printBlue('Creating animation')
        cc.printRed('Not implemented')

#    Documentation
# --------------------------------------------------------------------
    elif plottingMethod == 'doc':
        cc.printBlue('Creating plots for documentation')
        # test.plotDoc()

#    Unknown
# --------------------------------------------------------------------
    else:
        cc.printRed('Unknown plotting method {}'.format(plottingMethod))
