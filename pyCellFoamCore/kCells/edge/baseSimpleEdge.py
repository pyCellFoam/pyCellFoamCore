# -*- coding: utf-8 -*-
# =============================================================================
# BASE SIMPLE EDGE
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Aug 29 10:03:06 2018

'''

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
import numpy as np
import logging

# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------


#    kCells
# -------------------------------------------------------------------
from kCells.cell.baseSimpleCell import BaseSimpleCell
from kCells.node.node import Node


#    Complex & Grids
# -------------------------------------------------------------------


#    Tools
# -------------------------------------------------------------------
import tools.tumcolor as tc
from tools import Arrow3D
from tools import MyLogging
from tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)

# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class BaseSimpleEdge(BaseSimpleCell):
    '''

    '''

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self, *args, **kwargs):
        '''

        '''
        super().__init__(*args, **kwargs)
        _log.debug('Initialized BaseSimpleEdge')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getShowArrow(self):
        if self.belongsTo:
            return self.belongsTo.showArrow
        else:
            _log.warning('Simple Edge does not belong to a real cell, '
                                + 'using fixed standard value for showArrow')
            return True
    showArrow = property(__getShowArrow)
    '''
    Show or hide arrow in the plot. Information is taken from the edge that
    this simple edge belongs to.

    '''

    def __getLength(self):
        return np.linalg.norm(self.endNode.coordinates
                              - self.startNode.coordinates)
    length = property(__getLength)
    '''

    '''

# =============================================================================
#    METHODS
# =============================================================================

    def intersectWithBoundingBox(self, boundingBox):
        '''

        '''

        res = boundingBox.intersectLineWithBoundingBox(
            self.startNode.coordinates, self.endNode.coordinates)

        if res is not None:
            (_, coords) = res
            return Node(*coords)
        else:
            return None

# ------------------------------------------------------------------------
#    Plot edge using pyplot
# ------------------------------------------------------------------------

    def plotEdge(self,
                 ax,
                 *args,
                 showArrow=None,
                 showLabel=None,
                 color=None,
                 dx=0,
                 dy=0,
                 dz=0,
                 **kwargs):
        '''
        Plotting this simple edge in a given axes.

        :param Axes ax: A matplotlib.pyplot.axes object where the node will be
            plotted
        :param bool showArrow: Show or hide arrow in the plot
        :param bool showLabel: Show or hide label in the plot
        :param float dx: Distance of the label to the node in x-direction
        :param float dy: Distance of the label to the node in y-direction
        :param float dz: Distance of the label to the node in z-direction
        :param color: Plotting color if a color different from the one stored
            in the object is wanted.


        '''
        if showLabel is None:
            showLabel = self.showLabel
        if showArrow is None:
            showArrow = self.showArrow
        if color is None:
            color = self.color

        if not isinstance(color, tc.TUMcolor):
            _log.error('Cannot plot {} '.format(self) +
                              'with the wanted color {} '.format(color) +
                              '- it must be an instance of TUMcolor()')

        if self.isGeometrical:
            linestyle = '--'
            linewidth = 1
        else:
            linestyle = '-'
            linewidth = 1

        v1 = self.startNode.coordinates
        v2 = self.endNode.coordinates
        x = np.array([v1[0], v2[0]])
        y = np.array([v1[1], v2[1]])
        z = np.array([v1[2], v2[2]])
        ax.plot(x, y, z, color=color.html, ls=linestyle)

        # vector connection v1 and v2
        d = v2-v1

        # plot 3D arrow
        if showArrow:
            a = Arrow3D(v1+0.4*d,
                        v1+0.6*d,
                        mutation_scale=20,
                        lw=linewidth,
                        arrowstyle="-|>",
                        color=color.html,
                        ls=linestyle)
            ax.add_artist(a)

        # print Label
        if showLabel:
            ax.text(self.barycenter[0]+dx,
                    self.barycenter[1]+dy,
                    self.barycenter[2]+dz,
                    self.label_text,
                    color=color.html)

# ------------------------------------------------------------------------
#    Plot edge using VTK
# ------------------------------------------------------------------------
    def plotEdgeVtk(self,
                    myVtk,
                    showArrow=None,
                    showLabel=None,
                    arrowDiameter=1,
                    arrowLength=1,
                    color=None,
                    **kwargs):
        '''
        Plotting this edge into a given vtk window.

        :param myVtk: Instance of MyVtk class

        '''
        if showArrow is None:
            showArrow = self.showArrow

        if showLabel is None:
            showLabel = self.showLabel

        if color is None:
            color = self.color

        myVtk.addLine(self.startNode.coordinates,
                      self.endNode.coordinates,
                      lineWidth=4,
                      color=color.rgb01)

        if showLabel:
            myVtk.addTextAnnotationNumpy(self.barycenter, self.label_text)

        if showArrow:
            myVtk.addArrowCenterDirection(self.barycenter,
                                          self.directionVec,
                                          color=color.rgb01,
                                          length=arrowLength,
                                          diameter=arrowDiameter)

# ------------------------------------------------------------------------
#    Plot edge using TikZ
# ------------------------------------------------------------------------
    def plotEdgeTikZ(self,
                     tikzpicture,
                     showLabel=None,
                     color=None,
                     shortLabel=True,
                     showArrow=None,
                     **kwargs):
        '''

        '''
        lineOptions = []

        if showLabel is None:
            showLabel = self.showLabel
        if showArrow is None:
            showArrow = self.showArrow
        if color is None:
            color = self.color

        if self.grayInTikz:
            showLabel = False
            color = tc.TUMGrayMedium()
            showArrow = False

        if showArrow:
            lineOptions.append('->-')

        if self.isGeometrical:
            lineOptions.append('densely dashed')

        labelText = None
        if showLabel:
            if shortLabel:
                labelText = self.label_text_short
            else:
                labelText = self.label_text

        lineOptions.append(color.name)

        start = self.startNode.getTikZNode(tikzpicture)
        end = self.endNode.getTikZNode(tikzpicture)

        if not start:
            _log.info('{} has no tikZNode yet, '.format(self.startNode)
                             + 'adding it as a simple TikZCoordinate')
            self.startNode.plotNodeTikZ(tikzpicture, showInPlot=False)
            start = self.startNode.getTikZNode(tikzpicture)
        if not end:
            _log.info('{} has no tikZNode yet, '.format(self.endNode)
                             + 'adding it as a simple TikZCoordinate')
            self.endNode.plotNodeTikZ(tikzpicture, showInPlot=False)
            end = self.endNode.getTikZNode(tikzpicture)

        if not (start in tikzpicture.tikZNodes+tikzpicture.tikZCoordinates
                and end in tikzpicture.tikZNodes+tikzpicture.tikZCoordinates):
            _log.error('Must add nodes to tikZPicture '
                              + '"{}" first'.format(tikzpicture))
        else:
            tikzpicture.addTikZLine(start,
                                    end,
                                    lineOptions,
                                    intermediateText=labelText,
                                    intermediatePosition=self.tikZLabelPosition
                                    )


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':
    set_logging_format(logging.DEBUG)
    se1 = BaseSimpleEdge()
    print(se1.color)
    print(se1.color.rgb0255)
