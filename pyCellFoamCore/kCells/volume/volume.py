# -*- coding: utf-8 -*-
#==============================================================================
# VOLUME
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Jan 26 13:34:49 2018


'''
This is the explanation of the whole module and will be printed at the very
beginning


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

import numpy as np
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#from tumcolor import TUMcolor
import tools.tumcolor as tc
#from cell import Cell
import tools.colorConsole as cc
#import logging


from kCells import Cell

from tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


#==============================================================================
#    CLASS DEFINITION
#==============================================================================
class Volume(Cell):

    volumeCount = 0


#==============================================================================
#    SLOTS
#==============================================================================
#    __slots__ = ('__faces',
#                 '__rawFaces',
#                 '__barycenter','__showBarycenter',
#                 '__volume','__unalignedFaces')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,rawFaces,*args,num=None,label='v',unalignedFaces=False,**kwargs):
        if num == None:
            num = Volume.volumeCount
            Volume.volumeCount += 1

        super().__init__(*args,num=num,label=label,myReverse=False,loggerName=__name__,**kwargs)

        self.__rawFaces = rawFaces
        self.__faces =[]
        self.__barycenter = None
        self.__volume = None
        self.__showBarycenter = True
        self.__unalignedFaces = unalignedFaces
        self.color =  tc.TUMRose()
        self.setUp()
        _log.info('Created volume {}'.format(self.infoText))
        _log.debug('Initialized Node')






#==============================================================================
#    SETTER AND GETTER
#==============================================================================



    def __getVolume(self):
        if self.geometryChanged:
            self.setUp()
        return self.__volume
    volume = property(__getVolume)

    def __getBarycenter(self):
        if self.geometryChanged:
            self.setUp()
        return self.__barycenter
    barycenter = property(__getBarycenter)


    def __getFaces(self):
        if self.geometryChanged:
            self.setUp()
        return self.__faces
    def __setFaces(self,f):
        self.__rawFaces = f
        self.updateGeometry()
    faces = property(__getFaces,__setFaces)


    def __getShowBarycenter(self): return self.__showBarycenter
    def __setShowBarycenter(self,s): self.__showBarycenter = s
    showBarycenter =  property(__getShowBarycenter,__setShowBarycenter)

    def __getAlignFaces(self): return self.__alignFaces
    alignFaces = property(__getAlignFaces)
#
#
    def __getCategory(self): return super().category
    def __setCategory(self,c):
        self.category1 = c
        self.category2 = c
#        super(Cell,self).category2 = c
    category = property(__getCategory,__setCategory)
#
#    def __getCategory1(self): return super().category1
#    category1 = property(__getCategory1)
#
#    def __getCategory2(self): return super().category2
#    category2 = property(__getCategory2)


#==============================================================================
#    METHODS
#==============================================================================


    def setUp(self):
#        cc.printGreen('Volume: setting up')
        # Remove this volume from all old faces
        for s in self.__faces:
            s.delVolume(self)
        # (Re-)create volume
        if self.__unalignedFaces:
            self.__alignFaces()

        if self.__checkClosed(self.__rawFaces):
            self.__faces = self.__rawFaces
            self.__calcVolume()
            if self.__volume < 0:
                newFaces = [-f for f in self.__faces]
                _log.debug('{}: Faces pointed in the wrong direction'.format(self.infoText))
                self.__faces = newFaces
                self.__calcVolume()

            for s in self.__faces:
                s.addVolume(self)
            self.__calcBarycenter()
            self.geometryChanged = False
            _log.debug('Succesfully set up volume {}'.format(self.infoText))

        else:
            self.__faces = []

# ------------------------------------------------------------------------
#    Delete the entire volume
# ------------------------------------------------------------------------
    def delete(self):
        self.__rawFaces = []
        self.setUp()
        super().delete()



    def printVolume(self,printFaces=True,printEdges=False,printNodes=False):
        print('================================================================')
        print('================================================================')
        cc.printMagentaBackground('   ',end='')
        print(' Volume Number',self.num)#,self.infoText)
        print('================================================================')
        print('================================================================')
        print()
        print()
        numFaces = []
        for f in self.__faces:
                numFaces.append(f.num)

        print("Includes Faces:",numFaces)
        print()
        if printFaces:
            for f in self.__faces:
                f.printFace(printEdges,printNodes)
        print()
        print('================================================================')
        print('================================================================')
        print()
        print()
        print()



    def __alignFaces(self):
#        cc.printGreen('Volume: aligning faces')

        faces = self.__rawFaces.copy()

        myPrintDebug = _log.debug
#        myPrintDebug = cc.printYellow
        myPrintInfo = _log.info
        myPrintError = _log.error


        simpleEdges = []

        # Check if the normal vector points outwards
#            if np.dot(faces[0].simpleFaces[0].normalVec,node.coordinates-faces[0].simpleFaces[0].barycenter) > 0:
#                cc.printGreen('{}: first face points in the right direction'.format(self.infoText))
#            else:
#                cc.printRed('{}: first face points in the wrong direction'.format(self.infoText))

        # Do not do this if there are no faces
        if faces:
            for se in faces[0].simpleEdges:
                simpleEdges.append(se)
            facesForVolume = [faces[0],]
            faces.pop(0)

            myPrintDebug('Starting with edges {}'.format(simpleEdges))
            count = 0
            maxCount = 50

            while len(faces) > 0 and count < maxCount:
                count += 1
                # Go through all faces that are not added yet
                found = False
                for f in faces:

                    # Skip, if already found
                    if not found:
                        mf = -f

                        myPrintDebug('Trying to add face {} with simple edges {}'.format(f.infoText,f.simpleEdges))

                        # Go through all edges in current face
                        for se in f.simpleEdges:
                            # Skip, if already found
                            if not found:
                                mse = -se



                            # If the current edge is in the found edges and not the reversed one, then the reversed face should be added
                                if se in simpleEdges and not mse in simpleEdges:
                                    myPrintDebug('Found shared simple Edge {}'.format(se.infoText))
                                    found = True
                                    facesForVolume.append(mf)
                                    faces.remove(f)
                                    for se in mf.simpleEdges:
                                        simpleEdges.append(se)
                                    myPrintDebug('Simple edges so far: {}'.format(simpleEdges))

                                # If the reversed of the current edge is in the found edges, then the face should be added
                                elif not se in simpleEdges and mse in simpleEdges:
                                    myPrintDebug('Found shared simple Edge {}'.format(se.infoText))
                                    found = True
                                    facesForVolume.append(f)
                                    faces.remove(f)
                                    for se in f.simpleEdges:
                                        simpleEdges.append(se)
                                    myPrintDebug('Simple edges so far: {}'.format(simpleEdges))

                                # Detect possible errors
                                elif se in simpleEdges and mse in simpleEdges:
                                    myPrintError('One edge is not allowed to be more than twice (normal and reversed) in the same volume {}'.format(self.infoText))

                if not found:
                    myPrintError('Cannot add one of the faces {} to volume {}'.format(faces,self.infoText))
                    count = maxCount

    #        self.__facesTemp = facesForVolume

    #        for f in facesForVolume:
    #            for e in f.edges:
    #                if not e in self.__edgesTemp:
    #                    self.__edgesTemp.append(e)


            self.__rawFaces = facesForVolume
        else:
            self.__rawFaces = []








    def __checkClosed(self,faces):
        closed = True
        simpleEdges = []
        for f in faces:
            for e in f.edges:
#                print(e.num)
                for se in e.simpleEdges:
                    if se in simpleEdges:
                        _log.error('Error, simple edge {} occurs twice in volume {} which is not allowed'.format(se.infoText,self))
                        closed = False
                    else:
                        simpleEdges.append(se)

        for se in simpleEdges :
            mse = -se
            if not mse in simpleEdges:
                _log.error('Error, simple edge {} in the volume {} has no counterpart'.format(se.infoText,self.infoText))
                closed = False
        return closed


    def __calcBarycenter(self):
        r'''
        Calculate the barycenter of a 3-cell :math:`P` (which is confusingly
        also called volume).
        The formula is taken from here_.

        .. _here: http://www.ma.ic.ac.uk/~rn/centroid.pdf

        The barycenter in general can be calculated with the integral

        .. math::

            \mathbf{c} = \frac{1}{V} \iiint\limits_P \mathbf{x} \; \mathrm{d} V

        with :math:`\mathbf{x}` beeing the vector to each point in
        :math:`\mathbf{P}` and :math:`V` beeing the volume of :math:`P`.


        Applying the divergence theorem leads to:

        .. math::

            \mathbf{c} = \frac{1}{V} \iint\limits_{\partial P} \frac{1}{2} \mathbf{x}^\mathrm{T} \mathbf{x} \mathbf{n}   \; \mathrm{d} A

        For convenience we look at it coordinate wise:

        .. math::

            c_j = \frac{1}{V} \iint\limits_{\partial P} \frac{1}{2}  x_j^2 n_j   \; \mathrm{d} A

        The surface of the :math:`P` is devided into triangles, which gives us:

        .. math::

            c_j = \sum_i \iint\limits_{A_i} \frac{1}{2}  x_j^2 n_{i,j}   \; \mathrm{d} A

        The integral can be calculated by the midpoint formula. We denote the
        vectors to the corners of the triangle by :math:`o`, :math:`a` and
        :math:`b`.

        .. math::

            c_j = \frac{1}{24 V} \sum_i  A_i n_{j,i} \left(
                            (o_{i,j} + a_{i,j})^2
                            (o_{i,j} + b_{i,j})^2
                            (a_{i,j} + b_{i,j})^2
                            \right)

        As a reminder: :math:`i` is the index of the triangle, :math:`j` is the
        index of the dimension


        '''
        bc = np.array([0.,0.,0.])
        if len(self.__faces)>0:

            # Go through all 3 dimensions
            for d in range(3):
                e = np.zeros(3)
                e[d] = 1

                # Go through all faces in volume
                for f in self.__faces:

                    # Go through all simple faces in current face
                    for sf in f.simpleFaces:

                        # Choose first corner of simple face as local origin for all triangles
                        o = sf.coordinates[0]

                        # Build little triangles, with one corner always beeing the origin
                        # Attention, the same order as for the calculation of the area is used
                        # Therefor the areas do not have to be recalculated
                        for (n,(x,y)) in enumerate(zip(sf.coordinates[1:-1],sf.coordinates[2:])):
#                            tempvalue = sf.area[0][n] * np.dot(sf.normalVec,e)*((np.dot(o+x,e))**2+(np.dot(o+y,e))**2+(np.dot(x+y,e))**2)
                            bc[d] += sf.area[0][n] * sf.normalVec[d]*((o[d]+x[d])**2+(o[d]+y[d])**2+(x[d]+y[d])**2)

            if self.__volume < 1E-3:
                _log.error('{}: volume is close to zero or negative: {}'.format(self.infoText,self.__volume))
            else:
                bc = bc/(24*self.__volume)
        self.__barycenter = bc



    def __calcVolume(self):
        r'''
        Calculate the volume of a 3-cell :math:`P` (which is confusingly also
        called volume).
        The formula is taken from here_ and adapted for non triangular faces.

        .. _here: http://www.ma.ic.ac.uk/~rn/centroid.pdf

        We start with the simple calculation of the volume by integration:

        .. math::

            V = \iiint\limits_P 1 \; \mathrm{d}V

        Applying the divergence theorem leads to:

        .. math::

            V = \frac{1}{3} \iint\limits_{\partial P} \mathbf{x}^\mathrm{T}
            \mathbf{n} \; \mathrm{d} A

        with :math:`\mathbf{x}` beeing the vector to each point on
        :math:`\partial P` and the normalized normal vector :math:`\mathbf{n}`.
        Using the fact that :math:`\mathbf{x}^\mathrm{T} \mathbf{n}` is
        constant on each face (namely the perpendicular distance from the
        origin to the face) and assuming that the area :math:`A_i` of each face
        is known, we can rewrite the integral as the sum

        .. math::

            V =  \sum_i \frac{1}{3} A_i \mathbf{x}_i^\mathrm{T} \mathbf{n}_i

        where :math:`\mathbf{x}_i` is the vector to an arbitrary point on the
        :math:`i`-th face.


        '''

        volume = 0
        for f in self.__faces:
            for sf in f.simpleFaces:
                volume += 1/3*sf.area[1]*np.dot(sf.coordinates[0],sf.normalVec)
        self.__volume = volume


    def plotTemp(self,ax,temp,tempMin,tempMax):

        TUMBlue = np.array([0, 51, 89]) * (tempMax-temp)/(tempMax-tempMin)
        TUMOrange = np.array([247,166,0]) * (temp-tempMin)/(tempMax-tempMin)
        color = self.__rgbToHex(TUMBlue+TUMOrange)

        for f in self.faces:
            f.color = color
            f.showLabel = False
            f.showNormalVec = False
            f.plotFace(ax)



    def __rgbToHex(self,rgb):
        return('#'+self.__numToHex(rgb[0])+self.__numToHex(rgb[1])+self.__numToHex(rgb[2]))

    def __numToHex(self,num):
        s = hex(int(num))[2:]
        if len(s) == 1:
            s = '0'+s
        elif len(s) != 2:
            s = '00'
        return s

    def plotVolume(self,ax,showNormalVec = False,showLabel=None,showBarycenter=None,color=None,**kwargs):
        if self.faces:
            if color is None:
                color = self.color
            if showLabel == None:
                showLabel = self.showLabel
            if showBarycenter == None:
                showBarycenter = self.showBarycenter
            if self.geometryChanged:
                self.setUp()
            for f in self.__faces:
                f.plotFace(ax,showNormalVec=showNormalVec,showLabel=False,showBarycenter=False,color=color,**kwargs)
            if showBarycenter:
                ax.scatter(self.__barycenter[0],self.__barycenter[1],self.__barycenter[2],c=self.color.html)
            if showLabel:
                ax.text(self.barycenter[0],self.barycenter[1],self.barycenter[2],self.labelText,color=self.color.html)
        else:
            _log.error('Cannot plot empty volume {}'.format(self))



    def plotVolumeTikZ(self,pic,showLabel=None,color=None,shortLabel=True,**kwargs):

        if color is None:
            color = self.color

        if showLabel is None:
            showLabel = self.showLabel



        labelOptions = [color.name,]

        for f in self.faces:
            f.plotFaceTikZ(pic,showLabel=False,color=color,**kwargs)

        if showLabel:
            if shortLabel:
                tikZLabelText = self.labelTextShort
            else:
                tikZLabelText = self.labelText
        else:
            tikZLabelText = ''



        n = pic.addTikZNode(self.tikZName,self.barycenter,content=tikZLabelText,options=labelOptions)





    def plotVolumeTikZOld(self,*args,showLabel=True,color=None,**kwargs):

        if self.grayInTikz or not self.showInPlot:
            return ''
        else:
            colorFaces = color
            optionsNode = []

            if color is True:
                optionsNode.append(self.color.name)
                colorFaces = self.color
            elif color:
                optionsNode.append(color)

            optionsNodeText = ''
            if optionsNode:
                optionsNodeText = '['+','.join(optionsNode)+']'


            tikzText = ''

            if showLabel:
                tikzText += '\\node{} ({}) at ({}) {{{}}};\n'.format(optionsNodeText,self.tikZName,self.tikzCoords(self.barycenter),self.labelText)


            for f in self.faces:
                tikzText += f.plotFaceTikZ(*args,showLabel=False,grayInTikz=False,color=colorFaces,fill=True,draw=True,**kwargs)
            return tikzText









#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == "__main__":
    import tools.placeFigures as pf
    from kCells.node import Node
    from kCells.edge import Edge
    from kCells.face import Face


    set_logging_format(logging.DEBUG)



#        # Close all existing figures
#        plt.close("all")
#
    # Create new figures
    (figs,ax) = pf.getFigures(numTotal = 4)
#
#        cc.printBlue('Creating some nodes')
#        n1 = Node(0,0,0,num=1)
#        n2 = Node(1,0,0,num=2)
#        n3 = Node(1,1,0,num=3)
#        n4 = Node(0,1,0,num=4)
#        n5 = Node(0,0,1,num=5)
#        n6 = Node(1,0,1,num=6)
#        n7 = Node(1,1,1,num=7)
#        n8 = Node(0,1,1,num=8)
#        n9 = Node(0,0,2,num=5)
#        n10 = Node(1,0,2,num=6)
#        n11 = Node(1,1,2,num=7)
#        n12 = Node(0,1,2,num=8)
#
#        nodes = [n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12]
#        for n in nodes:
#            n.plotNode(ax[0])
#
#        cc.printBlue('Creating some edges')
#        # Create some Edges
#        e1 = Edge(n1,n2,num=1)
#        e2 = Edge(n2,n3,num=2)
#        e3 = Edge(n3,n4,num=3)
#        e4 = Edge(n4,n1,num=4)
#        e5 = Edge(n1,n5,num=5)
#        e6 = Edge(n2,n6,num=6)
#        e7 = Edge(n3,n7,num=7)
#        e8 = Edge(n4,n8,num=8)
#        e9 = Edge(n5,n6,num=9)
#        e10 = Edge(n6,n7,num=10)
#        e11 = Edge(n7,n8,num=11)
#        e12 = Edge(n8,n5,num=12)
#        e13 = Edge(n5,n9,num=13)
#        e14 = Edge(n6,n10,num=14)
#        e15 = Edge(n7,n11,num=15)
#        e16 = Edge(n8,n12,num=16)
#        e17 = Edge(n9,n10,num=17)
#        e18 = Edge(n10,n11,num=18)
#        e19 = Edge(n11,n12,num=19)
#        e20 = Edge(n12,n9,num=20)
#
#        edges = [e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13,e14,e15,e16,e17,e18,e19,e20]
#        for e in edges:
#            e.plotEdge(ax[0])
#
#
#        cc.printBlue('Creating some Faces')
#        f1 = Face([-e4,-e3,-e2,-e1],num=1)
#        f2 = Face([e1,e6,-e9,-e5],num=2)
#        f3 = Face([e2,e7,-e10,-e6],num=3)
#        f4 = Face([e3,e8,-e11,-e7],num=4)
#        f5 = Face([e4,e5,-e12,-e8],num=5)
#        f6 = Face([e9,e10,e11,e12],num=6)
#        f7 = Face([e9,e14,-e17,-e13],num=7)
#
#
#        faces = [f1,f2,f3,f4,f5,f6,f7]
#        for f in faces:
#            f.plotFace(ax[0])




#        print()
#        cc.printBlue('Creating volume with one missing face, this should fail',printImmediately=True)
#        v1 = Volume([f1,f2,f3,f4,f5],num=1)
#
#        print()
#        cc.printBlue('Creating volume with one wrong face, this should fail',printImmediately=True)
#        v1 = Volume([f1,f2,f3,f4,f6,f7],1)
#
##        print()
#        cc.printBlue('Creating volume with correct faces, this should work',printImmediately=True)
#        v1 = Volume([f1,f2,f3,f4,f5,f6],num=1)
#        print()
#
#        cc.printBlue('Interested in the volume of the 3-cell:',printImmediately=True)
#        cc.printGreen(v1.volume)
#        print()
#
#        cc.printBlue('Check barycenter:',printImmediately=True)
#        cc.printGreen(v1.barycenter)
#        print()
#
#        cc.printBlue('Check faces:')
#        cc.printGreen(v1.faces)
#
#
#
#        for n in [n1,n2,n3,n4]:
#            n.xCoordinate = n.xCoordinate+0.2
#        v1.plotVolume(ax[1])
#


#        print()
#        print()
#        print()
#
#
#
#
#
    # Create some Nodes
    n101 = Node(0,0,0, num=101)
    n102 = Node(10,0,0, num=102)
    n103 = Node(0,10,0, num=103)
    n104 = Node(0,0,10, num=104)
    nodes100 = [n101,n102,n103,n104]
    for n in nodes100:
        n.plotNode(ax[1])

    e101 = Edge(n101,n102, num=101)
    e102 = Edge(n102,n103, num=102)
    e103 = Edge(n103,n101, num=103)
    e104 = Edge(n101,n104, num=104)
    e105 = Edge(n102,n104, num=105)
    e106 = Edge(n103,n104, num=106)
    edges100 = [e101,e102,e103,e104,e105,e106]
    for e in edges100:
        e.plotEdge(ax[1])

    f101 = Face([e101,e105,-e104])
    f102 = Face([e102,e106,-e105])
    f103 = Face([e103,e104,-e106])
    f104 = Face([-e103,-e102,-e101])
    faces100 = [f101,f102,f103,f104]

    for f in faces100:
        f.plotFace(ax[1])

    v101 = Volume([f101,f102,f103,-f104],unalignedFaces=True)

    # v101.plotVolume(ax[0])

#        print([f.area[1] for f in Faces100])






    # cc.printBlue('Volume of {}: {}'.format(v101,v101.volume))
#
    # v101 = Volume([],unalignedFaces=True)

    # v101.category = 'inner'
    # print(v101.category,v101.category1,v101.category2)


    new_node = Node(5, 0, 0)

    new_edge_1 = Edge(n101, new_node)
    new_edge_2 = Edge(new_node, n102)

    f101.edges = [new_edge_1,new_edge_2,e105,-e104]
    f104.edges = [-e103,-e102,-new_edge_2, -new_edge_1]


    nodes_in_volume = []
    edges_in_volume = []
    faces_in_volume = v101.faces

    for f in faces_in_volume:
        for e in f.edges:
            if e.isReverse:
                e = -e
            if not e in edges_in_volume:
                edges_in_volume.append(e)

    for e in edges_in_volume:
        for n in [e.startNode, e.endNode]:
            if not n in nodes_in_volume:
                nodes_in_volume.append(n)


    v101.plotVolume(ax[0])

    for n in nodes_in_volume:
        n.plotNode(ax[2])

    for e in edges_in_volume:
        e.plotEdge(ax[2])

    for f in faces_in_volume:
        f.plotFace(ax[2])



    pf.setAxesEqual(ax[1])
    ax[1].view_init(20,140)
#



#
#
#
#        n201 = Node(-1/6*np.sqrt(3),0.5,0,1)
#        n202 = Node(-1/6*np.sqrt(3),-0.5,0,2)
#        n203 = Node(1/3*np.sqrt(3),0,0,3)
#        n204 = Node(0,0,1/3*np.sqrt(6),4)
#        nodes200 = [n201,n202,n203,n204]
#        for n in nodes200:
#            n.plotNode(ax[2])
#
#        e201 = Edge(n201,n202,1)
#        e202 = Edge(n202,n203,2)
#        e203 = Edge(n203,n201,3)
#        e204 = Edge(n201,n204,4)
#        e205 = Edge(n202,n204,5)
#        e206 = Edge(n203,n204,6)
#        edges200 = [e201,e202,e203,e204,e205,e206]
#        for e in edges200:
#            e.plotEdge(ax[2])
#
#
#        f201 = Face([e201,e205,-e204],1)
#        f202 = Face([e202,e206,-e205],2)
#        f203 = Face([e203,e204,-e206],3)
#        f204 = Face([-e203,-e202,-e201],4)
#        faces200 = [f201,f202,f203,f204]
#
#        for f in faces200:
#            f.plotFace(ax[2])
#        ax[1].set_zlim3d(-1,2)
#        ax[1].set_xlim3d(-1,2)
#        ax[1].set_ylim3d(-1,2)
#
#        v201 = Volume([f201,f202,f203,f204],201)
#
#
#
#
#    #    print([f.area[1] for f in Faces])
#        cc.printBlue('Volume of {}: {}'.format(v201,v201.volume))
#
#
#        cc.printBlue('Barycenter of {}: {}'.format(v1,v1.barycenter))
#        v1.plotVolume(ax[0])
#        v101.plotVolume(ax[1])
#        v201.plotVolume(ax[2])
#
#        f8 = Face([e10,e15,-e18,-e14],8)
#        f9 = Face([e11,e16,-e19,-e15],9)
#        f10 = Face([e12,e13,-e20,-e16],10)
#        f11 = Face([e17,e18,e19,e20],11)
#        faces.append(f8)
#        faces.append(f9)
#        faces.append(f10)
#        faces.append(f11)
#
#    #    for f in Faces:
#    #        f.plotFace(ax[3])
#
#        v2 = Volume([-f6,f7,f8,f9,f10,f11],2)
#    #    v2.plotVolume(ax[3])

