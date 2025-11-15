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
from pyCellFoamCore.tools.logging_formatter import set_logging_format

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
#    PLOTLY CLASS FOR FAST PLOTTING
# =============================================================================

class FacePlotly:
    def __init__(self, faces):
        self.faces = faces

    def plot_faces_plotly(self, fig=None, show_label=True, show_barycenter=True):

        # TODO: Instead of creating a new vertex for each triangle, reuse
        # vertices by creating one vertex per node and referencing them
        # multiple times.


        if fig is None:
            fig = go.Figure()

        # Prepare data for Plotly Mesh3d
        x_data = []
        y_data = []
        z_data = []
        i_data = []  # Triangle vertex indices
        j_data = []
        k_data = []
        triangle_colors = []


        barycenters_x = []
        barycenters_y = []
        barycenters_z = []
        barycenter_colors = []
        labels = []

        vertex_count = 0
        for face in self.faces:
            for sf in face.simpleFaces:
                if len(sf.simpleEdges) < 3:
                    _log.error("Simple face %s has less than 3 edges, which is invalid.", sf)
                elif len(sf.simpleEdges) == 3:
                    _log.debug("Simple face %s is a triangle.", sf)
                    x_data.extend([se.startNode.xCoordinate for se in sf.simpleEdges])
                    y_data.extend([se.startNode.yCoordinate for se in sf.simpleEdges])
                    z_data.extend([se.startNode.zCoordinate for se in sf.simpleEdges])
                    i_data.append(vertex_count)
                    j_data.append(vertex_count + 1)
                    k_data.append(vertex_count + 2)
                    vertex_count += 3
                    triangle_colors.append(sf.color.html)

                else:
                    _log.debug("Simple face %s has more than 3 edges, performing triangulation.", sf)
                    for se in sf.simpleEdges:
                        x_data.append(se.startNode.xCoordinate)
                        x_data.append(se.endNode.xCoordinate)
                        x_data.append(sf.barycenter[0])
                        y_data.append(se.startNode.yCoordinate)
                        y_data.append(se.endNode.yCoordinate)
                        y_data.append(sf.barycenter[1])
                        z_data.append(se.startNode.zCoordinate)
                        z_data.append(se.endNode.zCoordinate)
                        z_data.append(sf.barycenter[2])

                        i_data.append(vertex_count)
                        j_data.append(vertex_count + 1)
                        k_data.append(vertex_count + 2)
                        vertex_count += 3
                        triangle_colors.append(sf.color.html)

                barycenters_x.append(sf.barycenter[0])
                barycenters_y.append(sf.barycenter[1])
                barycenters_z.append(sf.barycenter[2])
                barycenter_colors.append(sf.color.html)
                labels.append(sf.label_text.replace("$", ""))


        fig.add_trace(go.Mesh3d(
            x=x_data,
            y=y_data,
            z=z_data,
            i=i_data,
            j=j_data,
            k=k_data,
            facecolor=triangle_colors,
            opacity=0.5,
            hoverinfo='skip',
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

        fig.update_layout(scene=dict(
            xaxis_title='X Axis',
            yaxis_title='Y Axis',
            zaxis_title='Z Axis'
        ))

        return fig



# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == "__main__":
    set_logging_format(logging.DEBUG)
    bf = BaseFace()
