# -*- coding: utf-8 -*-
# =============================================================================
# 3D CUBIC GRID
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue Aug 21 14:54:18 2018

'''
Creates a primal complex on a cubic grid.
To construct the cubic grid a class Cube is defined that can extend a given
grid by one cube and connect it to the existing nodes.
The construction of the grid is done in the PrimalComplex3DCubic class.

'''
# =============================================================================
#    IMPORTS
# =============================================================================
if __name__ == '__main__':
    import os
    os.chdir('../')

from kCells import Node
from kCells import Edge
from kCells import Face
from kCells import Volume
from complex import PrimalComplex3D, DualComplex3D
from tools import MyLogging
import tools.placeFigures as pf
import numpy as np
import tools.colorConsole as cc
import tools.tumcolor as tc


# =============================================================================
#    CUBE CLASS DEFINITION
# =============================================================================
class Cube:
    '''
    The following local numbering is used:

    .. image:: ../../../_static/grid3DCubicCube0.png
       :width: 400px
       :alt: 3D cubic grid nodes and edges
       :align: center

    .. image:: ../../../_static/grid3DCubicCube1.png
       :width: 400px
       :alt: 3D cubic grid edges and faces
       :align: center

    '''

# =============================================================================
#    CUBE SLOTS
# =============================================================================
#    __slots__ = ()

# =============================================================================
#    CUBE INITIALIZATION
# =============================================================================
    def __init__(self, x, y, z, a,
                 n0old=False,
                 n1old=False,
                 n2old=False,
                 n3old=False,
                 n4old=False,
                 n5old=False,
                 n6old=False,
                 n7old=False):
        '''

        :param float x: x-coordinate of cube center
        :param float y: x-coordinate of cube center
        :param float z: x-coordinate of cube center
        :param Node nIold: node that was created by another cube. Use this to
            connect cubes. I is the local number in this cube.



        '''

        # Store coordinates
        self.x = x
        self.y = y
        self.z = z

        # Create nodes
        self.n0 = self.__createNode(x-a/2, y-a/2, z-a/2, n0old)
        self.n1 = self.__createNode(x+a/2, y-a/2, z-a/2, n1old)
        self.n2 = self.__createNode(x-a/2, y+a/2, z-a/2, n2old)
        self.n3 = self.__createNode(x+a/2, y+a/2, z-a/2, n3old)
        self.n4 = self.__createNode(x-a/2, y-a/2, z+a/2, n4old)
        self.n5 = self.__createNode(x+a/2, y-a/2, z+a/2, n5old)
        self.n6 = self.__createNode(x-a/2, y+a/2, z+a/2, n6old)
        self.n7 = self.__createNode(x+a/2, y+a/2, z+a/2, n7old)
        self.nodes = [self.n0, self.n1, self.n2, self.n3, self.n4, self.n5, self.n6, self.n7]

        # Create edges
        self.e0 = self.__createEdge(self.n0, self.n1)
        self.e1 = self.__createEdge(self.n2, self.n3)
        self.e2 = self.__createEdge(self.n4, self.n5)
        self.e3 = self.__createEdge(self.n6, self.n7)
        self.e4 = self.__createEdge(self.n0, self.n2)
        self.e5 = self.__createEdge(self.n1, self.n3)
        self.e6 = self.__createEdge(self.n4, self.n6)
        self.e7 = self.__createEdge(self.n5, self.n7)
        self.e8 = self.__createEdge(self.n0, self.n4)
        self.e9 = self.__createEdge(self.n1, self.n5)
        self.e10 = self.__createEdge(self.n2, self.n6)
        self.e11 = self.__createEdge(self.n3, self.n7)
        self.edges = [self.e0, self.e1, self.e2, self.e3,
                      self.e4, self.e5, self.e6, self.e7,
                      self.e8, self.e9, self.e10, self.e11]

        # Create faces
        self.f0 = self.__createFace([self.e0, self.e5, -self.e1, -self.e4])
        self.f1 = self.__createFace([self.e2, self.e7, -self.e3, -self.e6])
        self.f2 = self.__createFace([self.e0, self.e9, -self.e2, -self.e8])
        self.f3 = self.__createFace([self.e1, self.e11, -self.e3, -self.e10])
        self.f4 = self.__createFace([self.e4, self.e10, -self.e6, -self.e8])
        self.f5 = self.__createFace([self.e5, self.e11, -self.e7, -self.e9])
        self.faces = [self.f0, self.f1, self.f2, self.f3, self.f4, self.f5]

        # Create volumes
        self.volume = Volume([-self.f0, self.f1, self.f2, -self.f3, -self.f4, self.f5])

# =============================================================================
#    CUBE MAGIC METHODS
# =============================================================================

    def  __repr__(self):
        return '🎲'+self.volume.infoText

# =============================================================================
#    CUBE METHODS
# =============================================================================

# ------------------------------------------------------------------------
#    Create node
# ------------------------------------------------------------------------
    def __createNode(self, x, y, z, nodeOld):
        '''
        Creating node at given location if no old node is given.

        :param int x: x-Coordinate of the node
        :param int y: y-Coordinate of the node
        :param int z: z-Coordinate of the node
        :param nodeOld: old node, if it already existed

        :return: New node

        '''

        if not nodeOld:
            return Node(x, y, z)
        else:
            return nodeOld

# ------------------------------------------------------------------------
#    Create edge
# ------------------------------------------------------------------------
    def __createEdge(self, n1, n2):
        '''
        Creating edge between two given nodes. If the edge already existed, the
        existing edge is returned.

        :param Node n1: Start node
        :param Node n2: End node
        :return: Edge betweend given nodes

        '''
        edgeExisted = False
        for e in n1.edges:
            if e.startNode == n2 or e.endNode == n2:
                edgeExisted = True
                oldEdge = e
        if not edgeExisted:
            return Edge(n1, n2)
        else:
            return oldEdge
# ------------------------------------------------------------------------
#    Create face
# ------------------------------------------------------------------------
    def __createFace(self, edges):
        '''
        Creating face between given edges. If the face already existed, the
        existing face is returned.

        :param Edge edges: list of edges to define face
        :return: Face defined by given edges

        '''

        # If an error occured in edge creation, do not create face
        if any([e == False for e in edges]):
            return False

        # Check if face already exists
        faceExisted = False
        facesOld = []
        for e in edges:
            for f in e.faces:
                if not f in facesOld:
                    facesOld.append(f)
                    facesOld.append(-f)
        for f in facesOld:
            if all([e in edges for e in f.edges]):
                faceExisted = True
                oldFace = f

        # Return face accordingly
        if not faceExisted:
            return Face(edges)
        else:
            return oldFace

# ------------------------------------------------------------------------
#    Set numbers to local numbering
# ------------------------------------------------------------------------
    def setLocalNumbering(self):
        for (i, n) in enumerate(self.nodes):
            n.num = i
        for (i, e) in enumerate(self.edges):
            e.num = i
        for (i, f) in enumerate(self.faces):
            f.num = i


# ------------------------------------------------------------------------
#    Plot cube
# ------------------------------------------------------------------------
    def plotCube(self, ax, plotNodes=True, plotEdges=True, plotFaces=True, **kwargs):
        if plotNodes:
            for n in self.nodes:
                n.plotNode(ax, **kwargs)
        if plotEdges:
            for e in self.edges:
                e.plotEdge(ax, **kwargs)
        if plotFaces:
            for f in self.faces:
                f.plotFace(ax, **kwargs)

# ------------------------------------------------------------------------
#    Plots for documentation
# ------------------------------------------------------------------------
    @classmethod
    def plotDoc(cls):
        '''
        Class method that creates all plots needed in the documentation.

        '''

        # Prepare figures
        (figs, ax) = pf.getFigures(numTotal=2)

        # Create a cube
        cube = Cube(0, 0, 0, 5)

        # Set numbering to local
        cube.setLocalNumbering()

        # Plot nodes & edges
        cube.plotCube(ax[0], plotFaces=False)

        # Plot edges & faces
        cube.plotCube(ax[1], plotNodes=False)

        # Export png files
        pf.exportPNG(figs[0], 'doc/_static/grid3DCubicCube0.png')
        pf.exportPNG(figs[1], 'doc/_static/grid3DCubicCube1.png')



#####################################################################################
#                           #####                                                   #
#                          #     #  #####      #    #####                           #
#                          #        #    #     #    #    #                          #
#                          #  ####  #    #     #    #    #                          #
#                          #     #  #####      #    #    #                          #
#                          #     #  #   #      #    #    #                          #
#                           #####   #    #     #    #####                           #
#                                                                                   #
#####################################################################################


# =============================================================================
#    GRID CLASS DEFINITION
# =============================================================================
def getComplexCubic(*args, **kwargs):
    raise NameError('This method is deprecated. Use PrimalComplex3DCubic class instead')

class Grid3DCubic(PrimalComplex3D):
    '''
    The Grid is constructed in the following steps:




    **Step 1: First cube in first row of first layer**

    The first cube is located at the origin.

    .. image:: ../../../_static/grid3DCubicComplex0.png
       :width: 400px
       :alt: cubic grid step 1
       :align: center




    **Step 2: First row in first layer**

    Cubes to the first row are added. The local nodes 0, 2, 4 and 6 are taken
    from the previous cube in x-direction

    .. image:: ../../../_static/grid3DCubicComplex1.png
       :width: 400px
       :alt: cubic grid step 2
       :align: center





    **Step 3: First cube in other rows of current layer**

    The other rows are started with a cube where the local nodes 0, 1, 4 and 5
    are taken from the previous cube in y-direction.

    .. image:: ../../../_static/grid3DCubicComplex2.png
       :width: 400px
       :alt: cubic grid step 3
       :align: center




    **Step 4: Other cubes in current layer**

    The layer is completed with cubes that have a predecessor in x- and in y-
    direction. Nodes 0, 1, 2, 4, 5 and 6 already exist.

    .. image:: ../../../_static/grid3DCubicComplex3.png
       :width: 400px
       :alt: cubic grid step 4
       :align: center



    **Step 5: First cube in first row of current layer**

    A new layer is started with a cube that is connected to the pevious layer
    by nodes 0, 1, 2 and 3 from previous cube in z-direction.

    .. image:: ../../../_static/grid3DCubicComplex4.png
       :width: 400px
       :alt: cubic grid step 5
       :align: center





    **Step 6: Other cubes in first row in current layer**

    The first row is filled with cubes that have a predecesser in x- and z-
    direction. Nodes 0, 1, 2, 3, 4 and 6 already exist.

    .. image:: ../../../_static/grid3DCubicComplex5.png
       :width: 400px
       :alt: cubic grid step 6
       :align: center




    **Step 7: First cube in current row of current layer**

    The following rows start with a cube where nodes 0, 1, 2, 3, 4 and 5 are
    known from the predecessor in y- and z-direction.

    .. image:: ../../../_static/grid3DCubicComplex6.png
       :width: 400px
       :alt: cubic grid step 7
       :align: center




    **Step 8: Other cubes in current row of current layer**

    In the final step, the whole grid is fille with cubes where nodes
    0, 1, 2, 3, 4, 5 and 6 are known from the predecessors in all three
    directions (only node 7 needs to be created)

    .. image:: ../../../_static/grid3DCubicComplex7.png
       :width: 400px
       :alt: cubic grid step 8
       :align: center




    '''
# =============================================================================
#    SLOTS
# =============================================================================
    __slots__ = ('__cubeStack')


# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self,
                 xNum,
                 yNum=None,
                 zNum=None,
                 borderVolumesBottom=False,
                 borderVolumesTop=False,
                 borderVolumesFront=False,
                 borderVolumesBack=False,
                 borderVolumesLeft=False,
                 borderVolumesRight=False,
                 borderVolumesAll=False,
                 a = 3.):

        '''

        :param xNum: number of cubes in x-direction
        :param yNum: number of cubes in y-direction (leave empty to set equal
                     to xNum)
        :param zNum: number of cubes in z-direction (leave empty to set equal
                     to xNum)
        :param borderVolumesX: Set all volumes at the according border as a
                               border Volume. X = Bottom, Top, Front, Back,
                               Left, Right, All

        '''

        if yNum == None:
            yNum = xNum
        if zNum == None:
            zNum = xNum



        if borderVolumesAll:
            borderVolumesBottom=True
            borderVolumesTop=True
            borderVolumesFront=True
            borderVolumesBack=True
            borderVolumesLeft=True
            borderVolumesRight=True



# Step 1: First cube in first row of first layer
# ---------------------------------------------------------------------
#            +----+----+----+
#           /    /    /    /|
#          /    /    /    / |
#         +----+----+----+  +
#        /    /    /    /| /|
#       /    /    /    / |/ |
#      +----+----+----+  +  +
#      |    |    |    | /| /|
#      |    |    |    |/ |/ |
#      +----+----+----+  +  +
#      |    |    |    | /| /
#      |    |    |    |/ |/
#      +----+----+----+  +
#      |XXXX|    |    | /
#      |XXXX|    |    |/
#      +----+----+----+

        row = [Cube(a/2, a/2, a/2, a)]



        for i in range(xNum-1):
            preCube = row[-1]
# Step 2: First row in first layer
# ---------------------------------------------------------------------
#            +----+----+----+
#      	    /    /    /    /|
#          /    /    /    / |
#         +----+----+----+  +
#        /    /    /    /| /|
#       /    /    /    / |/ |
#      +----+----+----+  +  +
#      |    |    |    | /| /|
#      |    |    |    |/ |/ |
#      +----+----+----+  +  +
#      |    |    |    | /| /
#      |    |    |    |/X|/
#      +----+----+----+XX+
#      |XXXX|XXXX|XXXX|X/
#      |XXXX|XXXX|XXXX|/
#      +----+----+----+
            row.append(Cube(x = preCube.x+a,
                            y = preCube.y,
                            z = preCube.z,
                            a = a,
                            n0old = preCube.n1,
                            n2old = preCube.n3,
                            n4old = preCube.n5,
                            n6old = preCube.n7))


        # First layer
        layer = [row, ]
        for j in range(yNum-1):
            preCubeY = layer[-1][0]
# Step 3: First cube in other rows of current layer
# ---------------------------------------------------------------------
#            +----+----+----+
#      	    /    /    /    /|
#          /    /    /    / |
#         +----+----+----+  +
#        /    /    /    /| /|
#       /    /    /    / |/ |
#      +----+----+----+  +  +
#      |    |    |    | /| /|
#      |    |    |    |/ |/ |
#      +----+----+----+  +  +
#  --> |    |    |    | /| /
#      |    |    |    |/X|/
#      +----+----+----+XX+
#      |XXXX|XXXX|XXXX|X/
#      |XXXX|XXXX|XXXX|/
#      +----+----+----+

            row = [Cube(x=preCubeY.x,
                        y=preCubeY.y+a,
                        z=preCubeY.z,
                        a=a,
                        n0old=preCubeY.n2,
                        n1old=preCubeY.n3,
                        n4old=preCubeY.n6,
                        n5old=preCubeY.n7), ]
            for i in range(xNum-1):
                preCubeX = row[-1]
                preCubeY = layer[-1][i+1]


# Step 4: Other cubes in current layer
# ---------------------------------------------------------------------
#            +----+----+----+
#           /    /    /    /|
#          /    /    /    / |
#         +----+----+----+  +
#        /    /    /    /| /|
#       /    /    /    / |/ |
#      +----+----+----+  +  +
#      |    |    |    | /| /|
#      |    |    |    |/ |/X|
#      +----+----+----+  +XX+
#      |    |    |    | /|X/
#      |    |    |    |/X|/
#      +----+----+----+XX+
#      |XXXX|XXXX|XXXX|X/
#      |XXXX|XXXX|XXXX|/
#      +----+----+----+


                row.append(Cube(x = preCubeX.x+a,
                            y = preCubeX.y,
                            z = preCubeX.z,
                            a = a,
                            n0old = preCubeX.n1,
                            n1old = preCubeY.n3,
                            n2old = preCubeX.n3,
                            n4old = preCubeX.n5,
                            n5old = preCubeY.n7,
                            n6old = preCubeX.n7))

            layer.append(row)

        # Complete stack
        stack = [layer, ]
        for k in range(zNum-1):
            preCubeZ = stack[-1][0][0]


# Step 5: First cube in first row of current layer
# ---------------------------------------------------------------------
#            +----+----+----+
#           /    /    /    /|
#          /    /    /    / |
#         +----+----+----+  +
#        /    /    /    /| /|
#       /    /    /    / |/ |
#      +----+----+----+  +  +
#      |    |    |    | /| /|
#      |    |    |    |/ |/X|
#      +----+----+----+  +XX+
#      |XXXX|    |    | /|X/
#      |XXXX|    |    |/X|/
#      +----+----+----+XX+
#      |XXXX|XXXX|XXXX|X/
#      |XXXX|XXXX|XXXX|/
#      +----+----+----+
            row = [Cube(x = preCubeZ.x,
                        y = preCubeZ.y,
                        z = preCubeZ.z+a,
                        a = a,
                        n0old = preCubeZ.n4,
                        n1old = preCubeZ.n5,
                        n2old = preCubeZ.n6,
                        n3old = preCubeZ.n7)]




            for i in range(xNum-1):
                preCubeX = row[-1]
                preCubeZ = stack[-1][0][i+1]

# Step 6: Other cubes in first row in current layer
# ---------------------------------------------------------------------
#            +----+----+----+
#      	    /    /    /    /|
#          /    /    /    / |
#         +----+----+----+  +
#        /    /    /    /| /|
#       /    /    /    / |/ |
#      +----+----+----+  +  +
#      |    |    |    | /| /|
#      |    |    |    |/X|/X|
#      +----+----+----+XX+XX+
#      |XXXX|XXXX|XXXX|X/|X/
#      |XXXX|XXXX|XXXX|/X|/
#      +----+----+----+XX+
#      |XXXX|XXXX|XXXX|X/
#      |XXXX|XXXX|XXXX|/
#      +----+----+----+
                row.append(Cube(x = preCubeZ.x,
                                y = preCubeZ.y,
                                z = preCubeZ.z+a,
                                a = a,
                                n0old = preCubeZ.n4,
                                n1old = preCubeZ.n5,
                                n2old = preCubeZ.n6,
                                n3old = preCubeZ.n7,
                                n4old = preCubeX.n5,
                                n6old = preCubeX.n7))
            layer = [row, ]




            for j in range(yNum-1):
                preCubeY = layer[-1][0]
                preCubeZ = stack[-1][j+1][0]


# Step 7: First cube in current row of current layer
# ---------------------------------------------------------------------
#            +----+----+----+
#           /    /    /    /|
#          /    /    /    / |
#         +----+----+----+  +
#        /    /    /    /| /|
#       /    /    /    / |/ |
#      +----+----+----+  +  +
#  --> |    |    |    | /| /|
#      |    |    |    |/X|/X|
#      +----+----+----+XX+XX+
#      |XXXX|XXXX|XXXX|X/|X/
#      |XXXX|XXXX|XXXX|/X|/
#      +----+----+----+XX+
#      |XXXX|XXXX|XXXX|X/
#      |XXXX|XXXX|XXXX|/
#      +----+----+----+

                row = [Cube(preCubeZ.x,
                            preCubeZ.y,
                            preCubeZ.z+a,
                            a = a,
                            n0old=preCubeY.n2,
                            n1old=preCubeY.n3,
                            n2old = preCubeZ.n6,
                            n3old = preCubeZ.n7,
                            n4old=preCubeY.n6,
                            n5old = preCubeY.n7), ]



                for i in range(xNum-1):
                    preCubeX = row[-1]
                    preCubeY = layer[-1][i+1]
                    preCubeZ = stack[-1][j+1][i+1]

# Step 8: Other cubes in current row of current layer
# ---------------------------------------------------------------------
#            +----+----+----+
#      	    /    /    /    /|
#          /    /    /    / |
#         +----+----+----+  +
#        /    /    /    /| /|
#       /    /    /    / |/X|
#      +----+----+----+  +XX+
#      |    |    |    | /|X/|
#      |    |    |    |/X|/X|
#      +----+----+----+XX+XX+
#      |XXXX|XXXX|XXXX|X/|X/
#      |XXXX|XXXX|XXXX|/X|/
#      +----+----+----+XX+
#      |XXXX|XXXX|XXXX|X/
#      |XXXX|XXXX|XXXX|/
#      +----+----+----+
                    row.append(Cube(x = preCubeZ.x,
                                    y = preCubeZ.y,
                                    z = preCubeZ.z+a,
                                    a = a,
                                    n0old = preCubeZ.n4,
                                    n1old = preCubeZ.n5,
                                    n2old = preCubeZ.n6,
                                    n3old = preCubeZ.n7,
                                    n4old = preCubeX.n5,
                                    n5old = preCubeY.n7,
                                    n6old = preCubeX.n7))
                layer.append(row)
            stack.append(layer)




        borderVolumes = []
        if borderVolumesBottom:
            bottom = []
            for row in stack[0]:
                for cube in row:
                    bottom.append(cube)
            for c in bottom:
                if not c.volume in borderVolumes:
                    borderVolumes.append(c.volume)

        if borderVolumesTop:
            top = []
            for row in stack[-1]:
                for cube in row:
                    top.append(cube)
            for c in top:
                if not c.volume in borderVolumes:
                    borderVolumes.append(c.volume)

        if borderVolumesFront:
            front = []
            for layer in stack:
                for cube in layer[0]:
                    front.append(cube)
            for c in front:
                if not c.volume in borderVolumes:
                    borderVolumes.append(c.volume)


        if borderVolumesBack:
            back = []
            for layer in stack:
                for cube in layer[-1]:
                    back.append(cube)
            for c in back:
                if not c.volume in borderVolumes:
                    borderVolumes.append(c.volume)

        if borderVolumesLeft:
            left = []
            for layer in stack:
                for row in layer:
                    left.append(row[0])
            for c in left:
                if not c.volume in borderVolumes:
                    borderVolumes.append(c.volume)

        if borderVolumesRight:
            right= []
            for layer in stack:
                for row in layer:
                    right.append(row[-1])
            for c in right:
                if not c.volume in borderVolumes:
                    borderVolumes.append(c.volume)



        for v in borderVolumes:
            v.category = 'border'
            v.color= tc.TUMRose()



        nodes = []
        edges = []
        faces = []
        volumes = []

        for layer in stack:
            for row in layer:
                for cube in row:
                    for n in cube.nodes:
                        if not n in nodes:
                            nodes.append(n)
                    for e in cube.edges:
                        if not e in edges:
                            edges.append(e)
                    for f in cube.faces:
                        if not f in faces:
                            faces.append(f)
                    if not cube.volume in volumes:
                        volumes.append(cube.volume)







        # Check if two nodes were generated at the same location
        for n1 in nodes:
            for n2 in nodes:
                if not n1 == n2:
                    if np.linalg.norm(n1.coordinates-n2.coordinates)<1e-4:
                        cc.printRed('It seems that two nodes were created at the same place')
                        cc.printRed(n1, n2)
                        print()

        super().__init__(nodes, edges, faces, volumes)

        self.__cubeStack = stack




# =============================================================================
#    SETTER AND GETTER
# =============================================================================
    def __getCubeStack(self): return self.__cubeStack
    cubeStack = property(__getCubeStack)


# =============================================================================
#    METHODS
# =============================================================================

# ------------------------------------------------------------------------
#    Plots for documentation
# ------------------------------------------------------------------------
    @classmethod
    def plotDoc(cls):
        '''
        Class method that creates all plots needed in the documentation.

        '''
        (figs, ax) = pf.getFigures(numTotal=9)
        comp = Grid3DCubic(3)
        print(comp.cubeStack)

        comp.plotComplex(ax[8], showLabel=False, plotEdges=False)
        pf.setAxesEqual(ax[8])


        # Step 1
        comp.cubeStack[0][0][0].plotCube(ax[0], showLabel=False, showArrow=False, showNormalVec=False, showBarycenter=False, plotNodes=False)

        # Step 2
        for c in comp.cubeStack[0][0]:
            c.plotCube(ax[1], showLabel=False, showArrow=False, showNormalVec=False, showBarycenter=False, plotNodes=False)

        # Step 3
        for c in comp.cubeStack[0][0]:
            c.plotCube(ax[2], showLabel=False, showArrow=False, showNormalVec=False, showBarycenter=False, plotNodes=False)
        comp.cubeStack[0][1][0].plotCube(ax[2], showLabel=False, showArrow=False, showNormalVec=False, showBarycenter=False, plotNodes=False)

        # Step 4
        for row in comp.cubeStack[0]:
            for c in row:
                c.plotCube(ax[3], showLabel=False, showArrow=False, showNormalVec=False, showBarycenter=False, plotNodes=False)

        # Step 5
        for row in comp.cubeStack[0]:
            for c in row:
                c.plotCube(ax[4], showLabel=False, showArrow=False, showNormalVec=False, showBarycenter=False, plotNodes=False)
        comp.cubeStack[1][0][0].plotCube(ax[4], showLabel=False, showArrow=False, showNormalVec=False, showBarycenter=False, plotNodes=False)

        # Step 6
        for row in comp.cubeStack[0]:
            for c in row:
                c.plotCube(ax[5], showLabel=False, showArrow=False, showNormalVec=False, showBarycenter=False, plotNodes=False)
        for c in comp.cubeStack[1][0]:
            c.plotCube(ax[5], showLabel=False, showArrow=False, showNormalVec=False, showBarycenter=False, plotNodes=False)

        # Step 7
        for row in comp.cubeStack[0]:
            for c in row:
                c.plotCube(ax[6], showLabel=False, showArrow=False, showNormalVec=False, showBarycenter=False, plotNodes=False)
        for c in comp.cubeStack[1][0]:
            c.plotCube(ax[6], showLabel=False, showArrow=False, showNormalVec=False, showBarycenter=False, plotNodes=False)
        comp.cubeStack[1][1][0].plotCube(ax[6], showLabel=False, showArrow=False, showNormalVec=False, showBarycenter=False, plotNodes=False)

        # Step 8:
        for layer in comp.cubeStack:
            for row in layer:
                for c in row:
                    c.plotCube(ax[7], showLabel=False, showArrow=False, showNormalVec=False, showBarycenter=False, plotNodes=False)




        for a in ax[:-1]:
            pf.copylimits(ax[8], a)
        for (i, f) in enumerate(figs):
            pf.exportPNG(f, 'doc/_static/grid3DCubicComplex'+str(i))

# =============================================================================
#    TEST FUNCTIONS
# =============================================================================

if __name__ == '__main__':
    with MyLogging('complexGeometry'):

#        nbc = False
        pc = Grid3DCubic(3, yNum=4, zNum=4, borderVolumesRight=True)

        dc = DualComplex3D(pc)


        axNum = -1
        (figs, axes) = pf.getFigures()

        axNum += 1
        pc.plotComplex(axes[axNum], showLabel=False, showNormalVec=False, showArrow=False)

        axNum += 1
        dc.plotComplex(axes[axNum], showLabel=False, showNormalVec=False, showArrow=False)

        axNum += 1
        for f in dc.additionalBorderFaces:
            f.plotFace(axes[axNum], showLabel=False, showNormalVec=False)

