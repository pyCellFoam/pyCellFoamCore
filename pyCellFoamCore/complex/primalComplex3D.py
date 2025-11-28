# -*- coding: utf-8 -*-
# =============================================================================
# PRIMAL COMPLEX 3D
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Mar  1 13:55:43 2019

'''


'''


# =============================================================================
#    IMPORTS
# =============================================================================

# ------------------------------------------------------------------------
#    Standard Libraries
# ------------------------------------------------------------------------
from itertools import chain
import logging

# ------------------------------------------------------------------------
#    Third-Party Libraries
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------

#    k-Cells
# -------------------------------------------------------------------
from pyCellFoamCore.k_cells.node.node import Node
from pyCellFoamCore.k_cells.edge.edge import Edge
from pyCellFoamCore.k_cells.face.face import Face
from pyCellFoamCore.k_cells.volume.volume import Volume

from pyCellFoamCore.k_cells.node.node import NodePlotly
from pyCellFoamCore.k_cells.edge.baseEdge import EdgePlotly
from pyCellFoamCore.k_cells.face.baseFace import FacePlotly


#    Complex
# -------------------------------------------------------------------
from pyCellFoamCore.complex.complex3D import Complex3D


#    Tools
# -------------------------------------------------------------------
import pyCellFoamCore.tools.colorConsole as cc
import pyCellFoamCore.tools.placeFigures as pf
# import pyCellFoamCore.tools.tumcolor as tc
from pyCellFoamCore.tools.logging_formatter import set_logging_format
from pyCellFoamCore.tools.myVTK import MyVTK


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


# =============================================================================
#    CLASS DEFINITION
# =============================================================================
class PrimalComplex3D(Complex3D):
    """
    Class for 3D primal complexes.
    """

# =============================================================================
#    SLOTS
# =============================================================================
    __slots__ = (
        '__boundingBox',
        '__dualComplex',
        '__renumber',
        '__changedNumbering',
        '__useCategory',
        "__volumes_to_combine",
        "__faces_to_combine",
    )

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(
        self,
        *args,
        renumber=True,
        boundingBox=None,
        volumes_to_combine=[],
        faces_to_combine=[],
        **kwargs
    ):
        _log.info("Initialize PrimalComplex3D")

        self.__boundingBox = boundingBox
        self.__renumber = renumber
        self.__changedNumbering = True
        self.__useCategory = 1
        self.__dualComplex = None
        self.__volumes_to_combine = volumes_to_combine
        self.__faces_to_combine = faces_to_combine
        super().__init__(*args,**kwargs)






#==============================================================================
#    SETTER AND GETTER
#==============================================================================


    def __getDualComplex(self): return self.__dualComplex
    def __setDualComplex(self,d):
        if self.__dualComplex is None:
            self.__dualComplex = d
        else:
            _log.error('Dual complex is already set')
    dualComplex = property(__getDualComplex,__setDualComplex)
    '''

    '''

    def __getUseCategory(self): return self.__useCategory
    def __setUseCategory(self,u):
        if u in [1,2]:
            self.__useCategory = u
            for c in chain(self.nodes,self.edges,self.faces,self.volumes):
                c.useCategory = u
            self.updateComplex3D()

            if self.__dualComplex:
                for c in chain(self.__dualComplex.nodes,self.__dualComplex.edges,self.__dualComplex.faces,self.__dualComplex.volumes):
                    c.useCategory = u
                self.__dualComplex.updateComplex3D()
        else:
            _log.error('Cannot set useCategory of to {} - It must be either 1 or 2'.format(u))
    useCategory = property(__getUseCategory,__setUseCategory)
    '''


    '''



    def __getChangedNumbering(self): return self.__changedNumbering
    changedNumbering = property(__getChangedNumbering)
    '''

    '''


#==============================================================================
#    MAGIC METHODS
#==============================================================================
    def  __repr__(self):
        return 'PrimalComplex3D with {} nodes, {} edges, {} faces and {} volumes'.format(len(self.nodes),len(self.edges),len(self.faces),len(self.volumes))

#==============================================================================
#    METHODS
#==============================================================================




    def setUp(self):
        '''

        '''
        _log.info('Called "Set Up" in PrimalComplex3D class')
        self.__categorizePrimal()
        self.sortPrimal()
        self.__combineAdditionalBorderFaces()
        self.__categorizeDual()
        self.__split_edges()
        self.sortPrimal()
        self.sortDual()
        super().setUp()








#    def __checkNumbering(self,myList):
#        '''
#
#        '''
#        if self.__numberingChanged:
#            self.renumberAll()
#        return myList

    def renumber(self):
        '''

        '''


        if self.useCategory == 1:
            self.renumberList(self.innerNodes1)
            self.renumberList(self.borderNodes1)
            self.renumberList(self.additionalBorderNodes1)
            self.renumberList(self.innerEdges1)
            self.renumberList(self.borderEdges1)
            self.renumberList(self.additionalBorderEdges1)
            self.renumberList(self.innerFaces1)
            self.renumberList(self.borderFaces1)
            self.renumberList(self.additionalBorderFaces1)
            self.renumberList(self.innerVolumes1)
            self.renumberList(self.borderVolumes1)
        elif self.useCategory == 2:
            self.renumberList(self.innerNodes2)
            self.renumberList(self.borderNodes2)
            self.renumberList(self.additionalBorderNodes2)
            self.renumberList(self.innerEdges2)
            self.renumberList(self.borderEdges2)
            self.renumberList(self.additionalBorderEdges2)
            self.renumberList(self.innerFaces2)
            self.renumberList(self.borderFaces2)
            self.renumberList(self.additionalBorderFaces2)
            self.renumberList(self.innerVolumes2)
            self.renumberList(self.borderVolumes2)
        else:
            _log.error('Unknown useCategory {}'.format(self.useCategory))

        self.renumberList(self.geometricNodes)
        self.renumberList(self.geometricEdges)

        if self.dualComplex:
            self.renumberList(self.dualComplex.geometricNodes)
            self.renumberList(self.dualComplex.geometricEdges)

#        if self.__dualComplex:
#            self.__dualComplex.reOrderAll()

        self.__changedNumbering = False






#-------------------------------------------------------------------------
#    Combine additional border faces
#-------------------------------------------------------------------------

    def __combineAdditionalBorderFaces(self):
        '''

        '''



        _log.info('Combining additional border face')

        #    Manual combine volumes
        #....................................................................

        for (v1, v2) in self.__volumes_to_combine:
            _log.debug("Combine volumes {} and {}".format(v1, v2))

            shared_faces = set(v1.faces).intersection(set([-f for f in v2.faces]))
            _log.debug("Shard faces: {}".format(shared_faces))

            if len(shared_faces) == 1:
                shared_face = list(shared_faces)[0]
                new_faces = [f for f in v1.faces if not f == shared_face] + [f for f in v2.faces if (not (-f == shared_face) and not f in v1.faces)]
                _log.debug("New faces: {}".format(new_faces))
                new_volume = Volume(new_faces)
                new_volume.category1 = v1.category1
                new_volume.category2 = v1.category2
                # _log.warning("volumes: {}".format(self.volumes))

                for v in [v1, v2]:
                    if v in self.volumes:
                        self.volumes.remove(v)
                    else:
                        _log.error("{} should have been in volumes but is not".format(v))
                    if v in self.borderVolumes:
                        self.borderVolumes.remove(v)
                    else:
                        _log.error("{} should have been in border volumes but is not".format(v))

                self.volumes.append(new_volume)
                if new_volume.category1 == "border":
                    self.borderVolumes.append(new_volume)
                else:
                    _log.error("New volume {} should have been a border volume".format(new_volume))
                v1.delete()
                v2.delete()
                if shared_face in self.faces:
                    self.faces.remove(shared_face)
                elif -shared_face in self.faces:
                    self.faces.remove(-shared_face)
                else:
                    _log.error("Cannot remove face {} from faces".format(shared_face))

                if shared_face.category1 == "additionalBorder":
                    if shared_face in self.additionalBorderFaces1:
                        self.additionalBorderFaces1.remove(shared_face)
                    elif -shared_face in self.additionalBorderFaces1:
                        self.additionalBorderFaces1.remove(-shared_face)
                    else:
                        _log.error("Cannot remove face {} from additional border faces 1".format(shared_face))

                    if shared_face in self.additionalBorderFaces2:
                        self.additionalBorderFaces2.remove(shared_face)
                    elif -shared_face in self.additionalBorderFaces1:
                        self.additionalBorderFaces2.remove(-shared_face)
                    else:
                        _log.error("Cannot remove face {} from additional border faces 2".format(shared_face))

                elif shared_face.category1 == "inner":
                    if shared_face in self.innerFaces:
                        self.innerFaces.remove(shared_face)
                    elif -shared_face in self.innerFaces:
                        self.innerFaces.remove(-shared_face)
                    else:
                        _log.error("Cannot remove face {} from inner faces".format(shared_face))

                else:
                    _log.error("Category1 of {} is {}!".format(shared_face, shared_face.category1))





            else:
                _log.error("Cannot combine volumes with {} shared faces".format(len(shared_faces)))

        #    Manual combine faces
        #....................................................................

        for (f1, f2) in self.__faces_to_combine:
            _log.debug("Combine faces {} and {}".format(f1, f2))
            shared_edges = set(f1.edges).intersection(set([-e for e in f2.edges]+f2.edges))
            _log.debug("Edges of face 1: {}".format(f1.edges))
            _log.debug("Edges of face 2: {}".format(f2.edges))
            _log.debug("shared edges: {}".format(shared_edges))

            if len(shared_edges) == 1:
                shared_edge = list(shared_edges)[0]

                if shared_edge in f2.edges:
                    edges_1_1 = f1.edges[:f1.edges.index(shared_edge)]
                    edges_2_1 = [-e for e in f2.edges[:f2.edges.index(shared_edge)]]
                    edges_2_1.reverse()
                    edges_2_2 = [-e for e in f2.edges[f2.edges.index(shared_edge)+1:]]
                    edges_2_2.reverse()
                    edges_1_2 = f1.edges[f1.edges.index(shared_edge)+1:]

                elif -shared_edge in f2.edges:
                    edges_1_1 = f1.edges[:f1.edges.index(shared_edge)]
                    edges_2_1 = f2.edges[f2.edges.index(-shared_edge)+1:]
                    edges_2_2 = f2.edges[:f2.edges.index(-shared_edge)]
                    edges_1_2 = f1.edges[f1.edges.index(shared_edge)+1:]


                _log.debug("1_1: {} | 2_1: {} | 2_2: {} | 1_2: {}".format(edges_1_1, edges_2_1, edges_2_2, edges_1_2))
                new_edges = edges_1_1 + edges_2_1 + edges_2_2 + edges_1_2
                _log.debug("new edges: {}".format(new_edges))
                new_face = Face(new_edges)
                new_face.category1 = f1.category1
                new_face.category2 = f1.category2
                if shared_edge in self.edges:
                    self.edges.remove(shared_edge)
                elif -shared_edge in self.edges:
                    self.edges.remove(-shared_edge)
                else:
                    _log.error("Edge {} should be found in list of edges, but is not".format(shared_edge))

                self.faces.append(new_face)
                if new_face.category1 == "additionalBorder":
                    self.additionalBorderFaces.append(new_face)
                else:
                    _log.error("Should only combine additional border faces but new face is {}".format(new_face.category1))

                volumes = set(f1.volumes).intersection(set(f2.volumes), set(self.volumes))
                _log.warning("volumes of combined faces: {}".format(volumes))
                for v in list(volumes):
                    _log.warning("Old faces: {}".format(v.faces))
                    faces_for_new_volume = v.faces.copy()
                    if f1 in faces_for_new_volume:
                        faces_for_new_volume.remove(f1)
                    elif -f1 in faces_for_new_volume:
                        faces_for_new_volume.remove(-f1)
                    else:
                        _log.error("Cannot remove face {}".format(f1))
                    if f2 in faces_for_new_volume:
                        faces_for_new_volume.remove(f2)
                    elif -f2 in faces_for_new_volume:
                        faces_for_new_volume.remove(-f2)
                    else:
                        _log.error("Cannot remove face {}".format(f2))
                    faces_for_new_volume.append(new_face)
                    _log.warning("New faces: {}".format(faces_for_new_volume))
                    new_volume = Volume(faces_for_new_volume, unalignedFaces=True)
                    new_volume.category1 = v.category1
                    new_volume.category2 = v.category2
                    self.volumes.remove(v)
                    if v in self.innerVolumes:
                        self.innerVolumes.remove(v)
                    elif v in self.borderVolumes:
                        self.borderVolumes.remove(v)
                    else:
                        _log.error("{} is neither part of the inner nor of the border volumes".format(v))
                    self.volumes.append(new_volume)
                    if new_volume.category1 == "border":
                        self.borderVolumes.append(new_volume)
                    else:
                        _log.error("New volume {} should have been a border volume".format(new_volume))
                    v.delete()
                    for f in [f1, f2]:
                        if f in self.faces:
                            self.faces.remove(f)
                        else:
                            _log.error("Cannot remove {} from faces".format(f))

                        if f in self.additionalBorderFaces1:
                            self.additionalBorderFaces1.remove(f)
                        else:
                            _log.error("Cannot remove {} from additional border faces 1".format(f))

                        if f in self.additionalBorderFaces2:
                            self.additionalBorderFaces2.remove(f)
                        else:
                            _log.error("Cannot remove {} from additional border faces 2".format(f))
                f1.delete()
                f2.delete()



            else:
                _log.error("Cannot combine faces with {} shared edges".format(len(shared_edges)))












        #
        #    Check need for combine volumes
        #....................................................................

        if True:
            need_combination = False
            for v in self.volumes:
                _log.debug("Checking volume {}".format(v))
                if v.category1 == "border":
                    _log.debug("Checking faces of border volume")
                    additional_border_faces = [
                        f for f in v.faces if f.category1 == "additionalBorder"
                    ]

                    if len(additional_border_faces) == 0:
                        _log.error("Volume {} is of type border but has no additional border faces".format(v))
                    elif len(additional_border_faces) == 1:
                        _log.debug("Found one additional border face. No need to combine volumes")
                    elif len(additional_border_faces) == 2:
                        _log.debug("Found two additional border faces. Checking if the rim is included")
                    elif len(additional_border_faces) == 3:
                        _log.debug("Found three additional border faces. Checking if the corner is included")
                        all_nodes = []
                        for f in additional_border_faces:
                            temp_nodes = []
                            for e in f.edges:
                                for n in [e.startNode, e.endNode]:
                                    if not n in temp_nodes:
                                        temp_nodes.append(n)
                            all_nodes.append(temp_nodes)
                        _log.debug("Found nodes: {}".format(all_nodes))
                        shared_nodes = set(all_nodes[0]).intersection(*[set(nodes) for nodes in all_nodes[1:]])
                        _log.debug("Shared nodes: {}".format(shared_nodes))

                        if len(shared_nodes) == 0:
                            _log.error("Found no shared nodes. Need to combine volume {}".format(v))
                            need_combination = True
                        elif len(shared_nodes) == 1:
                            _log.debug("One shared node. Everything OK")
                        else:
                            _log.error("{} shared nodes cannot be handled".format(len(shared_nodes)))
                            need_combination = True




                    else:
                        _log.error("Volume {} has {} additional border faces. This cannot be handled currently".format(v, len(additional_border_faces)))

                    # TODO
                    # Check that all additional border faces are connected and
                    # have no holes. Otherwise find the volume that this volume
                    # must be merged with
                    # Note: 3 faces must share a node, 2 faces must share an
                    # edge
                elif v.category1 == "inner":
                    _log.debug("Inner volumes do not need to be checked")
                else:
                    _log.error("Unknown category {}".format(v.category1))
            if need_combination:
                return




        #    Combine faces
        #....................................................................
        if True:
            for v in self.volumes:
                _log.debug('Combining additional border faces of volume {}'.format(v.info_text))
                facesToCombine = []
                facesToStay = []
                for f in v.faces:

                    if f.category == 'additionalBorder' and v.category != 'border':
                        _log.error('Face {} is an additional border face and belongs to volume {} of category {}. This should not be!'.format(f.info_text,self.info_text,self.category))

                    if f.category == 'additionalBorder' and v.category == 'border':
                        facesToCombine.append(f)
                    else:
                        facesToStay.append(f)
                if len(facesToCombine) == 0:
                    _log.debug('Volume {} has no faces to combine'.format(v.info_text))
                elif len(facesToCombine) == 1:
                    _log.debug('Volume {} has only one additional border face, so no need to combine'.format(v.info_text))
                elif len(facesToCombine) <= 3:

                    # Check if each face shares at least one edge with another face
                    edgesOfFaces = []
                    for f in facesToCombine:
                        edgesOfFaces.append(f.edges)

                    _log.debug('Edges of the faces that should be combined: {}'.format(edgesOfFaces))

                    anyFaceSeparated = False
                    for edges in edgesOfFaces:
                        thisFaceSeparated = True
                        edgesOfOtherFaces = edgesOfFaces
                        edgesOfOtherFaces.remove(edges)
                        for e in edges:
                            for otherEdges in edgesOfOtherFaces:
                                if e in otherEdges or -e in otherEdges:
                                    thisFaceSeparated = False
                        if thisFaceSeparated:
                            anyFaceSeparated = True


                    if anyFaceSeparated:
                        _log.info('Faces {} of volume {} are all additional border face but are not connected'.format(facesToCombine,v))
                    else:

                        _log.debug('Volume {} has {} additional border faces: {}, trying to combine them'.format(v.info_text,len(facesToCombine),facesToCombine))
                        edgesOfFace = []
                        for f in facesToCombine:
                            for sf in f.simpleFaces:
                                edgesOfFace.append([se.belongs_to for se in sf.simpleEdges])
                        _log.debug('Creating new face with the edges {}'.format(edgesOfFace))
                        newFace = Face(edgesOfFace)
                        newFace.category1 = 'additionalBorder'
                        _log.debug('Changing the faces of volume {} by keeping the faces {} and adding the new face {}'.format(v.info_text,facesToStay,newFace))
                        v.faces = [*facesToStay,newFace]  # TODO better: v.faces = faces.ToStay.append(newFace)
                        v.setUp()
                        for f in facesToCombine:
                            if f.is_reverse:
                                f = -f
                            if f in self.faces:
                                self.faces.remove(f)
                            else:
                                _log.error('Cannot remove face {} from faces!'.format(f.info_text))
                            if f in self.additionalBorderFaces1:
                                self.additionalBorderFaces1.remove(f)
                            else:
                                _log.error('Cannot remove face {} from additional border faces 1!'.format(f.info_text))
                            if f in self.additionalBorderFaces2:
                                self.additionalBorderFaces2.remove(f)
                            else:
                                _log.error('Cannot remove face {} from additional border faces 2!'.format(f.info_text))
                            f.delete()

                        self.faces.append(newFace)
                        self.additionalBorderFaces1.append(newFace)
                        self.additionalBorderFaces2.append(newFace)

                        for e in newFace.geometricEdges:
                            _log.debug('Edge {} is getting eliminated'.format(e.info_text))
                            if e in self.edges:
                                self.edges.remove(e)
                            else:
                                _log.error('Cannot remove edge {} from edges!'.format(e.info_text))
                            if e in self.additionalBorderEdges1:
                                self.additionalBorderEdges1.remove(e)
                                self.geometricEdges.append(e)
                            else:
                                _log.error('Cannot remove edge {} from additional border edges!'.format(e.info_text))

                else:
                    _log.error('Volume {} has {} additional border faces, this is too much!'.format(v,len(facesToCombine)))



        #    Combine edges
        #....................................................................
        if True:
            for f in self.faces:
                if len(f.volumes) == 2:
                    if f.volumes[0].category == 'border' and f.volumes[1].category == 'border' :
                        _log.debug('Found face {} between two border volumes {}'.format(f,f.volumes))
                        edgesToCombine = []
                        for e in f.edges:
                            if e.category == 'additionalBorder':
                                edgesToCombine.append(e)
                        _log.debug('Found additional border edges {}'.format(edgesToCombine))
                        lenEdgesToCombine = len(edgesToCombine)
                        if lenEdgesToCombine == 0:
                            _log.debug('Border volumes have no common aditional border edge')
#                            _log.error('Two border volumes ({}) should at least have one additionalBorderEdge in common'.format(f.volumes))
                        elif lenEdgesToCombine == 1:
                            _log.debug('Everything is fine, no need to combine')
                        elif lenEdgesToCombine == 2:
                            e0 = edgesToCombine[0]
                            e1 = edgesToCombine[1]
                            _log.debug('Trying to combine additional border edges {}'.format(edgesToCombine))

                            # TODO
                            #
                            _log.debug('Faces of edge {}: {}'.format(e0,e0.faces))
                            _log.debug('Faces of edge {}: {}'.format(e1,e1.faces))


                            newEdge = False


                            #
                            #      .      - . -O
                            #     /            |
                            #   .              | e_1
                            #  /     e_o       |
                            # O----------------O
                            # Start/end

                            if e0.endNode == e1.startNode:
                                _log.debug('Can combine them')
                                middleNode = e0.endNode
                                newEdge = Edge(e0.startNode,e1.endNode,geometricNodes = [middleNode])



                            #
                            #      .      - . -O
                            #     /            |
                            #   .              | e_0
                            #  /     e_1       |
                            # O----------------O
                            #                  Start/end

                            elif e1.endNode == e0.startNode:
                                _log.debug('Can combine them after rotation')
                                middleNode = e1.endNode
                                newEdge = Edge(e1.startNode,e0.endNode,geometricNodes = [middleNode])

                            else:
                                _log.debug('Additional border Edges {} and {} are not connected and therefor cannot be combined'.format(e0,e1))
#                                self.errorCells.append(e0)
#                                self.errorCells.append(e1)

                            if newEdge:
#                                newEdge.useCategory = self.__useCategory
                                newEdge.category1 = 'additionalBorder'
                                _log.debug('New edge: {}'.format(newEdge))

                                currentFaces = e0.faces[:]
                                for f in e1.faces:
                                    if not f in currentFaces:
                                        currentFaces.append(f)
                                for f in currentFaces:
                                    allEdges = f.rawEdges[:]
                                    _log.debug('Old edges in {}: {}'.format(f,f.rawEdges))
                                    for localEdges in allEdges:

                                        # Add new edge (only once)
                                        if e0 in localEdges:
                                            localEdges.insert(localEdges.index(e0),newEdge)
                                        elif e1 in localEdges:
                                            localEdges.insert(localEdges.index(e1),newEdge)

                                        # Remove old edges (maybe both)
                                        if e0 in localEdges:
                                            localEdges.remove(e0)
                                        if e1 in localEdges:
                                            localEdges.remove(e1)

                                    _log.debug('newEdges: {}'.format(allEdges))
                                    f.edges=allEdges
                                    f.setUp()
                                if e0.is_reverse:
                                    if -e0 in self.additionalBorderEdges1:
                                        self.additionalBorderEdges1.remove(-e0)
                                    else:
                                        _log.error('Edge {} should have been in additional border edges but was not there'.format(-e0))
                                    if -e0 in self.edges:
                                        self.edges.remove(-e0)
                                    else:
                                        _log.error('Edge {} should have been in edges but was not there'.format(-e0))
                                else:
                                    if e0 in self.additionalBorderEdges1:
                                        self.additionalBorderEdges1.remove(e0)
                                    else:
                                        _log.error('Edge {} should have been in additional border edges but was not there'.format(e0))
                                    if e0 in self.edges:
                                        self.edges.remove(e0)
                                    else:
                                        _log.error('Edge {} should have been in edges but was not there'.format(e0))
                                if e1.is_reverse:
                                    if -e1 in self.additionalBorderEdges1:
                                        self.additionalBorderEdges1.remove(-e1)
                                    else:
                                        _log.error('Edge {} should have been in additional border edges but was not there'.format(-e1))
                                    if -e1 in self.edges:
                                        self.edges.remove(-e1)
                                    else:
                                        _log.error('Edge {} should have been in edges but was not there'.format(-e1))
                                else:
                                    if e1 in self.additionalBorderEdges1:
                                        self.additionalBorderEdges1.remove(e1)
                                    else:
                                        _log.error('Edge {} should have been in additional border edges but was not there'.format(e1))
                                    if e1 in self.edges:
                                        self.edges.remove(e1)
                                    else:
                                        _log.error('Edge {} should have been in edges but was not there'.format(e1))
                                self.additionalBorderEdges1.append(newEdge)
                                self.edges.append(newEdge)
                                _log.info('Combined edges {} and {}'.format(e0,e1))
                                e0.delete()
                                e1.delete()

                        else:
                            _log.warning('Volumes {} share more than one additional border edge. This needs more work!'.format(f.volumes))
                            _log.warning('Edges: {}'.format(edgesToCombine))
                            for v in f.volumes:
                                if not v in self.errorCells:
                                    self.errorCells.append(v)



        #    Remove unused nodes
        #....................................................................
        if True:
            _log.debug('Removing geometric nodes')
            nodesToRemove = []
            for n in self.nodes:
                if n.is_geometrical:
                    nodesToRemove.append(n)
                    _log.debug('Eliminating node {}'.format(n.info_text))
                    if n in self.additionalBorderNodes1:
                        self.additionalBorderNodes1.remove(n)
                        self.geometricNodes.append(n)
                    else:
                        _log.error('After combining faces, only additional border nodes should have become geometric and not {}!'.format(n.info_text))

            for n in nodesToRemove:
                if n in self.nodes:
                    self.nodes.remove(n)
                else:
                    _log.error('Cannont remove node {} from nodes'.format(n.info_text))

        #    Remove unused edges
        #....................................................................
        if True:
            _log.debug('Removing geometric nodes')
            edgesToRemove = []
            for e in self.edges:
                if e.is_geometrical:
                    edgesToRemove.append(e)
                    _log.debug('Eliminating edge {}'.format(e))
                    if e in self.additionalBorderEdges1:
                        self.additionalBorderEdges1.remove(e)
                        self.geometricEdges.append(e)
                    else:
                        _log.error('After combining faces, only additional border nodes should have become geometric and not {}!'.format(n.info_text))

            for e in edgesToRemove:
                if e in self.edges:
                    self.edges.remove(e)
                else:
                    _log.error('Cannont remove edge {} from edges'.format(e))






#-------------------------------------------------------------------------
#    Categorize Primal
#-------------------------------------------------------------------------


    def __categorizePrimal(self):
        '''

        '''

        if True:
            _log.debug = _log.debug
            _log.info = _log.info
            _log.warning = _log.warning
            _log.error = _log.error
        else:
            _log.warning('Using prints instead of logger!')
            _log.debug = cc.printGreen
            _log.info = cc.printCyan
            _log.warning = cc.printYellow
            _log.error = cc.printRed


#    Categorize volumes
#-------------------------------------------------------------------------
        _log.info('Categorizing volumes')
        # Go through all volumes
        for v in self.volumes:

            # Uncategorized volumes are assumed to be inner volumes, however the user should be informed
            if v.category1 == 'undefined':
                _log.info('The category of volume {} is not defined, assuming it is an inner volume'.format(v))
                v.category = 'inner'
            else:
                _log.debug('Category1 of volume {} set correctly'.format(v))

#    Categorize faces
#-------------------------------------------------------------------------

        if True:
            _log.info('Categorizing faces')

            # Go through all faces
            for f in self.faces:

                # Uncategorized faces are categorized automatically
                if len(f.volumes) == 0:
                    _log.error('Face {} does not belong to a volume'.format(f))

                # Faces that belong to only one volume must be at some kind of border
                elif len(f.volumes) == 1:

                    # Check if volume is uncategorized. This should not be, because all volumes were categorized in the step above
                    if f.volumes[0].category == 'undefined':
                        _log.error('Volume {} should have been already categorized'.format(f.volumes[0]))

                    # If the face belongs to a single inner volume, it is a border face
                    elif f.volumes[0].category == 'inner':
                        f.category1 = 'border'
                        _log.debug('Face {} is a border face'.format(f))

                    # If the face belongs to a single border volume, it is an additional border face
                    elif f.volumes[0].category == 'border':
                        f.category1 = 'additionalBorder'
                        _log.debug('Face {} is an additional border face'.format(f.info_text))

                    # Anything else is not knwon
                    else:
                        _log.error('Unknown category of volume %s',f.volumes[0].info_text)

                # Faces that belong to two volumes are inner faces
                elif len(f.volumes) == 2:
                    f.category1 = 'inner'
                    _log.debug('Face {} is an inner face'.format(f.info_text))

                # Faces cannot belong to more than 2 volumes - at least in 3 dimensions ;)
                elif len(f.volumes) > 2:
                    _log.error('Face {} belongs to too many volumes'.format(f))



#    Categorize edges
#-------------------------------------------------------------------------

        if True:
            _log.info('Categorizing edges')

            for e in self.edges:
                # Edges that belong to a border face are border edges
                if any([f.category1 == 'border' for f in e.faces]):
                    e.category1 = 'border'
                    _log.debug('Edge {} is a border edge'.format(e))

                # Edges that  belong to additional border faces are additional border edges
                elif any([f.category1 == 'additionalBorder' for f in e.faces]):
                    e.category1 = 'additionalBorder'
                    _log.debug('Edge {} is an additional border edge'.format(e))

                # Edges that are not categorized so far are inner edges
                else:
                    e.category1 = 'inner'
                    _log.debug('Edge {} is an inner edge'.format(e))


#    Categorize nodes
#-------------------------------------------------------------------------
        if True:

            _log.info('Categorizing nodes')

            for n in self.nodes:

                # Nodes that belong to border edges are border nodes
                if any([e.category1 == 'border' for e in n.edges]):
                    n.category1 = 'border'
                    _log.debug('Node {} is a border node'.format(n))

                # Nodes that belong to additional border edges are additional border nodes
                elif any([e.category1 == 'additionalBorder' for e in n.edges]):
                    n.category1 = 'additionalBorder'
                    _log.debug('Node {} is an additional border node'.format(n))

                # Nodes that are not categorized so far are inner nodes
                else:
                    n.category1 = 'inner'
                    _log.debug('Node {} is an inner node'.format(n))



#-------------------------------------------------------------------------
#    Categorize Dual
#-------------------------------------------------------------------------


    def __categorizeDual(self):
        '''

        '''

        if True:
            _log.debug = _log.debug
            _log.info = _log.info
            _log.warning = _log.warning
            _log.error = _log.error
        else:
            _log.warning('Using prints instead of logger!')
            _log.debug = cc.printGreen
            _log.info = cc.printCyan
            _log.warning = cc.printYellow
            _log.error = cc.printRed

#    Categorize volumes
#-------------------------------------------------------------------------
        _log.info('Categorizing volumes')

         # Category 1 and 2 are identical for volumese
        for v in self.volumes:
            if v.category2 == 'undefined':
                v.category2 = v.category1

#    Categorize faces
#-------------------------------------------------------------------------
        _log.info('Categorizing faces')

        for f in self.faces:
            if f.category2 == 'undefined':
                if f.category1 == 'inner':
                    if any( [e.category1 == 'additionalBorder' for e in f.edges]):
                        f.category2 = 'border'
                    else:
                        f.category2 = 'inner'
                elif f.category1 == 'border':
                    f.category2 = 'inner'
                else:
                    f.category2 = f.category1
                    _log.debug('Copied category of {}'.format(f))
            else:
                _log.error('Category2 of {} was alreaddy set'.format(f))

#    Categorize nodes
#-------------------------------------------------------------------------
        _log.info('Categorizing nodes')

        # Category 1 and 2 are identical for nodes
        for n in self.nodes:
            if n.category2 == 'undefined':
                n.category2 = n.category1
                _log.debug('Copied category of {}'.format(n))
            else:
                _log.error('Category2 of {} was alreaddy set'.format(n))


#    Categorize edges
#-------------------------------------------------------------------------
        _log.info('Categorizing edges')

        for e in self.edges:

            if e.startNode.category2 == 'additionalBorder' or e.endNode.category2 == 'additionalBorder':
                if e.category1 == 'inner':
                    if e.category2 == 'undefined':
                        e.category2 = 'border'
                    else:
                        _log.error('Category2 of {} was alreaddy set'.format(e))
                elif e.category1 == 'additionalBorder':
                    if e.category2 == 'undefined':
                        e.category2 = 'additionalBorder'
                    else:
                        _log.error('Category2 of {} was alreaddy set'.format(e))


            else:
                if e.category2 == 'undefined':
                    e.category2 = 'inner'
                else:
                    _log.error('Category2 of {} was alreaddy set'.format(e))

#-------------------------------------------------------------------------
#    Split Edges
#-------------------------------------------------------------------------

    def __split_edges(self):
        _log.critical("Split edges")
        new_edges = []
        old_edges = []
        # v = self.volumes[12]
        # _log.critical("Volume: %s", v)
        # _log.critical("Faces: %s", v.faces)
        # for f in v.faces:
        #     _log.critical("Edges of %s: %s", f, f.edges)
        # e = self.edges[55]
        # _log.critical("Edge: %s", e)
        # _log.critical("Faces in edge: %s", e.faces)
        # stop = 4
        # count = 0
        for e in self.edges:
            if e.category1 == "inner" and e.startNode.category1 == "additionalBorder" and e.endNode.category1 == "additionalBorder":

                # count += 1
                _log.critical("")
                _log.critical("")
                _log.critical("")
                _log.critical("")
                # _log.critical("COUNT = %s", count)


                # if count > stop:
                    # _log.critical("%s > %s: Continue", count, stop)
                    # continue
                _log.critical("Edge to split: %s", e)

                new_node = Node(
                    (e.startNode.xCoordinate + e.endNode.xCoordinate)/2,
                    (e.startNode.yCoordinate + e.endNode.yCoordinate)/2,
                    (e.startNode.zCoordinate + e.endNode.zCoordinate)/2,
                )
                new_node.category1 = "inner"
                new_node.category2 = "inner"
                self.nodes.append(new_node)

                _log.critical("Old nodes: %s and %s. New node: %s",e.startNode.coordinates, e.endNode.coordinates, new_node.coordinates)

                new_edge_1 = Edge(e.startNode, new_node)
                new_edge_2 = Edge(new_node, e.endNode)
                new_edge_1.category1 = e.category1
                new_edge_1.category2 = e.category2
                new_edge_2.category1 = e.category1
                new_edge_2.category2 = e.category2

                new_edges.append(new_edge_1)
                new_edges.append(new_edge_2)
                old_edges.append(e)

                _log.critical("Faces: %s", e.faces)
                faces_to_work_on = e.faces[:]

                for f in faces_to_work_on:

                    _log.critical("")
                    _log.critical("")
                    _log.critical("Replace edge %s in face %s", e, f)

                    _log.critical("Old edges: %s", f.edges)
                    new_edges_face = []
                    if f.is_reverse:
                        _log.critical("Reversed face")
                        f = -f
                        _log.critical("Old edges in reversed face: %s", f.edges)

                        for e_ in f.edges:
                            if e_ == -e:
                                new_edges_face.append(-new_edge_2)
                                new_edges_face.append(-new_edge_1)
                            else:
                                new_edges_face.append(e_)


                    else:
                        _log.critical("Non-reversed face")
                        for e_ in f.edges:
                            if e_ == e:
                                new_edges_face.append(new_edge_1)
                                new_edges_face.append(new_edge_2)
                            else:
                                new_edges_face.append(e_)
                    f.edges = new_edges_face
                    _log.critical("New edges: %s", f.edges)

        for e in old_edges:
            self.edges.remove(e)

        for e in new_edges:
            self.edges.append(e)

    def updateComplex3D(self):
        '''

        '''
        if self.__renumber:
            self.__changedNumbering = True
        super().updateComplex3D()
        if self.dualComplex:
            self.dualComplex.updateComplex3D()


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================

if __name__ == '__main__':

    set_logging_format(logging.DEBUG)

    # --------------------------------------------------------------------
    #    Create sample data
    # --------------------------------------------------------------------

    _log.info('Create nodes')

    n000 = Node(0, 0, 0)
    n001 = Node(1, 0, 0)
    n002 = Node(1.5, 0, 0)
    n003 = Node(0, 1, 0)
    n004 = Node(1, 1, 0)
    n005 = Node(0, 1.5, 0)
    n006 = Node(1.5, 1.5, 0)
    n007 = Node(0, 0, 1)
    n008 = Node(1, 0, 1)
    n009 = Node(0, 1, 1)
    n010 = Node(1, 1, 1)
    n011 = Node(0, 0, 1.5)
    n012 = Node(1.5, 0, 1.5)
    n013 = Node(0, 1.5, 1.5)
    n014 = Node(1.5, 1.5, 1.5)

    nodes = [
        n000, n001, n002, n003, n004, n005, n006, n007, n008, n009,
        n010, n011, n012, n013, n014,
    ]

    _log.info('Create edges')

    e000 = Edge(n000, n001)
    e001 = Edge(n001, n002)
    e002 = Edge(n003, n004)
    e003 = Edge(n005, n006)
    e004 = Edge(n000, n003)
    e005 = Edge(n001, n004)
    e006 = Edge(n002, n006)
    e007 = Edge(n003, n005)
    e008 = Edge(n004, n006)
    e009 = Edge(n007, n008)
    e010 = Edge(n008, n010)
    e011 = Edge(n010, n009)
    e012 = Edge(n009, n007)
    e013 = Edge(n011, n012)
    e014 = Edge(n012, n014)
    e015 = Edge(n014, n013)
    e016 = Edge(n013, n011)
    e017 = Edge(n000, n007)
    e018 = Edge(n001, n008)
    e019 = Edge(n004, n010)
    e020 = Edge(n003, n009)
    e021 = Edge(n002, n012)
    e022 = Edge(n006, n014)
    e023 = Edge(n005, n013)
    e024 = Edge(n007, n011)
    e025 = Edge(n008, n012)
    e026 = Edge(n010, n014)
    e027 = Edge(n009, n013)

    edges = [
        e000, e001, e002, e003, e004, e005, e006, e007, e008, e009,
        e010, e011, e012, e013, e014, e015, e016, e017, e018, e019,
        e020, e021, e022, e023, e024, e025, e026, e027,
    ]

    _log.info('Create faces')

    f000 = Face([e000, e005, -e002, -e004])
    f001 = Face([e001, e006, -e008, -e005])
    f002 = Face([e002, e008, -e003, -e007])
    f003 = Face([e000, e018, -e009, -e017])
    f004 = Face([e005, e019, -e010, -e018])
    f005 = Face([e002, e019, e011, -e020])
    f006 = Face([e004, e020, e012, -e017])
    f007 = Face([e009, e010, e011, e012])
    f008 = Face([e009, e025, -e013, -e024])
    f009 = Face([e001, e021, -e025, -e018])
    f010 = Face([e006, e022, -e014, -e021])
    f011 = Face([e025, e014, -e026, -e010])
    f012 = Face([e008, e022, -e026, -e019])
    f013 = Face([e003, e022, e015, -e023])
    f014 = Face([e026, e015, -e027, -e011])
    f015 = Face([e007, e023, -e027, -e020])
    f016 = Face([e027, e016, -e024, -e012])
    f017 = Face([e013, e014, e015, e016])

    faces = [
        f000, f001, f002, f003, f004, f005, f006, f007, f008, f009,
        f010, f011, f012, f013, f014, f015, f016, f017,
    ]

    _log.info('Create volumes')

    v000 = Volume([-f000, f003, f004, -f005, -f006, f007])
    v001 = Volume([-f001, -f004, f009, f010, f011, -f012])
    v002 = Volume([-f002, f005, f012, -f013, f014, -f015])
    v003 = Volume([-f007, f008, -f011, -f014, -f016, f017])

    volumes = [
        v000, v001, v002, v003,
    ]

    for v in [v001, v002, v003]:
        v.category1 = "border"

    pc = PrimalComplex3D(nodes, edges, faces, volumes)

    # --------------------------------------------------------------------
    #    Plotting
    # --------------------------------------------------------------------

    # Choose plotting method. Possible choices: pyplot, VTK, TikZ, plotly, None
    PLOTTING_METHOD = "pyplot"

    match PLOTTING_METHOD:
        case "pyplot":
            _log.info("Plotting with pyplot selected.")
            (figs, axes) = pf.getFigures()
            pc.plotComplex(axes[0])
            pc.plotFaces(axes[1])
            pc.plotVolumes(axes[2])
            for f in figs:
                f.show()

        case "VTK":
            _log.info("Plotting with VTK selected.")
            myVTK = pc.plotComplexVTK(showLabel=False, showArrow=False)
            myVTK.start()

        case "TikZ":
            _log.info("Plotting with TikZ selected.")
            pic = pc.plotComplexTikZ()
            pic.scale = 5
            file = True
            pic.writeLaTeXFile('latex','primalComplex3D',compileFile=file,openFile=file)

            picNodes = pc.plotNodesTikZ()
            picNodes.scale = 2
            picNodes.writeTikZFile(filename='Complex3D0Nodes')

            picEdges = pc.plotEdgesTikZ()
            picEdges.scale = 2
            picEdges.writeTikZFile(filename='Complex3D1Edges')

            picFaces = pc.plotFacesTikZ()
            picFaces.scale = 2

            picFaces.writeTikZFile(filename='Complex3D2Faces')

        case "plotly":
            _log.info("Plotting with plotly selected.")

            node_plotly = NodePlotly(pc.nodes)
            edge_plotly = EdgePlotly(pc.edges)
            face_plotly = FacePlotly(pc.faces)

            plotly_fig_nodes_edges = node_plotly.plot_nodes_plotly(show_label=True)
            edge_plotly.plot_edges_plotly(plotly_fig_nodes_edges, show_label=True, show_barycenter=False, cone_size=0.05)
            plotly_fig_nodes_edges.show()

            plotly_fig_edges_faces = edge_plotly.plot_edges_plotly(show_label=False, show_barycenter=False, cone_size=0.05)
            face_plotly.plot_faces_plotly(plotly_fig_edges_faces, show_label=True, show_barycenter=False)
            plotly_fig_edges_faces.show()

        case "None":
            _log.info("No plotting selected.")

        case _:
            _log.error(
                "Unknown plotting '%s' method selected.",
                PLOTTING_METHOD,
            )
