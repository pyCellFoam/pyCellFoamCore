# -*- coding: utf-8 -*-
#==============================================================================
# SIMPLE EXAMPLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Dec  7 14:16:21 2017

'''

'''

# import os
# os.chdir('../')
#==============================================================================
#    IMPORTS
#==============================================================================
from kCells import Node
from kCells import Edge
from kCells import Face
from kCells import Volume
from tools import MyLogging
from complex import PrimalComplex3D, DualComplex3D
import tools.placeFigures as pf
import tools.colorConsole as cc
from complex import Complex3D
#import matplotlib.pyplot as plt
import tools.exportLaTeX as tex


#==============================================================================
#    PREPARE PLOT
#==============================================================================
with MyLogging ('simpleExample'):
    (figs,ax) = pf.getFigures(numTotal=8)
#    for a in ax:
#        pf.setAxesEqual(a)

#==============================================================================
#    NODES
#==============================================================================
    # Create nodes at [0,0,0], [1,0,0], [0,1,0] and [0,0,1]
    a = 3
    n0 = Node(0,0,0)
    n1 = Node(a,0,0)
    n2 = Node(0,a,0)
    n3 = Node(0,0,a)
    n4 = Node(2*a,0,0)
    n5 = Node(0,2*a,0)
    n6 = Node(0,0,2*a)
    n7 = Node(4*a,0,0)
    n8 = Node(0,4*a,0)
    n9 = Node(0,0,4*a)
    n10 = Node(2*a,2*a,0)
    n11 = Node(4*a,4*a,0)
    n12 = Node(4*a,2*a,0)
    n13 = Node(2*a,4*a,0)
    n14 = Node(4*a,0,2*a)
    n15 = Node(0,4*a,2*a)
    n16 = Node(2*a,2*a,2*a)
    n17 = Node(4*a,4*a,2*a)
    n18 = Node(4*a,2*a,2*a)
    n19 = Node(2*a,4*a,2*a)
    n20 = Node(2*a,0,2*a)
    n21 = Node(0,2*a,2*a)

    n22 = Node(4*a,0,4*a)
    n23 = Node(0,4*a,4*a)
    n24 = Node(2*a,2*a,4*a)
    n25 = Node(4*a,4*a,4*a)
    n26 = Node(4*a,2*a,4*a)
    n27 = Node(2*a,4*a,4*a)
    n28 = Node(2*a,0,4*a)
    n29 = Node(0,2*a,4*a)




    # put all nodes in a list to simplify handling:
    nodes = [
        n0,n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,
        n20,n21,n22,n23,n24,n25,n26,n27,n28,n29
    ]

    # plot all nodes
    for n in nodes:
        n.plotNode(ax[0])



#==============================================================================
#    EDGES
#==============================================================================
    # Create some edges by defining their endpoints
    e0 = Edge(n0,n1)
    e1 = Edge(n0,n2)
    e2 = Edge(n0,n3)
    e3 = Edge(n1,n2)
    e4 = Edge(n1,n3)
    e5 = Edge(n2,n3)
    e6 = Edge(n1,n4)
    e7 = Edge(n2,n5)
    e8 = Edge(n3,n6)
    e9 = Edge(n4,n5)
    e10 = Edge(n5,n6)
    e11 = Edge(n6,n4)
    e12 = Edge(n5,n8)
    e13 = Edge(n4,n10)
    e14 = Edge(n10,n13)
    e15 = Edge(n7,n12)
    e16 = Edge(n12,n11)
    e17 = Edge(n4,n7)
    e18 = Edge(n5,n10)
    e19 = Edge(n10,n12)
    e20 = Edge(n8,n13)
    e21 = Edge(n13,n11)
    e22 = Edge(n6,n20)
    e23 = Edge(n20,n14)
    e24 = Edge(n21,n16)
    e25 = Edge(n16,n18)
    e26 = Edge(n15,n19)
    e27 = Edge(n19,n17)
    e28 = Edge(n6,n21)
    e29 = Edge(n21,n15)
    e30 = Edge(n20,n16)
    e31 = Edge(n16,n19)
    e32 = Edge(n14,n18)
    e33 = Edge(n18,n17)
    e34 = Edge(n19,n16)
    e35 = Edge(n16,n20)
    e36 = Edge(n17,n18)
    e37 = Edge(n18,n14)
    e38 = Edge(n23,n29)
    e39 = Edge(n29,n9)
    e40 = Edge(n27,n24)
    e41 = Edge(n24,n28)
    e42 = Edge(n25,n26)
    e43 = Edge(n26,n22)
    e44 = Edge(n23,n27)
    e45 = Edge(n27,n25)
    e46 = Edge(n29,n24)
    e47 = Edge(n24,n26)
    e48 = Edge(n9,n28)
    e49 = Edge(n28,n22)
    e50 = Edge(n4,n20)
    e51 = Edge(n7,n14)
    e52 = Edge(n5,n21)
    e53 = Edge(n10,n16)
    e54 = Edge(n12,n18)
    e55 = Edge(n8,n15)
    e56 = Edge(n13,n19)
    e57 = Edge(n11,n17)
    e58 = Edge(n15,n23)
    e59 = Edge(n19,n27)
    e60 = Edge(n17,n25)
    e61 = Edge(n21,n29)
    e62 = Edge(n16,n24)
    e63 = Edge(n18,n26)
    e64 = Edge(n6,n9)
    e65 = Edge(n20,n28)
    e66 = Edge(n14,n22)



    # Put them in a list, too
    edges = [e0,e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13,e14,e15,e16,e17,e18,e19,
             e20,e21,e22,e23,e24,e25,e26,e27,e28,e29,
             e30,e31,e32,e33,e34,e35,e36,e37,e38,e39,
             e40,e41,e42,e43,e44,e45,e46,e47,e48,e49,
             e50,e51,e52,e53,e54,e55,e56,e57,e58,e59,
             e60,e61,e62,e63,e64,e65,e66]

    # plot all edges
    for e in edges:
        e.plotEdge(ax[0])
        e.plotEdge(ax[1])





#==============================================================================
#    FACES
#==============================================================================
    # Create faces by defining the border edges
    f0 = Face([e0,e4,-e2])
    f1 = Face([e3,e5,-e4])
    f2 = Face([e0,e3,-e1])
    f3 = Face([e1,e5,-e2])
    f4 = Face([e7,e10,-e8,-e5])
    f5 = Face([e4,e8,e11,-e6])
    f6 = Face([e3,e7,-e9,-e6])
    f7 = Face([e9,e10,e11])
    f8 = Face([e9,e18,-e13])
    f9 = Face([e11,e50,-e22])
    f10 = Face([e10,e28,-e52])
    f11 = Face([e12,e20,-e14,-e18])
    f12 = Face([e13,e19,-e15,-e17])
    f13 = Face([e14,e21,-e16,-e19])

    # Put faces in a list, we've seen that before ;)
    faces = [f0,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13]

    # Plot the faces
    for f in faces:
        f.plotFace(ax[1])
        f.plotFace(ax[2])



#==============================================================================
#    VOLUME
#==============================================================================
    #Create a volume by defining the border faces
    v0 = Volume([f0,f1,-f2,-f3])
    v1 = Volume([-f1,-f5,-f4,f6,f7])


    volumes = [v0, v1]

    for v in volumes:
        v.plotVolume(ax[2])


# #==============================================================================
# #    PRIMAL COMPLEX
# #==============================================================================

#     pc = PrimalComplex3D(nodes,edges,faces,volumes)
#     pc.plotComplex(ax[4])




# #==============================================================================
# #    DUAL COMPLEX
# #==============================================================================
#     dc = DualComplex3D(pc)
#     dc.plotComplex(ax[5],plotFaces=True,showLabel=False, showNormalVec=False)





