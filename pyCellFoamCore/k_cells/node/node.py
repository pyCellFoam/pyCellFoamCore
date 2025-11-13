# -*- coding: utf-8 -*-
# =============================================================================
# NODE
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Dec  7 09:02:56 2017

'''
Class for primal nodes

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
#    Third-Party Libraries
# ------------------------------------------------------------------------

import numpy as np


# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------

#    kCells
# -------------------------------------------------------------------
from k_cells.cell import Cell

#    Tools
# --------------------------------------------------------------------
from tools import MyLogging
import tools.tumcolor as tc
import tools.colorConsole as cc
import tools.placeFigures as pf
from tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)

# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class Node(Cell):
    '''
    A class to define nodes.

    '''
    nodeCount = 0

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self, x, y, z, *args, num=None, label='n', **kwargs):
        '''
        Defines the node by setting its coordinates.

        :param float x: x-coordinate of the node
        :param float y: y-coordinate of the node
        :param float z: z-coordinate of the node
        :param int num: number of the node
        :param str label: text the node is labelled with when plotted

        '''

        if num is None:
            num = Node.nodeCount
            Node.nodeCount += 1

        super().__init__(*args,
                         num=num,
                         label=label,
                         myReverse=False,
                         **kwargs)

        self.__coordinates = np.array([float(x), float(y), float(z)])
        self.color = tc.TUMOrange()
        self.__edges = []
        self.__simpleEdges = []
        self.__connectedNodes = []
        self.__sphere = None
        self.geometryChanged = False
        self.__projectedNode = None
        self.__projectionEdge = None
        self.__draw = True
        self.__onBoundingBoxSides = []
        self.__tikZNodes = {}
        _log.info('Created node {}'.format(self.info_text))
        _log.debug('Initialized Node')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getCoordinates(self): return self.__coordinates

    def __setCoordinates(self, c):
        self.__coordinates[0] = float(c[0])
        self.__coordinates[1] = float(c[1])
        self.__coordinates[2] = float(c[2])
        self.updateGeometry()

    coordinates = property(__getCoordinates, __setCoordinates)
    '''
    The x-, y- and z-coordinates of the node, in a numpy array.

    '''

    def __getXCoordinate(self): return self.__coordinates[0]

    def __setXCoordinate(self, x):
        self.__coordinates[0] = float(x)
        self.updateGeometry()

    xCoordinate = property(__getXCoordinate, __setXCoordinate)
    '''
    The x-coordinate of the node.

    '''

    def __getYCoordinate(self): return self.__coordinates[1]

    def __setYCoordinate(self, y):
        self.__coordinates[1] = float(y)
        self.updateGeometry()

    yCoordinate = property(__getYCoordinate, __setYCoordinate)
    '''
    The y-coordinate of the node.

    '''

    def __getZCoordinate(self): return self.__coordinates[2]

    def __setZCoordinate(self, z):
        self.__coordinates[2] = float(z)
        self.updateGeometry()

    zCoordinate = property(__getZCoordinate, __setZCoordinate)
    '''
    The z-coordinate of the node.

    '''

    def __getEdges(self): return self.__edges

    edges = property(__getEdges)
    '''
    All edges that this node is part of. It can be either the start node,
    the end node, or a geometric node.

    '''

    def __getSimpleEdges(self): return self.__simpleEdges

    simpleEdges = property(__getSimpleEdges)
    '''
    All simple edges that this node is part of. It can be either the start node
    or the end node.

    '''

    def __getConnectedNodes(self): return self.__connectedNodes

    connectedNodes = property(__getConnectedNodes)
    '''
    All neighbouring nodes that are connected to this node via an edge.

    '''

    # def __getSphere(self):
    #     if not self.__sphere:
    #         self.__sphere = Sphere(1, self.coordinates)
    #     return self.__sphere
    # sphere = property(__getSphere)
    # '''
    # Geometric object to handle the visualization.
    #
    # '''

    def __getRadius(self): return self.sphere.radius

    def __setRadius(self, r): self.sphere.radius = r

    radius = property(__getRadius, __setRadius)

    '''
    Radius of the node or respectively a sphere with the identical volume.

    '''

    def __getProjectedNode(self): return self.__projectedNode

    def __setProjectedNode(self, p): self.__projectedNode = p

    projectedNode = property(__getProjectedNode, __setProjectedNode)
    '''

    '''

    def __getOnBoundingBoxSides(self): return self.__onBoundingBoxSides

    def __setOnBoundingBoxSides(self, o): self.__onBoundingBoxSides = o

    onBoundingBoxSides = property(__getOnBoundingBoxSides,
                                  __setOnBoundingBoxSides)
    '''

    '''

    def __getProjectionEdge(self): return self.__projectionEdge

    def __setProjectionEdge(self, p): self.__projectionEdge = p

    projectionEdge = property(__getProjectionEdge, __setProjectionEdge)
    '''

    '''

    def __getTikZNodes(self): return self.__tikZNodes
    tikZNodes = property(__getTikZNodes)
    '''

    '''

# =============================================================================
#    METHODS
# =============================================================================

    def getTikZNode(self, tikZPicture):
        '''

        '''
        if tikZPicture in self.tikZNodes:
            return self.tikZNodes[tikZPicture]
        else:
            _log.info('This node does not belong to the' +
                             ' given tikzpicture')
            return None

    def __setTikZNode(self, tikZPicture, tikZNode):
        '''

        '''
        if tikZPicture in self.tikZNodes:
            _log.error('This node already belongs to the' +
                              ' given tikzpicture')
        else:
            self.tikZNodes[tikZPicture] = tikZNode

# ------------------------------------------------------------------------
#    Print node
# ------------------------------------------------------------------------

    def printNode(self):
        '''
        Prints information about the node in the console including

        * Number
        * Coordinates
        * Attached edges

        '''
        print('-------------------------------------------------------')
        cc.printRedBackground('   ', end='')
        print(' Node Number', self.num)
        print('-------------------------------------------------------')
        print()
        print('Coordinates:')
        print('-----------')
        print(self.coordinates)
        print()
        if len(self.__edges) > 0:
            if len(self.__edges) > 1:
                print('this Node belongs to', len(self.__edges), 'Edges:')
            else:
                print('this Node belongs to', len(self.__edges), 'Edge:')
            print([e.num for e in self.__edges])
        else:
            print('This Node does not belong to an Edge')
        print()
        print('-------------------------------------------------------')
        print()

# ------------------------------------------------------------------------
#    Plotting methods
# ------------------------------------------------------------------------

    def plotNode(self,
                 ax,
                 *args,
                 size=50,
                 showLabel=None,
                 dx=0,
                 dy=0,
                 dz=0,
                 color=None,
                 **kwargs):
        '''
        Plotting this node in a given axes.

        :param Axes ax: A matplotlib.pyplot.axes object where the node will be
                        plotted
        :param int size: size of the dot in the scatter plot
        :param bool showLabel: Show or hide label in the plot
        :param float dx: Distance of the label to the node in x-direction
        :param float dy: Distance of the label to the node in y-direction
        :param float dz: Distance of the label to the node in z-direction
        :param color: Plotting color if a color different from the one stored
            in the object is wanted.


        '''
        if self.showInPlot:
            if self.isDeleted:
                _log.error('Cannot plot deleted node {}'.format(self))
            else:
                if showLabel is None:
                    showLabel = self.showLabel

                if color is None:
                    plotColor = self.color.html
                else:
                    plotColor = color.html

                if self.isGeometrical:
                    ax.scatter(self.__coordinates[0],
                               self.__coordinates[1],
                               self.__coordinates[2],
                               c='w',
                               edgecolors=plotColor,
                               s=size)
                else:
                    ax.scatter(self.__coordinates[0],
                               self.__coordinates[1],
                               self.__coordinates[2],
                               c=plotColor,
                               s=size)
                if showLabel:
                    ax.text(self.__coordinates[0]+dx,
                            self.__coordinates[1]+dy,
                            self.__coordinates[2]+dz,
                            self.label_text,
                            color=plotColor)
        else:
            _log.warning('Plotting of node {} is disabled'.format(self))

    def plotNodeVtk(self, myVTK, showLabel=None, color=None, **kwargs):
        '''
        Plotting this node into a given vtk window.

        '''

        if showLabel is None:
            showLabel = self.showLabel

        if color is None:
            color = self.color.rgb0255

        if showLabel:
            myVTK.addScatterPoint(self.xCoordinate,
                                  self.yCoordinate,
                                  self.zCoordinate,
                                  self.label_text,
                                  color=color)
        else:
            myVTK.addScatterPoint(self.xCoordinate,
                                  self.yCoordinate,
                                  self.zCoordinate,
                                  color=color)

    def plotNodeTikZ(self,
                     tikZPic,
                     showLabel=None,
                     draw=None,
                     fill=None,
                     color=None,
                     showInPlot=None,
                     dim=3,
                     size=2,
                     **kwargs):
        '''

        '''

        nodeOptions = []
        labelOptions = []

        if color is None:
            color = self.color

        if self.grayInTikz:
            showLabel = False
            color = tc.TUMGrayMedium()

        if showLabel is None:
            showLabel = self.showLabel

        if showInPlot is None:
            showInPlot = self.showInPlot

        if draw is None:
            if self.isGeometrical:
                draw = False
            else:
                draw = self.showInPlot

        if fill is None:
            if self.category == 'additionalBorder' or self.isGeometrical:
                fill = False
            else:
                fill = True

        if draw:
            nodeOptions.append('circle')
            nodeOptions.append('inner sep=0pt')
            nodeOptions.append('minimum size={}mm'.format(size))
            nodeOptions.append('color={}'.format(color.name))
            if self.isGeometrical:
                nodeOptions.append('densely dashed')

            labelOptions.append('color={}'.format(color.name))

            if fill:
                nodeOptions.append('fill')
            else:
                nodeOptions.append('draw')

            if showLabel:
                if len(labelOptions) == 0:
                    labelOptionsText = ''
                else:
                    labelOptionsText = '[' + ', '.join(labelOptions) + ']'
                nodeOptions.append('label = {{{}{}: {}}}'
                                   .format(labelOptionsText,
                                           self.tikZLabelPosition,
                                           self.label_text))

        if dim == 2:
            coordinates = self.coordinates[:2]
        else:
            coordinates = self.coordinates

        if showInPlot:
            self.__setTikZNode(tikZPic,
                               tikZPic.addTikZNode(self.tikz_name,
                                                   coordinates,
                                                   options=nodeOptions))
        else:
            self.__setTikZNode(tikZPic,
                               tikZPic.addTikZCoordinate(self.tikz_name,
                                                         coordinates))

    def distToBoundingBox(self, boundingBox):
        '''
        Calculate the distances of a node from the border faces of a given
        bounding box.


        '''

        return boundingBox.distToBoundingBox(self.coordinates)

    def moveToBoundingBox(self, boundingBox, myPrintInfo=None):
        '''
        A function that moves a node onto the bounding box if the distance
        between node and bounding box is below a given threshold


        '''
        if myPrintInfo is None:
            myPrintInfo = _log.info

        (_, side) = boundingBox.distToBoundingBox(self.coordinates)
        projectedCoordinates = side.projectOnBoundingBoxSide(self.coordinates)

        self.coordinates = projectedCoordinates
        self.onBoundingBoxSides.append(side)

    def moveToBoundingBoxSide(self, side):
        '''

        '''

        projectedCoordinates = side.projectOnBoundingBoxSide(self.coordinates)
        self.coordinates = projectedCoordinates
        self.onBoundingBoxSides.append(side)

    def boundingBoxProjection(self, boundingBox, myPrintInfo=None):
        '''
        Returns another node that results by projecting this node onto the
        closest wall of a given bounding box.

        '''

        if myPrintInfo is None:
            myPrintInfo = _log.info

        if self.__projectedNode:
            myPrintInfo('Projection was calculated before')

        else:
            (_, side) = boundingBox.distToBoundingBox(self.coordinates)
            projectedCoordinates = side.projectOnBoundingBoxSide(
                self.coordinates)

            newNode = Node(projectedCoordinates[0],
                           projectedCoordinates[1],
                           projectedCoordinates[2])
            self.__projectedNode = newNode
            newNode.onBoundingBoxSides.append(side)

        return self.__projectedNode

#    def plotSphere(self, ax):
#        '''
#        Plotting a sphere that represents the volume attached to this node in
#        a given axes.
#
#        .. todo:: The radius is still fixed to 1, make this changeable
#
#        :param Axes ax: A matplotlib.pyplot.axes object where the sphere will
#                        be plotted
#        '''
#        self.sphere.plotSphere(ax)

# ------------------------------------------------------------------------
#    Edge management
# ------------------------------------------------------------------------

    def addSimpleEdge(self, simpleEdge):
        '''
        If a simple edge is generated by defining the start node and end node,
        also the nodes need to know that they belong to the edge.

        :param SimpleEdge simpleEdge: A simple edge or reversed simple edge
            where this node will be part of

        '''
        if simpleEdge in self.__simpleEdges:
            _log.error('Simple edge %s already belongs to node %s!',
                              simpleEdge.infoText, self.info_text)
        else:
            self.__simpleEdges.append(simpleEdge)

    def delSimpleEdge(self, simpleEdge):
        '''
        If a simple edge is deleted or the edge needs to be defined by another
        node, the node must know that it does not belong to the simple edge
        anymore.

        :param Edge edge: A simple edge or reversed simple edge where this node
            was part of

        '''
        if simpleEdge in self.__simpleEdges:
            self.__simpleEdges.remove(simpleEdge)
            _log.debug('Removed simple edge %s from node %s',
                             simpleEdge.infoText, self.info_text)
        else:
            _log.error('Cannot remove simple edge %s from node %s!',
                              simpleEdge.infoText, self.info_text)

    def addEdge(self, edge):
        '''
        If an edge is generated by defining the start node and end node, also
        the nodes need to know that they belong to the edge.

        The new edge connects this node to another node, this connection is
        saved as well.

        :param Edge edge: An edge or reversed edge where this node will be part
        of.


        '''
        if edge in self.__edges:
            _log.error('Edge %s already belongs to node %s!',
                              edge.infoText, self.info_text)
        else:
            self.__edges.append(edge)
            _log.debug('Added edge {} to node {}'
                             .format(edge.num, self.num))

            if not self.isGeometrical:
                if edge.startNode == self and edge.endNode == self:
                    _log.error('Start and end cannot be identical')
                elif edge.startNode == self:
                    self.__connectedNodes.append(edge.endNode)
                elif edge.endNode == self:
                    self.__connectedNodes.append(edge.startNode)
                elif self in edge.geometricNodes:
                    _log.error('Node {} should be geometric'
                                      .format(self.info_text))
                else:
                    _log.error('Cannot find connected node')

    def delEdge(self, edge):
        '''
        If an edge is deleted or the edge needs to be defined by another
        node, the node must know that it does not belong to the edge anymore.

        The edge used to connect this node to another node, this connection is
        deleted as well.

        :param Edge edge: An edge or reversed edge where this node was part of

        '''

        if edge in self.__edges:
            self.__edges.remove(edge)
            _log.debug('Removed edge {} from node {}'
                             .format(edge.num, self.num))

            if not self.isGeometrical:
                if edge.startNode == self and edge.endNode == self:
                    _log.error('Start and end cannot be identical')
                elif edge.startNode == self:
                    if edge.endNode in self.connectedNodes:
                        self.__connectedNodes.remove(edge.endNode)
                    else:
                        _log.error(
                            'Node {} should have been connected to node {}'
                            .format(edge.endNode.infoText, self.info_text))
                elif edge.endNode == self:
                    if edge.startNode in self.connectedNodes:
                        self.__connectedNodes.remove(edge.startNode)
                    else:
                        _log.error(
                            'Node {} should have been connected to node {}'
                            .format(edge.startNode.infoText, self.info_text))
                else:
                    _log.error('Cannot find connected node')
        else:
            _log.error('Cannot remove edge {} from node {}!'
                              .format(edge.infoText, self.info_text))

    def updateGeometry(self):
        '''
        Register the changed geometry in this node and in all connected edges.

        '''
        _log.debug('Updating node {}'.format(self))
        for e in self.__edges:
            e.updateGeometry()
        if self.__sphere:
            self.__sphere.update()

    @classmethod
    def plotDoc(cls):
        '''
        Create the plots used in documentation.

        '''

        # Create Node
        n101 = Node(0.1, 0.2, 0.3, num=1)

        # Create figure
        (figs, ax) = pf.getFigures(numTotal=1)

        # Plot node
        n101.plotNode(ax[0])

        # Add labels
        pf.setAxesEqual(ax[0])
        pf.setLabels(ax[0])

        # Create image files
        pf.exportPNG(figs[0], 'doc/_static/node1.png')


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================
if __name__ == '__main__':

    set_logging_format(logging.DEBUG)

    # Choose plotting method. Possible choices: pyplot, VTK, TikZ, None
    plottingMethod = 'pyplot'

    cc.printBlue('Create nodes')

    n0 = Node(0, 0, 0)
    n1 = Node(4, 5, 6, label=r'\hat{R}')
    n2 = Node(1, 2, 3)
    n3 = Node(2, 6, 3)
    n4 = Node(9, 5, 5)
    n5 = Node(8, 5, 1)

    nodes = [n0, n1, n2, n3, n4, n5]

    cc.printBlue('Change some parameters')
    n0.label = 'S'
    n1.yCoordinate = -2
    n2.coordinates = np.array([-1, -1, -3])
    n3.showLabel = False

    cc.printBlue('Create bounding box')
    # bb = BoundingBox([0, 10], [0, 10], [0, 10])

    if plottingMethod is None or plottingMethod == 'None':
        cc.printBlue('Plotting disabled')

    elif plottingMethod == 'pyplot':
        cc.printBlue('Plot using pyplot')
        (figs, axes) = pf.getFigures()
        for n in nodes:
            n.plotNode(axes[0])
        # bb.plotBoundingBox(axes[0])

    elif plottingMethod == 'VTK':
        cc.printBlue('Plot using VTK')
        # myVTK = MyVTK()
        # for n in nodes:
        #     n.plotNodeVtk(myVTK)
        # bb.plotBoundingBoxVtk(myVTK)
        # myVTK.start()
    elif plottingMethod == 'TikZ':
        cc.printBlue('Plot using TikZ')
        from tools.tikZPicture.tikZPicture3D import TikZPicture3D
        tikZPic = TikZPicture3D()
        origin = tikZPic.addTikZCoordinate('origin', np.array([0, 0, 0]))
        tikZPic.addTikZCoSy3D(origin)
        for n in nodes:
            n.plotNodeTikZ(tikZPic)
        # bb.plotBoundingBoxTikZ(tikZPic)
        tikZPic.writeLaTeXFile('latex', 'node',
                               compileFile=True, openFile=True)

    else:
        cc.printRed('Unknown plotting method {}'.format(plottingMethod))
