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

from kCells.node.node import Node
from kCells.edge.edge import Edge
from kCells.face.face import Face
from kCells.volume.volume import Volume

from complex.primalComplex3D import PrimalComplex3D
from complex.dualComplex3D import DualComplex3D



set_logging_format(logging.DEBUG)


# n0 = Node(0.0, -2.5, 5.0, num=0)
# n1 = Node(2.5, 0.0, 5.0, num=1)
# n3 = Node(-2.5, 0.0, 5.0, num=3)
# n4 = Node(0.0, -5.0, 2.5, num=4)
# n5 = Node(5.0, 0.0, 2.5, num=5)
n7 = Node(-5.0, 0.0, 2.5, num=7)
# n8 = Node(2.5, -5.0, 0.0, num=8)
# n9 = Node(5.0, -2.5, 0.0, num=9)
# n14 = Node(-5.0, -2.5, 0.0, num=14)
# n15 = Node(-2.5, -5.0, 0.0, num=15)
# n16 = Node(0.0, -5.0, -2.5, num=16)
# n17 = Node(5.0, 0.0, -2.5, num=17)
# n20 = Node(0.0, -2.5, -5.0, num=20)
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


# e0 = Edge(n0, n1, num=0)
# e3 = Edge(n3, n0, num=3)
# e4 = Edge(n4, n0, num=4)
# e5 = Edge(n5, n1, num=5)
# e7 = Edge(n3, n7, num=7)
# e8 = Edge(n9, n8, num=8)
# e9 = Edge(n9, n5, num=9)
# e16 = Edge(n14, n7, num=16)
# e17 = Edge(n15, n14, num=17)
# e18 = Edge(n4, n15, num=18)
# e19 = Edge(n8, n4, num=19)
# e21 = Edge(n8, n16, num=21)
# e22 = Edge(n9, n17, num=22)
# e28 = Edge(n16, n20, num=28)
# e29 = Edge(n17, n21, num=29)
# e32 = Edge(n20, n21, num=32)
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
# e1011 = Edge(n1000, n1, num=1011)
# e1012 = Edge(n5, n1001, num=1012)
e1013 = Edge(n1001, n155, num=1013)
e1014 = Edge(n165, n171, num=1014)
e1015 = Edge(n1001, n165, num=1015)
e1016 = Edge(n1001, n153, num=1016)
e1017 = Edge(n21, n153, num=1017)
e1018 = Edge(n1000, n151, num=1018)
# e1019 = Edge(n8, n165, num=1019)
# e1020 = Edge(n9, n1001, num=1020)
# e1021 = Edge(n4, n151, num=1021)
# e1022 = Edge(n0, n1000, num=1022)
e1023 = Edge(n1000, n159, num=1023)
# e1024 = Edge(n16, n147, num=1024)
# e1025 = Edge(n147, n20, num=1025)
# e1026 = Edge(n15, n167, num=1026)
# e1027 = Edge(n167, n14, num=1027)
e1028 = Edge(n7, n159, num=1028)
# e1029 = Edge(n1000, n3, num=1029)
# e1030 = Edge(n1001, n17, num=1030)
# e1033 = Edge(n17, n5, num=1033)
e1034 = Edge(n157, n7, num=1034)
e1035 = Edge(n157, n21, num=1035)
# e1036 = Edge(n3, n1, num=1036)
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


# f1 = Face([-e19, -e8, e9, e5, -e0, -e4], num=1)
# f4 = Face([-e16, -e17, -e18, e4, -e3, e7], num=4)
# f9 = Face([-e21, -e8, e22, e29, -e32, -e28], num=9)
# f141 = Face([e1024, e1025, -e28], num=141)
# f183 = Face([e1026, e1027, -e17], num=183)
faces = []
# faces = [f1, f4, f9, f141, f183]




f1000 = Face([e1000,e1001,e1002,e1003], num=1000)

f1005 = Face([e1000,e1005,-e1013,e1016,-e1004], num=1005)
f1006 = Face([e1001,e1007,-e1023,e1010,-e1005], num=1006)
# f1009 = Face([e1010,-e1013,-e1012,e5,-e1011], num=1009)
# f1010 = Face([e1028,-e1023,e1029,e7], num=1010)
# f1011 = Face([e1021,-e1018,-e1022,-e4], num=1011)
# f1012 = Face([e3, e1022, e1029], num=1012)
# f1013 = Face([e0, -e1011, -e1022], num=1013)
# f1014 = Face([e8,e1019,-e1015,-e1020], num=1014)
# f1015 = Face([e9, e1012, -e1020], num=1015)
# f1016 = Face([e22, -e1030, -e1020], num=1016)
# f1017 = Face([e32, e1017, -e332, -e1009, e1025], num=1017)
f1018 = Face([e335, -e1010, e1018, e1008], num=1018)
f1019 = Face([e346, -e1023, e1018, -e347], num=1019)
f1020 = Face([e331, -e1015, e1016, -e332], num=1020)
f1021 = Face([e335, -e1013, e1015, e1014], num=1021)
# f1022 = Face([e16, e1028, -e346, e345, e1027], num=1022)
# f1023 = Face([e21, e1024, e1009, e331, -e1019], num=1023)
# f1024 = Face([e19, e1021, e1008, -e1014, -e1019], num=1024)
# f1025 = Face([e18, e1026, -e345, e347, -e1021], num=1025)
# f1026 = Face([e29, e1017, -e1016, e1030], num=1026)
f1027 = Face([e1003, e1004, -e1017, -e1035, -e1006], num=1027)
f1028 = Face([e1002, e1006, e1034, e1028, -e1007], num=1028)
# f1029 = Face([e9, -e1033, -e22], num=1029)
# f1030 = Face([e3, e0, -e1036], num=1030)
# f1031 = Face([e1034, -e7, e1036, -e5, -e1033, e29, -e1035], num=1031)
# f1032 = Face([[e1035, -e32, -e1025, -e344, e343], [e344, -e1024, -e21, e19, e18, e1026, -e342], [e342, e1027, e16, -e1034, -e343]], num=1032) #  [e343, e1034, -e16, -e1027, -e342]
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

# v1002 = Volume([f1017, f1023, -f1020, -f1026, -f141, f9, -f1016, f1014])
# v1003 = Volume([-f1014, -f1021, f1018, f1011, -f1013, -f1, f1015, f1009, -f1024])
# v1004 = Volume([-f1022, -f1025, f183, -f4, f1010, -f1011, -f1012, -f1019])
# v1005 = Volume([f1006, f1005, -f1000, f1027, f1028, f1026, -f1031, f1029, -f1030, f1012, f1013, -f1015, f1016, -f1009, -f1010], num=1005)
# v1006 = Volume([f1032, f1031, f1, f4, -f9, -f183, f141, f1030, -f1029])
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






