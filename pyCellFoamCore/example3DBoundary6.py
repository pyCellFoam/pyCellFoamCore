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


n0 = Node(0.0, -2.5, 5.0, num=0)
n1 = Node(2.5, 0.0, 5.0, num=1)
n2 = Node(0.0, 2.5, 5.0, num=2)
n3 = Node(-2.5, 0.0, 5.0, num=3)
n4 = Node(0.0, -5.0, 2.5, num=4)
n5 = Node(5.0, 0.0, 2.5, num=5)
n6 = Node(0.0, 5.0, 2.5, num=6)
n7 = Node(-5.0, 0.0, 2.5, num=7)
n8 = Node(2.5, -5.0, 0.0, num=8)
n9 = Node(5.0, -2.5, 0.0, num=9)
n10 = Node(5.0, 2.5, 0.0, num=10)
n11 = Node(2.5, 5.0, 0.0, num=11)
n12 = Node(-2.5, 5.0, 0.0, num=12)
n13 = Node(-5.0, 2.5, 0.0, num=13)
n14 = Node(-5.0, -2.5, 0.0, num=14)
n15 = Node(-2.5, -5.0, 0.0, num=15)
n16 = Node(0.0, -5.0, -2.5, num=16)
n17 = Node(5.0, 0.0, -2.5, num=17)
n18 = Node(0.0, 5.0, -2.5, num=18)
n19 = Node(-5.0, 0.0, -2.5, num=19)
n20 = Node(0.0, -2.5, -5.0, num=20)
n21 = Node(2.5, 0.0, -5.0, num=21)
n22 = Node(0.0, 2.5, -5.0, num=22)
n23 = Node(-2.5, 0.0, -5.0, num=23)
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
nodes = [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23,
         n153, n155, n157, n159, n168, n169, n172, n173, n147, n151, n165, n167, n170, n171, n174, n175]

n1000 = Node(0.0, 0.0, 15.0, num=1000)
n1001 = Node(15.0, 0.0, 0.0, num=1001)
nodes1000 = [n1000, n1001]
for n in nodes1000:
    nodes.append(n)


e0 = Edge(n0, n1, num=0)
e1 = Edge(n1, n2, num=1)
e2 = Edge(n2, n3, num=2)
e3 = Edge(n3, n0, num=3)
e4 = Edge(n4, n0, num=4)
e5 = Edge(n5, n1, num=5)
e6 = Edge(n2, n6, num=6)
e7 = Edge(n3, n7, num=7)
e8 = Edge(n9, n8, num=8)
e9 = Edge(n9, n5, num=9)
e10 = Edge(n5, n10, num=10)
e11 = Edge(n11, n10, num=11)
e12 = Edge(n11, n6, num=12)
e13 = Edge(n6, n12, num=13)
e14 = Edge(n13, n12, num=14)
e15 = Edge(n7, n13, num=15)
e16 = Edge(n14, n7, num=16)
e17 = Edge(n15, n14, num=17)
e18 = Edge(n4, n15, num=18)
e19 = Edge(n8, n4, num=19)
e21 = Edge(n8, n16, num=21)
e22 = Edge(n9, n17, num=22)
e23 = Edge(n17, n10, num=23)
e24 = Edge(n11, n18, num=24)
e25 = Edge(n18, n12, num=25)
e26 = Edge(n19, n13, num=26)
e28 = Edge(n16, n20, num=28)
e29 = Edge(n17, n21, num=29)
e30 = Edge(n22, n18, num=30)
e31 = Edge(n23, n19, num=31)
e32 = Edge(n20, n21, num=32)
e33 = Edge(n21, n22, num=33)
e34 = Edge(n22, n23, num=34)
# e36 = Edge(n24, n25, num=36)
# e37 = Edge(n25, n26, num=37)
# e38 = Edge(n26, n27, num=38)
# e39 = Edge(n27, n24, num=39)
# e40 = Edge(n28, n24, num=40)
# e41 = Edge(n29, n25, num=41)
# e42 = Edge(n26, n30, num=42)
# e43 = Edge(n27, n5, num=43)
# e44 = Edge(n32, n31, num=44)
# e45 = Edge(n32, n29, num=45)
# e46 = Edge(n29, n33, num=46)
# e47 = Edge(n34, n33, num=47)
# e48 = Edge(n34, n30, num=48)
# e49 = Edge(n30, n35, num=49)
# e50 = Edge(n10, n35, num=50)
# e51 = Edge(n36, n9, num=51)
# e52 = Edge(n28, n36, num=52)
# e53 = Edge(n31, n28, num=53)
# e54 = Edge(n37, n36, num=54)
# e57 = Edge(n38, n33, num=57)
# e58 = Edge(n34, n39, num=58)
# e59 = Edge(n39, n35, num=59)
# e60 = Edge(n37, n40, num=60)
# e61 = Edge(n38, n41, num=61)
# e62 = Edge(n42, n39, num=62)
# e63 = Edge(n43, n17, num=63)
# e65 = Edge(n41, n42, num=65)
# e66 = Edge(n42, n43, num=66)
# e67 = Edge(n43, n40, num=67)
# e128 = Edge(n80, n81, num=128)
# e129 = Edge(n81, n82, num=129)
# e130 = Edge(n82, n83, num=130)
# e132 = Edge(n84, n80, num=132)
# e133 = Edge(n85, n81, num=133)
# e134 = Edge(n82, n86, num=134)
# e135 = Edge(n83, n87, num=135)
# e136 = Edge(n89, n88, num=136)
# e137 = Edge(n89, n85, num=137)
# e138 = Edge(n85, n90, num=138)
# e139 = Edge(n91, n90, num=139)
# e140 = Edge(n91, n86, num=140)
# e141 = Edge(n86, n92, num=141)
# e142 = Edge(n93, n92, num=142)
# e143 = Edge(n87, n93, num=143)
# e145 = Edge(n95, n94, num=145)
# e147 = Edge(n88, n84, num=147)
# e148 = Edge(n96, n95, num=148)
# e149 = Edge(n88, n96, num=149)
# e150 = Edge(n89, n97, num=150)
# e151 = Edge(n97, n90, num=151)
# e152 = Edge(n91, n98, num=152)
# e153 = Edge(n98, n92, num=153)
# e154 = Edge(n99, n93, num=154)
# e155 = Edge(n94, n99, num=155)
# e156 = Edge(n96, n0, num=156)
# e157 = Edge(n97, n1, num=157)
# e158 = Edge(n2, n98, num=158)
# e159 = Edge(n3, n99, num=159)
# e161 = Edge(n101, n102, num=161)
# e162 = Edge(n102, n103, num=162)
# e163 = Edge(n103, n100, num=163)
# e164 = Edge(n104, n100, num=164)
# e165 = Edge(n105, n101, num=165)
# e166 = Edge(n102, n106, num=166)
# e167 = Edge(n103, n85, num=167)
# e168 = Edge(n108, n107, num=168)
# e170 = Edge(n105, n109, num=170)
# e171 = Edge(n110, n109, num=171)
# e172 = Edge(n110, n106, num=172)
# e173 = Edge(n106, n111, num=173)
# e174 = Edge(n90, n111, num=174)
# e175 = Edge(n112, n89, num=175)
# e176 = Edge(n104, n112, num=176)
# e178 = Edge(n113, n112, num=178)
# e179 = Edge(n107, n113, num=179)
# e180 = Edge(n108, n114, num=180)
# e181 = Edge(n114, n109, num=181)
# e182 = Edge(n110, n115, num=182)
# e183 = Edge(n115, n111, num=183)
# e184 = Edge(n113, n24, num=184)
# e185 = Edge(n114, n25, num=185)
# e186 = Edge(n26, n115, num=186)
# e187 = Edge(n27, n97, num=187)
# e240 = Edge(n81, n103, num=240)
# e244 = Edge(n21, n43, num=244)
# e248 = Edge(n112, n88, num=248)
# e249 = Edge(n113, n28, num=249)
# e250 = Edge(n96, n4, num=250)
# e251 = Edge(n36, n8, num=251)
# e257 = Edge(n99, n7, num=257)
# e261 = Edge(n114, n29, num=261)
# e286 = Edge(n153, n38, num=286)
# e287 = Edge(n153, n41, num=287)
# e290 = Edge(n155, n101, num=290)
# e293 = Edge(n155, n105, num=293)
e295 = Edge(n157, n19, num=295)
e298 = Edge(n157, n23, num=298)
# e301 = Edge(n159, n87, num=301)
# e303 = Edge(n159, n83, num=303)
# e348 = Edge(n16, n20, geometricNodes=[n147], num=348)
# e349 = Edge(n37, n40, geometricNodes=[n146], num=349)
# e350 = Edge(n104, n100, geometricNodes=[n150], num=350)
# e351 = Edge(n84, n80, geometricNodes=[n151], num=351)
# e352 = Edge(n108, n107, geometricNodes=[n164], num=352)
# e353 = Edge(n32, n31, geometricNodes=[n165], num=353)
# e354 = Edge(n95, n94, geometricNodes=[n166], num=354)
# e355 = Edge(n15, n14, geometricNodes=[n167], num=355)
# e271 = Edge(n146, n147, num=271)
# e279 = Edge(n150, n151, num=279)
# e316 = Edge(n164, n165, num=316)
# e319 = Edge(n166, n167, num=319)
e346 = Edge(n175, n159, num=346)
e345 = Edge(n175, n167, num=345)
e347 = Edge(n175, n151, num=347)
# e333 = Edge(n171, n150, num=333)
# e334 = Edge(n171, n164, num=334)
e335 = Edge(n171, n155, num=335)
e331 = Edge(n170, n165, num=331)
# e330 = Edge(n170, n146, num=330)
e332 = Edge(n170, n153, num=332)
e342 = Edge(n174, n167, num=342)
e343 = Edge(n174, n157, num=343)
e344 = Edge(n174, n147, num=344)

edges = [e0, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15,
         e16, e17, e18, e19, e21, e22, e23, e24, e25, e26, e28, e29, e30,
         e31, e32, e33, e34, e295, e298, e346, e345, e347,
         e335, e331, e332, e342, e343, e344]
# edges = [e0, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e21, e22, e23, e24, e25, e26, e28, e29, e30, e31, e32, e33, e34, e36, e37, e38, e39, e40, e41, e42, e43, e44, e45, e46, e47, e48, e49, e50, e51, e52, e53, e54, e57, e58, e59, e60, e61, e62, e63, e65, e66, e67, e128, e129, e130, e132, e133, e134, e135, e136, e137, e138, e139, e140, e141, e142, e143, e145, e147, e148, e149, e150, e151, e152, e153, e154, e155, e156, e157, e158, e159, e161, e162, e163, e164, e165, e166, e167, e168, e170, e171, e172, e173, e174, e175, e176, e178, e179, e180, e181, e182, e183, e184, e185, e186, e187, e240, e244, e248, e249, e250, e251, e257, e261, e286, e287, e290, e293, e295, e298, e301, e303, e348, e349, e350, e351, e352, e353, e354, e355, e271, e279, e316, e319, e346, e345, e347, e333, e334, e335, e331, e330, e332, e342, e343, e344]

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
e1011 = Edge(n1000, n1, num=1011)
e1012 = Edge(n5, n1001, num=1012)
e1013 = Edge(n1001, n155, num=1013)
e1014 = Edge(n165, n171, num=1014)
e1015 = Edge(n1001, n165, num=1015)
e1016 = Edge(n1001, n153, num=1016)
e1017 = Edge(n21, n153, num=1017)
e1018 = Edge(n1000, n151, num=1018)
e1019 = Edge(n8, n165, num=1019)
e1020 = Edge(n9, n1001, num=1020)
e1021 = Edge(n4, n151, num=1021)
e1022 = Edge(n0, n1000, num=1022)
e1023 = Edge(n1000, n159, num=1023)
e1024 = Edge(n16, n147, num=1024)
e1025 = Edge(n147, n20, num=1025)
e1026 = Edge(n15, n167, num=1026)
e1027 = Edge(n167, n14, num=1027)
e1028 = Edge(n7, n159, num=1028)
e1029 = Edge(n1000, n3, num=1029)
e1030 = Edge(n1001, n17, num=1030)

edges1000 = [e1000,e1001,e1002,e1003,e1004,e1005,e1006,e1007,e1008,e1009,
             e1010,e1011,e1012,e1013,e1014,e1015,e1016,e1017,e1018,e1019,
             e1020,e1021,e1022,e1023,e1024,e1025,e1026,e1027,e1028,e1029,
             e1030]
for e in edges1000:
    edges.append(e)


# edges = [e344, -e1024, -e21, e19, e18, e355, -e342]


f0 = Face([e0, e1, e2, e3], num=0)
f1 = Face([-e19, -e8, e9, e5, -e0, -e4], num=1)
f2 = Face([e10, -e11, e12, -e6, -e1, -e5], num=2)
f3 = Face([e13, -e14, -e15, -e7, -e2, e6], num=3)
f4 = Face([-e16, -e17, -e18, e4, -e3, e7], num=4)
f6 = Face([e22, e23, -e10, -e9], num=6)
f7 = Face([e24, e25, -e13, -e12], num=7)
f9 = Face([-e21, -e8, e22, e29, -e32, -e28], num=9)
f10 = Face([e23, -e11, e24, -e30, -e33, -e29], num=10)
f11 = Face([e25, -e14, -e26, -e31, -e34, e30], num=11)
f141 = Face([e1024, e1025, -e28], num=141)
f161 = Face([-e298, e295, -e31], num=161)
f183 = Face([e1026, e1027, -e17], num=183)
f227 = Face([[e342, e1027, e16, e15, -e26, -e295, -e343], [e344, -e1024, -e21, e19, e18, e1026, e1027, -e342], [e343, e298, -e34, -e33, -e32, -e1025, -e1024, -e344]], num=227)
faces = []
faces = [f0, f1, f2, f3, f4, f6, f7, f9, f10, f11, f141, f161, f183, f227]




f1000 = Face([e1000,e1001,e1002,e1003], num=1000)

# f1001 = Face([-e1004,e1000,e1005,e293,e170,-e181,e261,e46,-e57,-e286], num=1001)
# f1002 = Face([-e1005,e1001,e1007,e303,-e130,-e129,e240,-e162,-e161,-e290], num=1002)
# f1003 = Face([-e1006,-e1002,e1007,e301,e143,-e154,e257,e15,-e26,-e295], num=1003)
# f1004 = Face([-e1006,e1003,e1004,e287,e65,e66,-e244,e33,e34,-e298], num=1004)
f1005 = Face([e1000,e1005,-e1013,e1016,-e1004], num=1005)
f1006 = Face([e1001,e1007,-e1023,e1010,-e1005], num=1006)
f1007 = Face([e1002,e1006,e295,e26,-e15,e1028,-e1007], num=1007)
f1008 = Face([e1003,e1004,-e1017,e33,e34,-e298,-e1006], num=1008)
f1009 = Face([e1010,-e1013,-e1012,e5,-e1011], num=1009)
f1010 = Face([e1028,-e1023,e1029,e7], num=1010)
f1011 = Face([e1021,-e1018,-e1022,-e4], num=1011)
f1012 = Face([e3, e1022, e1029], num=1012)
f1013 = Face([e0, -e1011, -e1022], num=1013)
f1014 = Face([e8,e1019,-e1015,-e1020], num=1014)
f1015 = Face([e9, e1012, -e1020], num=1015)
f1016 = Face([e22, -e1030, -e1020], num=1016)
f1017 = Face([e32, e1017, -e332, -e1009, e1025], num=1017)
f1018 = Face([e335, -e1010, e1018, e1008], num=1018)
f1019 = Face([e346, -e1023, e1018, -e347], num=1019)
f1020 = Face([e331, -e1015, e1016, -e332], num=1020)
f1021 = Face([e335, -e1013, e1015, e1014], num=1021)
f1022 = Face([e16, e1028, -e346, e345, e1027], num=1022)
f1023 = Face([e21, e1024, e1009, e331, -e1019], num=1023)
f1024 = Face([e19, e1021, e1008, -e1014, -e1019], num=1024)
f1025 = Face([e18, e1026, -e345, e347, -e1021], num=1025)
f1026 = Face([e29, e1017, -e1016, e1030], num=1026)
# edges = [e18, e1026, -e345, e347, e1021]
faces1000 = [f1000,f1005,f1006,f1007,f1008,f1009,f1010,f1011,f1012,f1013,f1014,f1015,f1016,
             f1017, f1018, f1019, f1020, f1021, f1022, f1023, f1024, f1025, f1026]

for f in faces1000:
    faces.append(f)

# v11 = Volume([-f116, f76, f61, f101, f117, -f118, -f18, -f1, -f119, f120], num=11)
# v16 = Volume([f119, f25, f9, -f114, f142, -f141, f220], num=16)
# v18 = Volume([-f150, f151, f106, -f69, -f53, f116, f221], num=18)
# v25 = Volume([-f177, f73, f132, -f117, -f15, f178, f222], num=25)
# v26 = Volume([-f182, f64, f118, -f127, -f4, f183, f223], num=26)
# v41 = Volume([f53, f54, f55, f58, f59, -f61, -f62, -f63, -f64, -f0, -f151, -f167, f182, f224], num=41)
# v44 = Volume([f67, f68, f69, f72, -f58, -f74, -f73, -f75, -f76, -f14, f150, f158, f177, f225], num=44)
# v47 = Volume([f14, f15, f16, f17, f18, f21, -f6, -f23, -f24, -f25, -f178, -f142, -f152, f226], num=47)
v50 = Volume([f0, f1, f2, f3, f4, f6, f7, -f9, -f10, -f11, -f183, f141, f161, f227], num=50)
volumes = [v50,]
# volumes = [v11, v16, v18, v25, v26, v41, v44, v47, v50]
# volumes_b = [v11, v16, v18, v25, v26, v41, v44, v47, v50]

faces_for_volume = [-f1022, -f1025, f183, -f4, f1010, -f1011, -f1012, -f1019]

# v1000 = Volume([-f1000,f1001,f1002,-f1003,f1004,-f2, -f3, -f7, f10, f11, -f16, -f17, -f21, f23, f24, -f54, -f55, -f59, f62, f63, -f67, -f68, -f72, f74, f75, -f101, -f106, f114, f127, -f132, f152, -f158, -f161, f167], num=1000)
v1001 = Volume([-f0, -f2, -f3, -f6, -f7, f10, f11, -f161, -f1000, f1005, f1006, f1007, f1008, -f1009, -f1010, f1012, f1013, -f1015, f1016, f1026])
v1002 = Volume([f1017, f1023, -f1020, -f1026, -f141, f9, -f1016, f1014])
v1003 = Volume([-f1014, -f1021, f1018, f1011, -f1013, -f1, f1015, f1009, -f1024])
v1004 = Volume([-f1022, -f1025, f183, -f4, f1010, -f1011, -f1012, -f1019])
volumes1000 = [v1001, v1002, v1003, v1004]
for v in volumes1000:
    volumes.append(v)
# #

volumes_b = [v50, v1002, v1003, v1004]
for v in volumes_b:
    v.category1 = "border"

pc = PrimalComplex3D(nodes, edges, faces, volumes, renumber=True)
dc = None
dc = DualComplex3D(pc)


(figs,ax) = pf.getFigures(numTotal=8)

pf.setLabels(ax[0])

for n in nodes:
    n.plotNode(ax[0], showLabel=True)

for e in edges:
    e.plotEdge(ax[0], showLabel=False, showArrow=False)
    e.plotEdge(ax[1], showLabel=True, showArrow=True)
    e.plotEdge(ax[2], showLabel=False, showArrow=False)

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






