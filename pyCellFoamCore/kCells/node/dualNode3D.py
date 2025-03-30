# -*- coding: utf-8 -*-
# =============================================================================
# DUAL NODE 3D
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Dec  7 14:16:21 2017

'''
The 3 dimensional dual of a volume is a node. The dual geometrical location of
the node depends on the category of the primal volume


Inner volume
--------------------------------------------------------------------------
For inner volumes, the dual node is at the barycentre of the volume.

.. image:: ../../../_static/dualNode3D_0.png
   :width: 400px
   :alt: 3D dual node for inner volume
   :align: center


Border volume
--------------------------------------------------------------------------
A border volume always has to include one additional border face. Depending on
how many simple faces the additional border face includes, it is determined,
whether the border volume is somewhere inside the border of the complete
domain, at the rim, or at a corner.


Border volume inside the border
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If the additional border face consists of one simple face, it is assumed, that
the volume lies inside. Therefor, the dual node is put in the barycenter of
the additional border face. This equates the 2D dual of of the additonal border
face. Note that this 2D dual is not needed in the complex, since duals of
additional border faces are not needed.

.. image:: ../../../_static/dualNode3D_1.png
   :width: 400px
   :alt: 3D dual of border volume with one additional border face
   :align: center

Border volume at the rim
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If the additional border face consists of two simple faces, it is assumed, that
the volume lies at the rim. Therefor, the dual node is put in the barycenter of
the edge that connects the two simple faces. This equates the 1D dual of of the
edge. Note that this 1D dual is not needed in the complex, since the edge
between two simple faces always has to be geometrical and therefor does not
occur in the complex itself.

.. image:: ../../../_static/dualNode3D_2.png
   :width: 400px
   :alt: alternate text
   :align: center

Border volume at the corner
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If the additional border face consists of three simple faces, it is assumed,
that the volume lies at the corner. Therefor, the dual node is put at the same
position as the node that connects the three simple faces. This equates the 0D
dual of of the node. Note that this 0D dual is not needed in the complex, since
the node connection three simple faces always has to be geometrical and
therefor does not occur in the complex itself.

.. image:: ../../../_static/dualNode3D_3.png
   :width: 400px
   :alt: alternate text
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
    os.chdir('../../../')


# ------------------------------------------------------------------------
#    Standard Libraries
# ------------------------------------------------------------------------

import numpy as np

# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------


#    kCells
# -------------------------------------------------------------------
from kCells.node.node import Node
from kCells.node.dualNode2D import DualNode2D
from kCells.node.dualNode1D import DualNode1D
from kCells.node.dualNode0D import DualNode0D
from kCells.cell import DualCell


#    Tools
# -------------------------------------------------------------------
import tools.colorConsole as cc


# =============================================================================
#    CLASS DEFINITION
# =============================================================================

class DualNode3D(Node, DualCell):
    '''

    '''

# =============================================================================
#    NEW
# =============================================================================

    def __new__(cls, volume, *args, **kwargs):
        '''
        Depending on the geometry of the primal volume, the dual node is either
        calculated as a 3D dual in this class or as a 2D, 1D or 0D dual in the
        according class.

        '''
        cc.printRed("Creating dual Node 3D")
        cc.printRed("Number of additional border faces: {}".format(len([f for f in volume.faces if f.category1 == 'additionalBorder'])))


        if volume.category1 == 'border' and \
            len([f for f in volume.faces
                 if f.category1 == 'additionalBorder']) == 1:
            additionalBorderFace = [f for f in volume.faces
                                    if f.category1 == 'additionalBorder'][0]
            cc.printRed("Additional border face: {}".format(additionalBorderFace))

            if len(additionalBorderFace.simpleFaces) == 1:
                return DualNode2D(additionalBorderFace.simpleFaces[0].
                                  belongsTo,
                                  volume=volume)
            elif len(additionalBorderFace.simpleFaces) == 2:
                edges1 = [se.belongsTo for se in
                          additionalBorderFace.simpleFaces[0].simpleEdges]
                edges2 = [se.belongsTo for se in
                          additionalBorderFace.simpleFaces[1].simpleEdges]
                rimEdge = None
                for e in edges1:
                    me = -e
                    if me in edges2:
                        if rimEdge is None:
                            if e.isReverse:
                                rimEdge = me
                            else:
                                rimEdge = e
                        else:
                            return super(DualNode3D, cls).__new__(cls)

                if rimEdge:
                    return DualNode1D(rimEdge, face=additionalBorderFace,
                                      volume=volume)
                else:
                    return super(DualNode3D, cls).__new__(cls)

            elif len(additionalBorderFace.simpleFaces) == 3:
                cc.printYellow("Found three additional border faces")
                geometricNode = None
                geometricNodes = additionalBorderFace.geometricNodes
                geometricEdges = additionalBorderFace.geometricEdges
                cc.printGreen("Number of geometric nodes: {}".format(len(geometricNodes)))
                cc.printGreen("Number of geometric edges: {}".format(len(geometricEdges)))
                if len(geometricNodes) == 1:
                    geometricNode = geometricNodes[0]

                else:
                    possibleNodes = []
                    for n in geometricNodes:
                        ok = True
                        for e in geometricEdges:
                            if not (e.startNode == n or e.endNode == n):
                                ok = False
                        if ok:
                            possibleNodes.append(n)
                    if len(possibleNodes) == 1:
                        geometricNode = possibleNodes[0]

                if geometricNode:
                    return DualNode0D(geometricNode,
                                      volume=volume,
                                      face=additionalBorderFace,
                                      edge=[e for e in geometricNode.edges
                                            if e.isGeometrical])
                else:
                    return super(DualNode3D, cls).__new__(cls)
            else:
                return super(DualNode3D, cls).__new__(cls)

        else:
            return super(DualNode3D, cls).__new__(cls)

# =============================================================================
#    INITIALIZATION
# =============================================================================

    def __init__(self,
                 volume,
                 *args,
                 myPrintDebug=None,
                 myPrintError=None,
                 **kwargs):
        '''
        :param Volume volume: Primal volume to which a 0D dual is wanted to be
            calculated
        :param myPrintDebug: alternate printing function to redirect debug
            messages.
        :param myPrintError: alternate printing function to redirect error
            messages.

        '''

        super().__init__(0, 0, 0,
                         *args,
                         num=volume.num,
                         **kwargs)

        additionalBorderFace = None

        if True:
            if myPrintDebug is None:
                myPrintDebug = self.logger.debug
            # myPrintInfo = self.logger.info
            myPrintWarning = self.logger.warning
            if myPrintError is None:
                myPrintError = self.logger.error
        else:
            self.logger.warning('Using prints instead of logger!')
            myPrintDebug = cc.printGreen
            # myPrintInfo = cc.printCyan
            myPrintWarning = cc.printYellow
            myPrintError = cc.printRed
# ------------------------------------------------------------------------
#    Inner volume
# ------------------------------------------------------------------------
        if volume.category1 == 'inner':
            x = volume.barycenter[0]
            y = volume.barycenter[1]
            z = volume.barycenter[2]


# ------------------------------------------------------------------------
#    Border volume
# ------------------------------------------------------------------------
        elif volume.category1 == 'border':

            additionalBorderFaces = [f for f in volume.faces
                                     if f.category1 == 'additionalBorder']

            if len(additionalBorderFaces) == 0:
                x = 0
                y = 0
                z = 0
                myPrintError('Border volume {} '.format(volume.infoText) +
                             'should have exactly one additional border face')

            elif len(additionalBorderFaces) == 1:
                myPrintDebug('Volume {} '.format(volume.infoText) +
                             'has the additional border face {}'
                             .format(additionalBorderFace.infoText) +
                             'with {} simple faces'
                             .format(len(additionalBorderFace.simpleFaces)))
                additionalBorderFace = additionalBorderFaces[0]

#    1 simple face --> border
# ------------------------------------------------------------------------
                if len(additionalBorderFace.simpleFaces) == 1:
                    myPrintDebug('Border face {} '
                                 .format(additionalBorderFace.infoText) +
                                 'has one simple face, putting dual node in ' +
                                 'the barycenter of the face')
                    bc = additionalBorderFace.barycenter[0]
                    x = bc[0]
                    y = bc[1]
                    z = bc[2]

#    2 simple faces --> rim
# ------------------------------------------------------------------------
                elif len(additionalBorderFace.simpleFaces) == 2:
                    myPrintDebug('Border face {} '
                                 .format(additionalBorderFace.infoText) +
                                 'has two simple faces, putting dual node ' +
                                 'in the barycenter of the connecting edge')
                    edges1 = [se.belongsTo for se in additionalBorderFace
                              .simpleFaces[0].simpleEdges]
                    edges2 = [se.belongsTo for se in additionalBorderFace
                              .simpleFaces[1].simpleEdges]
                    myPrintDebug(edges1, edges2)

                    rimEdge = None
                    for e in edges1:
                        me = -e
                        if me in edges2:
                            if rimEdge is None:
                                if e.isReverse:
                                    rimEdge = me
                                else:
                                    rimEdge = e
                            else:
                                myPrintError('Face {} '
                                             .format(additionalBorderFace
                                                     .infoText) +
                                             'has more than one connecting ' +
                                             'edge, this should not be!')
                    bc = rimEdge.barycenter[0]
                    x = bc[0]
                    y = bc[1]
                    z = bc[2]

#    3 simple faces --> corner
# ------------------------------------------------------------------------
                elif len(additionalBorderFace.simpleFaces) == 3:

                    geometricNode = None
                    myPrintDebug('Border face {} '
                                 .format(additionalBorderFace.infoText) +
                                 'has three simple faces, putting dual node ' +
                                 'in connecting corner')
                    geometricNodes = additionalBorderFace.geometricNodes
                    geometricEdges = additionalBorderFace.geometricEdges
                    myPrintDebug('Face {} '.format(additionalBorderFace) +
                                 'has {} '.format(len(geometricNodes)) +
                                 'additional border nodes and {} '
                                 .format(len(geometricEdges)) +
                                 'additional border edges')
                    if len(geometricNodes) == 1:
                        myPrintDebug('Only one geometric node, '
                                     'this must be the corner')
                        geometricNode = geometricNodes[0]

                    else:
                        possibleNodes = []
                        for n in geometricNodes:
                            ok = True
                            for e in geometricEdges:
                                if not (e.startNode == n or e.endNode == n):
                                    ok = False
                            if ok:
                                myPrintDebug('Geometric node {} '.format(n) +
                                             'connects to all geometric edges')
                                possibleNodes.append(n)
                        if len(possibleNodes) == 1:
                            geometricNode = possibleNodes[0]
                            myPrintDebug('Found geometric node for corner')
                        else:
                            myPrintError('Cannot find geometric node in the ' +
                                         'corner of volume {}'.format(volume))

                    if geometricNode:
                        x = geometricNode.xCoordinate
                        y = geometricNode.yCoordinate
                        z = geometricNode.zCoordinate
                    else:
                        x = 0
                        y = 0
                        z = 0
                        self.delete()

                else:
                    x = 0
                    y = 0
                    z = 0
                    self.delete()
                    myPrintError('Border face {} '
                                 .format(additionalBorderFace.infoText) +
                                 'must have one, two or three simple faces, ' +
                                 'but has {}'
                                 .format(len(
                                     additionalBorderFace.simpleFaces)))

            else:
                myPrintWarning('Border volume {} with more than one '.format(volume) +
                               'additional Border face')
                x = volume.barycenter[0]
                y = volume.barycenter[1]
                z = volume.barycenter[2]

        else:
            x = 0
            y = 0
            z = 0
            self.delete()
            self.logger.error('Unknown category {} of volume {}'
                              .format(volume.category1, volume.infoText))

        self.xCoordinate = x
        self.yCoordinate = y
        self.zCoordinate = z

        self.category1 = volume.category1
        self.category2 = volume.category2
        self.dualCell3D = volume
        volume.dualCell3D = self
        if additionalBorderFace is not None:
            additionalBorderFace.dualCell2D = self

        self.logger.debug('Initialized DualNode3D')

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
        from kCells.edge import Edge
        from kCells.face import Face
        from kCells.volume import Volume
        import tools.placeFigures as pf
        import tools.tumcolor as tc
# .....................................................................---
#    Inner volume
# .......................................................................-
        n100 = Node(0, 0, 0)
        n101 = Node(1, 0, 0)
        n102 = Node(0, 1, 0)
        n103 = Node(0, 0, 1)

        e100 = Edge(n100, n101, num=0)
        e101 = Edge(n100, n102, num=1)
        e102 = Edge(n100, n103, num=2)
        e103 = Edge(n101, n102, num=3)
        e104 = Edge(n101, n103, num=4)
        e105 = Edge(n102, n103, num=5)

        edges100 = [e100, e101, e102, e103, e104, e105]

        f100 = Face([e100, e103, -e101])
        f101 = Face([e101, e105, -e102])
        f102 = Face([e100, e104, -e102])
        f103 = Face([e103, e105, -e104])

        faces100 = [f100, f101, f102, f103]
        for f in faces100:
            f.category1 = 'inner'

        v100 = Volume([-f100, -f101, f102, f103], num=100)
        v100.category1 = 'inner'

        dn100 = DualNode3D(v100)

        (figs, ax) = pf.getFigures(3, 2)
        for e in edges100:
            e.plotEdge(ax[0])
        for f in faces100:

            f.showNormalVec = False
            f.plotFace(ax[0])

        dn100.color = tc.TUMRose()
        dn100.plotNode(ax[0], size=200)

# .......................................................................-
#    Border volume with one additional border face
# .......................................................................-

        n200 = Node(0, 0, 0, num=0)
        n201 = Node(1, 0, 0, num=1)
        n202 = Node(0, 1, 0, num=2)
        n203 = Node(0, 0, 1, num=3)

        e200 = Edge(n200, n201, num=0)
        e201 = Edge(n200, n202, num=1)
        e202 = Edge(n200, n203, num=2)
        e203 = Edge(n201, n202, num=3)
        e204 = Edge(n201, n203, num=4)
        e205 = Edge(n202, n203, num=5)

        edges200 = [e200, e201, e202, e203, e204, e205]

        f200 = Face([e200, e203, -e201], num=0)
        f201 = Face([e201, e205, -e202], num=1)
        f202 = Face([e200, e204, -e202], num=2)
        f203 = Face([e203, e205, -e204], num=3)

        faces200 = [f200, f201, f202, f203]

        f202.category1 = 'additionalBorder'
        for f in [f200, f201, f203]:
            f.category1 = 'inner'

        v200 = Volume([-f200, -f201, f202, f203], num=200)
        v200.category1 = 'border'
        dn200 = DualNode3D(v200)

        for e in edges200:
            e.plotEdge(ax[1])
        for f in faces200:
            f.showNormalVec = False
            f.plotFace(ax[1])

        dn200.color = tc.TUMRose()
        dn200.plotNode(ax[1], size=200)

# .......................................................................-
#    Border Volume with two additional border faces
# .......................................................................-

        n300 = Node(0, 0, 0, num=0)
        n301 = Node(1, 0, 0, num=1)
        n302 = Node(0, 1, 0, num=2)
        n303 = Node(0, 0, 1, num=3)

        e300 = Edge(n300, n301, num=0)
        e301 = Edge(n300, n302, num=1)
        e302 = Edge(n300, n303, num=2)
        e303 = Edge(n301, n302, num=3)
        e304 = Edge(n301, n303, num=4)
        e305 = Edge(n302, n303, num=5)

        edges300 = [e300, e301, e302, e303, e304, e305]

        f301 = Face([e301, e305, -e302], num=1)
        f302 = Face([[e300, e304, -e302], [e301, -e303, -e300]], num=300)
        f303 = Face([e303, e305, -e304], num=3)

        faces300 = [f301, f302, f303]

        f302.category1 = 'additionalBorder'
        for f in [f301, f303]:
            f.category1 = 'inner'

        v300 = Volume([-f301, f302, f303], num=1)
        v300.category1 = 'border'
        dn300 = DualNode3D(v300)

        for e in edges300:
            e.plotEdge(ax[2])
        for f in faces300:

            f.showNormalVec = False
            f.plotFace(ax[2])

        dn300.color = tc.TUMRose()
        dn300.plotNode(ax[2], size=200)

# .......................................................................-
#    Border Volume with three additional border faces
# .......................................................................-

        n400 = Node(0, 0, 0, num=0)
        n401 = Node(1, 0, 0, num=1)
        n402 = Node(0, 1, 0, num=2)
        n403 = Node(0, 0, 1, num=3)

        e400 = Edge(n400, n401, num=0)
        e401 = Edge(n400, n402, num=1)
        e402 = Edge(n400, n403, num=2)
        e403 = Edge(n401, n402, num=3)
        e404 = Edge(n401, n403, num=4)
        e405 = Edge(n402, n403, num=5)

        edges400 = [e400, e401, e402, e403, e404, e405]

        f402 = Face([[e400, e404, -e402], [e401, -e403, -e400],
                     [e402, -e405, -e401]], num=2)
        f403 = Face([e403, e405, -e404], num=3)

        faces400 = [f402, f403]

        f402.category1 = 'additionalBorder'
        f403.category1 = 'inner'
        v400 = Volume([f402, f403], num=400)
        v400.category1 = 'border'
        dn400 = DualNode3D(v400)

        for e in edges400:
            e.plotEdge(ax[3])
        for f in faces400:
            f.showNormalVec = False
            f.plotFace(ax[3])

        dn400.color = tc.TUMRose()
        dn400.plotNode(ax[3], size=200)

# ........................................................................
#    Export plots
# ........................................................................

        for i in range(4):
            pf.exportPNG(figs[i], 'doc/_static/dualNode3D_'+str(i))
#            pf.setAxesEqual(ax[i])
#            pf.setLabels(ax[i])
#            plt.figure(figs[i].number)
#            plt.savefig('doc/_static/dualNode3D_'+str(i)+'.png', dpi=300)


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == "__main__":
    from kCells.edge import Edge
    from kCells.face import Face
    from kCells.volume import Volume
    import tools.placeFigures as pf
    # import tools.colorConsole as cc
    # import matplotlib.pyplot as plt
    import tools.tumcolor as tc
    from tools import MyLogging

# ------------------------------------------------------------------------
#    Inner volume
# ------------------------------------------------------------------------
    with MyLogging('dualNode3D', False):

        n100 = Node(0, 0, 0)
        n101 = Node(2, 0, 0)
        n102 = Node(0, 2, 0)
        n103 = Node(0, 0, 2)
        nodes100 = [n100, n101, n102, n103]

        e100 = Edge(n100, n101, num=0)
        e101 = Edge(n100, n102, num=1)
        e102 = Edge(n100, n103, num=2)
        e103 = Edge(n101, n102, num=3)
        e104 = Edge(n101, n103, num=4)
        e105 = Edge(n102, n103, num=5)

        edges100 = [e100, e101, e102, e103, e104, e105]

        f100 = Face([e100, e103, -e101])
        f101 = Face([e101, e105, -e102])
        f102 = Face([e100, e104, -e102])
        f103 = Face([e103, e105, -e104])

        faces100 = [f100, f101, f102, f103]
        for f in faces100:
            f.useCategory = 1
            f.category1 = 'inner'

        v100 = Volume([-f100, -f101, f102, f103], num=1)
        v100.useCategory = 1
        v100.category1 = 'inner'

        dn100 = DualNode3D(v100)

# ------------------------------------------------------------------------
#    Border volume with one additional border face
# ------------------------------------------------------------------------

        n200 = Node(0, 0, 0, num=0)
        n201 = Node(2, 0, 0, num=1)
        n202 = Node(0, 2, 0, num=2)
        n203 = Node(0, 0, 2, num=3)
        nodes200 = [n200, n201, n202, n203]

        e200 = Edge(n200, n201, num=0)
        e201 = Edge(n200, n202, num=1)
        e202 = Edge(n200, n203, num=2)
        e203 = Edge(n201, n202, num=3)
        e204 = Edge(n201, n203, num=4)
        e205 = Edge(n202, n203, num=5)

        edges200 = [e200, e201, e202, e203, e204, e205]

        f200 = Face([e200, e203, -e201], num=0)
        f201 = Face([e201, e205, -e202], num=1)
        f202 = Face([e200, e204, -e202], num=2)
        f203 = Face([e203, e205, -e204], num=3)

        faces200 = [f200, f201, f202, f203]

        f202.useCategory = 1
        f202.category1 = 'additionalBorder'
        for f in [f200, f201, f203]:
            f.useCategory1 = 1
            f.category1 = 'inner'

        v200 = Volume([-f200, -f201, f202, f203], num=2)
        v200.useCategory = 1
        v200.category1 = 'border'
        dn200 = DualNode3D(v200)

# ------------------------------------------------------------------------
#    Border Volume with two additional border faces
# ------------------------------------------------------------------------

        n300 = Node(0, 0, 0, num=0)
        n301 = Node(2, 0, 0, num=1)
        n302 = Node(0, 2, 0, num=2)
        n303 = Node(0, 0, 2, num=3)
        nodes300 = [n300, n301, n302, n303]

        e300 = Edge(n300, n301, num=0)
        e301 = Edge(n300, n302, num=1)
        e302 = Edge(n300, n303, num=2)
        e303 = Edge(n301, n302, num=3)
        e304 = Edge(n301, n303, num=4)
        e305 = Edge(n302, n303, num=5)

        edges300 = [e300, e301, e302, e303, e304, e305]

        f301 = Face([e301, e305, -e302], num=1)
        f302 = Face([[e300, e304, -e302], [e301, -e303, -e300]], num=2)
        f303 = Face([e303, e305, -e304], num=3)

        faces300 = [f301, f302, f303]

        f302.useCategory = 1
        f302.category1 = 'additionalBorder'
        for f in [f301, f303]:
            f.useCategory = 1
            f.category1 = 'inner'

        v300 = Volume([-f301, f302, f303], num=3)
        v300.useCategory = 1
        v300.category1 = 'border'
        dn300 = DualNode3D(v300)

# ------------------------------------------------------------------------
#    Border Volume with three additional border faces
# ------------------------------------------------------------------------

        n400 = Node(0, 0, 0, num=0)
        n401 = Node(2, 0, 0, num=1)
        n402 = Node(0, 2, 0, num=2)
        n403 = Node(0, 0, 2, num=3)
        nodes400 = [n400, n401, n402, n403]

        e400 = Edge(n400, n401, num=0)
        e401 = Edge(n400, n402, num=1)
        e402 = Edge(n400, n403, num=2)
        e403 = Edge(n401, n402, num=3)
        e404 = Edge(n401, n403, num=4)
        e405 = Edge(n402, n403, num=5)

        edges400 = [e400, e401, e402, e403, e404, e405]

        f402 = Face([[e400, e404, -e402], [e401, -e403, -e400],
                     [e402, -e405, -e401]], num=2)
        f403 = Face([e403, e405, -e404], num=3)

        faces400 = [f402, f403]

        f402.category1 = 'additionalBorder'
        f403.category1 = 'inner'
        v400 = Volume([f402, f403], num=4)
        v400.category1 = 'border'
        dn400 = DualNode3D(v400)

# ------------------------------------------------------------------------
#    Border Volume with three additional border faces and more than one
#    additional border node
# ------------------------------------------------------------------------

        n500 = Node(0, 0, 0, num=0)
        n501 = Node(1, 0, 0, num=1)
        n502 = Node(1, 1, 0, num=2)
        n503 = Node(0, 1, 0, num=3)
        n504 = Node(0, 0, 1, num=4)
        n505 = Node(1, 0, 1, num=5)
        n506 = Node(1, 1, 1, num=6)
        n507 = Node(0, 1, 1, num=7)
        nodes500 = [n500, n501, n502, n503, n504, n505, n506, n507]

        e500 = Edge(n500, n501, num=0)
        e501 = Edge(n505, n502, num=1, geometricNodes=n501)
        e502 = Edge(n502, n507, num=2, geometricNodes=n503)
        e503 = Edge(n503, n500, num=3)
        e504 = Edge(n504, n505, num=4)
        e505 = Edge(n505, n506, num=5)
        e506 = Edge(n506, n507, num=6)
        e507 = Edge(n507, n504, num=7)
        e508 = Edge(n500, n504, num=8)
        e509 = Edge(n502, n506, num=9)
        edges500 = [e500, e501, e502, e503, e504, e505, e506, e507, e508, e509]

        f500 = Face([[e500, e501, e502, e503], [-e500, e508, e504, e501],
                     [-e503, e502, e507, -e508]], num=0,
                    category='additionalBorder')
        f501 = Face([e504, e505, e506, e507], num=1)
        f502 = Face([e501, e509, -e505], num=2)
        f503 = Face([-e502, e509, e506, ], num=3)
        faces500 = [f500, f501, f502, f503]

        v500 = Volume([-f500, f501, f502, -f503], num=500)
        v500.category1 = 'border'

        dn500 = DualNode3D(v500)

# ------------------------------------------------------------------------
#    Check dualities
# ------------------------------------------------------------------------

        cc.printBlue()
        cc.printBlue('Example 1')
        cc.printBlue('-'*30)
        cc.printWhite('Dual:', dn100,
                      '3D primal:', dn100.dualCell3D,
                      '3D dual:', dn100.dualCell3D.dualCell3D)

        cc.printBlue()
        cc.printBlue('Example 2')
        cc.printBlue('-'*30)
        try:
            cc.printWhite('Dual:', dn200,
                          '3D primal:', dn200.dualCell3D,
                          '3D dual:', dn200.dualCell3D.dualCell3D)
        except Exception as e:
            cc.printRed(e)
        try:
            cc.printWhite('Dual:', dn200,
                          '2D primal:', dn200.dualCell2D,
                          '2D dual:', dn200.dualCell2D.dualCell2D)
        except Exception as e:
            cc.printRed(e)

        cc.printBlue()
        cc.printBlue('Example 3')
        cc.printBlue('-'*30)
        try:
            cc.printWhite('Dual:', dn300,
                          '3D primal:', dn300.dualCell3D,
                          '3D dual:', dn300.dualCell3D.dualCell3D)
        except Exception as e:
            cc.printRed(e)
        try:
            cc.printWhite('Dual:', dn300,
                          '2D primal:', dn300.dualCell2D,
                          '2D dual:', dn300.dualCell2D.dualCell2D)
        except Exception as e:
            cc.printRed(e)
        try:
            cc.printWhite('Dual:', dn300,
                          '1D primal:', dn300.dualCell1D,
                          '1D dual:', dn300.dualCell1D.dualCell1D)
        except Exception as e:
            cc.printRed(e)

        cc.printBlue()
        cc.printBlue('Example 4')
        cc.printBlue('-'*30)
        try:
            cc.printWhite('Dual:', dn400,
                          '3D primal:', dn400.dualCell3D,
                          '3D dual:', dn400.dualCell3D.dualCell3D)
        except Exception as e:
            cc.printRed(e)
        try:
            cc.printWhite('Dual:', dn400, '2D primal:',
                          dn400.dualCell2D, '2D dual:',
                          dn400.dualCell2D.dualCell2D)
        except Exception as e:
            cc.printRed(e)
        try:
            cc.printWhite('Dual:', dn400,
                          '1D primal:', dn400.dualCell1D,
                          '1D dual:', [e.dualCell1D for e in dn400.dualCell1D])
        except Exception as e:
            cc.printRed(e)

        try:
            cc.printWhite('Dual:', dn400,
                          '0D primal:', dn400.dualCell0D,
                          '0D dual:', dn400.dualCell0D.dualCell0D)
        except Exception as e:
            cc.printRed(e)

        cc.printBlue()
        cc.printBlue('Example 5')
        cc.printBlue('-'*30)
        try:
            cc.printWhite('Dual:', dn500,
                          '3D primal:', dn500.dualCell3D,
                          '3D dual:', dn500.dualCell3D.dualCell3D)
        except Exception as e:
            cc.printRed(e)
        try:
            cc.printWhite('Dual:', dn500,
                          '2D primal:', dn500.dualCell2D,
                          '2D dual:', dn500.dualCell2D.dualCell2D)
        except Exception as e:
            cc.printRed(e)
        try:
            cc.printWhite('Dual:', dn500,
                          '1D primal:', dn500.dualCell1D,
                          '1D dual:', [e.dualCell1D for e in dn500.dualCell1D])
        except Exception as e:
            cc.printRed(e)

        try:
            cc.printWhite('Dual:', dn500,
                          '0D primal:', dn500.dualCell0D,
                          '0D dual:', dn500.dualCell0D.dualCell0D)
        except Exception as e:
            cc.printRed(e)

# ------------------------------------------------------------------------
#    Plotting
# ------------------------------------------------------------------------

        # Choose plotting method.
        # Possible choices: pyplot, VTK, TikZ, animation, doc, None
        plottingMethod = 'TikZ'


#    Disabled
# --------------------------------------------------------------------
        if plottingMethod is None or plottingMethod == 'None':
            cc.printBlue('Plotting disabled')

#    Pyplot
# --------------------------------------------------------------------
        elif plottingMethod == 'pyplot':
            cc.printBlue('Plot using pyplot')
            (figs, axes) = pf.getFigures()

            for e in edges100:
                e.plotEdge(axes[0])
            for f in faces100:

                f.showNormalVec = False
                f.plotFace(axes[0])

            dn100.color = tc.TUMRose()
            dn100.plotNode(axes[0], size=200)

            for e in edges200:
                e.plotEdge(axes[1])
            for f in faces200:
                f.showNormalVec = False
                f.plotFace(axes[1])

            dn200.color = tc.TUMRose()
            dn200.plotNode(axes[1], size=200)

            for e in edges300:
                e.plotEdge(axes[2])
            for f in faces300:

                f.showNormalVec = False
                f.plotFace(axes[2])

            dn300.color = tc.TUMRose()
            dn300.plotNode(axes[2], size=200)

            for e in edges400:
                e.plotEdge(axes[3])
            for f in faces400:
                f.showNormalVec = False
                f.plotFace(axes[3])

            dn400.color = tc.TUMRose()
            dn400.plotNode(axes[3], size=200)

            for n in nodes500:
                n.plotNode(axes[4])
            for e in edges500:
                e.plotEdge(axes[4])
            for f in faces500:
                f.plotFace(axes[4])

            dn500.color = tc.TUMRose()
            dn500.plotNode(axes[4], size=500)

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

            tikZPic100 = TikZPicture3D()
            origin = tikZPic100.addTikZCoordinate('origin',
                                                  np.array([0, 0, 0]))
            tikZPic100.addTikZCoSy3D(origin)
            for n in nodes100:
                n.plotNodeTikZ(tikZPic100, showLabel=False)
            for e in edges100:
                e.plotEdgeTikZ(tikZPic100, showLabel=False, showArrow=False)
            dn100.plotNodeTikZ(tikZPic100, size=4, color=tc.TUMRose())
            tikZPic100.writeLaTeXFile('latex', 'dualNode1',
                                      compileFile=True, openFile=True)

            tikZPic200 = TikZPicture3D()
            origin = tikZPic200.addTikZCoordinate('origin',
                                                  np.array([0, 0, 0]))
            tikZPic200.addTikZCoSy3D(origin)
            for n in nodes200:
                n.plotNodeTikZ(tikZPic200, showLabel=False)
            for e in edges200:
                e.plotEdgeTikZ(tikZPic200, showLabel=False, showArrow=False)
            dn200.plotNodeTikZ(tikZPic200, size=4, color=tc.TUMRose())
            tikZPic200.writeLaTeXFile('latex', 'dualNode2',
                                      compileFile=True, openFile=True)

            tikZPic300 = TikZPicture3D()
            origin = tikZPic300.addTikZCoordinate('origin',
                                                  np.array([0, 0, 0]))
            tikZPic300.addTikZCoSy3D(origin)
            for n in nodes300:
                n.plotNodeTikZ(tikZPic300, showLabel=False)
            for e in edges300:
                e.plotEdgeTikZ(tikZPic300, showLabel=False, showArrow=False)
            dn300.plotNodeTikZ(tikZPic300, size=4, color=tc.TUMRose())
            tikZPic300.writeLaTeXFile('latex', 'dualNode3',
                                      compileFile=True, openFile=True)

            tikZPic400 = TikZPicture3D()
            origin = tikZPic400.addTikZCoordinate('origin',
                                                  np.array([0, 0, 0]))
            tikZPic400.addTikZCoSy3D(origin)
            for n in nodes400:
                n.plotNodeTikZ(tikZPic400, showLabel=False)
            for e in edges400:
                e.plotEdgeTikZ(tikZPic400, showLabel=False, showArrow=False)
            dn400.plotNodeTikZ(tikZPic400, size=4, color=tc.TUMRose())
            tikZPic400.writeLaTeXFile('latex', 'dualNode4',
                                      compileFile=True, openFile=True)

#    Animation
# --------------------------------------------------------------------
        elif plottingMethod == 'animation':
            cc.printBlue('Creating animation')
            cc.printRed('Not implemented')

#    Documentation
# --------------------------------------------------------------------
        elif plottingMethod == 'doc':
            cc.printBlue('Creating plots for documentation')
            DualNode3D.plotDoc()

#    Unknown
# --------------------------------------------------------------------
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))
