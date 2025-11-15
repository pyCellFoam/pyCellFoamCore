# -*- coding: utf-8 -*-
#==============================================================================
# PRIMAL COMPLEX 3D
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Mar  1 13:55:43 2019

'''


'''


#==============================================================================
#    IMPORTS
#==============================================================================
#-------------------------------------------------------------------------
#    Change to Main Directory
#-------------------------------------------------------------------------
import os
if __name__ == '__main__':
    os.chdir('../')


#-------------------------------------------------------------------------
#    Standard Libraries
#-------------------------------------------------------------------------
from itertools import chain
import logging

#import numpy as np
#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------


from pyCellFoamCore.boundingBox.boundingBox import BoundingBox

#    kCells
#--------------------------------------------------------------------
from pyCellFoamCore.k_cells.node.node import Node
from pyCellFoamCore.k_cells.edge.edge import Edge
from pyCellFoamCore.k_cells.face.face import Face
from pyCellFoamCore.k_cells.volume.volume import Volume

#    Complex & Grids
#--------------------------------------------------------------------
from pyCellFoamCore.complex.complex3D import Complex3D

#    Tools
#--------------------------------------------------------------------
import pyCellFoamCore.tools.colorConsole as cc
import pyCellFoamCore.tools.placeFigures as pf
import pyCellFoamCore.tools.tumcolor as tc
from pyCellFoamCore.tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class PrimalComplex3D(Complex3D):
    '''

    '''

#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__boundingBox',
                 '__dualComplex',
                 '__renumber',
                 '__changedNumbering',
                 '__useCategory',
                 "__volumes_to_combine",
                 "__faces_to_combine")

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,*args,renumber=True,boundingBox=None, volumes_to_combine=[], faces_to_combine=[],**kwargs):
        '''

        '''
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
                                newEdge = Edge(e0.startNode,e1.endNode,geometricNodes = middleNode)



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
                                newEdge = Edge(e1.startNode,e0.endNode,geometricNodes = middleNode)

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






    def cutAtBoundingBox(self):
        '''

        '''

        _log.error('Cutting at bounding box')

        for n in self.borderNodes1 + self.additionalBorderNodes1 + self.innerNodes1:

            (dist,side) = self.__boundingBox.distToBoundingBox(n.coordinates)

            if dist > 0:
                cc.printYellow('{} lies inside the bb, closest side: {}'.format(n,side))
            else:
                cc.printYellow('{} lies outside the bb, closest side: {}'.format(n,side))



        for e in self.edges:
            intersectionNodes = e.intersectWithBoundingBox(self.__boundingBox)
            cc.printGreen(intersectionNodes)
            if len(intersectionNodes) == 1:
                if intersectionNodes[0] is not None:
                    self.nodes.append(intersectionNodes[0])


#            (dist1,_) = self.__boundingBox.distToBoundingBox(e.startNode.coordinates)
#            (dist2,_) = self.__boundingBox.distToBoundingBox(e.endNode.coordinates)
#
#            if dist1*dist2 < 0:
#                cc.printCyan('{} crosses the bounding box'.format(e))
#                e.color = tc.TUMRose()
#            else:
#                cc.printCyan('{} does not cross the bounding box'.format(e))
#








#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':



    set_logging_format(logging.DEBUG)
    cc.printBlue('Create nodes')
    n0 = Node(0,0,0)
    n1 = Node(1,0,0)
    n2 = Node(1.5,0,0)
    n3 = Node(0,1,0)
    n4 = Node(1,1,0)
    n5 = Node(0,1.5,0)
    n6 = Node(1.5,1.5,0)
    n7 = Node(0,0,1)
    n8 = Node(1,0,1)
    n9 = Node(0,1,1)
    n10 = Node(1,1,1)
    n11 = Node(0,0,1.5)
    n12 = Node(1.5,0,1.5)
    n13 = Node(0,1.5,1.5)
    n14 = Node(1.5,1.5,1.5)


    nodes = [n0,n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14]


    cc.printBlue('Create edges')
    e0 = Edge(n0,n1)
    e1 = Edge(n1,n2)
    e2 = Edge(n3,n4)
    e3 = Edge(n5,n6)
    e4 = Edge(n0,n3)
    e5 = Edge(n1,n4)
    e6 = Edge(n2,n6)
    e7 = Edge(n3,n5)
    e8 = Edge(n4,n6)
    e9 = Edge(n7,n8)
    e10 = Edge(n8,n10)
    e11 = Edge(n10,n9)
    e12 = Edge(n9,n7)
    e13 = Edge(n11,n12)
    e14 = Edge(n12,n14)
    e15 = Edge(n14,n13)
    e16 = Edge(n13,n11)
    e17 = Edge(n0,n7)
    e18 = Edge(n1,n8)
    e19 = Edge(n4,n10)
    e20 = Edge(n3,n9)
    e21 = Edge(n2,n12)
    e22 = Edge(n6,n14)
    e23 = Edge(n5,n13)
    e24 = Edge(n7,n11)
    e25 = Edge(n8,n12)
    e26 = Edge(n10,n14)
    e27 = Edge(n9,n13)

    edges = [e0,e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13,e14,e15,e16,e17,e18,e19,e20,e21,e22,e23,e24,e25,e26,e27]

    cc.printBlue('Create faces')
    f0 = Face([e0,e5,-e2,-e4])
    f1 = Face([e1,e6,-e8,-e5])
    f2 = Face([e2,e8,-e3,-e7])
    f3 = Face([e0,e18,-e9,-e17])
    f4 = Face([e5,e19,-e10,-e18])
    f5 = Face([e2,e19,e11,-e20])
    f6 = Face([e4,e20,e12,-e17])
    f7 = Face([e9,e10,e11,e12])
    f8 = Face([e9,e25,-e13,-e24])
    f9 = Face([e1,e21,-e25,-e18])
    f10 = Face([e6,e22,-e14,-e21])
    f11 = Face([e25,e14,-e26,-e10])
    f12 = Face([e8,e22,-e26,-e19])
    f13 = Face([e3,e22,e15,-e23])
    f14 = Face([e26,e15,-e27,-e11])
    f15 = Face([e7,e23,-e27,-e20])
    f16 = Face([e27,e16,-e24,-e12])
    f17 = Face([e13,e14,e15,e16])


    faces = [f0,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17]


    cc.printBlue('Create volumes')

    v0 = Volume([-f0,f3,f4,-f5,-f6,f7])
    v1 = Volume([-f1,-f4,f9,f10,f11,-f12])
    v2 = Volume([-f2,f5,f12,-f13,f14,-f15])
    v3 = Volume([-f7,f8,-f11,-f14,-f16,f17])

    facesForVolume = [-f7,f8,-f11,-f14,-f16,f17]

    volumes = [v0,v1,v2,v3]

    for v in [v1,v2,v3]:
        v.category1 = 'border'



    # bb = BoundingBox([0.2,1.2],[0.2,1.2],[0.2,1.2])

    pc = PrimalComplex3D(nodes,edges,faces,volumes)



    # pc.cutAtBoundingBox()





#-------------------------------------------------------------------------
#    Plotting
#-------------------------------------------------------------------------

    # Choose plotting method. Possible choices: pyplot, VTK, TikZ, animation, doc, None
    plottingMethod = 'pyplot'


#    Disabled
#---------------------------------------------------------------------
    if plottingMethod is None or plottingMethod == 'None':
        cc.printBlue('Plotting disabled')

#    Pyplot
#---------------------------------------------------------------------
    elif plottingMethod == 'pyplot':
        cc.printBlue('Plot using pyplot')
        (figs,axes) = pf.getFigures()
        pc.plotComplex(axes[0])
        pc.plotFaces(axes[1])
        pc.plotVolumes(axes[2])
        # bb.plotBoundingBox(axes[0])

#    VTK
#---------------------------------------------------------------------
    elif plottingMethod == 'VTK' :
        cc.printBlue('Plot using VTK')
        cc.printRed('Not implemented')

#    TikZ
#---------------------------------------------------------------------
    elif plottingMethod == 'TikZ' :
        cc.printBlue('Plot using TikZ')
        pic = pc.plotComplexTikZ()
        pic.scale = 5
        file = False
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


        print(pc.incidenceMatrix1)
        # print(pc.incidenceMatrix2)
        print(pc.incidenceMatrix3)

        # picFaces = pc.plotVolumesTikZ()
        # picFaces.scale = 2
        # picFaces.writeTikZFile(filename='Complex3D3Volumes')

#    Animation
#---------------------------------------------------------------------
    elif plottingMethod == 'animation':
        cc.printBlue('Creating animation')
        cc.printRed('Not implemented')

#    Documentation
#---------------------------------------------------------------------
    elif plottingMethod == 'doc':
        cc.printBlue('Creating plots for documentation')
        test.plotDoc()

#    Unknown
#---------------------------------------------------------------------
    else:
        cc.printRed('Unknown plotting method {}'.format(plottingMethod))
