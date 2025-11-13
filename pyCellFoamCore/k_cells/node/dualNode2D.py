# -*- coding: utf-8 -*-
# =============================================================================
# DUAL NODE 2D
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Jul  6 14:09:24 2018

'''
The location of a node that is dual to a face depends on the number of simple
faces. More than three simple faces is not possible. The other cases are
explained below.

1 simple face
--------------------------------------------------------------------------
The standard case is one simple face, where the the dual node is located
at the barycenter of the face.

.. image:: ../../../_static/dualNode2D_0.png
   :width: 400px
   :alt: 2D dual node
   :align: center

If one of the edges is an additional border edge, the 2D dual node of the face
is the 1D dual of the additonal border edge

.. image:: ../../../_static/dualNode2D_3.png
   :width: 400px
   :alt: 2D dual node
   :align: center


2 simple faces
--------------------------------------------------------------------------
At the rim of the additional border, two simple face may occur. These two
simple faces are connected by one geometric edges. So this case quals the 1D
dual of the geometric edge.

.. image:: ../../../_static/dualNode2D_1.png
   :width: 400px
   :alt: 2D dual node
   :align: center

3 simple faces
--------------------------------------------------------------------------
A face at the corner of the additional border consists of three simple faces.
The geometric edges of this face intersect in one point (the corner). So this
case equals the 0D dual of the corner node.

.. image:: ../../../_static/dualNode2D_2.png
   :width: 400px
   :alt: 2D dual node
   :align: center



'''
# =============================================================================
#    IMPORTS
# =============================================================================
# ------------------------------------------------------------------------
#    Change to Main Directory
# ------------------------------------------------------------------------
import os
if __name__ == '__main__':
    os.chdir('../../')

# ------------------------------------------------------------------------
#    Standard Libraries
# ------------------------------------------------------------------------

import logging

# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------

#    kCells
# -------------------------------------------------------------------
from k_cells.cell import DualCell

#    Tools
# -------------------------------------------------------------------
import tools.colorConsole as cc

from k_cells.node.node import Node
from k_cells.node.dualNode1D import DualNode1D
from k_cells.node.dualNode0D import DualNode0D
from tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class DualNode2D(Node, DualCell):
    '''

    '''

# =============================================================================
#    SLOTS
# =============================================================================
#    __slots__ = ()

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __new__(cls, face, *args, volume=None, **kwargs):
        '''
        Depending on the geometry of the primal face, the dual node is either
        calculated as a 2D dual in this class or as a 1D or 0D dual in the
        according class.

        '''

        if len(face.simpleFaces) == 2 and len(face.geometricEdges) == 1:
            return DualNode1D(face.geometricEdges[0], face=face)
        elif len(face.simpleFaces) == 3 and len(face.geometricNodes) == 1:
            return DualNode0D(face.geometricNodes[0], face=face)
        elif len(face.simpleFaces) == 1 and \
            len([e for e in face.edges
                 if e.category == 'additionalBorder']) == 1:
            additionalBorderEdges = [e for e in face.edges
                                     if e.category == 'additionalBorder']
            return DualNode1D(additionalBorderEdges[0], face=face)
        else:
            return super(DualNode2D, cls).__new__(cls)

    def __init__(self,
                 face,
                 *args,
                 volume=None,
                 **kwargs):
        '''
        :param Face face: Primal face to which a 2D dual is wanted to be
            calculated
        :param Volume volume: If this dual node is generated as a special case
            of a higher dimension, the duality is stored also in the volume.


        '''

        super().__init__(0, 0, 0,
                         *args,
                         num=face.num,
                         **kwargs)

        if volume:
            self.category1 = volume.category1
            self.category2 = volume.category2

        elif face.category1 == 'border':
            self.category1 = 'additionalBorder'
            self.category2 = 'additionalBorder'

        else:
            self.category1 = face.category1
            self.category2 = face.category2



        _log.debug('Calculating 2D dual of {}'.format(face))

# ------------------------------------------------------------------------
#    Standard-Case: One simple face
# ------------------------------------------------------------------------

        if len(face.barycenter) == 1:
            bc = face.barycenter[0]

            self.xCoordinate = bc[0]
            self.yCoordinate = bc[1]
            self.zCoordinate = bc[2]

# ------------------------------------------------------------------------
#    Two simple faces, for example at rim
# ------------------------------------------------------------------------

        elif len(face.barycenter) == 2:
            # if len(face.geometricEdges) == 1:
            #     if face.geometricEdges[0].dualCell1D == None:
            #         dn = DualNode1D(face.geometricEdges[0])
            #         self.xCoordinate = dn.xCoordinate
            #         self.yCoordinate = dn.yCoordinate
            #         self.zCoordinate = dn.zCoordinate
            if not len(face.geometricEdges) == 1:
                _log.error('Face {} '.format(face.infoText) +
                             'has two barycenters and should so have one ' +
                             'geometric edge, but has {}'
                             .format(len(face.geometricEdges)))

# ------------------------------------------------------------------------
#    Three simple faces, for example at corner
# ------------------------------------------------------------------------
        elif len(face.barycenter) == 3:

            # # find all geometric Nodes
            # geometricNodes = []
            # for e in face.geometricEdges:
            #     if e.startNode.isGeometrical:
            #         if e.startNode not in geometricNodes:
            #             geometricNodes.append(e.startNode)
            #     if e.endNode.isGeometrical:
            #         if e.endNode not in geometricNodes:
            #             geometricNodes.append(e.endNode)

            # if len(geometricNodes) == 1:
            #     coord = geometricNodes[0].coordinates
            #     self.xCoordinate = coord[0]
            #     self.yCoordinate = coord[1]
            #     self.zCoordinate = coord[2]

            if not len(face.geometricNodes) == 1:
                _log.error('Face {} '.format(face.infoText) +
                             'has three barycenters and should so have one ' +
                             'geometric node, but has {}'
                             .format(len(face.geometricNodes)))
        else:
            _log.error('Cannot calculate 2D dual of face {} '
                         .format(face.infoText) +
                         'that has more than one simple Face, ' +
                         'it has {}'.format(len(face.simpleFaces)))

        self.dualCell2D = face
        face.dualCell2D = self

        if volume:
            volume.dualCell3D = self
            self.dualCell3D = volume

        _log.debug('Initialized DualNode2D')

# =============================================================================
#    METHODS
# =============================================================================

# ------------------------------------------------------------------------
#    Plot for Documentation
# ------------------------------------------------------------------------

    @classmethod
    def plotDoc(cls):
        '''
        Create the plots used in documentation.

        '''
        import tools.tumcolor as tc
        import tools.placeFigures as pf

        from k_cells.edge import Edge
        from k_cells.face import Face

        # Create nodes for example 1
        n0 = Node(0, 0, 0)
        n1 = Node(1, 0, 0)
        n2 = Node(0, 1, 0)
        nodes0 = [n0, n1, n2]

        # Create nodes for example 2
        n3 = Node(0, 0, 1)
        n4 = Node(1, 0, 1)
        n5 = Node(1, 1, 2)
        n6 = Node(0, 1, 1)
        nodes1 = [n3, n4, n5, n6]

        # Create nodes for example 3
        n7 = Node(0, 0, 2)
        n8 = Node(1, 0, 2)
        n9 = Node(0, 1, 2)
        n10 = Node(0, 0, 3)
        nodes2 = [n7, n8, n9, n10]

        # Create nodes for example 3
        n11 = Node(0, 0, 4)
        n12 = Node(1, 0, 4)
        n13 = Node(0, 1, 4)
        nodes3 = [n11, n12, n13]

        # Create edges for example 1
        e0 = Edge(n0, n1)
        e1 = Edge(n1, n2)
        e2 = Edge(n2, n0)
        edges0 = [e0, e1, e2]

        # Create edges for example 2
        e3 = Edge(n3, n4)
        e4 = Edge(n4, n5)
        e5 = Edge(n5, n6)
        e6 = Edge(n6, n3)
        e7 = Edge(n4, n6)
        edges1 = [e3, e4, e5, e6, e7]

        # Create edges for example 3
        e8 = Edge(n7, n8)
        e9 = Edge(n8, n9)
        e10 = Edge(n9, n7)
        e11 = Edge(n8, n10)
        e12 = Edge(n10, n7)
        e13 = Edge(n10, n9)
        edges2 = [e8, e9, e10, e11, e12, e13]

        # Create edgesfor example 4
        e14 = Edge(n11, n12, category='additionalBorder')
        e15 = Edge(n12, n13, category='inner')
        e16 = Edge(n13, n11, category='inner')
        edges3 = [e14, e15, e16]

        # Create faces
        f0 = Face([e0, e1, e2])
        f1 = Face([[e3, e7, e6], [e5, -e7, e4]])
        f2 = Face([[e8, e9, e10], [-e8, -e12, -e11], [-e10, -e13, e12]])
        f3 = Face([e14, e15, e16])

        # Create dual nodes
        dn0 = DualNode2D(f0)
        dn1 = DualNode2D(f1)
        dn2 = DualNode2D(f2)
        dn3 = DualNode2D(f3)

        # Create figures
        (figs, ax) = pf.getFigures(2, 2)

        # Plot example 1: inner face
        for n in nodes0:
            n.plotNode(ax[0])
        for e in edges0:
            e.plotEdge(ax[0])
        f0.plotFace(ax[0])
        dn0.color = tc.TUMRose()
        dn0.plotNode(ax[0], size=150)

        # Plot example 2: border face with 1 geometric edge
        for n in nodes1:
            n.plotNode(ax[1])
        for e in edges1:
            e.plotEdge(ax[1])
        f1.plotFace(ax[1])
        dn1.color = tc.TUMRose()
        dn1.plotNode(ax[1], size=150)

        # Plot example 3: border face with 1 geometric node
        for n in nodes2:
            n.plotNode(ax[2])
        for e in edges2:
            e.plotEdge(ax[2])
        f2.plotFace(ax[2])
        dn2.color = tc.TUMRose()
        dn2.plotNode(ax[2], size=150)

        # Plot example 4: face with 1 additional Border edge
        for n in nodes3:
            n.plotNode(ax[3])
        for e in edges3:
            e.plotEdge(ax[3])
        f3.plotFace(ax[3])
        dn3.color = tc.TUMRose()
        dn3.plotNode(ax[3], size=150)

        # Create image files
        for i in range(4):
            pf.exportPNG(figs[i], filename='doc/_static/dualNode2D_'+str(i))


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':
    from k_cells.edge import Edge
    from k_cells.face import Face
    import tools.placeFigures as pf
    from tools import MyLogging
    import tools.tumcolor as tc

    set_logging_format(logging.DEBUG)

    n0 = Node(0, 0, 0)
    n1 = Node(1, 0, 0)
    n2 = Node(0, 1, 0)
    nodes0 = [n0, n1, n2]

    n3 = Node(0, 0, 1)
    n4 = Node(1, 0, 1)
    n5 = Node(1, 1, 2)
    n6 = Node(0, 1, 1)
    nodes1 = [n3, n4, n5, n6]

    n7 = Node(0, 0, 2)
    n8 = Node(1, 0, 2)
    n9 = Node(0, 1, 2)
    n10 = Node(0, 0, 3)
    nodes2 = [n7, n8, n9, n10]

    n11 = Node(0, 0, 4)
    n12 = Node(1, 0, 4)
    n13 = Node(0, 1, 4)
    nodes3 = [n11, n12, n13]

    e0 = Edge(n0, n1)
    e1 = Edge(n1, n2)
    e2 = Edge(n2, n0)
    edges0 = [e0, e1, e2]

    e3 = Edge(n3, n4)
    e4 = Edge(n4, n5)
    e5 = Edge(n5, n6)
    e6 = Edge(n6, n3)
    e7 = Edge(n4, n6)
    edges1 = [e3, e4, e5, e6, e7]

    e8 = Edge(n7, n8)
    e9 = Edge(n8, n9)
    e10 = Edge(n9, n7)
    e11 = Edge(n8, n10)
    e12 = Edge(n10, n7)
    e13 = Edge(n10, n9)
    edges2 = [e8, e9, e10, e11, e12, e13]

    e14 = Edge(n11, n12, category='additionalBorder')
    e15 = Edge(n12, n13, category='inner')
    e16 = Edge(n13, n11, category='inner')
    edges3 = [e14, e15, e16]

    f0 = Face([e0, e1, e2])
    f1 = Face([[e3, e7, e6], [e5, -e7, e4]])
    f2 = Face([[e8, e9, e10], [-e8, -e12, -e11], [-e10, -e13, e12]])
    f3 = Face([e14, e15, e16])

    dn0 = DualNode2D(f0)
    dn1 = DualNode2D(f1)
    dn2 = DualNode2D(f2)
    dn3 = DualNode2D(f3)

    (figs, ax) = pf.getFigures(2, 2)
    for n in nodes0:
        n.plotNode(ax[0])
    for e in edges0:
        e.plotEdge(ax[0])
    f0.plotFace(ax[0])
    dn0.color = tc.TUMRose()
    dn0.plotNode(ax[0], size=150)

    for n in nodes1:
        n.plotNode(ax[1])
    for e in edges1:
        e.plotEdge(ax[1])
    f1.plotFace(ax[1])
    dn1.color = tc.TUMRose()
    dn1.plotNode(ax[1], size=150)

    for n in nodes2:
        n.plotNode(ax[2])
    for e in edges2:
        e.plotEdge(ax[2])
    f2.plotFace(ax[2])
    dn2.color = tc.TUMRose()
    dn2.plotNode(ax[2], size=150)

    for n in nodes3:
        n.plotNode(ax[3])
    for e in edges3:
        e.plotEdge(ax[3])
    f3.plotFace(ax[3])
    dn3.color = tc.TUMRose()
    dn3.plotNode(ax[3], size=150)

    cc.printBlue()
    cc.printBlue('Example 1')
    cc.printBlue('-'*30)
    cc.printWhite('Dual:', dn0, '2D primal:', dn0.dualCell2D)

    cc.printBlue()
    cc.printBlue('Example 2')
    cc.printBlue('-'*30)
    cc.printWhite('Dual:', dn1, '2D primal:', dn1.dualCell2D)
    cc.printWhite('Dual:', dn1, '1D primal:', dn1.dualCell1D)

    cc.printBlue()
    cc.printBlue('Example 3')
    cc.printBlue('-'*30)
    cc.printWhite('Dual:', dn2, '2D primal:', dn2.dualCell2D)
    cc.printWhite('Dual:', dn2, '1D primal:', dn2.dualCell1D)
    cc.printWhite('Dual:', dn2, '0D primal:', dn2.dualCell0D)

    cc.printBlue()
    cc.printBlue('Example 4')
    cc.printBlue('-'*30)
    cc.printWhite('Dual:', dn3, '2D primal:', dn3.dualCell2D)
    cc.printWhite('Dual:', dn3, '1D primal:', dn3.dualCell1D)
