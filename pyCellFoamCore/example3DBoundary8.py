# -*- coding: utf-8 -*-
#==============================================================================
# TITLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Jun 26 11:17:19 2025

import logging

from tools.logging_formatter import set_logging_format
import tools.placeFigures as pf
import tools.tumcolor as tc

from k_cells.node.node import Node
from k_cells.edge.edge import Edge
from k_cells.face.face import Face
from k_cells.volume.volume import Volume

from complex.primalComplex3D import PrimalComplex3D
from complex.dualComplex3D import DualComplex3D



set_logging_format(logging.DEBUG)


n7 = Node(-5.0, 0.0, 2.5, num=7)
n21 = Node(2.5, 0.0, -5.0, num=21)
n153 = Node(15.0, 0.0, -5.0, num=153)
n155 = Node(15.0, 0.0, 15.0, num=155)
n157 = Node(-5.0, 0.0, -5.0, num=157)
n159 = Node(-5.0, 0.0, 15.0, num=159)
n168 = Node(15.0, 15.0, -5.0, num=168)
n169 = Node(15.0, 15.0, 15.0, num=169)
n172 = Node(-5.0, 15.0, -5.0, num=172)
n173 = Node(-5.0, 15.0, 15.0, num=173)
n147 = Node(0.0, -5.0, -5.0, num=147)
n151 = Node(0.0, -5.0, 15.0, num=151)
n165 = Node(15.0, -5.0, 0.0, num=165)
n167 = Node(-5.0, -5.0, 0.0, num=167)
n170 = Node(15.0, -5.0, -5.0, num=170)
n171 = Node(15.0, -5.0, 15.0, num=171)
n174 = Node(-5.0, -5.0, -5.0, num=174)
n175 = Node(-5.0, -5.0, 15.0, num=175)
nodes = [n7, n21,
         n153, n155, n157, n159, n168, n169, n172, n173, n147, n151, n165, n167, n170, n171, n174, n175]

n1000 = Node(0.0, 0.0, 15.0, num=1000)
n1001 = Node(15.0, 0.0, 0.0, num=1001)
n1002 = Node(5, 0, 0, num=1002)
n1003 = Node(0, 0, 5, num=1003)
n1004 = Node(0, -5, 0, num=1004)
nodes1000 = [n1000, n1001, n1002, n1003, n1004]
for n in nodes1000:
    nodes.append(n)


e346 = Edge(n175, n159, num=346)
e345 = Edge(n175, n167, num=345)
e347 = Edge(n175, n151, num=347)
e335 = Edge(n171, n155, num=335)
e331 = Edge(n170, n165, num=331)
e332 = Edge(n170, n153, num=332)
e342 = Edge(n174, n167, num=342)
e343 = Edge(n174, n157, num=343)
e344 = Edge(n174, n147, num=344)

edges = []

edges = [e346, e345, e347,
          e335, e331, e332, e342, e343, e344]

e1000 = Edge(n168, n169, num=1000)
e1001 = Edge(n169, n173, num=1001)
e1002 = Edge(n173, n172, num=1002)
e1003 = Edge(n172, n168, num=1003)
e1004 = Edge(n168, n153, num=1004)
e1005 = Edge(n169, n155, num=1005)
e1006 = Edge(n172, n157, num=1006)
e1007 = Edge(n173, n159, num=1007)
e1008 = Edge(n151, n171, num=1008)
e1009 = Edge(n147, n170, num=1009)
e1010 = Edge(n1000, n155, num=1010)
e1013 = Edge(n1001, n155, num=1013)
e1014 = Edge(n165, n171, num=1014)
e1015 = Edge(n1001, n165, num=1015)
e1016 = Edge(n1001, n153, num=1016)
e1017 = Edge(n21, n153, num=1017)
e1018 = Edge(n1000, n151, num=1018)
e1023 = Edge(n1000, n159, num=1023)
e1028 = Edge(n7, n159, num=1028)
e1034 = Edge(n157, n7, num=1034)
e1035 = Edge(n157, n21, num=1035)
e1037 = Edge(n1001, n1002, num=1037)
e1038 = Edge(n1000, n1003, num=1038)
e1039 = Edge(n21, n1002, num=1039)
e1040 = Edge(n1002, n1003, num=1040)
e1041 = Edge(n7, n1003, num=1041)
e1042 = Edge(n167, n1004, num=1042)
e1043 = Edge(n147, n1004, num=1043)
e1044 = Edge(n7, n167, num=1044)
e1045 = Edge(n1004, n165, num=1045)
e1046 = Edge(n1003, n1004, num=1046)
e1047 = Edge(n1002, n1004, num=1047)
e1048 = Edge(n21, n147, num=1048)
e1049 = Edge(n7, n1004, num=1049)
e1050 = Edge(n21, n1004, num=1050)
e1051 = Edge(n1004, n151, num=1051)

edges1000 = [e1000,e1001,e1002,e1003,e1004,e1005,e1006,e1007,e1008,e1009,
              e1010,e1013,e1014,e1015,e1016,e1017,e1018,
              e1023,e1028,
              e1034, e1035, e1037, e1038, e1039, e1040, e1041,
              e1042, e1043, e1044, e1045, e1046, e1047, e1048,
              e1049, e1050, e1051]
for e in edges1000:
    edges.append(e)


edges_for_face = [e1042, e1051, -e347, e345]


faces = []




f1000 = Face([e1000,e1001,e1002,e1003], num=1000)

f1005 = Face([e1000,e1005,-e1013,e1016,-e1004], num=1005)
f1006 = Face([e1001,e1007,-e1023,e1010,-e1005], num=1006)
f1018 = Face([e335, -e1010, e1018, e1008], num=1018)
f1019 = Face([e346, -e1023, e1018, -e347], num=1019)
f1020 = Face([e331, -e1015, e1016, -e332], num=1020)
f1021 = Face([e335, -e1013, e1015, e1014], num=1021)
f1027 = Face([e1003, e1004, -e1017, -e1035, -e1006], num=1027)
f1028 = Face([e1002, e1006, e1034, e1028, -e1007], num=1028)
f1033 = Face([e1017, -e1016, e1037, -e1039], num=1033)
f1034 = Face([e1037, e1040, -e1038, e1010, -e1013], num=1034)
f1035 = Face([e1028, -e1023, e1038, -e1041], num=1035)
f1036 = Face([e1035, e1039, e1040, -e1041, -e1034], num=1036)
f1037 = Face([e1017, -e332, -e1009, -e1048], num=1037)
f1038 = Face([e1035, e1048, -e344, e343], num=1038)
f1039 = Face([e1037, e1047, e1045, -e1015], num=1039)
f1040 = Face([e1040, e1046, -e1047], num=1040)
f1041 = Face([e1046, -e1049, e1041], num=1041)
f1042 = Face([e1042, -e1049, e1044], num=1042)
f1043 = Face([e1048, e1043, -e1050], num=1043)
f1044 = Face([e1044, -e345, e346, -e1028], num=1044)
f1045 = Face([e342, -e1044, -e1034, -e343], num=1045)
f1046 = Face([e1038, e1046, e1051, -e1018], num=1046)
f1047 = Face([e1039, e1047, -e1050], num=1047)
f1048 = Face([e1045, e1014, -e1008, -e1051], num=1048)
f1049 = Face([e1042, e1051, -e347, e345], num=1049)
f1050 = Face([e1009, e331, -e1045, -e1043], num=1050)
f1051 = Face([e344, e1043, -e1042, -e342], num=1051)

faces1000 = [f1000,f1005,f1006,
              f1018, f1019, f1020, f1021,
              f1027, f1028, f1033, f1034, f1035, f1036, f1037, f1038, f1039,
              f1040, f1041, f1042, f1043, f1044, f1045, f1046, f1047, f1048,
              f1049, f1050, f1051]

for f in faces1000:
    faces.append(f)

volumes = []

faces_for_volume = []
faces_for_volume = [f1038, f1045, f1051, -f1036, f1040, f1041, f1042, -f1043, f1047]

v1007 = Volume([-f1000, f1005, f1006, f1027, f1028, -f1034, f1036, f1033, -f1035], num=1007)
v1008 = Volume([-f1020, -f1033, f1039, f1050, f1037, f1043, -f1047], num=1008)
v1009 = Volume([f1018, -f1021, f1048, -f1039, -f1040, f1034, f1046], num=1009)
v1010 = Volume([-f1019, f1035, -f1046, f1044, f1041, f1049, -f1042], num=1010)
v1011 = Volume([f1038, f1045, f1051, -f1036, f1040, -f1041, f1042, -f1043, f1047], num=1011)
volumes1000 = [v1007, v1008, v1009, v1010, v1011]
for v in volumes1000:
    volumes.append(v)

volumes_b = [v1008, v1009, v1010, v1011]
for v in volumes_b:
    v.category1 = "border"

pc = PrimalComplex3D(nodes, edges, faces, volumes, renumber=True)
dc = None
dc = DualComplex3D(pc)


(figs,ax) = pf.getFigures(numTotal=8)

pf.setLabels(ax[0])

for n in nodes:
    n.plotNode(ax[0], showLabel=True)
    n.plotNode(ax[3], showLabel=False)
    n.plotNode(ax[4], showLabel=False)

for e in edges:
    e.plotEdge(ax[0], showLabel=False, showArrow=False)
    e.plotEdge(ax[1], showLabel=True, showArrow=True)
    e.plotEdge(ax[2], showLabel=False, showArrow=False)

for e in edges_for_face:
    e.plotEdge(ax[3])

for f in faces:
    f.plotFace(ax[2], showLabel=True, showNormalVec=False, showBarycenter=False)

for v in volumes:
    v.plotVolume(ax[3], showLabel=False, showBarycenter=False, showNormalVec=False)


pf.setAxesEqual(ax[4])

if dc:
    for n in dc.nodes:
        n.plotNode(ax[4], showLabel=False)
        n.plotNode(ax[1], showLabel=False)

    for e in  dc.edges:
        e.plotEdge(ax[5], showLabel=False, showArrow=False)

    for f in dc.faces:
        f.plotFace(ax[6], showLabel=False, showNormalVec=False, showBarycenter=False)

    for v in dc.volumes:
        v.plotVolume(ax[7], showLabel=False, showBarycenter=False)

for f in faces_for_volume:
    f.plotFace(ax[4])

n = nodes[1]
v = n.dualCell3D

n.plotNode(ax[7])
v.plotVolume(ax[7], color=tc.TUMBlack())


# n_test = nodes[0]
# n_test.plotNode(ax[1])
# n_test.dualCell3D.plotVolume(ax[1])
# n_test.dualCell3D.faces[-1].plotFace(ax[1])

# for n in nodes:
#     in_volume = False
#     for e in n.edges:
#         for f in e.faces:
#             if v50 in f.volumes:
#                 in_volume = True

#     if not in_volume:
#         print(n)
