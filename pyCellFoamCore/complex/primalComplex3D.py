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
#import numpy as np
#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------


from boundingBox import BoundingBox

#    kCells
#--------------------------------------------------------------------
from kCells import Node, Edge, Face
from kCells.volume.volume import Volume

#    Complex & Grids
#--------------------------------------------------------------------
from complex.complex3D import Complex3D

#    Tools
#--------------------------------------------------------------------
import tools.colorConsole as cc
import tools.placeFigures as pf
from tools import MyLogging
import tools.tumcolor as tc



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
            self.logger.error('Dual complex is already set')
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
            self.logger.error('Cannot set useCategory of to {} - It must be either 1 or 2'.format(u))
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
        self.logger.info('Called "Set Up" in PrimalComplex3D class')
        self.__categorizePrimal()
        self.sortPrimal()
        self.__combineAdditionalBorderFaces()
        self.__categorizeDual()
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
            self.logger.error('Unknown useCategory {}'.format(self.useCategory))

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
        if False:
            myPrintDebug = self.logger.debug
            myPrintInfo = self.logger.info
            myPrintWarning = self.logger.warning
            myPrintError = self.logger.error
        else:
            self.logger.warning('Using prints instead of logger!')
            myPrintDebug = cc.printGreen
            myPrintInfo = cc.printCyan
            myPrintWarning = cc.printYellow
            myPrintError = cc.printRed


        myPrintInfo('Combining additional border face')

        #    Manual combine volumes
        #....................................................................

        for (v1, v2) in self.__volumes_to_combine:
            myPrintDebug("Combine volumes {} and {}".format(v1, v2))

            shared_faces = set(v1.faces).intersection(set([-f for f in v2.faces]))
            myPrintDebug("Shard faces: {}".format(shared_faces))

            if len(shared_faces) == 1:
                shared_face = list(shared_faces)[0]
                new_faces = [f for f in v1.faces if not f == shared_face] + [f for f in v2.faces if (not (-f == shared_face) and not f in v1.faces)]
                myPrintDebug("New faces: {}".format(new_faces))
                new_volume = Volume(new_faces)
                new_volume.category1 = v1.category1
                new_volume.category2 = v1.category2
                # myPrintWarning("volumes: {}".format(self.volumes))

                for v in [v1, v2]:
                    if v in self.volumes:
                        self.volumes.remove(v)
                    else:
                        myPrintError("{} should have been in volumes but is not".format(v))
                    if v in self.borderVolumes:
                        self.borderVolumes.remove(v)
                    else:
                        myPrintError("{} should have been in border volumes but is not".format(v))

                self.volumes.append(new_volume)
                if new_volume.category1 == "border":
                    self.borderVolumes.append(new_volume)
                else:
                    myPrintError("New volume {} should have been a border volume".format(new_volume))
                v1.delete()
                v2.delete()
                if shared_face in self.faces:
                    self.faces.remove(shared_face)
                elif -shared_face in self.faces:
                    self.faces.remove(-shared_face)
                else:
                    myPrintError("Cannot remove face {} from faces".format(shared_face))

                if shared_face.category1 == "additionalBorder":
                    if shared_face in self.additionalBorderFaces1:
                        self.additionalBorderFaces1.remove(shared_face)
                    elif -shared_face in self.additionalBorderFaces1:
                        self.additionalBorderFaces1.remove(-shared_face)
                    else:
                        myPrintError("Cannot remove face {} from additional border faces 1".format(shared_face))

                    if shared_face in self.additionalBorderFaces2:
                        self.additionalBorderFaces2.remove(shared_face)
                    elif -shared_face in self.additionalBorderFaces1:
                        self.additionalBorderFaces2.remove(-shared_face)
                    else:
                        myPrintError("Cannot remove face {} from additional border faces 2".format(shared_face))

                elif shared_face.category1 == "inner":
                    if shared_face in self.innerFaces:
                        self.innerFaces.remove(shared_face)
                    elif -shared_face in self.innerFaces:
                        self.innerFaces.remove(-shared_face)
                    else:
                        myPrintError("Cannot remove face {} from inner faces".format(shared_face))

                else:
                    myPrintError("Category1 of {} is {}!".format(shared_face, shared_face.category1))





            else:
                myPrintError("Cannot combine volumes with {} shared faces".format(len(shared_faces)))

        #    Manual combine faces
        #....................................................................

        for (f1, f2) in self.__faces_to_combine:
            myPrintDebug("Combine faces {} and {}".format(f1, f2))
            shared_edges = set(f1.edges).intersection(set([-e for e in f2.edges]+f2.edges))
            myPrintDebug("Edges of face 1: {}".format(f1.edges))
            myPrintDebug("Edges of face 2: {}".format(f2.edges))
            myPrintDebug("shared edges: {}".format(shared_edges))

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


                myPrintDebug("1_1: {} | 2_1: {} | 2_2: {} | 1_2: {}".format(edges_1_1, edges_2_1, edges_2_2, edges_1_2))
                new_edges = edges_1_1 + edges_2_1 + edges_2_2 + edges_1_2
                myPrintDebug("new edges: {}".format(new_edges))
                new_face = Face(new_edges)
                new_face.category1 = f1.category1
                new_face.category2 = f1.category2
                if shared_edge in self.edges:
                    self.edges.remove(shared_edge)
                elif -shared_edge in self.edges:
                    self.edges.remove(-shared_edge)
                else:
                    myPrintError("Edge {} should be found in list of edges, but is not".format(shared_edge))

                self.faces.append(new_face)
                if new_face.category1 == "additionalBorder":
                    self.additionalBorderFaces.append(new_face)
                else:
                    myPrintError("Should only combine additional border faces but new face is {}".format(new_face.category1))

                volumes = set(f1.volumes).intersection(set(f2.volumes), set(self.volumes))
                myPrintWarning("volumes of combined faces: {}".format(volumes))
                for v in list(volumes):
                    myPrintWarning("Old faces: {}".format(v.faces))
                    faces_for_new_volume = v.faces.copy()
                    if f1 in faces_for_new_volume:
                        faces_for_new_volume.remove(f1)
                    elif -f1 in faces_for_new_volume:
                        faces_for_new_volume.remove(-f1)
                    else:
                        myPrintError("Cannot remove face {}".format(f1))
                    if f2 in faces_for_new_volume:
                        faces_for_new_volume.remove(f2)
                    elif -f2 in faces_for_new_volume:
                        faces_for_new_volume.remove(-f2)
                    else:
                        myPrintError("Cannot remove face {}".format(f2))
                    faces_for_new_volume.append(new_face)
                    myPrintWarning("New faces: {}".format(faces_for_new_volume))
                    new_volume = Volume(faces_for_new_volume, unalignedFaces=True)
                    new_volume.category1 = v.category1
                    new_volume.category2 = v.category2
                    self.volumes.remove(v)
                    if v in self.innerVolumes:
                        self.innerVolumes.remove(v)
                    elif v in self.borderVolumes:
                        self.borderVolumes.remove(v)
                    else:
                        myPrintError("{} is neither part of the inner nor of the border volumes".format(v))
                    self.volumes.append(new_volume)
                    if new_volume.category1 == "border":
                        self.borderVolumes.append(new_volume)
                    else:
                        myPrintError("New volume {} should have been a border volume".format(new_volume))
                    v.delete()
                    for f in [f1, f2]:
                        if f in self.faces:
                            self.faces.remove(f)
                        else:
                            myPrintError("Cannot remove {} from faces".format(f))

                        if f in self.additionalBorderFaces1:
                            self.additionalBorderFaces1.remove(f)
                        else:
                            myPrintError("Cannot remove {} from additional border faces 1".format(f))

                        if f in self.additionalBorderFaces2:
                            self.additionalBorderFaces2.remove(f)
                        else:
                            myPrintError("Cannot remove {} from additional border faces 2".format(f))
                f1.delete()
                f2.delete()



            else:
                myPrintError("Cannot combine faces with {} shared edges".format(len(shared_edges)))












        #
        #    Check need for combine volumes
        #....................................................................

        if True:
            need_combination = False
            for v in self.volumes:
                myPrintDebug("Checking volume {}".format(v))
                if v.category1 == "border":
                    myPrintDebug("Checking faces of border volume")
                    additional_border_faces = [
                        f for f in v.faces if f.category1 == "additionalBorder"
                    ]

                    if len(additional_border_faces) == 0:
                        myPrintError("Volume {} is of type border but has no additional border faces".format(v))
                    elif len(additional_border_faces) == 1:
                        myPrintDebug("Found one additional border face. No need to combine volumes")
                    elif len(additional_border_faces) == 2:
                        myPrintDebug("Found two additional border faces. Checking if the rim is included")
                    elif len(additional_border_faces) == 3:
                        myPrintDebug("Found three additional border faces. Checking if the corner is included")
                        all_nodes = []
                        for f in additional_border_faces:
                            temp_nodes = []
                            for e in f.edges:
                                for n in [e.startNode, e.endNode]:
                                    if not n in temp_nodes:
                                        temp_nodes.append(n)
                            all_nodes.append(temp_nodes)
                        myPrintDebug("Found nodes: {}".format(all_nodes))
                        shared_nodes = set(all_nodes[0]).intersection(*[set(nodes) for nodes in all_nodes[1:]])
                        myPrintDebug("Shared nodes: {}".format(shared_nodes))

                        if len(shared_nodes) == 0:
                            myPrintError("Found no shared nodes. Need to combine volume {}".format(v))
                            need_combination = True
                        elif len(shared_nodes) == 1:
                            myPrintDebug("One shared node. Everything OK")
                        else:
                            myPrintError("{} shared nodes cannot be handled".format(len(shared_nodes)))
                            need_combination = True




                    else:
                        myPrintError("Volume {} has {} additional border faces. This cannot be handled currently".format(v, len(additional_border_faces)))

                    # TODO
                    # Check that all additional border faces are connected and
                    # have no holes. Otherwise find the volume that this volume
                    # must be merged with
                    # Note: 3 faces must share a node, 2 faces must share an
                    # edge
                elif v.category1 == "inner":
                    myPrintDebug("Inner volumes do not need to be checked")
                else:
                    myPrintError("Unknown category {}".format(v.category1))
            if need_combination:
                return




        #    Combine faces
        #....................................................................
        if True:
            for v in self.volumes:
                myPrintDebug('Combining additional border faces of volume {}'.format(v.infoText))
                facesToCombine = []
                facesToStay = []
                for f in v.faces:

                    if f.category == 'additionalBorder' and v.category != 'border':
                        myPrintError('Face {} is an additional border face and belongs to volume {} of category {}. This should not be!'.format(f.infoText,self.infoText,self.category))

                    if f.category == 'additionalBorder' and v.category == 'border':
                        facesToCombine.append(f)
                    else:
                        facesToStay.append(f)
                if len(facesToCombine) == 0:
                    myPrintDebug('Volume {} has no faces to combine'.format(v.infoText))
                elif len(facesToCombine) == 1:
                    myPrintDebug('Volume {} has only one additional border face, so no need to combine'.format(v.infoText))
                elif len(facesToCombine) <= 3:

                    # Check if each face shares at least one edge with another face
                    edgesOfFaces = []
                    for f in facesToCombine:
                        edgesOfFaces.append(f.edges)

                    myPrintDebug('Edges of the faces that should be combined: {}'.format(edgesOfFaces))

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
                        myPrintInfo('Faces {} of volume {} are all additional border face but are not connected'.format(facesToCombine,v))
                    else:

                        myPrintDebug('Volume {} has {} additional border faces: {}, trying to combine them'.format(v.infoText,len(facesToCombine),facesToCombine))
                        edgesOfFace = []
                        for f in facesToCombine:
                            for sf in f.simpleFaces:
                                edgesOfFace.append([se.belongsTo for se in sf.simpleEdges])
                        myPrintDebug('Creating new face with the edges {}'.format(edgesOfFace))
                        newFace = Face(edgesOfFace)
                        newFace.category1 = 'additionalBorder'
                        myPrintDebug('Changing the faces of volume {} by keeping the faces {} and adding the new face {}'.format(v.infoText,facesToStay,newFace))
                        v.faces = [*facesToStay,newFace]  # TODO better: v.faces = faces.ToStay.append(newFace)
                        v.setUp()
                        for f in facesToCombine:
                            if f.isReverse:
                                f = -f
                            if f in self.faces:
                                self.faces.remove(f)
                            else:
                                myPrintError('Cannot remove face {} from faces!'.format(f.infoText))
                            if f in self.additionalBorderFaces1:
                                self.additionalBorderFaces1.remove(f)
                            else:
                                myPrintError('Cannot remove face {} from additional border faces 1!'.format(f.infoText))
                            if f in self.additionalBorderFaces2:
                                self.additionalBorderFaces2.remove(f)
                            else:
                                myPrintError('Cannot remove face {} from additional border faces 2!'.format(f.infoText))
                            f.delete()

                        self.faces.append(newFace)
                        self.additionalBorderFaces1.append(newFace)
                        self.additionalBorderFaces2.append(newFace)

                        for e in newFace.geometricEdges:
                            myPrintDebug('Edge {} is getting eliminated'.format(e.infoText))
                            if e in self.edges:
                                self.edges.remove(e)
                            else:
                                myPrintError('Cannot remove edge {} from edges!'.format(e.infoText))
                            if e in self.additionalBorderEdges1:
                                self.additionalBorderEdges1.remove(e)
                                self.geometricEdges.append(e)
                            else:
                                myPrintError('Cannot remove edge {} from additional border edges!'.format(e.infoText))

                else:
                    myPrintError('Volume {} has {} additional border faces, this is too much!'.format(v,len(facesToCombine)))



        #    Combine edges
        #....................................................................
        if True:
            for f in self.faces:
                if len(f.volumes) == 2:
                    if f.volumes[0].category == 'border' and f.volumes[1].category == 'border' :
                        myPrintDebug('Found face {} between two border volumes {}'.format(f,f.volumes))
                        edgesToCombine = []
                        for e in f.edges:
                            if e.category == 'additionalBorder':
                                edgesToCombine.append(e)
                        myPrintDebug('Found additional border edges {}'.format(edgesToCombine))
                        lenEdgesToCombine = len(edgesToCombine)
                        if lenEdgesToCombine == 0:
                            myPrintDebug('Border volumes have no common aditional border edge')
#                            myPrintError('Two border volumes ({}) should at least have one additionalBorderEdge in common'.format(f.volumes))
                        elif lenEdgesToCombine == 1:
                            myPrintDebug('Everything is fine, no need to combine')
                        elif lenEdgesToCombine == 2:
                            e0 = edgesToCombine[0]
                            e1 = edgesToCombine[1]
                            myPrintDebug('Trying to combine additional border edges {}'.format(edgesToCombine))

                            # TODO
                            #
                            myPrintDebug('Faces of edge {}: {}'.format(e0,e0.faces))
                            myPrintDebug('Faces of edge {}: {}'.format(e1,e1.faces))


                            newEdge = False


                            #
                            #      .      - . -O
                            #     /            |
                            #   .              | e_1
                            #  /     e_o       |
                            # O----------------O
                            # Start/end

                            if e0.endNode == e1.startNode:
                                myPrintDebug('Can combine them')
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
                                myPrintDebug('Can combine them after rotation')
                                middleNode = e1.endNode
                                newEdge = Edge(e1.startNode,e0.endNode,geometricNodes = middleNode)

                            else:
                                myPrintDebug('Additional border Edges {} and {} are not connected and therefor cannot be combined'.format(e0,e1))
#                                self.errorCells.append(e0)
#                                self.errorCells.append(e1)

                            if newEdge:
#                                newEdge.useCategory = self.__useCategory
                                newEdge.category1 = 'additionalBorder'
                                myPrintDebug('New edge: {}'.format(newEdge))

                                currentFaces = e0.faces[:]
                                for f in e1.faces:
                                    if not f in currentFaces:
                                        currentFaces.append(f)
                                for f in currentFaces:
                                    allEdges = f.rawEdges[:]
                                    myPrintDebug('Old edges in {}: {}'.format(f,f.rawEdges))
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

                                    myPrintDebug('newEdges: {}'.format(allEdges))
                                    f.edges=allEdges
                                    f.setUp()
                                if e0.isReverse:
                                    if -e0 in self.additionalBorderEdges1:
                                        self.additionalBorderEdges1.remove(-e0)
                                    else:
                                        self.logger.error('Edge {} should have been in additional border edges but was not there'.format(-e0))
                                    if -e0 in self.edges:
                                        self.edges.remove(-e0)
                                    else:
                                        self.logger.error('Edge {} should have been in edges but was not there'.format(-e0))
                                else:
                                    if e0 in self.additionalBorderEdges1:
                                        self.additionalBorderEdges1.remove(e0)
                                    else:
                                        self.logger.error('Edge {} should have been in additional border edges but was not there'.format(e0))
                                    if e0 in self.edges:
                                        self.edges.remove(e0)
                                    else:
                                        self.logger.error('Edge {} should have been in edges but was not there'.format(e0))
                                if e1.isReverse:
                                    if -e1 in self.additionalBorderEdges1:
                                        self.additionalBorderEdges1.remove(-e1)
                                    else:
                                        self.logger.error('Edge {} should have been in additional border edges but was not there'.format(-e1))
                                    if -e1 in self.edges:
                                        self.edges.remove(-e1)
                                    else:
                                        self.logger.error('Edge {} should have been in edges but was not there'.format(-e1))
                                else:
                                    if e1 in self.additionalBorderEdges1:
                                        self.additionalBorderEdges1.remove(e1)
                                    else:
                                        self.logger.error('Edge {} should have been in additional border edges but was not there'.format(e1))
                                    if e1 in self.edges:
                                        self.edges.remove(e1)
                                    else:
                                        self.logger.error('Edge {} should have been in edges but was not there'.format(e1))
                                self.additionalBorderEdges1.append(newEdge)
                                self.edges.append(newEdge)
                                self.logger.info('Combined edges {} and {}'.format(e0,e1))
                                e0.delete()
                                e1.delete()

                        else:
                            myPrintWarning('Volumes {} share more than one additional border edge. This needs more work!'.format(f.volumes))
                            myPrintWarning('Edges: {}'.format(edgesToCombine))
                            for v in f.volumes:
                                if not v in self.errorCells:
                                    self.errorCells.append(v)



        #    Remove unused nodes
        #....................................................................
        if True:
            myPrintDebug('Removing geometric nodes')
            nodesToRemove = []
            for n in self.nodes:
                if n.isGeometrical:
                    nodesToRemove.append(n)
                    myPrintDebug('Eliminating node {}'.format(n.infoText))
                    if n in self.additionalBorderNodes1:
                        self.additionalBorderNodes1.remove(n)
                        self.geometricNodes.append(n)
                    else:
                        myPrintError('After combining faces, only additional border nodes should have become geometric and not {}!'.format(n.infoText))

            for n in nodesToRemove:
                if n in self.nodes:
                    self.nodes.remove(n)
                else:
                    myPrintError('Cannont remove node {} from nodes'.format(n.infoText))

        #    Remove unused edges
        #....................................................................
        if True:
            myPrintDebug('Removing geometric nodes')
            edgesToRemove = []
            for e in self.edges:
                if e.isGeometrical:
                    edgesToRemove.append(e)
                    myPrintDebug('Eliminating edge {}'.format(e))
                    if e in self.additionalBorderEdges1:
                        self.additionalBorderEdges1.remove(e)
                        self.geometricEdges.append(e)
                    else:
                        myPrintError('After combining faces, only additional border nodes should have become geometric and not {}!'.format(n.infoText))

            for e in edgesToRemove:
                if e in self.edges:
                    self.edges.remove(e)
                else:
                    myPrintError('Cannont remove edge {} from edges'.format(e))









#-------------------------------------------------------------------------
#    Categorize Primal
#-------------------------------------------------------------------------


    def __categorizePrimal(self):
        '''

        '''

        if True:
            myPrintDebug = self.logger.debug
            myPrintInfo = self.logger.info
            myPrintWarning = self.logger.warning
            myPrintError = self.logger.error
        else:
            self.logger.warning('Using prints instead of logger!')
            myPrintDebug = cc.printGreen
            myPrintInfo = cc.printCyan
            myPrintWarning = cc.printYellow
            myPrintError = cc.printRed


#    Categorize volumes
#-------------------------------------------------------------------------
        myPrintInfo('Categorizing volumes')
        # Go through all volumes
        for v in self.volumes:

            # Uncategorized volumes are assumed to be inner volumes, however the user should be informed
            if v.category1 == 'undefined':
                myPrintInfo('The category of volume {} is not defined, assuming it is an inner volume'.format(v))
                v.category = 'inner'
            else:
                myPrintDebug('Category1 of volume {} set correctly'.format(v))

#    Categorize faces
#-------------------------------------------------------------------------

        if True:
            myPrintInfo('Categorizing faces')

            # Go through all faces
            for f in self.faces:

                # Uncategorized faces are categorized automatically
                if len(f.volumes) == 0:
                    myPrintError('Face {} does not belong to a volume'.format(f))

                # Faces that belong to only one volume must be at some kind of border
                elif len(f.volumes) == 1:

                    # Check if volume is uncategorized. This should not be, because all volumes were categorized in the step above
                    if f.volumes[0].category == 'undefined':
                        myPrintError('Volume {} should have been already categorized'.format(f.volumes[0]))

                    # If the face belongs to a single inner volume, it is a border face
                    elif f.volumes[0].category == 'inner':
                        f.category1 = 'border'
                        myPrintDebug('Face {} is a border face'.format(f))

                    # If the face belongs to a single border volume, it is an additional border face
                    elif f.volumes[0].category == 'border':
                        f.category1 = 'additionalBorder'
                        myPrintDebug('Face {} is an additional border face'.format(f.infoText))

                    # Anything else is not knwon
                    else:
                        myPrintError('Unknown category of volume %s',f.volumes[0].infoText)

                # Faces that belong to two volumes are inner faces
                elif len(f.volumes) == 2:
                    f.category1 = 'inner'
                    myPrintDebug('Face {} is an inner face'.format(f.infoText))

                # Faces cannot belong to more than 2 volumes - at least in 3 dimensions ;)
                elif len(f.volumes) > 2:
                    myPrintError('Face {} belongs to too many volumes'.format(f))



#    Categorize edges
#-------------------------------------------------------------------------

        if True:
            myPrintInfo('Categorizing edges')

            for e in self.edges:
                # Edges that belong to a border face are border edges
                if any([f.category1 == 'border' for f in e.faces]):
                    e.category1 = 'border'
                    myPrintDebug('Edge {} is a border edge'.format(e))

                # Edges that  belong to additional border faces are additional border edges
                elif any([f.category1 == 'additionalBorder' for f in e.faces]):
                    e.category1 = 'additionalBorder'
                    myPrintDebug('Edge {} is an additional border edge'.format(e))

                # Edges that are not categorized so far are inner edges
                else:
                    e.category1 = 'inner'
                    myPrintDebug('Edge {} is an inner edge'.format(e))


#    Categorize nodes
#-------------------------------------------------------------------------
        if True:

            myPrintInfo('Categorizing nodes')

            for n in self.nodes:

                # Nodes that belong to border edges are border nodes
                if any([e.category1 == 'border' for e in n.edges]):
                    n.category1 = 'border'
                    myPrintDebug('Node {} is a border node'.format(n))

                # Nodes that belong to additional border edges are additional border nodes
                elif any([e.category1 == 'additionalBorder' for e in n.edges]):
                    n.category1 = 'additionalBorder'
                    myPrintDebug('Node {} is an additional border node'.format(n))

                # Nodes that are not categorized so far are inner nodes
                else:
                    n.category1 = 'inner'
                    myPrintDebug('Node {} is an inner node'.format(n))



#-------------------------------------------------------------------------
#    Categorize Dual
#-------------------------------------------------------------------------


    def __categorizeDual(self):
        '''

        '''

        if True:
            myPrintDebug = self.logger.debug
            myPrintInfo = self.logger.info
            myPrintWarning = self.logger.warning
            myPrintError = self.logger.error
        else:
            self.logger.warning('Using prints instead of logger!')
            myPrintDebug = cc.printGreen
            myPrintInfo = cc.printCyan
            myPrintWarning = cc.printYellow
            myPrintError = cc.printRed

#    Categorize volumes
#-------------------------------------------------------------------------
        myPrintInfo('Categorizing volumes')

         # Category 1 and 2 are identical for volumese
        for v in self.volumes:
            if v.category2 == 'undefined':
                v.category2 = v.category1

#    Categorize faces
#-------------------------------------------------------------------------
        myPrintInfo('Categorizing faces')

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
                    myPrintDebug('Copied category of {}'.format(f))
            else:
                myPrintError('Category2 of {} was alreaddy set'.format(f))

#    Categorize nodes
#-------------------------------------------------------------------------
        myPrintInfo('Categorizing nodes')

        # Category 1 and 2 are identical for nodes
        for n in self.nodes:
            if n.category2 == 'undefined':
                n.category2 = n.category1
                myPrintDebug('Copied category of {}'.format(n))
            else:
                myPrintError('Category2 of {} was alreaddy set'.format(n))


#    Categorize edges
#-------------------------------------------------------------------------
        myPrintInfo('Categorizing edges')

        for e in self.edges:

            if e.startNode.category2 == 'additionalBorder' or e.endNode.category2 == 'additionalBorder':
                if e.category1 == 'inner':
                    if e.category2 == 'undefined':
                        e.category2 = 'border'
                    else:
                        myPrintError('Category2 of {} was alreaddy set'.format(e))
                elif e.category1 == 'additionalBorder':
                    if e.category2 == 'undefined':
                        e.category2 = 'additionalBorder'
                    else:
                        myPrintError('Category2 of {} was alreaddy set'.format(e))


            else:
                if e.category2 == 'undefined':
                    e.category2 = 'inner'
                else:
                    myPrintError('Category2 of {} was alreaddy set'.format(e))



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

        self.logger.error('Cutting at bounding box')

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



    with MyLogging('PrimalComplex3D'):
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



        bb = BoundingBox([0.2,1.2],[0.2,1.2],[0.2,1.2])

        pc = PrimalComplex3D(nodes,edges,faces,volumes)



        # pc.cutAtBoundingBox()





#-------------------------------------------------------------------------
#    Plotting
#-------------------------------------------------------------------------

        # Choose plotting method. Possible choices: pyplot, VTK, TikZ, animation, doc, None
        plottingMethod = 'TikZ'


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
            bb.plotBoundingBox(axes[0])

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










