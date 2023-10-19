# -*- coding: utf-8 -*-
# =============================================================================
# DUAL EDGE 3D
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Jul  6 13:23:04 2018

'''
In 3D, an edge is dual to a face. Additional border faces have no dual. For
inner and border faces, the dual edge is calculated as described in the
following.
The orientation of the dual edge is given by the normal vector of the primal
face.

Inner face
--------------------------------------------------------------------------

An inner face belongs to two volumes. The dual edge connects the dual nodes of
these two volumes.

.. image:: ../../../_static/dualEdge3D_1.png
   :width: 400px
   :alt: 3D dual edge of an inner face
   :align: center


Border face
--------------------------------------------------------------------------

A border face belongs to one volume. The dual edge connects the dual node of
this volume with the 2D dual node of the face itself.

.. image:: ../../../_static/dualEdge3D_0.png
   :width: 400px
   :alt: 3D dual edge of a border face
   :align: center


'''
# =============================================================================
#    IMPORTS
# =============================================================================
if __name__ == '__main__':
    import os
    os.chdir('../../')

from kCells.cell import DualCell
from kCells.edge.edge import Edge
from kCells.node import Node, DualNode3D, DualNode2D
import tools.colorConsole as cc
import numpy as np
from tools import MyLogging
import tools.placeFigures as pf


# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class DualEdge3D(Edge, DualCell):
    '''
    Create 3D dual edge of a primal face

    '''

# =============================================================================
#    SLOTS
# =============================================================================
#    __slots__ = ()

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self,
                 face,
                 *args,
                 myPrintDebug=None,
                 myPrintError=None,
                 **kwargs):
        '''

        :param Face face: Primal face

        '''

        n1 = Node(0, 0, 0)
        n2 = Node(1, 0, 0)
        super().__init__(n1, n2,
                         *args,
                         num=face.num,
                         **kwargs)

        if True:
            if myPrintDebug is None:
                myPrintDebug = self.logger.debug
            # myPrintInfo = self.logger.info
            # myPrintWarning = self.logger.warning
            if myPrintError is None:
                myPrintError = self.logger.error
        else:
            self.logger.warning('Using prints instead of logger!')
            myPrintDebug = cc.printGreen
            # myPrintInfo = cc.printCyan
            # myPrintWarning = cc.printYellow
            myPrintError = cc.printRed

        self.category1 = face.category1
        self.category2 = face.category2

        # If the primal volumes have no 3D duals yet, calculate them
        for v in face.volumes:
            if v.dualCell3D is None:
                myPrintDebug('Calculating dual node of {}'.format(v))
                DualNode3D(v)
        # If the primal face has no 2D dual yet, calculate it
        if face.dualCell2D is None:
            myPrintDebug('Calculating dual node of {}'.format(face))
            DualNode2D(face)
            myPrintDebug('Finished calculation of ' +
                         'dual node of {}'.format(face))

# ------------------------------------------------------------------------
#    Inner face
# ------------------------------------------------------------------------

        if face.category1 == 'inner':
            myPrintDebug('\nCreating dual edge for inner face {}'.format(face))

            # An inner face must belong to two volumes,
            # check this before going on
            if len(face.volumes) == 2:

                myPrintDebug('dualEdge3D: Set start node of {} '.format(self) +
                             'to node {} '.format(face.volumes[0].dualCell3D) +
                             'at {}'
                             .format(face.volumes[0].dualCell3D.coordinates))
                self.startNode = face.volumes[0].dualCell3D
                myPrintDebug('dualEdge3D: Set end node of {} '.format(self) +
                             'to node {} '.format(face.volumes[1].dualCell3D) +
                             'at {}'
                             .format(face.volumes[1].dualCell3D.coordinates))
                self.endNode = face.volumes[1].dualCell3D

                # The 2D dual node is set as intermediate point for
                # the 3D dual edge
                self.geometricNodes = face.dualCell2D

                # Setup edge to get direction vectors correct
                self.setUp()

                # If the direction vectors align, then the geometric node is
                # unneccesary and can be removed
                if np.linalg.norm(
                        self.directionVec[0] - self.directionVec[1]) < 1e-4:
                    myPrintDebug('dualEdge3D: Removing geometric node of {}'
                                 .format(self))
                    self.geometricNodes = []
                    self.setUp()

            else:
                myPrintError('Face {} is inner '.format(face.infoText) +
                             'and should therefor belong to two volumes, ' +
                             'but belongs to {}'.format(len(face.volumes)))

# ------------------------------------------------------------------------
#    Border face
# ------------------------------------------------------------------------

        elif face.category1 == 'border':
            myPrintDebug('Creating dual edge for border face {}'.format(face))
            if len(face.volumes) == 1:

                self.startNode = face.volumes[0].dualCell3D
                self.endNode = face.dualCell2D
                self.setUp()

            else:
                myPrintError('Face {} is border '.format(face.infoText) +
                             'and should therefor belong to one volume, ' +
                             'but belongs to {}'.format(len(face.volumes)))

        else:
            myPrintError('Unknown category {} of face {}'
                         .format(face.category, face.infoText))

        # If the edge was created in the wrong direction
        # (according to the prescribed direction of the primal face),
        # it needs to be swapped
        if np.inner(self.directionVec[0], face.normalVec[0]) < 0:
            myPrintDebug('Swapping edge {} '.format(self) +
                         'because it is in the wrong direction')
            self.swap()

        # Check direction
        if np.inner(self.directionVec[0], face.normalVec[0]) > 0:
            myPrintDebug('{}: direction ok'.format(self.infoText))
        else:
            myPrintError('{}: direction not ok'.format(self.infoText))

        self.dualCell3D = face
        face.dualCell3D = self

        # TODO: If the additional border edges share one face,
        # then they should become one edge.
        # Like this, the dual of the dual is unique again!!!
        if self.category1 == 'inner':
            for e in face.edges:
                if e.category1 == 'additionalBorder':
                    if e.isReverse:
                        e.dualCell2D = -self
                    else:
                        e.dualCell2D = self

                    # TODO change this!!!
                    self.logger.info('Setting {}'.format(self) +
                                     ' as dual of edge {}.'.format(e) +
                                     ' This should not be done here')

        myPrintDebug('Initialized DualEdge3D')

# =============================================================================
#    METHODS
# =============================================================================
# ------------------------------------------------------------------------
#    Plot for Documentation
# ------------------------------------------------------------------------
    @classmethod
    def plotDoc(cls):
        from kCells.face import Face
        from kCells.volume import Volume

        with MyLogging('dualEdge3D'):

            # Create nodes
            n0 = Node(0, 0, 0)
            n1 = Node(1, 0, 0)
            n2 = Node(0, 1, 0)
            n3 = Node(0, 0, 1)
            n4 = Node(0.5, 0.5, 1)

            # Create edges
            e0 = Edge(n0, n1)
            e1 = Edge(n0, n2)
            e2 = Edge(n0, n3)
            e3 = Edge(n1, n2)
            e4 = Edge(n1, n3)
            e5 = Edge(n2, n3)
            e6 = Edge(n1, n4)
            e7 = Edge(n2, n4)
            e8 = Edge(n3, n4)

            # Create faces
            f0 = Face([e0, e3, -e1])
            f1 = Face([e1, e5, -e2])
            f2 = Face([e0, e4, -e2])
            f3 = Face([e3, e5, -e4])
            f4 = Face([e4, e8, -e6])
            f5 = Face([e5, e8, -e7])
            f6 = Face([e3, e7, -e6])
            faces = [f0, f1, f2, f3, f4, f5, f6]
            for f in faces:
                if f == f3:
                    f.category = 'inner'
                else:
                    f.category = 'border'

            # Create volumes
            v1 = Volume([-f0, -f1, f2, f3])
            v2 = Volume([f6, f5, -f4, -f3])
            volumes = [v1, v2]
            for v in volumes:
                v.category = 'inner'

            # Create figures
            (figs, ax) = pf.getFigures(2, 1)

            # Calculate dual edges
            de0 = DualEdge3D(f0)
            de3 = DualEdge3D(f3)

            # Plot volumes
            for v in volumes:
                v.showLabel = False
                v.showBarycenter = False
                v.plotVolume(ax[0])
                v.plotVolume(ax[1])

            # Plot dual edges
            de0.plotEdge(ax[0])
            de3.plotEdge(ax[1])

            # Plot primal faces
            f0.plotFace(ax[0])
            f3.plotFace(ax[1])

            # Plot dual nodes
            for n in de0.topologicNodes:
                n.plotNode(ax[0])
            for n in de3.topologicNodes:
                n.plotNode(ax[1])

            # Rotate figure
            for a in ax:
                a.view_init(17, 142)

            # Export png files
            for (i, f) in enumerate(figs):
                pf.exportPNG(f, 'doc/_static/dualEdge3D_'+str(i))


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================
if __name__ == "__main__":
    from kCells.face import Face
    from kCells.volume import Volume

    with MyLogging('dualEdge3D'):

        a = 2
# ------------------------------------------------------------------------
#    Create some examples
# ------------------------------------------------------------------------

        n0 = Node(0, 0, 0)
        n1 = Node(a, 0, 0)
        n2 = Node(a, a, 0)
        n3 = Node(0, a, 0)
        n4 = Node(a, 2 * a, 0)
        n5 = Node(0, 2 * a, 0)
        n6 = Node(0, 0, a)
        n7 = Node(a, 0, a)
        n8 = Node(a, a, a)
        n9 = Node(0, a, a)
        n10 = Node(a, 2 * a, a)
        n11 = Node(0, 2 * a, a)

        nodes = [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11]

        e0 = Edge(n0, n1)
        e1 = Edge(n1, n2)
        e2 = Edge(n2, n3)
        e3 = Edge(n3, n0)
        e4 = Edge(n2, n4)
        e5 = Edge(n4, n5)
        e6 = Edge(n5, n3)

        e7 = Edge(n6, n7)
        e8 = Edge(n7, n8)
        e9 = Edge(n8, n9)
        e10 = Edge(n9, n6)
        e11 = Edge(n8, n10)
        e12 = Edge(n10, n11)
        e13 = Edge(n11, n9)

        e14 = Edge(n0, n6)
        e15 = Edge(n1, n7)
        e16 = Edge(n2, n8)
        e17 = Edge(n3, n9)
        e18 = Edge(n4, n10)
        e19 = Edge(n5, n11)

        edges = [e0, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13,
                 e14, e15, e16, e17, e18, e19]

        f0 = Face([e0, e1, e2, e3])
        f1 = Face([e4, e5, e6, -e2])
        f2 = Face([e7, e8, e9, e10])
        f3 = Face([e11, e12, e13, -e9])
        f4 = Face([e6, e17, -e13, -e19])
        f5 = Face([e3, e14, -e10, -e17])
        f6 = Face([-e4, e16, e11, -e18])
        f7 = Face([-e1, e15, e8, -e16])
        f8 = Face([e5, e19, -e12, -e18])
        f9 = Face([e2, e17, -e9, -e16])
        f10 = Face([-e0, e14, e7, -e15])

        faces = [f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]

        for f in faces:
            if f == f9:
                f.category1 = 'inner'
            elif f == f10:
                f.category1 = 'additionalBorder'
            else:
                f.category1 = 'border'

        # faces1 = [-f0, f2, f5, f9, -f7, -f10]
        v0 = Volume([-f1, f4, f3, -f6, f8, -f9])
        v1 = Volume([-f0, f2, f5, f9, -f7, -f10])

        v0.category1 = 'inner'
        v1.category1 = 'border'

        volumes = [v0, v1]

        de1 = DualEdge3D(f9)
        de2 = DualEdge3D(f8)
        dualEdges = [de1, de2]


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
            for n in nodes:
                n.plotNode(axes[0])
            for e in edges:
                e.plotEdge(axes[0])
                e.plotEdge(axes[1])
            for f in faces:
                f.plotFace(axes[1])
                f.plotFace(axes[2])
            for v in volumes:
                v.plotVolume(axes[3])
            for de in dualEdges:
                de.plotEdge(axes[3])

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
            from tools.tikZPicture.tikZPerspective import TikZPerspective
            perspective = TikZPerspective('bla',
                                          np.array([-0.9, 0.3]),
                                          np.array([-0.8, -0.4]),
                                          np.array([0, 1]))
            tikZPic1 = TikZPicture3D(perspective)
            for v in volumes:
                v.plotVolumeTikZ(tikZPic1)
            f9.plotFaceTikZ(tikZPic1)
            de1.plotEdgeTikZ(tikZPic1)
            tikZPic1.writeLaTeXFile('latex', 'dualEdge1',
                                    compileFile=True, openFile=True)

            tikZPic2 = TikZPicture3D(perspective)
            v0.plotVolumeTikZ(tikZPic2)
            f8.plotFaceTikZ(tikZPic2)
            de2.plotEdgeTikZ(tikZPic2)
            tikZPic2.writeLaTeXFile('latex', 'dualEdge2',
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

#    Unknown
# --------------------------------------------------------------------
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))

        if False:

            n0 = Node(0, 0, 0)
            n1 = Node(1, 0, 0)
            n2 = Node(0, 1, 0)
            n3 = Node(0, 0, 1)
            n4 = Node(0.5, 0.5, 1)
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

            f0 = Face([e0, e3, -e1])
            f1 = Face([e1, e5, -e2])
            f2 = Face([e0, e4, -e2])
            f3 = Face([e3, e5, -e4])
            f4 = Face([e4, e8, -e6])
            f5 = Face([e5, e8, -e7])
            f6 = Face([e3, e7, -e6])
            faces = [f0, f1, f2, f3, f4, f5, f6]
            for f in faces:
                if f == f3:
                    f.category = 'inner'
                else:
                    f.category = 'border'

            v1 = Volume([-f0, -f1, f2, f3])
            v2 = Volume([f6, f5, -f4, -f3])
            volumes = [v1, v2]
            for v in volumes:
                v.category = 'inner'

            (figs, ax) = pf.getFigures(2, 2)
            for e in edges:
                e.plotEdge(ax[0])
            for f in faces:
                f.plotFace(ax[0])

            for v in volumes:
                v.plotVolume(ax[1])

            de0 = DualEdge3D(f0, myPrintDebug=cc.printYellow)
            de3 = DualEdge3D(f3, myPrintDebug=cc.printYellow)

            for v in volumes:
                v.showLabel = False
                v.showBarycenter = False
                v.plotVolume(ax[2])
                v.plotVolume(ax[3])

            de0.plotEdge(ax[2])
            de3.plotEdge(ax[3])

            for n in de0.topologicNodes:
                n.plotNode(ax[2])

            for n in de3.topologicNodes:
                n.plotNode(ax[3])

            for a in ax:
                a.view_init(17, 142)

            if False:
                DualEdge3D.plotDoc()
