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
from k_cells import Node
from k_cells import Edge
from k_cells import Face
from k_cells import Volume
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
    n1 = Node(2*a,0,0)
    n2 = Node(4*a,0,0)
    n3 = Node(0,2*a,0)
    n4 = Node(2*a,2*a,0)
    n5 = Node(4*a,2*a,0)
    n6 = Node(0,4*a,0)
    n7 = Node(2*a,4*a,0)
    n8 = Node(4*a,4*a,0)
    n9 = Node(0,0,2*a)
    n10 = Node(2*a,0,2*a)
    n11 = Node(4*a,0,2*a)
    n12 = Node(0,2*a,2*a)
    n13 = Node(2*a,2*a,2*a)
    n14 = Node(4*a,2*a,2*a)
    n15 = Node(0,4*a,2*a)
    n16 = Node(2*a,4*a,2*a)
    n17 = Node(4*a,4*a,2*a)
    n18 = Node(0,0,4*a)
    n19 = Node(2*a,0,4*a)
    n20 = Node(4*a,0,4*a)
    n21 = Node(0,2*a,4*a)
    n22 = Node(2*a,2*a,4*a)
    n23 = Node(4*a,2*a,4*a)
    n24 = Node(0,4*a,4*a)
    n25 = Node(2*a,4*a,4*a)
    n26 = Node(4*a,4*a,4*a)
    # n1 = Node(a,0,0)
    # n2 = Node(0,a,0)
    # n3 = Node(0,0,a)
    # n4 = Node(2*a,0,0)
    # n5 = Node(0,2*a,0)
    # n6 = Node(0,0,2*a)
    # n7 = Node(4*a,0,0)
    # n8 = Node(0,4*a,0)
    # n9 = Node(0,0,4*a)
    # n10 = Node(2*a,2*a,0)
    # n11 = Node(4*a,4*a,0)
    # n12 = Node(4*a,2*a,0)
    # n13 = Node(2*a,4*a,0)
    # n14 = Node(4*a,0,2*a)
    # n15 = Node(0,4*a,2*a)
    # n16 = Node(2*a,2*a,2*a)
    # n17 = Node(4*a,4*a,2*a)
    # n18 = Node(4*a,2*a,2*a)
    # n19 = Node(2*a,4*a,2*a)
    # n20 = Node(2*a,0,2*a)
    # n21 = Node(0,2*a,2*a)

    # n22 = Node(4*a,0,4*a)
    # n23 = Node(0,4*a,4*a)
    # n24 = Node(2*a,2*a,4*a)
    # n25 = Node(4*a,4*a,4*a)
    # n26 = Node(4*a,2*a,4*a)
    # n27 = Node(2*a,4*a,4*a)
    # n28 = Node(2*a,0,4*a)
    # n29 = Node(0,2*a,4*a)




    # put all nodes in a list to simplify handling:
    nodes = [
        n0,n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,
        n20,n21,n22,n23,n24,n25,n26
    ]

    # plot all nodes
    for n in nodes:
        n.plotNode(ax[0])



# #==============================================================================
# #    EDGES
# #==============================================================================
#     # Create some edges by defining their endpoints
    e0 = Edge(n0,n1)
    e1 = Edge(n1,n2)
    e2 = Edge(n3,n4)
    e3 = Edge(n4,n5)
    e4 = Edge(n6,n7)
    e5 = Edge(n7,n8)
    e6 = Edge(n9,n10)
    e7 = Edge(n10,n11)
    e8 = Edge(n12,n13)
    e9 = Edge(n13,n14)
    e10 = Edge(n15,n16)
    e11 = Edge(n16,n17)
    e12 = Edge(n18,n19)
    e13 = Edge(n19,n20)
    e14 = Edge(n21,n22)
    e15 = Edge(n22,n23)
    e16 = Edge(n24,n25)
    e17 = Edge(n25,n26)
    e18 = Edge(n0,n3)
    e19 = Edge(n3,n6)
    e20 = Edge(n1,n4)
    e21 = Edge(n4,n7)
    e22 = Edge(n2,n5)
    e23 = Edge(n5,n8)
    e24 = Edge(n9,n12)
    e25 = Edge(n12,n15)
    e26 = Edge(n10,n13)
    e27 = Edge(n13,n16)
    e28 = Edge(n11,n14)
    e29 = Edge(n14,n17)
    e30 = Edge(n18,n21)
    e31 = Edge(n21,n24)
    e32 = Edge(n19,n22)
    e33 = Edge(n22,n25)
    e34 = Edge(n20,n23)
    e35 = Edge(n23,n26)
    e36 = Edge(n0,n9)
    e37 = Edge(n9,n18)
    e38 = Edge(n1,n10)
    e39 = Edge(n10,n19)
    e40 = Edge(n2,n11)
    e41 = Edge(n11,n20)
    e42 = Edge(n3,n12)
    e43 = Edge(n12,n21)
    e44 = Edge(n4,n13)
    e45 = Edge(n13,n22)
    e46 = Edge(n5,n14)
    e47 = Edge(n14,n23)
    e48 = Edge(n6,n15)
    e49 = Edge(n15,n24)
    e50 = Edge(n7,n16)
    e51 = Edge(n16,n25)
    e52 = Edge(n8,n17)
    e53 = Edge(n17,n26)

    e54 = Edge(n0,n4)
    e55 = Edge(n9,n13)
    # e56 = Edge(n3,n9)
#     e54 = Edge(n12,n18)
#     e55 = Edge(n8,n15)
#     e56 = Edge(n13,n19)
#     e57 = Edge(n11,n17)
#     e58 = Edge(n15,n23)
#     e59 = Edge(n19,n27)
#     e60 = Edge(n17,n25)
#     e61 = Edge(n21,n29)
#     e62 = Edge(n16,n24)
#     e63 = Edge(n18,n26)
#     e64 = Edge(n6,n9)
#     e65 = Edge(n20,n28)
#     e66 = Edge(n14,n22)



#     # Put them in a list, too
    edges = [e0,e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13,e14,e15,e16,e17,e18,e19,
              e20,e21,e22,e23,e24,e25,e26,e27,e28,e29,
              e30,e31,e32,e33,e34,e35,e36,e37,e38,e39,
              e40,e41,e42,e43,e44,e45,e46,e47,e48,e49,
              e50,e51,e52,e53,e54,e55]#,e56]#,e57,e58,e59,
#              e60,e61,e62,e63,e64,e65,e66]

    # plot all edges
    for e in edges:
        e.plotEdge(ax[0])
        e.plotEdge(ax[1])





# #==============================================================================
# #    FACES
# #==============================================================================
#     # Create faces by defining the border edges
    f0 = Face([e0,e20,-e54])
    f1 = Face([e1,e22,-e3,-e20])
    f2 = Face([e2,e21,-e4,-e19])
    f3 = Face([e3,e23,-e5,-e21])
    f4 = Face([e6,e26,-e55])
    f5 = Face([e7,e28,-e9,-e26])
    f6 = Face([e8,e27,-e10,-e25])
    f7 = Face([e9,e29,-e11,-e27])
    f8 = Face([e12,e32,-e14,-e30])
    f9 = Face([e13,e34,-e15,-e32])
    f10 = Face([e14,e33,-e16,-e31])
    f11 = Face([e15,e35,-e17,-e33])
    f12 = Face([e0,e38,-e6,-e36])
    f13 = Face([e1,e40,-e7,-e38])
    f14 = Face([e2,e44,-e8,-e42])
    f15 = Face([e3,e46,-e9,-e44])
    f16 = Face([e4,e50,-e10,-e48])
    f17 = Face([e5,e52,-e11,-e50])
    f18 = Face([e6,e39,-e12,-e37])
    f19 = Face([e7,e41,-e13,-e39])
    f20 = Face([e8,e45,-e14,-e43])
    f21 = Face([e9,e47,-e15,-e45])
    f22 = Face([e10,e51,-e16,-e49])
    f23 = Face([e11,e53,-e17,-e51])
    f24 = Face([e36,e24,-e42,-e18])
    f25 = Face([e38,e26,-e44,-e20])
    f26 = Face([e40,e28,-e46,-e22])
    f27 = Face([e42,e25,-e48,-e19])
    f28 = Face([e44,e27,-e50,-e21])
    f29 = Face([e46,e29,-e52,-e23])
    f30 = Face([e37,e30,-e43,-e24])
    f31 = Face([e39,e32,-e45,-e26])
    f32 = Face([e41,e34,-e47,-e28])
    f33 = Face([e43,e31,-e49,-e25])
    f34 = Face([e45,e33,-e51,-e27])
    f35 = Face([e47,e35,-e53,-e29])
    f36 = Face([e18,e2,-e54])
    f37 = Face([e24,e8,-e55])
    f38 = Face([e36,e55,-e44,-e54])


#     # Put faces in a list, we've seen that before ;)
    faces = [f0,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,
              f13,f14,f15,f16,f17,f18,f19,f20,f21,f22,f23,f24,
              f25,f26,f27,f28,f29,f30,f31,f32,f33,f34,f35,
              f36,f37,f38]

#     # Plot the faces
    for f in faces:
        f.plotFace(ax[1],showNormalVec=False,showBarycenter=False)
        f.plotFace(ax[2])



# #==============================================================================
# #    VOLUME
# #==============================================================================
#     #Create a volume by defining the border faces
    v0 = Volume([-f0,f4,f12,-f25,f38])
    v1 = Volume([-f1,f5,f13,-f15,f25,-f26])
    v2 = Volume([-f2,f6,f14,-f16,f27,-f28])
    v3 = Volume([-f3,f7,f15,-f17,f28,-f29])
    v4 = Volume([-f4,f8,f18,-f20,f30,-f31,f37])
    v5 = Volume([-f5,f9,f19,-f21,f31,-f32])
    v6 = Volume([-f6,f10,f20,-f22,f33,-f34])
    v7 = Volume([-f7,f11,f21,-f23,f34,-f35])
    v8 = Volume([f36,-f37,-f14,f24,-f38])


    volumes = [v0, v1, v2, v3, v4, v5, v6, v7, v8]

    for v in volumes:
        v.plotVolume(ax[2])
        v.plotVolume(ax[3])


# #==============================================================================
# #    PRIMAL COMPLEX
# #==============================================================================

    for v in [v8, v2, v4, v6]:
        v.category1 = "border"
    pc = PrimalComplex3D(nodes,edges,faces,volumes)
    pc.plotComplex(ax[4])




# #==============================================================================
# #    DUAL COMPLEX
# #==============================================================================
    dc = DualComplex3D(pc)
    dc.plotComplex(ax[5],plotFaces=True,showLabel=False, showNormalVec=False)
