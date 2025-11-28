# -*- coding: utf-8 -*-
#==============================================================================
# TITLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Mon Jul 23 19:59:39 2018

'''
This is the explanation of the whole module and will be printed at the very
beginning

Use - signs to declare a headline
--------------------------------------------------------------------------

* this is an item
* this is another one

#. numbered lists
#. are also possible


Maths
--------------------------------------------------------------------------

Math can be inline :math:`a^2 + b^2 = c^2` or displayed

.. math::

   (a + b)^2 = a^2 + 2ab + b^2

   (a - b)^2 = a^2 - 2ab + b^2

Always remember that the last line has to be blank

'''
#==============================================================================
#    IMPORTS
#==============================================================================
if __name__== '__main__':
    import os
    os.chdir('../../')

# ------------------------------------------------------------------------
#    Standard Libraries
# ------------------------------------------------------------------------
import logging

from pyCellFoamCore.k_cells.cell.dual_cell import DualCell
from pyCellFoamCore.k_cells.volume.volume import Volume
from pyCellFoamCore.k_cells.face.dualFace3D import DualFace3D
import pyCellFoamCore.tools.colorConsole as cc
import numpy as np

from pyCellFoamCore.tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class DualVolume3D(Volume,DualCell):
    '''
    This is the explanation of this class.

    '''

#==============================================================================
#    SLOTS
#==============================================================================
#    __slots__ = ('__facesTemp',
#                 '__edgesTemp')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,node,*args,**kwargs):

        '''
        This is the explanation of the __init__ method.

        All parameters should be listed:

        :param int a: Some Number
        :param str b: Some String

        '''

        super().__init__([],
                         *args,
                         num = node.num,
                         unalignedFaces = True,
                         **kwargs)
        self.__edgesTemp = []

        self.category1 = node.category
        self.category2 = node.category


        _log.info('Creating dual volume of node {}'.format(node.info_text))
        unalignedFaces = []
        for e in node.edges:
            if not e.is_geometrical and not e.category1 == 'additionalBorder':
                if not e.dualCell3D:
                    DualFace3D(e)
                unalignedFaces.append(e.dualCell3D)

        if node.category1 == 'border':
            unalignedFaces.append(node.dualCell2D)
        _log.debug('Faces to define volume: {}'.format(unalignedFaces))

#        cc.printMagenta('DualVolume3D:',unalignedFaces)

        for f in unalignedFaces:
            if not f:
                unalignedFaces.remove(f)


        if all(unalignedFaces):
#            for f in faces:
#                for e in f.edges:
#                    e.setUp()
#                f.setUp()

            if False:
                simpleEdges = []

                # Check if the normal vector points outwards
    #            if np.dot(faces[0].simpleFaces[0].normalVec,node.coordinates-faces[0].simpleFaces[0].barycenter) > 0:
    #                cc.printGreen('{}: first face points in the right direction'.format(self.info_text))
    #            else:
    #                cc.printRed('{}: first face points in the wrong direction'.format(self.info_text))

                for se in unalignedFaces[0].simpleEdges:
                    simpleEdges.append(se)
                facesForVolume = [unalignedFaces[0],]
                unalignedFaces.pop(0)

                _log.debug('Starting with edges {}'.format(simpleEdges))
                count = 0
                maxCount = 50

                while len(unalignedFaces) > 0 and count < maxCount:
                    count += 1
                    # Go through all faces that are not added yet
                    found = False
                    for f in unalignedFaces:

                        # Skip, if already found
                        if not found:
                            mf = -f

                            _log.debug('Trying to add face {} with simple edges {}'.format(f.info_text,f.simpleEdges))

                            # Go through all edges in current face
                            for se in f.simpleEdges:
                                # Skip, if already found
                                if not found:
                                    mse = -se



                                # If the current edge is in the found edges and not the reversed one, then the reversed face should be added
                                    if se in simpleEdges and not mse in simpleEdges:
                                        _log.debug('Found shared simple Edge {}'.format(se.info_text))
                                        found = True
                                        facesForVolume.append(mf)
                                        unalignedFaces.remove(f)
                                        for se in mf.simpleEdges:
                                            simpleEdges.append(se)
                                        _log.debug('Simple edges so far: {}'.format(simpleEdges))

                                    # If the reversed of the current edge is in the found edges, then the face should be added
                                    elif not se in simpleEdges and mse in simpleEdges:
                                        _log.debug('Found shared simple Edge {}'.format(se.info_text))
                                        found = True
                                        facesForVolume.append(f)
                                        unalignedFaces.remove(f)
                                        for se in f.simpleEdges:
                                            simpleEdges.append(se)
                                        _log.debug('Simple edges so far: {}'.format(simpleEdges))

                                    # Detect possible errors
                                    elif se in simpleEdges and mse in simpleEdges:
                                        _log.error('One edge is not allowed to be more than twice (normal and reversed) in the same volume {}'.format(self.info_text))

                    if not found:
                        _log.error('Cannot add one of the faces {} to volume {}'.format(unalignedFaces,self.info_text))
                        count = maxCount

                self.__facesTemp = facesForVolume

                for f in facesForVolume:
                    for e in f.edges:
                        if not e in self.__edgesTemp:
                            self.__edgesTemp.append(e)


                self.faces = facesForVolume

            else:
                self.faces = unalignedFaces

#            cc.printMagenta('DualVolume3D:',unalignedFaces)
            self.setUp()
            if self.faces:
                _log.info('Created dual volume of node {}'.format(node.info_text))
                self.dualCell3D = node
                node.dualCell3D = self
            else:
                _log.error('Failed to create dual volume of node {}'.format(node.info_text))



#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getFacesTemp(self): return self.__facesTemp
    def __setFacesTemp(self,f): self.__facesTemp = f
    facesTemp = property(__getFacesTemp,__setFacesTemp)


    def __getEdgesTemp(self): return self.__edgesTemp
    def __setEdgesTemp(self,e): self.__edgesTemp = e
    edgesTemp = property(__getEdgesTemp,__setEdgesTemp)

#==============================================================================
#    METHODS
#==============================================================================

#-------------------------------------------------------------------------
#    Method 1
#-------------------------------------------------------------------------


#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':

    from tools import MyLogging
    from k_cells.node import Node
    from k_cells.edge import Edge
    from k_cells.face import Face
    import tools.placeFigures as pf

    set_logging_format(logging.DEBUG)

    a = 2
    cc.printBlue('Creating nodes')
    n0  = Node(  0,  0,  0)
    n1  = Node(  a,  0,  0)
    n2  = Node(2*a,  0,  0)
    n3  = Node(  0,  a,  0)
    n4  = Node(  a,  a,  0)
    n5  = Node(2*a,  a,  0)
    n6  = Node(  0,2*a,  0)
    n7  = Node(  a,2*a,  0)
    n8  = Node(2*a,2*a,  0)
    n9  = Node(  0,  0,  a)
    n10 = Node(  a,  0,  a)
    n11 = Node(2*a,  0,  a)
    n12 = Node(  0,  a,  a)
    n13 = Node(  a,  a,  a)
    n14 = Node(2*a,  a,  a)
    n15 = Node(  0,2*a,  a)
    n16 = Node(  a,2*a,  a)
    n17 = Node(2*a,2*a,  a)
    n18 = Node(  0,  0,2*a)
    n19 = Node(  a,  0,2*a)
    n20 = Node(2*a,  0,2*a)
    n21 = Node(  0,  a,2*a)
    n22 = Node(  a,  a,2*a)
    n23 = Node(2*a,  a,2*a)
    n24 = Node(  0,2*a,2*a)
    n25 = Node(  a,2*a,2*a)
    n26 = Node(2*a,2*a,2*a)

    nodes = [ n0, n1, n2, n3, n4, n5, n6, n7, n8, n9,
             n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,
             n20,n21,n22,n23,n24,n25,n26]


    cc.printBlue('Creating edges')
    e0  = Edge( n0, n1)
    e1  = Edge( n1, n2)
    e2  = Edge( n3, n4)
    e3  = Edge( n4, n5)
    e4  = Edge( n6, n7)
    e5  = Edge( n7, n8)
    e6  = Edge( n9,n10)
    e7  = Edge(n10,n11)
    e8  = Edge(n12,n13)
    e9  = Edge(n13,n14)
    e10 = Edge(n15,n16)
    e11 = Edge(n16,n17)
    e12 = Edge(n18,n19)
    e13 = Edge(n19,n20)
    e14 = Edge(n21,n22)
    e15 = Edge(n22,n23)
    e16 = Edge(n24,n25)
    e17 = Edge(n25,n26)

    e18 = Edge( n0, n3)
    e19 = Edge( n1, n4)
    e20 = Edge( n2, n5)
    e21 = Edge( n3, n6)
    e22 = Edge( n4, n7)
    e23 = Edge( n5, n8)
    e24 = Edge( n9,n12)
    e25 = Edge(n10,n13)
    e26 = Edge(n11,n14)
    e27 = Edge(n12,n15)
    e28 = Edge(n13,n16)
    e29 = Edge(n14,n17)
    e30 = Edge(n18,n21)
    e31 = Edge(n19,n22)
    e32 = Edge(n20,n23)
    e33 = Edge(n21,n24)
    e34 = Edge(n22,n25)
    e35 = Edge(n23,n26)

    e36 = Edge( n0, n9)
    e37 = Edge( n1,n10)
    e38 = Edge( n2,n11)
    e39 = Edge( n3,n12)
    e40 = Edge( n4,n13)
    e41 = Edge( n5,n14)
    e42 = Edge( n6,n15)
    e43 = Edge( n7,n16)
    e44 = Edge( n8,n17)
    e45 = Edge( n9,n18)
    e46 = Edge(n10,n19)
    e47 = Edge(n11,n20)
    e48 = Edge(n12,n21)
    e49 = Edge(n13,n22)
    e50 = Edge(n14,n23)
    e51 = Edge(n15,n24)
    e52 = Edge(n16,n25)
    e53 = Edge(n17,n26)



    edges = [ e0, e1, e2, e3, e4, e5, e6, e7, e8, e9,
             e10,e11,e12,e13,e14,e15,e16,e17,e18,e19,
             e20,e21,e22,e23,e24,e25,e26,e27,e28,e29,
             e30,e31,e32,e33,e34,e35,e36,e37,e38,e39,
             e40,e41,e42,e43,e44,e45,e46,e47,e48,e49,
             e50,e51,e52,e53]


    cc.printBlue('Creating faces')
    f0  = Face([ e0,e19, -e2,-e18])
    f1  = Face([ e1,e20, -e3,-e19])
    f2  = Face([ e2,e22, -e4,-e21])
    f3  = Face([ e3,e23, -e5,-e22])
    f4  = Face([ e6,e25, -e8,-e24])
    f5  = Face([ e7,e26, -e9,-e25])
    f6  = Face([ e8,e28,-e10,-e27])
    f7  = Face([ e9,e29,-e11,-e28])
    f8  = Face([e12,e31,-e14,-e30])
    f9  = Face([e13,e32,-e15,-e31])
    f10 = Face([e14,e34,-e16,-e33])
    f11 = Face([e15,e35,-e17,-e34])

    f12 = Face([ e0,e37, -e6,-e36])
    f13 = Face([ e1,e38, -e7,-e37])
    f14 = Face([ e2,e40, -e8,-e39])
    f15 = Face([ e3,e41, -e9,-e40])
    f16 = Face([ e4,e43,-e10,-e42])
    f17 = Face([ e5,e44,-e11,-e43])
    f18 = Face([ e6,e46,-e12,-e45])
    f19 = Face([ e7,e47,-e13,-e46])
    f20 = Face([ e8,e49,-e14,-e48])
    f21 = Face([ e9,e50,-e15,-e49])
    f22 = Face([e10,e52,-e16,-e51])
    f23 = Face([e11,e53,-e17,-e52])

    f24 = Face([e18,e39,-e24,-e36])
    f25 = Face([e19,e40,-e25,-e37])
    f26 = Face([e20,e41,-e26,-e38])
    f27 = Face([e21,e42,-e27,-e39])
    f28 = Face([e22,e43,-e28,-e40])
    f29 = Face([e23,e44,-e29,-e41])
    f30 = Face([e24,e48,-e30,-e45])
    f31 = Face([e25,e49,-e31,-e46])
    f32 = Face([e26,e50,-e32,-e47])
    f33 = Face([e27,e51,-e33,-e48])
    f34 = Face([e28,e52,-e34,-e49])
    f35 = Face([e29,e53,-e35,-e50])

    faces = [ f0, f1, f2, f3, f4, f5, f6, f7, f8, f9,
             f10,f11,f12,f13,f14,f15,f16,f17,f18,f19,
             f20,f21,f22,f23,f24,f25,f26,f27,f28,f29,
             f30,f31,f32,f33,f34,f35]



    cc.printBlue('Creating volumes')
    v0 = Volume([-f0, f4,f12,-f14,-f24,f25])
    v1 = Volume([-f1, f5,f13,-f15,-f25,f26])
    v2 = Volume([-f2, f6,f14,-f16,-f27,f28])
    v3 = Volume([-f3, f7,f15,-f17,-f28,f29])
    v4 = Volume([-f4, f8,f18,-f20,-f30,f31])
    v5 = Volume([-f5, f9,f19,-f21,-f31,f32])
    v6 = Volume([-f6,f10,f20,-f22,-f33,f34])
    v7 = Volume([-f7,f11,f21,-f23,-f34,f35])

    volumes = [ v0, v1, v2, v3, v4, v5, v6, v7]



    for c in nodes+edges+faces+volumes:
        c.category = 'inner'


    cc.printBlue('Plotting')
    (figs,ax) = pf.getFigures()
    for n in nodes:
        n.plotNode(ax[0])

    for e in edges:
        e.plotEdge(ax[0])

    pf.copylimits(ax[0],ax[1])
    for f in faces:
        f.plotFace(ax[1])

    pf.copylimits(ax[0],ax[2])
    for v in volumes:
        v.plotVolume(ax[2])


    from k_cells.node import DualNode3D
    from k_cells.edge import DualEdge3D
#        from kCells.face import DualFace3D
    for v in volumes:
        n = DualNode3D(v)
        n.plotNode(ax[2])

    for f in [f25,f15,f5,f7,f4,f6,f31,f34,f14,f20,f21,f28]:
        f.plotFace(ax[0])
        e = DualEdge3D(f)
        e.plotEdge(ax[1])


    for e in [e25,e9,e28,e8,e49,e40]:
        e.plotEdge(ax[2])
        f = DualFace3D(e)
        f.plotFace(ax[2])





    dv = DualVolume3D(n13)

    dv.plotVolume(ax[0])
