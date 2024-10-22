# -*- coding: utf-8 -*-
# =============================================================================
# FACE
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Dec 13 15:19:20 2017


'''

Construction of a face (2-cell)
--------------------------------------------------------------------------
A 2-cell is defined by a closed loop of 1-cells (edges): a closed 1 chain.
The edges are not necessarily lying in the same plane, therefor a face can
consists of more than one simple face. The correct simple faces of a face can
be identified in two ways:

* The edges are given in a list of list, where every list represents a simple
  face.
* The simple faces must be found via triangulation.

The mixture of both is also possible. Meaning that the edges are given in a
list of lists where not every list represents a simple face, but a "pseudo"
simple face that still needs to be triangulated. This can be used to impose
a wanted structure onto the simple faces where needed and let the rest of the
subdivision be calculated automatically.




The overall process consists of the following steps:

Step 1: Finding the simple edges
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Since one edge could be part of more than one simple face, the correct simple
edge(s) must be found for a simple face.


Step 2: Triangulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Triangulation can be done in different ways. A given closed loop of edges as
given in the first picture can be triangulated by alternately taking  an edge
on the left and on the right side. The result can be seen in the second
picture.
If a geometric edge is wanted at a specific place, for example between nodes 6
and 7, this edge can be generated beforehand and two pseudo-simple faces can be
passed when creating the face.
Alternatively a new geometric node can be generated at the center of a face as
shown in the last picture.

.. image:: ../../../_static/face2.png
   :width: 40 %
   :alt: Edges to define a face
.. image:: ../../../_static/face3.png
   :width: 40 %
   :alt: face with automatic alternating triangulation
.. image:: ../../../_static/face4.png
   :width: 40 %
   :alt: alternate text
.. image:: ../../../_static/face5.png
   :width: 40 %
   :alt: alternate text



Alternating
"""""""""""""""""""""""""""""""""""""""""""""""""""



Center
"""""""""""""""""""""""""""""""""""""""""""""""""""





Step 3: Categorization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^





Important properties
--------------------------------------------------------------------------

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

from kCells.node import Node
from kCells.edge import BaseEdge, Edge
from kCells.face.baseFace import BaseFace
from kCells.cell import Cell
from kCells.face.simpleFace import SimpleFace
from kCells.face.reversedFace import ReversedFace

import tools.colorConsole as cc

import tools.alphaNum as an
from tools import MyLogging
import tools.tumcolor as tc

import numpy as np


def alternate(a, b):
    """Yield alternatingly from two lists,
    then yield the remainder of the longer list."""
    for A, B in zip(a, b):
        yield A
        yield B
    yield from a[len(b):] or b[len(a):]


# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class Face(BaseFace, Cell):
    '''
    Defines the face and prepares further properties.

    '''

    faceCount = 0

# =============================================================================
#    INITIALIZATION
# =============================================================================

    def __init__(self,
                 rawEdges,
                 *args,
                 num=None,
                 label='f',
                 triangulate=False,
                 triangulationMethod='center',
                 sortEdges=False,
                 forceTriangulate=False,
                 **kwargs):
        '''

        '''

        if num is None:
            num = Face.faceCount
            Face.faceCount += 1

        super().__init__(*args,
                         loggerName=__name__,
                         label=label,
                         num=num,
                         myReverse=ReversedFace(myReverse=self),
                         **kwargs)

        self.__rawEdges = rawEdges[:]
        self.__edges = []
        self.__geometricEdges = []
        self.__geometricNodes = []
        self.__simpleFaces = []
        self.__showNormalVec = True
        self.__showBarycenter = True
        self.__volumes = []
        self.__centerNodes = []
        self.__triangulate = triangulate
        self.__sortEdges = sortEdges
        self.__forceTriangulate = forceTriangulate
        self.triangulationMethod = triangulationMethod
        self.color = tc.TUMGreen()
        self.setUp()
        self.logger.info('Created face {}'.format(self.infoText))
        self.logger.debug('Initialized Face')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================
    def __getEdges(self):
        if self.geometryChanged:
            self.setUp()
        return self.__edges

    def __setEdges(self, edges):
        self.__rawEdges = edges
        self.updateGeometry()

    edges = property(__getEdges, __setEdges)

    def __getRawEdges(self):
        return self.__rawEdges

    rawEdges = property(__getRawEdges)

    def __getSimpleFaces(self):
        if self.geometryChanged:
            self.setUp()
        return self.__simpleFaces

    simpleFaces = property(__getSimpleFaces)

    def __getGeometricEdges(self):
        if self.geometryChanged:
            self.setUp()
        return self.__geometricEdges

    geometricEdges = property(__getGeometricEdges)

    def __getGeometricNodes(self):
        if self.geometryChanged:
            self.setUp()
        return self.__geometricNodes

    geometricNodes = property(__getGeometricNodes)

    def __getCenterNodes(self):
        if self.geometryChanged:
            self.setUp()
        return self.__centerNodes

    centerNodes = property(__getCenterNodes)

    def __getSortEdges(self): return self.__sortEdges

    def __setSortEdges(self, s): self.__sortEdges = s

    sortEdges = property(__getSortEdges, __setSortEdges)

    def __getShowNormalVec(self): return self.__showNormalVec

    def __setShowNormalVec(self, s): self.__showNormalVec = s

    showNormalVec = property(__getShowNormalVec, __setShowNormalVec)

    def __getShowBarycenter(self): return self.__showBarycenter

    def __setShowBarycenter(self, s): self.__showBarycenter = s

    showBarycenter = property(__getShowBarycenter, __setShowBarycenter)

    def __getVolumes(self): return self.__volumes

    volumes = property(__getVolumes)

    def __getPolygons(self):
        if self.geometryChanged:
            self.setUp()
        return [sf.polygon for sf in self.simpleFaces]

    polygons = property(__getPolygons)

    def __getTopologicNodes(self): return self.__topologicNodes

    topologicNodes = property(__getTopologicNodes)

    def __getTriangulate(self): return self.__triangulate

    triangulate = property(__getTriangulate)

    def __getTriangulationmethod(self): return self.__triangulationMethod

    def __setTriangulationmethod(self, t):
        if t in ['center', 'alternating']:
            self.__triangulationMethod = t
        else:
            self.__triangulationMethod = None
            self.logger.error('Unknown triangulation method {} for face {}'
                              .format(t, self))

    triangulationMethod = property(__getTriangulationmethod,
                                   __setTriangulationmethod)

# =============================================================================
#    METHODS
# =============================================================================

# ------------------------------------------------------------------------
#    Set up face
# ------------------------------------------------------------------------

    def setUp(self):
        '''


        '''

        self.logger.info('setting up face {}'.format(self))
        for e in self.__edges+self.__geometricEdges:
            e.delFace(self)

        for sf in self.__simpleFaces:
            sf.delete()
        self.__simpleFaces = []
        self.__centerNodes = []

        if len(self.__rawEdges) > 0:

            # Raw edges should be a list of lists. If they are just one
            # list, put it in another list with just one entry
            if isinstance(self.__rawEdges[0], BaseEdge):
                self.__rawEdges = [self.__rawEdges, ]

            if self.__sortEdges:
                if len(self.__rawEdges) == 1:
                    self.__sortRawEdges()
                else:
                    self.logger.error(
                        'Sorting of edges is only possible with one ' +
                        'predefined closed circle of edges')

            self.logger.debug('{} simple faces are needed for face {}'
                              .format(str(len(self.__rawEdges)), self))
            allEdges = []
            allNodes = []
            num = 0

            # Find all simple edges to define simple faces
            for subEdges in self.__rawEdges:

                simpleEdges = []

                # Add all simple Edges of first raw edge of this set
                self.logger.debug('Starting with edge {}'.format(subEdges[0]))
                for se in subEdges[0].simpleEdges:
                    simpleEdges.append(se)

                # Go through the other raw Edges of this set
                for e in subEdges[1:]:
                    self.logger.debug('Adding edge {}'.format(e.infoText))
                    found = False
                    # Go through all the already found simple edges,
                    # but in inversed direction
                    for seOld in reversed(simpleEdges):
                        if not found:
                            # Got through the simple edges of the new edge
                            # to be added
                            for seNew in e.simpleEdges:
                                self.logger.debug(
                                    'Trying edge with start {} and end {}'
                                    .format(seNew.startNode, seNew.endNode))
                                # If the nodes are the same, then the first
                                # simple edge that should be added is found
                                if seNew.startNode == seOld.endNode:
                                    found = True
                                    self.logger.debug(
                                        'node {} and {} are the same'
                                        .format(seNew.startNode,
                                                seOld.endNode))
                                else:
                                    self.logger.debug(
                                        'node {} and {} are not the same'
                                        .format(seNew.startNode,
                                                seOld.endNode))
                                    self.logger.debug('seNew.endNode {}'
                                                      .format(seNew.endNode))

                                # If the beginning was found (maybe in a
                                # previous iteration of this for loop), then
                                # add all other simple edges of this new edges
                                if found:
                                    self.logger.debug('found')
                                    simpleEdges.append(seNew)

                        # If a connection between the last simple edge and the
                        # new full edge is not found, then there were to may
                        # simple edges from the last edge added to simpleEdges,
                        # therefore remove the last one and try again
                        if not found:
                            self.logger.debug('removing')
                            simpleEdges.remove(seOld)

                # The list of simple edges now looks like that:
                # [? ? ok ok ok ok ? ? ?]
                if len(simpleEdges) > 0:
                    nodes = [simpleEdges[0].startNode, ]
                    for se in simpleEdges:
                        nodes.append(se.endNode)
                    self.logger.debug(
                        'Nodes before cutting first and last simple edges ' +
                        'in subface {} of face {}: {}'
                        .format(an.alphaNum(num),
                                self.infoText,
                                ', '.join(n.infoText for n in nodes)))

                    # Start and end of this list still has to be adjusted
                    count = 0
                    while len(simpleEdges) > 0 \
                            and simpleEdges[-1].endNode \
                            != simpleEdges[0].startNode \
                            and count < 50:
                        count += 1
                        # Check if the last node occurs in the other nodes
                        # again and could maybe close the circle
                        if nodes[-1] in nodes[:-1]:
                            self.logger.debug('last node ok')
                        else:
                            self.logger.debug('last node not ok')
                            if len(simpleEdges) > 0:
                                simpleEdges.pop()
                                nodes.pop()

                        # Check if the first node occurs in the other nodes
                        # again and could maybe close the circle
                        if nodes[0] in nodes[1:]:
                            self.logger.debug('first node ok')
                        else:
                            self.logger.debug('first node not ok')
                            if len(simpleEdges) > 0:
                                simpleEdges.pop(0)
                                nodes.pop(0)

                    # The list of simple edges now should like that:
                    # [ok ok ok ok ok ok]
                    # Check that the cycled could really be closed and that it
                    # is not empty
                    if len(simpleEdges) > 0 and \
                            simpleEdges[-1].endNode \
                            == simpleEdges[0].startNode:
                        self.logger.debug('Found complete simple face')
                    else:
                        self.logger.error('Simple face cannot be built.')
                        if num == 50:
                            self.logger.error('Reached iteration limit')
                        if len(simpleEdges) == 0 or len(nodes) == 0:
                            self.logger.error(
                                'Removed all simple edges while trying to ' +
                                'close the cycle of edges: {} in face {}'
                                .format(', '.
                                        join([se.infoText for se in subEdges]),
                                        self.infoText))
                            self.delete()

                    # Find all real edges to define real Face
                    for e in subEdges:

                        # If the reversed edge is also part of the same face,
                        # this is a geometrical edge, otherwise it is a real
                        # edge
                        if e not in allEdges and not e.isGeometrical:
                            me = -e
                            if me in allEdges:
                                allEdges.remove(me)
                                try:
                                    e.isGeometrical = True
                                except Exception as ex:
                                    self.logger.error(
                                        'Error "{}"'.format(ex) +
                                        ', when setting {} to geometrical'
                                        .format(str(e)))
                            else:
                                allEdges.append(e)

                    for n in nodes:
                        if n not in allNodes:
                            allNodes.append(n)

                    if self.__forceTriangulate or \
                            (self.__triangulate and len(simpleEdges) > 3):
                        # Note: for exactly 3 simple edges, triangulation is
                        # not necessary

                        # Alternating Triangulation
                        # -------------------------------

                        if self.__triangulationMethod == 'alternating':

                            # First triangle
                            se1 = simpleEdges[0]
                            se2 = simpleEdges[1]
                            ge2 = Edge(se2.endNode,
                                       se1.startNode,
                                       isGeometrical=True)
                            localSimpleEdges = [se1, se2, ge2.simpleEdges[0]]

                            self.__simpleFaces.append(
                                SimpleFace(localSimpleEdges,
                                           belongsTo=self,
                                           labelSuffix='('
                                           + an.alphaNum(num)
                                           + ')'))
                            num += 1

                            # Inner triangles
                            edgesToDo = simpleEdges[2:]
                            numEdgesToDo = len(edgesToDo)
                            fromEnd = True
                            for i in range(numEdgesToDo-2):

                                ge1 = -ge2

                                if fromEnd:
                                    # Taking from end
                                    nextSimpleEdge = edgesToDo[-1]
                                    edgesToDo.pop()
                                    ge2 = Edge(ge1.endNode,
                                               nextSimpleEdge.startNode,
                                               isGeometrical=True)
                                    localSimpleEdges = [ge1.simpleEdges[0],
                                                        ge2.simpleEdges[0],
                                                        nextSimpleEdge]

                                else:
                                    # Taking from beginning
                                    nextSimpleEdge = edgesToDo[0]
                                    edgesToDo.pop(0)
                                    ge2 = Edge(nextSimpleEdge.endNode,
                                               ge1.startNode,
                                               isGeometrical=True)
                                    localSimpleEdges = [nextSimpleEdge,
                                                        ge2.simpleEdges[0],
                                                        ge1.simpleEdges[0]]

                                self.__simpleFaces.append(
                                    SimpleFace(localSimpleEdges,
                                               belongsTo=self,
                                               labelSuffix='('
                                               + an.alphaNum(num)
                                               + ')'))
                                num += 1
                                fromEnd = not fromEnd

                            # last triangle
                            ge1 = -ge2
                            se1 = edgesToDo[0]
                            se2 = edgesToDo[1]

                            localSimpleEdges = [ge1.simpleEdges[0], se1, se2]
                            self.__simpleFaces.append(
                                SimpleFace(localSimpleEdges,
                                           belongsTo=self,
                                           labelSuffix='('
                                           + an.alphaNum(num)
                                           + ')'))

                        # Centered Triangulation
                        # -------------------------------
                        elif self.__triangulationMethod == 'center':

                            # Determine location of new geometric node
                            nodesInSimpleFace = [se.startNode
                                                 for se in simpleEdges]
                            newCoords = np.zeros(3)
                            for n in nodesInSimpleFace:
                                newCoords += n.coordinates
                            newCoords /= len(nodesInSimpleFace)
                            newNode = Node(newCoords[0],
                                           newCoords[1],
                                           newCoords[2],
                                           isGeometrical=True)
                            self.__centerNodes.append(newNode)

                            allNodes.append(newNode)

                            # Create first geometric edges
                            currentSimpleEdge = simpleEdges[0]
                            ge2 = Edge(currentSimpleEdge.startNode,
                                       newNode,
                                       isGeometrical=True)
                            ge2Save = ge2
                            for (num, se) in enumerate(simpleEdges[:-1]):
                                ge1 = ge2
                                ge2 = Edge(se.endNode,
                                           newNode,
                                           isGeometrical=True)
                                self.__simpleFaces.append(
                                    SimpleFace([se,
                                                ge2.simpleEdges[0],
                                                -ge1.simpleEdges[0]],
                                               belongsTo=self,
                                               labelSuffix='('
                                               + an.alphaNum(num) + ')'))

                            num += 1
                            ge1 = ge2
                            ge2 = ge2Save
                            self.__simpleFaces.append(
                                SimpleFace([simpleEdges[-1],
                                            ge2.simpleEdges[0],
                                            -ge1.simpleEdges[0]],
                                           belongsTo=self,
                                           labelSuffix='('
                                           + an.alphaNum(num)+')'))

                        else:
                            self.logger.error('Unknown triangulation method')

                    else:
                        self.__simpleFaces.append(
                            SimpleFace(simpleEdges,
                                       belongsTo=self,
                                       labelSuffix='('+an.alphaNum(num)+')'))
                        num += 1
                else:
                    self.logger.error(
                        'Subface of {} '.format(self.infoText) +
                        'is not defined correctly. ' +
                        'Edges {} do not define a '.format(subEdges) +
                        'closed circle')

            self.__edges = allEdges
            if len(self.__simpleFaces) == 1:
                self.__simpleFaces[0].labelSuffix = ''

            borderNodes = []
            for e in allEdges:
                for n in [e.startNode, e.endNode]:
                    if n not in borderNodes:
                        borderNodes.append(n)

            for n in allNodes:
                if n not in borderNodes:
                    n.isGeometrical = True

            self.__geometricEdges = []

            for sf in self.__simpleFaces:
                for se in sf.simpleEdges:
                    e = se.belongsTo
#                        cc.printGreen(se.belongsTo)
#                        pass
#                for group in self.__rawEdges:
#                    for e in group:
                    if e.isReverse:
                        e = -e
                    if e not in allEdges and -e not in allEdges  \
                            and e not in self.__geometricEdges:
                        self.__geometricEdges.append(e)

            self.__geometricNodes = []
            for n in allNodes:
                if n.isGeometrical and n not in self.__geometricNodes:
                    self.__geometricNodes.append(n)

            for e in [*self.__edges, *self.__geometricEdges]:
                e.addFace(self)

            # Storing topologic nodes
            self.__topologicNodes = []
            for e in self.__edges:
                for n in e.topologicNodes:
                    if n not in self.__topologicNodes:
                        self.__topologicNodes.append(n)

        else:
            self.__edges = []
            self.__topologicNodes = []

        self.geometryChanged = False

# ------------------------------------------------------------------------
#    Update geometry
# ------------------------------------------------------------------------

    def updateGeometry(self):
        self.logger.debug('Update Face{}'.format(self.infoText))
        super().updateGeometry()
        for v in self.__volumes:
            v.updateGeometry()

# ------------------------------------------------------------------------
#    Simplify face by combining simple faces
# ------------------------------------------------------------------------

    def simplifyFace(self):
        if self.geometryChanged:
            self.setUp()

        tol = 1E-3
        edgesToBeRemoved = []
        self.logger.info('{}: Simplifying. Old raw edges: {}'
                         .format(self.infoText, self.__rawEdges))
        for e in self.__geometricEdges:
            attachedSimpleFaces = []
            for sf in self.__simpleFaces:
                if any([se in sf.simpleEdges for se in e.simpleEdges]) \
                        or any([se.myReverse in sf.simpleEdges
                                for se in e.simpleEdges]):
                    attachedSimpleFaces.append(sf)
            self.logger.debug('geometric edge {} is attached to {}'
                              .format(e, attachedSimpleFaces))

            if len(attachedSimpleFaces) > 1:
                normalVec0 = attachedSimpleFaces[0].normalVec

                if all([np.linalg.norm(normalVec0-sf.normalVec) < tol
                        for sf in attachedSimpleFaces[1:]]):
                    if e not in edgesToBeRemoved:
                        edgesToBeRemoved.append(e)
                else:
                    self.logger.debug('Cannot be removed')

            else:
                self.logger.error(
                    '{}: geometric edge {} '
                    .format(self.infoText, e.infoText) +
                    'should belong to a minimum of 2 simple faces, ' +
                    'but only belongs to {}!'
                    .format(len(attachedSimpleFaces)))

        self.logger.debug('Going to remove edges {}'.format(edgesToBeRemoved))
        for e in edgesToBeRemoved:
            pack1 = None
            pack2 = None
            for edges in self.__rawEdges:
                if e in edges:
                    if not pack1:
                        pack1 = edges
                    else:
                        self.logger.error('error')

                if -e in edges:
                    if not pack2:
                        pack2 = edges
                    else:
                        self.logger.error('error')

            self.logger.debug('pack1: {} pack2: {}'.format(pack1, pack2))
            if pack1 == pack2:

                if e in pack1 and -e in pack1:
                    pack1.remove(e)
                    pack1.remove(-e)
                    self.logger.debug(
                        'Edge {} and its reverse '.format(e) +
                        'are in the same pack, it is now: {}'.format(pack1))

                else:
                    self.logger.error(
                        'error, both packs are the same, but do not contain ' +
                        'the removable edge and its reverse')

            else:
                pack12 = []
                found = False
                for e1 in pack1:
                    if e == e1:
                        found = True
                    if not found and e1 not in pack12:
                        pack12.append(e1)
                found = False
                for e2 in pack2:
                    if found and e2 not in pack12:
                        pack12.append(e2)
                    if -e == e2:
                        found = True
                found = False
                for e2 in pack2:
                    if -e == e2:
                        found = True
                    if not found and e2 not in pack12:
                        pack12.append(e2)

                found = False
                for e1 in pack1:
                    if found and e1 not in pack12:
                        pack12.append(e1)
                    if e1 == e:
                        found = True

                self.logger.debug('{}: New pack: {}'
                                  .format(self.infoText, pack12))


#            pack12 = [*pack1, *pack2]
#            if e in pack12:
#                pack12.remove(e)
#            else:
#                cc.printRed('error')
#            if -e in pack12:
#                pack12.remove(-e)
#            else:
#                cc.printRed('error')

#            if not pack1 == pack2:
                self.__rawEdges.remove(pack1)
                self.__rawEdges.remove(pack2)
                self.__rawEdges.append(pack12)
#            else:
#                if e in pack1 and -e in pack1:
#                    pack1.remove(e)
#                    pack1.remove(-e)
#                else:
#                    cc.printRed('error')

#                    edges.remove(-e)
#            self.data.rawEdges.remove(e)
#            self.data.rawEdges.remove(-e)

        self.logger.info('{}: Simplified simple faces, new raw edges: {}'
                         .format(self.infoText, self.__rawEdges))
        self.updateGeometry()
#        ml.setStreamLevel(self.logger)

# ------------------------------------------------------------------------
#    Linear interpolation
# ------------------------------------------------------------------------
    def interpolateLinear(self, myPrintDebug=None, myPrintError=None):
        if not myPrintDebug:
            myPrintDebug = self.logger.debug
        if not myPrintError:
            myPrintError = self.logger.error

        if len(self.simpleFaces) != 1:
            myPrintError('Must have 1 simple face, but {} has {}'
                         .format(self, len(self.simpleFaces)))
            return None
        else:
            myPrintDebug('Number of simple faces is ok')

        if len(self.edges) != 3:
            myPrintError('Must have 3 edges, but {} has {}'
                         .format(self, len(self.edges)))
            return None
        else:
            myPrintDebug('Number of edges is ok')

        nodes = [e.startNode for e in self.edges]

        entries = []
        for (n, e) in zip(nodes[2:]+nodes[0:2], self.edges):
            myPrintDebug('Node {} is opposite of edge {}'.format(n, e))
            v = e.simpleEdges[0].connectionVec
            myPrintDebug('Vector of edge: {}'.format(v))
            entry = (n.num, -v[1], v[0])
            myPrintDebug('{}'.format(entry))
            entries.append(entry)

        return entries

# ------------------------------------------------------------------------
#    Volume handling
# ------------------------------------------------------------------------

    def addVolume(self, v):
        if v in self.__volumes:
            self.logger.error('Volume {} already belongs to face {}'
                              .format(v, self))
        else:
            self.__volumes.append(v)

    def delVolume(self, v):
        if v in self.__volumes:
            self.__volumes.remove(v)
        else:
            self.logger.error('Face {} is not part of volume {}'
                              .format(self, v))

# ------------------------------------------------------------------------
#    Delete the entire face
# ------------------------------------------------------------------------
    def delete(self):
        self.logger.debug('Delete Face {}'.format(self.infoText))
        if self.__volumes:
            self.logger.error(
                'Cannot delete face {} because it belongs to a volume'
                .format(self.infoText))
        else:
            self.__rawEdges = []
            self.setUp()
            super().delete()

# ------------------------------------------------------------------------
#    Update text
# ------------------------------------------------------------------------
    def updateText(self):
        for sf in self.__simpleFaces:
            sf.updateText()
        super().updateText()

    def __sortRawEdges(self):
        edgesUnsorted = self.__rawEdges[0][:]
        edgesSorted = [edgesUnsorted[0], ]

        edgesUnsorted.pop(0)

        counter = 0
        maxCounter = 50
        while len(edgesUnsorted) > 0 and counter < maxCounter:
            counter += 1
            for e in edgesUnsorted:
                if e.startNode == edgesSorted[-1].endNode:
                    edgesSorted.append(e)
                    edgesUnsorted.remove(e)
                elif e.endNode == edgesSorted[-1].endNode:
                    edgesSorted.append(-e)
                    edgesUnsorted.remove(e)

        if counter >= maxCounter:
            self.logger.error('Cannot find closed circle to define face {}'
                              .format(self.infoText))
            return False

        else:
            self.__rawEdges = [edgesSorted, ]

# ------------------------------------------------------------------------
#    Plot for Documentation
# ------------------------------------------------------------------------
    @classmethod
    def plotDoc(cls):
        '''
        Create all plots needed for the documentation.

        '''
        import tools.placeFigures as pf

        (figs, axes) = pf.getFigures(numTotal=6)
        axNum = -1

        a = 5
        n100 = Node(0, 0, 0)
        n101 = Node(a, 0, 0)
        n102 = Node(a, a, 0)
        n103 = Node(0, a, 0)
        nodes100 = [n100, n101, n102, n103]

        e100 = Edge(n100, n101)
        e101 = Edge(n101, n102)
        e102 = Edge(n102, n103)
        e103 = Edge(n103, n100)
        edges100 = [e100, e101, e102, e103]

        f100 = Face([e100, e101, e102, e103])

        axNum += 1
        for n in nodes100:
            n.plotNode(axes[axNum])

        for e in edges100:
            e.plotEdge(axes[axNum])

        f100.plotFace(axes[axNum])
        pf.setAxesEqual(axes[axNum])
        pf.exportPNG(figs[0], 'doc/_static/face1')

        n1000 = Node(0, 0, -1, num=0)
        n1001 = Node(0.5, -1, 0, num=1)
        n1002 = Node(2, 0, 1.5, num=2)
        n1003 = Node(2, 1, 1, num=3)
        n1004 = Node(1.5, 2, 0, num=4)
        n1005 = Node(0.5, 2, 0, num=5)
        n1006 = Node(0, 1, 0, num=6)
        n1007 = Node(1, -1, 0, num=7)
        nodes1000 = [n1000, n1001, n1002, n1003, n1004, n1005, n1006, n1007]

        e1000 = Edge(n1000, n1001, num=0)
        e1001 = Edge(n1001, n1002, geometricNodes=[n1007, ], num=1)
        e1002 = Edge(n1002, n1003, num=2)
        e1003 = Edge(n1003, n1005, geometricNodes=[n1004, ], num=3)
        e1004 = Edge(n1005, n1006, num=4)
        e1005 = Edge(n1006, n1000, num=5)
        e1006 = Edge(n1006, n1001, num=6)

        edges1000 = [e1000, e1001, e1002, e1003, e1004, e1005]

        f1000 = Face([[e1000, -e1006, e1005],
                      [e1001, e1002, e1003, e1004, e1006]],
                     triangulate=True,
                     triangulationMethod='alternating')

        f1001 = Face([e1000, e1001, e1002, e1003, e1004, e1005],
                     triangulate=True,
                     triangulationMethod='alternating')
        f1002 = Face([e1000, e1001, e1002, e1003, e1004, e1005],
                     triangulate=True,
                     triangulationMethod='center')

        axNum += 1
        for n in nodes1000:
            n.plotNode(axes[axNum])
        axes[axNum].view_init(34, -132)
        for e in edges1000:
            e.plotEdge(axes[axNum])
        pf.exportPNG(figs[axNum], 'doc/_static/face2')

        axNum += 1
        for n in nodes1000:
            n.plotNode(axes[axNum])
        for e in [*f1000.edges, *f1000.geometricEdges]:
            e.plotEdge(axes[axNum])
        f1000.plotFace(axes[axNum])
        axes[axNum].view_init(34, -132)
        pf.exportPNG(figs[axNum], 'doc/_static/face3')

        axNum += 1
        for n in nodes1000:
            n.plotNode(axes[axNum])
        for e in [*f1001.edges, *f1001.geometricEdges]:
            e.plotEdge(axes[axNum])
        f1001.plotFace(axes[axNum])
        axes[axNum].view_init(34, -132)
        pf.exportPNG(figs[axNum], 'doc/_static/face4')

        axNum += 1
        for n in nodes1000:
            n.plotNode(axes[axNum])
        for e in [*f1002.edges, *f1002.geometricEdges]:
            e.plotEdge(axes[axNum])
        f1002.plotFace(axes[axNum])
        axes[axNum].view_init(34, -132)
        pf.exportPNG(figs[axNum], 'doc/_static/face5')


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':

    import tools.placeFigures as pf

    with MyLogging('Face'):
        # Create figures on second screen
        (figs, ax) = pf.getFigures(numTotal=9)

        plotCase = 3

        axNum = -1

        if plotCase == 0:
            Face.plotDoc()

    # ------------------------------------------------------------------------
    #    Case 1
    # ------------------------------------------------------------------------
        if plotCase == 1:

            cc.printBlue('Create case 1: no special things')

            # Create some nodes
            n101 = Node(0, 0, 0, num=1)
            n102 = Node(1, 0, 0, num=2)
            n103 = Node(0.5, 1, 0, num=3)
            nodes100 = [n101, n102, n103]

            # Create some edges
            e101 = Edge(n101, n102, num=1)
            e102 = Edge(n102, n103, num=2)
            e103 = Edge(n103, n101, num=3)
            edges100 = [e101, e102, e103]

            # Create face
            f101 = Face([e101, e102, e103], num=1)

            # Plot
            axNum += 1
            for n in nodes100:
                n.plotNode(ax[axNum])
            for e in edges100:
                e.plotEdge(ax[axNum])
            f101.plotFace(ax[axNum])
            ax[axNum].set_title('Case 1')

    # ------------------------------------------------------------------------
    #    Case 2
    # ------------------------------------------------------------------------
            cc.printBlue('Create case 2: geometric node in plane')

            # Create some nodes
            n201 = Node(0, 0, 0, num=1)
            n202 = Node(1, 0, 0, num=2)
            n203 = Node(0.5, 1, 0, num=3)
            n204 = Node(0.8, 0.8, 0, num=4)
            nodes200 = [n201, n202, n203, n204]

            # Create some edges
            e201 = Edge(n201, n202, num=1)
            e202 = Edge(n202, n203, num=2, geometricNodes=[n204, ])
            e203 = Edge(n203, n201, num=3)
            edges200 = [e201, e202, e203]

            # Create face
            f201 = Face([e201, e202, e203], num=2)

            # Plot
            axNum += 1
            for n in nodes200:
                n.plotNode(ax[axNum])
            for e in edges200:
                e.plotEdge(ax[axNum])
            f201.plotFace(ax[axNum])
            ax[axNum].set_title('Case 2')

    # ------------------------------------------------------------------------
    #    Case 3
    # ------------------------------------------------------------------------
            cc.printBlue('Create case 3: geometric node out of plane')

            # Create some nodes
            n301 = Node(0, 0, 0, num=1)
            n302 = Node(1, 0, 0, num=2)
            n303 = Node(0.5, 1, 0, num=3)
            n304 = Node(0.8, 0.8, 0.5, num=4)
            nodes300 = [n301, n302, n303, n304]

            # Create some edges
            e301 = Edge(n301, n302, num=1)
            e302 = Edge(n302, n303, num=2, geometricNodes=[n304, ])
            e303 = Edge(n303, n301, num=3)
            e304 = Edge(n301, n304, num=4)
            edges300 = [e301, e302, e303, e304]

            # Create face
            f301 = Face([[e301, e302, -e304], [e302, e303, e304]], num=3)

            # Plot
            axNum += 1
            for n in nodes300:
                n.plotNode(ax[axNum])
            for e in edges300:
                e.plotEdge(ax[axNum])
            f301.plotFace(ax[axNum])
            ax[axNum].set_title('Case 3')

    # ------------------------------------------------------------------------
    #    Case 4
    # ------------------------------------------------------------------------
            cc.printBlue('Create case 4: topological node out of plane')

            # Create some nodes
            n401 = Node(0, 0, 0, num=1)
            n402 = Node(1, 0, 0, num=2)
            n403 = Node(0.5, 1, 0, num=3)
            n404 = Node(0.8, 0.8, 0.5, num=4)
            nodes400 = [n401, n402, n403, n404]

            # Create some edges
            e401 = Edge(n401, n402, num=1)
            e402 = Edge(n402, n404, num=2)
            e403 = Edge(n404, n403, num=3)
            e404 = Edge(n403, n401, num=4)
            e405 = Edge(n404, n401, num=5)
            edges400 = [e401, e402, e403, e404, e405]

            # Create face
            f401 = Face([[e401, e402, e405], [-e405, e403, e404]], num=4)

            # Plot
            axNum += 1
            for n in nodes400:
                n.plotNode(ax[axNum])
            for e in edges400:
                e.plotEdge(ax[axNum])
            f401.plotFace(ax[axNum])
            ax[axNum].set_title('Case 4')

    # ------------------------------------------------------------------------
    #    Case 5
    # ------------------------------------------------------------------------
            cc.printBlue('Create case 5: geometrical node inside face')

            # Create some nodes
            n501 = Node(0, 0, 0, num=1)
            n502 = Node(1, 0, 0, num=2)
            n503 = Node(0.5, 1, 0, num=3)
            n504 = Node(0.5, 0.5, 0.5, num=4)
            nodes500 = [n501, n502, n503, n504]

            # Create some edges
            e501 = Edge(n501, n502, num=1)
            e502 = Edge(n502, n503, num=2)
            e503 = Edge(n503, n501, num=3)
            e504 = Edge(n501, n504, num=4)
            e505 = Edge(n502, n504, num=5)
            e506 = Edge(n503, n504, num=6)
            edges500 = [e501, e502, e503, e504, e505, e506]

            f501 = Face([[e501, e505, -e504],
                         [e502, e506, -e505],
                         [e503, e504, -e506]],
                        num=5)

            # Plot
            axNum += 1
            f501.setUp()
            for n in nodes500:
                n.plotNode(ax[axNum])
            for e in edges500:
                e.plotEdge(ax[axNum])
            f501.plotFace(ax[axNum])
            ax[axNum].set_title('Case 5')

    # ------------------------------------------------------------------------
    #    Case 6
    # ------------------------------------------------------------------------
            cc.printBlue('Create case 6: several geometrical nodes')

            # Create some nodes
            n601 = Node(0, 0, 0, num=601)
            n602 = Node(1, 0, 0, num=602)
            n603 = Node(0.5, 1, 0, num=603)
            n604 = Node(0.5, 0.3, 0.5, num=604)
            n605 = Node(0.5, 0.7, 0.5, num=605)
            n606 = Node(0.75, 0.75, 0, num=606)
            n607 = Node(0.25, 0.75, 0, num=607)
            nodes600 = [n601, n602, n603, n604, n605, n606, n607]

            # Create some edges
            e601 = Edge(n601, n602, num=601)
            e602 = Edge(n602, n603, num=602, geometricNodes=[n606, ])
            e603 = Edge(n603, n601, num=603, geometricNodes=[n607, ])
            e604 = Edge(n601, n604, num=604)
            e605 = Edge(n602, n604, num=605)
            e606 = Edge(n604, n605, num=606)
            e607 = Edge(n605, n603, num=607)
            e608 = Edge(n607, n606, num=608, geometricNodes=[n605, ])
            e609 = Edge(n607, n606, num=609, geometricNodes=[n604, ])
            edges600 = [e601, e602, e603, e604, e605, e606, e607, e608, e609]

            f601 = Face([[e603, e608, e607],
                         [-e607, e608, e602],
                         [e601, e605, -e604],
                         [e602, -e609, -e605],
                         [e609, -e608, -e606],
                         [e609, e606, -e608],
                         [e603, e604, -e609]],
                        num=601)

            # Plot
            axNum += 1
            for n in nodes600:
                n.plotNode(ax[axNum])
            for e in edges600:
                e.plotEdge(ax[axNum])
            f601.plotFace(ax[axNum])
            ax[axNum].set_title('Case 6')

    # ------------------------------------------------------------------------
    #    Case 7
    # ------------------------------------------------------------------------
            cc.printBlue('Create case 7: fancy')

            # Create some nodes
            n701 = Node(0, 0, -0.5, num=701)
            n702 = Node(3, 0, -0.5, num=702)
            n703 = Node(1, 1, 0, num=703)
            n704 = Node(2, 1, 0, num=704)
            n705 = Node(3, 1, 0, num=705)
            n706 = Node(0.5, 2.5, 2, num=706)
            n707 = Node(2, 2, 1.5, num=707)
            n708 = Node(3, 2, 1.5, num=708)
            n709 = Node(2, 3, 2, num=709)
            nodes700 = [n701, n702, n703, n704, n705, n706, n707, n708, n709]

            # Create some edges
            e701 = Edge(n701, n705, num=701, geometricNodes=n702)
            e702 = Edge(n701, n702, num=702, geometricNodes=[n703, n704])
            e703 = Edge(n705, n708, num=703)
            e704 = Edge(n704, n705, num=704)
            e705 = Edge(n706, n707, num=705, geometricNodes=n703)
            e706 = Edge(n701, n706, num=706)
            e707 = Edge(n706, n708, num=707, geometricNodes=n709)
            e708 = Edge(n706, n708, num=708, geometricNodes=n707)
            e709 = Edge(n707, n709, num=709)
            edges700 = [e701, e702, e703, e704, e705, e706, e707, e708, e709]

            f701 = Face([[e701, -e702],
                         [e701, -e704, e702],
                         [e702, -e705, -e706],
                         [e703, -e708, -e705, e702, e704],
                         [e705, -e708],
                         [e709, -e707, e708],
                         [e708, -e707, -e709]],
                        num=701)

            # Plot
            axNum += 1
            for n in nodes700:
                n.plotNode(ax[axNum])
            for e in edges700:
                e.plotEdge(ax[axNum])
            f701.plotFace(ax[axNum])
            ax[axNum].set_title('Case 7')
    #        f701.simplifyFace()

    # ------------------------------------------------------------------------
    #    Case 8
    # ------------------------------------------------------------------------
            cc.printBlue('Create case 8: simplification')
            n801 = Node(0, 0, 0, num=801)
            n802 = Node(1, 0, 0, num=802)
            n803 = Node(1, 1, 0, num=803)
            n804 = Node(0, 1, 0, num=804)
            nodes800 = [n801, n802, n803, n804]

            e801 = Edge(n801, n802, num=801)
            e802 = Edge(n802, n803, num=802)
            e803 = Edge(n803, n804, num=803)
            e804 = Edge(n804, n801, num=804)
            e805 = Edge(n801, n803, num=805)
            edges800 = [e801, e802, e803, e804, e805]

            f801 = Face([[e801, e802, -e805], [e805, e803, e804]], num=801)
            cc.printYellow('Geometric edges before simplification:',
                           f801.geometricEdges)
            mf = -f801

            # Plot
            axNum += 1
            for n in nodes800:
                n.plotNode(ax[axNum])
            for e in edges800:
                e.plotEdge(ax[axNum])

            f801.plotFace(ax[axNum])
            ax[axNum].set_title('Case 8 before')

            mf.simplifyFace()

            axNum += 1
            for n in nodes800:
                n.plotNode(ax[axNum])
            for e in f801.edges:
                e.plotEdge(ax[axNum])
            f801.plotFace(ax[axNum])
            ax[axNum].set_title('Case 8 after')
            cc.printYellow('Geometric edges after simplification:',
                           f801.geometricEdges)

    # ------------------------------------------------------------------------
    #    Case 1 changes
    # ------------------------------------------------------------------------
        if plotCase == 2:

            cc.printBlue('Change case 1: one coordinate in one node of face')
            cc.printYellow('Checking normal vector before and after changing')
            cc.printGreen(f101.normalVec)
            n101.zCoordinate = 3
            cc.printGreen(f101.normalVec)
            # Plot
            axNum += 1
            for n in nodes100:
                n.plotNode(ax[axNum])
            for e in edges100:
                e.plotEdge(ax[axNum])
            f101.plotFace(ax[axNum])
            pf.setAxesEqual(ax[axNum])
            ax[axNum].set_title('Case 1 changed')

    # ------------------------------------------------------------------------
    #    Case 2 changes
    # ------------------------------------------------------------------------
            cc.printBlue('Change case 2: one coordinate in all nodes')
            for n in nodes200:
                n.zCoordinate = 2

            # Plot
            axNum += 1
            for n in nodes200:
                n.plotNode(ax[axNum])
            for e in edges200:
                e.plotEdge(ax[axNum])
            f201.plotFace(ax[axNum])
            ax[axNum].set_title('Case 2 changed')

    # ------------------------------------------------------------------------
    #    Case 3 changes
    # ------------------------------------------------------------------------
            cc.printBlue('Change case 3: replace one node')
            n305 = Node(0.5, 1, -0.5, num=5)
            e302.endNode = n305
            e303.startNode = n305
            nodes300.append(n305)

            # Plot
            axNum += 1
            for n in nodes300:
                n.plotNode(ax[axNum])
            for e in edges300:
                e.plotEdge(ax[axNum])
            f301.plotFace(ax[axNum])
            ax[axNum].set_title('Case 3 changed')

    # ------------------------------------------------------------------------
    #    Case 4 changes
    # ------------------------------------------------------------------------
            cc.printBlue('Change case 4: replace an edge')
            n405 = Node(0.5, -0.5, -0.5, num=405)
            nodes400.append(n405)

            # Plot
            axNum += 1
            for n in nodes400:
                n.plotNode(ax[axNum])
            for e in edges400:
                e.plotEdge(ax[axNum])
            f401.plotFace(ax[axNum])
            ax[axNum].set_title('Case 4 changed')

    # ------------------------------------------------------------------------
    #    Case 1 reversed
    # ------------------------------------------------------------------------
            cc.printBlue('Reverse case 1')
            axNum += 1
            for n in nodes100:
                n.plotNode(ax[axNum])
            for e in edges100:
                e.myReverse.plotEdge(ax[axNum])
            f101.myReverse.plotFace(ax[axNum])
            pf.setAxesEqual(ax[axNum])
            ax[axNum].set_title('Case 1 reversed')

    # ------------------------------------------------------------------------
    #    Case 6 reversed
    # ------------------------------------------------------------------------
            cc.printBlue('Reverse case 6')
            axNum += 1
            for n in nodes600:
                n.plotNode(ax[axNum])
            for e in edges600:
                e.myReverse.plotEdge(ax[axNum])
            f601.myReverse.plotFace(ax[axNum])
            pf.setAxesEqual(ax[axNum])
            ax[axNum].set_title('Case 6 reversed')

    # ------------------------------------------------------------------------
    #    Check setter and getter
    # ------------------------------------------------------------------------
            cc.printBlue('Check some values')
            cc.printYellow('edges:', f601.edges)
            cc.printYellow('geometricEdges:', f601.geometricEdges)
            cc.printYellow('simpleFaces:', f601.simpleFaces)
            cc.printYellow('normalVec:')
            for v in f601.normalVec:
                cc.printYellow('\t', v)
            f601.showNormalVec = False
            cc.printYellow('showNormalVec:', f601.showNormalVec)
            f601.showBarycenter = False
            cc.printYellow('showBarycenter:', f601.showBarycenter)

            mf601 = -f601
            cc.printGreen('edges:', mf601.edges)
            cc.printGreen('geometricEdges:', mf601.geometricEdges)
            cc.printGreen('simpleFaces:', mf601.simpleFaces)
            cc.printGreen('normalVec:')
            for v in f601.normalVec:
                cc.printGreen('\t', v)
            print()
            for v in mf601.normalVec:
                cc.printGreen('\t', v)
            mf601.showNormalVec = True
            cc.printGreen('showNormalVec:',
                          mf601.showNormalVec,
                          f601.showNormalVec)
            mf601.showBarycenter = True
            cc.printGreen('showBarycenter:',
                          mf601.showBarycenter,
                          f601.showBarycenter)
            cc.printGreen('Barycenter:')
            for b in f601.barycenter:
                cc.printGreen('\t', b)
            print()
            for b in mf601.barycenter:
                cc.printGreen('\t', b)

            cc.printBlue('Test of non-convex face')

            n900 = Node(0, 0, 0)
            n901 = Node(2, 0, 2)
            n902 = Node(0, 2, 0)
            n903 = Node(0.5, 1, 0.5)
            n904 = Node(2, 0, 0)
            n905 = Node(0.5, 1, 0)

            nodes900 = [n900, n901, n902, n903, n904, n905]

            e900 = Edge(n902, n903)
            e901 = Edge(n903, n900)
            e902 = Edge(n900, n901)
            e903 = Edge(n901, n902)
            e904 = Edge(n900, n904)
            e905 = Edge(n904, n902)
            e906 = Edge(n902, n905)
            e907 = Edge(n905, n900)
            edges900 = [e900, e901, e902, e903, e904, e905, e906, e907]

            f900 = Face([e900, e901, e902, e903])
            f901 = Face([e906, e907, e904, e905])
            faces900 = [f900, f901]
            axNum += 1
            for n in nodes900:
                n.plotNode(ax[axNum])
            for e in edges900:
                e.plotEdge(ax[axNum])
            for f in faces900:
                f.plotFace(ax[axNum])
            ax[axNum].set_title('Non-convex face')

    # ------------------------------------------------------------------------
    #    Automatic triangulation
    # ------------------------------------------------------------------------
        if plotCase == 3:

            cc.printBlue('Automatic triangulation')
            n1000 = Node(0, 0, -1)
            n1001 = Node(0.5, -1, 0)
            n1002 = Node(2, 0, 1.5)
            n1003 = Node(2, 1, 1)
            n1004 = Node(1.5, 2, 0)
            n1005 = Node(0.5, 2, 0)
            n1006 = Node(0, 1, 0)
            n1007 = Node(1, -1, 0)
            nodes1000 = [n1000, n1001, n1002, n1003,
                         n1004, n1005, n1006, n1007]

            e1000 = Edge(n1000, n1001)
            e1001 = Edge(n1001, n1002, geometricNodes=[n1007, ])
            e1002 = Edge(n1002, n1003)
            e1003 = Edge(n1003, n1005, geometricNodes=[n1004, ])
            e1004 = Edge(n1005, n1006)
            e1005 = Edge(n1006, n1000)
            e1006 = Edge(n1006, n1001)

            edges1000 = [e1000, e1001, e1002, e1003, e1004, e1005, e1006]

            f1000 = Face([[e1000, -e1006, e1005],
                          [e1001, e1002, e1003, e1004, e1006]],
                         triangulate=True,
                         triangulationMethod='alternating')

            f1001 = Face([e1000, e1001, e1002, e1003, e1004, e1005],
                         triangulate=True,
                         triangulationMethod='alternating')
            f1002 = Face([e1000, e1001, e1002, e1003, e1004, e1005],
                         triangulate=True,
                         triangulationMethod='center')

            axNum += 1
            for n in nodes1000:
                n.plotNode(ax[axNum])


#            edges1000.remove(e1006)
#            for e in edges1000:
#                e.plotEdge(ax[axNum])
#
            for e in [*f1000.edges, *f1000.geometricEdges]:
                e.plotEdge(ax[axNum])
            f1000.plotFace(ax[axNum])

            axNum += 1
            for e in [*f1001.edges, *f1001.geometricEdges]:
                e.plotEdge(ax[axNum])
            f1001.plotFace(ax[axNum])

            axNum += 1
            for e in [*f1002.edges, *f1002.geometricEdges]:
                e.plotEdge(ax[axNum])
            f1002.plotFace(ax[axNum])
            for n in f1002.geometricNodes:
                n.plotNode(ax[axNum])

    # ------------------------------------------------------------------------
    #    Automatic edge sorting
    # ------------------------------------------------------------------------

            n1100 = Node(0, 0, 0)
            n1101 = Node(1, 0, 0)
            n1102 = Node(1, 1, 0)
            n1103 = Node(0.5, 1.5, 0)
            n1104 = Node(0, 1, 0)

            nodes1100 = [n1100, n1101, n1102, n1103, n1104]

            e1100 = Edge(n1100, n1101)
            e1101 = Edge(n1101, n1102)
            e1102 = Edge(n1102, n1103)
            e1103 = Edge(n1103, n1104)
            e1104 = Edge(n1104, n1100)

            edges1100 = [e1100, e1101, e1102, e1103, e1104]

            f1100 = Face([e1100, -e1101, e1103, e1104, e1102],
                         sortEdges=True,
                         triangulate=True)
#            f1100 = Face([e1100, e1101, e1102, e1103, e1104])

            axNum += 1
            for n in nodes1100:
                n.plotNode(ax[axNum])

            for e in edges1100:
                e.plotEdge(ax[axNum])

            f1100.plotFace(ax[axNum])

# ------------------------------------------------------------------------
#    Figure Setup
# ------------------------------------------------------------------------

        for a in ax:
            pf.setAxesEqual(a)
            pf.setLabels(a)

        if False:
            import tools.myVTK as myv
            myVTK = myv.MyVTK()
            for sf in f1002.simpleFaces:
                sf.plotFaceVtk(myVTK)
#            for sf in f1002.simpleFaces:
            f1002.plotFlowVtk(myVTK, 2)
            myVTK.start()

        # TODO: Was passiert, wenn man in einer
        # reversedFace Kanten austauscht???
