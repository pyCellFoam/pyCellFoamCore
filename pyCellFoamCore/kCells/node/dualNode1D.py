# -*- coding: utf-8 -*-
# =============================================================================
# DUAL NODE 1D
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Jul  6 15:30:48 2018

'''
The location of the node that is dual to a primal edge depends on two tings:

    - Number of simple edges
    - Category of start and end node

Primal edges may consist of a maximum of 2 simple edges.


1 simple edge
--------------------------------------------------------------------------
If there is only one simple edge, there are three possibilities for the dual
node.

center
    New node at the center of the simple edge

start
    The 1D dual node of the edge is the same as the 0D dual node of the start
    node

end
    The 1D dual node of the edge is the same as the 0D dual node of the end
    node


The following combinations of start and end node may occure.

+------------------------+--------------+---------------+-------------------------+
|                        | start: inner | start: border | start: additional border|
+========================+==============+===============+=========================+
| end: inner             | center       | center        | start                   |
+------------------------+--------------+---------------+-------------------------+
| end: boder             | center       | center        | start                   |
+------------------------+--------------+---------------+-------------------------+
| end: additional border | end          | end           | center                  |
+------------------------+--------------+---------------+-------------------------+

.. image:: ../../../_static/dualNode1D_0.png
   :width: 400px
   :alt: 1D dual node in the center
   :align: center

.. image:: ../../../_static/dualNode1D_2.png
   :width: 400px
   :alt: 1D dual node at start or end node
   :align: center


2 simple edges
--------------------------------------------------------------------------
Two simple edges means that there is one geometric node that connects them. The
dual node is at this geometric node, meaning it is its 0D dual.

.. image:: ../../../_static/dualNode1D_1.png
   :width: 400px
   :alt: 1D dual node at geometric node
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
#    Local Libraries
# ------------------------------------------------------------------------


#    kCells
# -------------------------------------------------------------------
from kCells.node.node import Node
from kCells.cell import DualCell
from kCells.node.dualNode0D import DualNode0D

#    Tools
# -------------------------------------------------------------------

import tools.colorConsole as cc
import tools.placeFigures as pf


# =============================================================================
#    CLASS DEFINITION
# =============================================================================

class DualNode1D(Node, DualCell):
    '''


    '''

# =============================================================================
#    SLOTS
# =============================================================================
#    __slots__ = ()

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __new__(cls, edge, *args, **kwargs):
        '''
        Depending on the geometry of the primal edge, the dual node is either
        calculated as a 1D dual in this class or as a 0D dual of the geometric
        node in the DualNode0D class.

        '''

        if len(edge.simpleEdges) == 2:
            primalNode = edge.geometricNodes[0]
            # cc.printMagenta('2 Simple edges: returning 0D dual node at' +
            #                 ' geometric node')
            return DualNode0D(primalNode, *args, edge=edge, **kwargs)
        else:
            BStart = edge.startNode.category == 'additionalBorder'
            BEnd = edge.endNode.category == 'additionalBorder'
            if BStart ^ BEnd:
                # cc.printMagenta('One additonal border node, returning ' +
                #                 '0D dual node at B node')
                if BStart:
                    return DualNode0D(edge.startNode, edge=edge)
                if BEnd:
                    return DualNode0D(edge.endNode, edge=edge)

            else:
                return super(DualNode1D, cls).__new__(cls)

    def __init__(self,
                 edge,
                 *args,
                 myPrintDebug=None,
                 myPrintError=None,
                 face=None,
                 volume=None,
                 **kwargs):
        '''
        :param Edge edge: Primal edge to which a 1D dual is wanted to be
            calculated.
        :param myPrintDebug: alternate printing function to redirect debug
            messages.
        :param myPrintError: alternate printing function to redirect error
            messages.
        :param Face face: If this dual node is generated as a special case of
            a higher dimension, the duality is stored also in the face.
        :param Volume volume: If this dual node is generated as a special case
            of a higher dimension, the duality is stored also in the volume.


        '''

        if volume:
            num = volume.num
        elif face:
            num = face.num
        else:
            num = edge.num

        super().__init__(0, 0, 0,
                         *args,
                         num=num,
                         **kwargs)

        if volume:
            self.category1 = volume.category1
            self.category2 = volume.category2
        elif face:
            self.category1 = face.category1
            self.category2 = face.category2
        else:
            if edge.category1 == 'border' and len(edge.faces) == 1:
                self.category1 = 'additionalBorder'
                self.category2 = 'additionalBorder'
            else:
                self.category1 = edge.category1
                self.category2 = edge.category2

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

        if len(edge.barycenter) == 1:
            myPrintDebug('Calculating dual node of {}'.format(edge))
            bc = edge.barycenter[0]
            self.xCoordinate = bc[0]
            self.yCoordinate = bc[1]
            self.zCoordinate = bc[2]
            self.dualCell1D = edge
            edge.dualCell1D = self
            if face:
                face.dualCell2D = self
                self.dualCell2D = face
            if volume:
                volume.dualCell3D = self
                self.dualCell3D = volume
        else:
            myPrintError('Cannot calculate 1D dual of edge {}'
                         .format(edge.infoText) +
                         ' that has more than one simple edge, ' +
                         'it has {}'.format(len(edge.simpleEdges)))
            self.delete()

        myPrintDebug('Initialized DualNode1D')

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
        from kCells.edge import Edge

        # Create nodes
        n0 = Node(0, 0, 0, category='inner')
        n1 = Node(0, 1, 0, category='inner')
        n2 = Node(1, 1, 0, category='border')
        n3 = Node(1, 0, 1, category='border')
        n4 = Node(1, 0, 0, category='border')
        n5 = Node(2, 0, 0, category='inner')
        n6 = Node(2, 1, 0, category='additionalBorder')

        # Put nodes that will be plotted for each example together in lists
        nodes1 = [n0, n1]
        nodes2 = [n2, n3, n4]
        nodes3 = [n5, n6]

        # Create edges
        e0 = Edge(n0, n1)
        e1 = Edge(n2, n3, geometricNodes=n4)
        e2 = Edge(n5, n6)

        # Create dual nodes to edges defined before
        dn0 = DualNode1D(e0)
        dn1 = DualNode1D(e1)
        dn2 = DualNode1D(e2)

        # Create figures
        (figs, ax) = pf.getFigures(2, 2)

        # Plot example 1: inner edge
        for n in nodes1:
            n.plotNode(ax[0])
        e0.plotEdge(ax[0])
        dn0.color = tc.TUMRose()
        dn0.plotNode(ax[0], size=100)

        # Plot example 2: edge with a kink
        for n in nodes2:
            n.plotNode(ax[1])
        e1.plotEdge(ax[1])
        dn1.color = tc.TUMRose()
        dn1.plotNode(ax[1], size=100)

        # Plot example 3: edge with additional border node
        for n in nodes3:
            n.plotNode(ax[2])
        e2.plotEdge(ax[2])
        dn2.color = tc.TUMRose()
        dn2.plotNode(ax[2], size=100)

        # Create image files
        for i in range(3):
            pf.exportPNG(figs[i], filename='doc/_static/dualNode1D_'+str(i))


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == "__main__":
    import tools.tumcolor as tc

    from kCells.edge import Edge
    from tools import MyLogging
    with MyLogging('dualNode2D', False):

        cc.printBlue('Creating nodes')
        n0 = Node(0, 0, 0, category='inner')
        n1 = Node(0, 1, 0, category='inner')
        n2 = Node(1, 1, 0, category='border')
        n3 = Node(1, 0, 1, category='border')
        n4 = Node(1, 0, 0, category='border')
        n5 = Node(2, 0, 0, category='inner')
        n6 = Node(2, 1, 0, category='additionalBorder')

        nodes1 = [n0, n1]
        nodes2 = [n2, n3, n4]
        nodes3 = [n5, n6]

        cc.printBlue('Creating edges')
        e0 = Edge(n0, n1)
        e1 = Edge(n2, n3, geometricNodes=n4)
        e2 = Edge(n5, n6)
        edges = [e0, e1, e2]

        cc.printBlue('Creating dual nodes')
        dn0 = DualNode1D(e0)
        dn1 = DualNode1D(e1)
        dn2 = DualNode1D(e2)

        cc.printBlue()
        cc.printBlue('Example 1')
        cc.printBlue('-'*30)
        cc.printWhite('Dual:', dn0, '1D primal:', dn0.dualCell1D)

        cc.printBlue()
        cc.printBlue('Example 2')
        cc.printBlue('-'*30)
        cc.printWhite('Dual:', dn1, '1D primal:', dn1.dualCell1D)
        cc.printWhite('Dual:', dn1, '0D primal:', dn1.dualCell0D)

        cc.printBlue()
        cc.printBlue('Example 3')
        cc.printBlue('-'*30)
        cc.printWhite('Dual:', dn2, '1D primal:', dn2.dualCell1D)
        cc.printWhite('Dual:', dn2, '0D primal:', dn2.dualCell0D)

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
            for n in nodes1:
                n.plotNode(axes[0])
            e0.plotEdge(axes[0])
            dn0.color = tc.TUMRose()
            dn0.plotNode(axes[0], size=100)

            for n in nodes2:
                n.plotNode(axes[1])
            e1.plotEdge(axes[1])
            dn1.color = tc.TUMRose()
            dn1.plotNode(axes[1], size=100)

            for n in nodes3:
                n.plotNode(axes[2])
            e2.plotEdge(axes[2])
            dn2.color = tc.TUMRose()
            dn2.plotNode(axes[2], size=100)

#    VTK
# --------------------------------------------------------------------
        elif plottingMethod == 'VTK':
            cc.printBlue('Plot using VTK')
            cc.printRed('Not implemented')

#    TikZ
# --------------------------------------------------------------------
        elif plottingMethod == 'TikZ':
            cc.printBlue('Plot using TikZ')
            cc.printRed('Not implemented')

#    Animation
# --------------------------------------------------------------------
        elif plottingMethod == 'animation':
            cc.printBlue('Creating animation')
            cc.printRed('Not implemented')

#    Documentation
# --------------------------------------------------------------------
        elif plottingMethod == 'doc':
            cc.printBlue('Creating plots for documentation')
            DualNode1D.plotDoc()

#    Unknown
# --------------------------------------------------------------------
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))
