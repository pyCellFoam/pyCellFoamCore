# -*- coding: utf-8 -*-
# =============================================================================
# BASE EDGE
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
# ------------------------------------------------------------------------
#    Standard Libraries
# ------------------------------------------------------------------------

import logging

# ------------------------------------------------------------------------
#    Third-Party Libraries
# ------------------------------------------------------------------------

import plotly.graph_objects as go

# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------

#    kCells
# -------------------------------------------------------------------
from pyCellFoamCore.k_cells.cell.base_cell import BaseCell

#    Tools
# -------------------------------------------------------------------

import pyCellFoamCore.tools.colorConsole as cc
from pyCellFoamCore.tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


# =============================================================================
#    CLASS DEFINITION
# =============================================================================

class BaseEdge(BaseCell):
    '''


    '''

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self, *args, **kwargs):
        '''


        '''

        super().__init__(*args, **kwargs)
        _log.debug('Initialized BaseEdge')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getBarycenter(self):
        return [se.barycenter for se in self.simpleEdges]

    barycenter = property(__getBarycenter)
    '''
    Returns a list of barycenters of all simple edges that the edge consists
    of.

    '''

    def __getDirectionVec(self):
        return [se.directionVec for se in self.simpleEdges]

    directionVec = property(__getDirectionVec)
    '''
    Returns a list of direction vectors of all simple edges that the edge
    consists of.

    '''

    def __getTopologicNodes(self): return [self.startNode, self.endNode]

    topologicNodes = property(__getTopologicNodes)
    '''

    '''

    def __getLength(self):
        lengths = []
        totalLenth = 0
        for se in self.simpleEdges:
            lengths.append(se.length)
            totalLenth += se.length
        return [lengths, totalLenth]
    length = property(__getLength)
    '''

    '''

# =============================================================================
#    METHODS
# =============================================================================

    def intersectWithBoundingBox(self, *args, **kwargs):
        '''

        '''
        nodes = []
        for se in self.simpleEdges:
            nodes.append(se.intersectWithBoundingBox(*args, **kwargs))
        return nodes

# ------------------------------------------------------------------------
#    Plotting
# ------------------------------------------------------------------------
    def plotEdge(self, *args, **kwargs):
        '''
        Plot all simple edges in a given pyplot axis

        :param ax: pyplot axis

        '''
        if self.showInPlot:

            if not self.simpleEdges:
                _log.warning('Edge {} '.format(self) +
                                    'has no simple edges, ' +
                                    'maybe it was deleted')
            for se in self.simpleEdges:
                se.plotEdge(*args, **kwargs)

        else:
            _log.warning('Plotting of edge {} is disabled'.format(self))

    def plotEdgeVtk(self, *args, **kwargs):
        '''
        Plot all simple edges in a given vtk window.

        :param myVtk: Instance of MyVtk class

        '''
        for se in self.simpleEdges:
            se.plotEdgeVtk(*args, **kwargs)

    def plotEdgeTikZ(self, *args, repeatLabel=True, **kwargs):
        '''

        '''
        if self.showInPlot:
            if repeatLabel:
                for se in self.simpleEdges:
                    se.plotEdgeTikZ(*args, **kwargs)
            else:
                self.simpleEdges[0].plotEdgeTikZ(*args, **kwargs)
                for se in self.simpleEdges[1:]:
                    se.plotEdgeTikZ(*args, showLabel=False, **kwargs)

#    def plotHeatFlow(self, ax, Q, Qmax, lmax):
#        for se in self.simpleEdges:
#            se.plotHeatFlow(ax, Q/len(self.simpleEdges), Qmax, lmax)

    def printEdge(self, printNodes=True):
        '''
        Prints information about the edge in the console including

        * Number
        * Start node and end node
        * Attached faces

        '''
        print('==========================================================')
        cc.printBlueBackground('   ', end='')
        print(' Edge ', self.info_text)
        print('==========================================================')
        print()
        print('Label:'+self.label_text)
        print()
        print('Defined by Node', self.startNode.num, 'and', self.endNode.num)
        print()
        if printNodes:
            print('Start Node:')
            print('-----------')
            self.startNode.printNode()
            print()
            print('End Node:')
            print('-----------')
            self.endNode.printNode()
            print()
        if len(self.faces) > 0:
            if len(self.faces) > 1:
                print('this edge belongs to', len(self.faces), 'Faces:')
            else:
                print('this edge belongs to', len(self.faces), 'Face:')
            print([f.num for f in self.faces])
        else:
            print('This Edge does not belong to a Face')
        print()
        print('==========================================================')
        print()
        print()
        print()

# =============================================================================
#    PLOTLY CLASS FOR FAST PLOTTING
# =============================================================================

class EdgePlotly:
    def __init__(self, edges):
        self.edges = edges

    def plot_edges_plotly(self, fig=None, show_label=True, show_barycenter=True, show_direction=True, cone_size=2):


        if fig is None:
            fig = go.Figure()

        lines_x = []
        lines_y = []
        lines_z = []
        lines_colors = []

        barycenters_x = []
        barycenters_y = []
        barycenters_z = []
        barycenter_colors = []
        cones_direction_x = []
        cones_direction_y = []
        cones_direction_z = []
        labels = []

        for edge in self.edges:
            for se in edge.simpleEdges:
                sn = se.startNode
                en = se.endNode
                lines_x.extend([sn.xCoordinate, en.xCoordinate, None])
                lines_y.extend([sn.yCoordinate, en.yCoordinate, None])
                lines_z.extend([sn.zCoordinate, en.zCoordinate, None])
                barycenters_x.append(se.barycenter[0])
                barycenters_y.append(se.barycenter[1])
                barycenters_z.append(se.barycenter[2])
                barycenter_colors.append(se.color.html)
                cones_direction_x.append(se.directionVec[0])
                cones_direction_y.append(se.directionVec[1])
                cones_direction_z.append(se.directionVec[2])
                labels.append(se.label_text.replace("$", ""))
                lines_colors.extend([se.color.html, se.color.html, "#000000"])

        cones = {}

        for (x, y, z, u, v, w, color) in zip(barycenters_x, barycenters_y, barycenters_z,
                                      cones_direction_x, cones_direction_y, cones_direction_z,
                                      barycenter_colors):
            if color in cones:
                cones[color]['x'].append(x)
                cones[color]['y'].append(y)
                cones[color]['z'].append(z)
                cones[color]['u'].append(u)
                cones[color]['v'].append(v)
                cones[color]['w'].append(w)
            else:
                cones[color] = {'x': [x], 'y': [y], 'z': [z], 'u': [u], 'v': [v], 'w': [w]}

        fig.add_trace(go.Scatter3d(
            x=lines_x,
            y=lines_y,
            z=lines_z,
            mode='lines',
            line=dict(color=lines_colors, width=2),
            hoverinfo='skip',
            showlegend=False,
        ))

        if show_barycenter or show_label:
            if show_barycenter and not show_label:
                mode = 'markers'
            elif not show_barycenter and show_label:
                mode = 'text'
            else:
                mode = 'markers+text'

            fig.add_trace(go.Scatter3d(
                x=barycenters_x,
                y=barycenters_y,
                z=barycenters_z,
                mode=mode,
                text=labels,
                textposition='top center',
                marker=dict(
                    size=4,
                    color=barycenter_colors,
                    symbol='circle'
                ),
                showlegend=False,
            ))

        if show_direction:
            for (color, cone) in cones.items():
                fig.add_trace(go.Cone(
                    x=cone['x'],
                    y=cone['y'],
                    z=cone['z'],
                    u=cone['u'],
                    v=cone['v'],
                    w=cone['w'],
                    sizemode="raw",
                    sizeref=cone_size,
                    anchor="tip",
                    showscale=False,
                    colorscale=[[0, color], [1, color]],
                    showlegend=False,
                ))

        fig.update_layout(scene=dict(
            xaxis_title='X Axis',
            yaxis_title='Y Axis',
            zaxis_title='Z Axis'
        ))

        return fig

# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':
    set_logging_format(logging.DEBUG)
    e1 = BaseEdge()
