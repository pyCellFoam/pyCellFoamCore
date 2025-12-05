# Auto-generated code for Complex3D
import logging
from pyCellFoamCore.k_cells.node.node import Node
from pyCellFoamCore.k_cells.node.node import NodePlotly
from pyCellFoamCore.k_cells.edge.edge import Edge
from pyCellFoamCore.k_cells.edge.baseEdge import EdgePlotly
from pyCellFoamCore.k_cells.face.face import Face
from pyCellFoamCore.k_cells.face.baseFace import FacePlotly
from pyCellFoamCore.k_cells.volume.volume import Volume
from pyCellFoamCore.k_cells.volume.volume import VolumePlotly
from pyCellFoamCore.tools.logging_formatter import set_logging_format
import pyCellFoamCore.tools.tumcolor as tc
from pyCellFoamCore.complex.primalComplex3D import PrimalComplex3D
from pyCellFoamCore.complex.dualComplex3D import DualComplex3D

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)

def get_k_cells():

    n0 = Node(1.08, 1.23, 0.15, num=0)
    n1 = Node(0.78, 0.96, 0.3, num=1)
    n2 = Node(0.57, 1.1099999999999999, 0.36, num=2)
    n3 = Node(1.5899999999999999, 1.17, 0.44999999999999996, num=3)
    n4 = Node(1.86, 1.26, 0.48, num=4)
    n5 = Node(1.65, 1.26, 0.51, num=5)
    n6 = Node(1.2, 0.36, 0.63, num=6)
    n7 = Node(0.96, 0.54, 0.63, num=7)
    n8 = Node(0.96, 0.6599999999999999, 0.69, num=8)
    n9 = Node(1.38, 0.51, 0.72, num=9)
    n10 = Node(1.26, 0.72, 0.78, num=10)
    n11 = Node(0.48, 1.05, 0.87, num=11)
    n12 = Node(0.63, 0.21, 1.02, num=12)
    n13 = Node(0.78, 0.75, 1.05, num=13)
    n14 = Node(1.68, 0.3, 1.17, num=14)
    n15 = Node(1.23, 0.21, 0.0, num=15)
    n16 = Node(0.32999999999999996, 0.24, 0.0, num=16)
    n17 = Node(1.68, 0.21, 1.3199999999999998, num=17)
    n18 = Node(1.71, 0.39, 1.3199999999999998, num=18)
    n19 = Node(0.6, 0.54, 1.3199999999999998, num=19)
    n20 = Node(0.72, 0.54, 0.0, num=20)
    n21 = Node(0.72, 0.8099999999999999, 0.0, num=21)
    n22 = Node(0.96, 0.87, 1.3199999999999998, num=22)
    n23 = Node(1.3199999999999998, 0.87, 1.3199999999999998, num=23)
    n24 = Node(0.21, 0.99, 0.0, num=24)
    n25 = Node(1.1099999999999999, 1.23, 0.0, num=25)
    n26 = Node(1.68, 1.29, 1.3199999999999998, num=26)
    n27 = Node(0.63, 1.71, 1.3199999999999998, num=27)
    n28 = Node(0.42, 1.6199999999999999, 1.3199999999999998, num=28)
    n29 = Node(0.21, 0.0, 0.3, num=29)
    n30 = Node(0.8999999999999999, 1.71, 0.3, num=30)
    n31 = Node(0.51, 1.71, 0.32999999999999996, num=31)
    n32 = Node(1.44, 1.71, 0.6599999999999999, num=32)
    n33 = Node(0.42, 0.0, 0.87, num=33)
    n34 = Node(1.1099999999999999, 0.0, 0.8999999999999999, num=34)
    n35 = Node(0.72, 0.0, 1.1099999999999999, num=35)
    n36 = Node(1.8599999999999999, 0.57, 0.44999999999999996, num=36)
    n37 = Node(0.0, 0.8999999999999999, 0.8099999999999999, num=37)
    n38 = Node(1.8599999999999999, 0.36, 1.02, num=38)
    n39 = Node(0.0, 0.48, 1.1099999999999999, num=39)
    n10000 = Node(1.8599999999999999, 1.245, 0.0, num=10000)
    n10001 = Node(1.005, 1.71, 0.0, num=10001)
    n10002 = Node(0.36, 1.71, 0.0, num=10002)
    n10003 = Node(0.0, 0.9449999999999998, 0.0, num=10003)
    n10004 = Node(1.8599999999999999, 1.71, 0.57, num=10004)
    n10005 = Node(1.8599999999999999, 1.275, 1.3199999999999998, num=10005)
    n10006 = Node(1.17, 0.0, 0.0, num=10006)
    n10007 = Node(1.395, 0.0, 1.3199999999999998, num=10007)
    n10008 = Node(0.6599999999999999, 0.0, 1.3199999999999998, num=10008)
    n10009 = Node(1.8599999999999999, 0.285, 1.3199999999999998, num=10009)
    n10010 = Node(1.8599999999999999, 0.375, 1.3199999999999998, num=10010)
    n10011 = Node(0.06999999999999996, 0.0, 0.0, num=10011)
    n10012 = Node(0.0, 0.51, 1.3199999999999998, num=10012)
    n10013 = Node(0.0, 1.2599999999999998, 1.3199999999999998, num=10013)
    gn0 = Node(0.9224999999999999, 1.0574999999999999, 0.11249999999999999, num=0)
    gn1 = Node(1.4759999999999998, 1.2269999999999999, 0.21600000000000003, num=1)
    gn2 = Node(1.134, 0.9479999999999998, 0.47400000000000003, num=2)
    gn3 = Node(1.02375, 1.47, 0.11249999999999999, num=3)
    gn4 = Node(0.768, 1.3439999999999999, 0.288, num=4)
    gn5 = Node(1.332, 1.416, 0.414, num=5)
    gn6 = Node(0.828, 0.7020000000000001, 0.324, num=6)
    gn7 = Node(0.57, 0.9675, 0.16499999999999998, num=7)
    gn8 = Node(0.7140000000000001, 0.906, 0.654, num=8)
    gn9 = Node(0.4125, 1.38, 0.1725, num=9)
    gn10 = Node(0.25199999999999995, 0.9989999999999999, 0.40800000000000003, num=10)
    gn11 = Node(0.5474999999999999, 1.365, 0.72, num=11)
    gn12 = Node(1.566, 0.8459999999999999, 0.576, num=12)
    gn13 = Node(1.5, 1.0619999999999998, 0.876, num=13)
    gn14 = Node(1.6724999999999999, 1.485, 0.5549999999999999, num=14)
    gn15 = Node(1.7325, 1.27125, 0.9074999999999999, num=15)
    gn16 = Node(1.0274999999999999, 0.4125, 0.315, num=16)
    gn17 = Node(1.4175, 0.4125, 0.45, num=17)
    gn18 = Node(1.152, 0.558, 0.6900000000000001, num=18)
    gn19 = Node(1.1774999999999998, 0.1425, 0.38249999999999995, num=19)
    gn20 = Node(0.9239999999999998, 0.22200000000000003, 0.8579999999999999, num=20)
    gn21 = Node(1.4074999999999998, 0.22999999999999998, 1.01, num=21)
    gn22 = Node(0.5449999999999999, 0.255, 0.47, num=22)
    gn23 = Node(0.786, 0.54, 0.942, num=23)
    gn24 = Node(1.056, 0.774, 1.0319999999999998, num=24)
    gn25 = Node(1.6949999999999998, 0.43500000000000005, 0.84, num=25)
    gn26 = Node(1.47, 0.558, 1.062, num=26)
    gn27 = Node(0.38249999999999995, 1.29, 1.0799999999999998, num=27)
    gn28 = Node(0.372, 0.744, 1.0319999999999998, num=28)
    gn29 = Node(0.7124999999999999, 1.065, 1.1400000000000001, num=29)
    gn30 = Node(0.4125, 0.3075, 1.0799999999999998, num=30)
    gn31 = Node(0.6525000000000001, 0.1875, 1.1925, num=31)
    gn32 = Node(1.77, 0.28874999999999995, 1.2075, num=32)
    gn33 = Node(1.7774999999999999, 0.35624999999999996, 1.2075, num=33)
    nodes = [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21, n22, n23, n24, n25, n26, n27, n28, n29, n30, n31, n32, n33, n34, n35, n36, n37, n38, n39, n10000, n10001, n10002, n10003, n10004, n10005, n10006, n10007, n10008, n10009, n10010, n10011, n10012, n10013]
    geometric_nodes = [gn0, gn1, gn2, gn3, gn4, gn5, gn6, gn7, gn8, gn9, gn10, gn11, gn12, gn13, gn14, gn15, gn16, gn17, gn18, gn19, gn20, gn21, gn22, gn23, gn24, gn25, gn26, gn27, gn28, gn29, gn30, gn31, gn32, gn33]

    x_min = min(node.xCoordinate for node in nodes+geometric_nodes)
    x_max = max(node.xCoordinate for node in nodes+geometric_nodes)
    y_min = min(node.yCoordinate for node in nodes+geometric_nodes)
    y_max = max(node.yCoordinate for node in nodes+geometric_nodes)
    z_min = min(node.zCoordinate for node in nodes+geometric_nodes)
    z_max = max(node.zCoordinate for node in nodes+geometric_nodes)

    n20000 = Node(x_min, y_min, z_min, num=20000)
    n20001 = Node(x_max, y_min, z_min, num=20001)
    n20002 = Node(x_min, y_max, z_min, num=20002)
    n20003 = Node(x_max, y_max, z_min, num=20003)
    n20004 = Node(x_min, y_min, z_max, num=20004)
    n20005 = Node(x_max, y_min, z_max, num=20005)
    n20006 = Node(x_min, y_max, z_max, num=20006)
    n20007 = Node(x_max, y_max, z_max, num=20007)

    n20008 = Node(1.5, y_max, z_max, num=20008)
    n20009 = Node(0, 0, 1, num=20009)
    n20010 = Node(x_max, 0.6, z_min, num=20010)

    nodes.extend([n20000, n20001, n20002, n20003, n20004, n20005, n20006, n20007, n20008, n20009, n20010])


    for n in nodes+geometric_nodes:
        n.xCoordinate = n.xCoordinate * 10
        n.yCoordinate = n.yCoordinate * 10
        n.zCoordinate = n.zCoordinate * 10

    e0 = Edge(n0, n1, num=0)
    e1 = Edge(n0, n3, num=1)
    e2 = Edge(n0, n25, num=2)
    e3 = Edge(n0, n30, num=3)
    e4 = Edge(n1, n2, num=4)
    e5 = Edge(n1, n8, num=5)
    e6 = Edge(n1, n21, num=6)
    e7 = Edge(n2, n11, num=7)
    e8 = Edge(n2, n24, num=8)
    e9 = Edge(n2, n31, num=9)
    e10 = Edge(n3, n4, num=10)
    e11 = Edge(n3, n5, num=11)
    e12 = Edge(n3, n10, num=12)
    e13 = Edge(n4, n5, num=13)
    e14 = Edge(n5, n26, num=14)
    e15 = Edge(n5, n32, num=15)
    e16 = Edge(n6, n7, num=16)
    e17 = Edge(n6, n9, num=17)
    e18 = Edge(n6, n15, num=18)
    e19 = Edge(n6, n34, num=19)
    e20 = Edge(n7, n8, num=20)
    e21 = Edge(n7, n12, num=21)
    e22 = Edge(n7, n20, num=22)
    e23 = Edge(n8, n10, num=23)
    e24 = Edge(n8, n13, num=24)
    e25 = Edge(n9, n10, num=25)
    e26 = Edge(n9, n14, num=26)
    e27 = Edge(n9, n36, num=27)
    e28 = Edge(n10, n23, num=28)
    e29 = Edge(n11, n13, num=29)
    e30 = Edge(n11, n27, num=30)
    e31 = Edge(n11, n37, num=31)
    e32 = Edge(n12, n19, num=32)
    e33 = Edge(n12, n33, num=33)
    e34 = Edge(n12, n35, num=34)
    e35 = Edge(n13, n19, num=35)
    e36 = Edge(n13, n22, num=36)
    e37 = Edge(n14, n17, num=37)
    e38 = Edge(n14, n18, num=38)
    e39 = Edge(n14, n38, num=39)
    e40 = Edge(n15, n36, num=40)
    e41 = Edge(n16, n20, num=41)
    e42 = Edge(n16, n29, num=42)
    e43 = Edge(n19, n39, num=43)
    e44 = Edge(n20, n21, num=44)
    e45 = Edge(n22, n23, num=45)
    e46 = Edge(n23, n26, num=46)
    e47 = Edge(n26, n32, num=47)
    e48 = Edge(n27, n31, num=48)
    e49 = Edge(n27, n28, num=49)
    e50 = Edge(n28, n37, num=50)
    e51 = Edge(n29, n33, num=51)
    e52 = Edge(n30, n31, num=52)
    e53 = Edge(n33, n39, num=53)
    e54 = Edge(n33, n35, num=54)
    e55 = Edge(n37, n39, num=55)
    e10000 = Edge(n21, n25, num=10000)
    e10001 = Edge(n25, n10000, num=10001)
    e10002 = Edge(n10000, n4, num=10002)
    e10003 = Edge(n30, n10001, num=10003)
    e10004 = Edge(n10001, n25, num=10004)
    e10005 = Edge(n32, n30, num=10005)
    e10006 = Edge(n24, n21, num=10006)
    e10007 = Edge(n31, n10002, num=10007)
    e10008 = Edge(n10002, n24, num=10008)
    e10009 = Edge(n24, n10003, num=10009)
    e10010 = Edge(n10003, n37, num=10010)
    e10011 = Edge(n4, n36, num=10011)
    e10012 = Edge(n4, n10004, num=10012)
    e10013 = Edge(n10004, n32, num=10013)
    e10014 = Edge(n4, n10005, num=10014)
    e10015 = Edge(n10005, n26, num=10015)
    e10016 = Edge(n20, n15, num=10016)
    e10017 = Edge(n34, n10006, num=10017)
    e10018 = Edge(n10006, n15, num=10018)
    e10019 = Edge(n35, n34, num=10019)
    e10020 = Edge(n34, n10007, num=10020)
    e10021 = Edge(n10007, n17, num=10021)
    e10022 = Edge(n38, n36, num=10022)
    e10023 = Edge(n23, n18, num=10023)
    e10024 = Edge(n22, n27, num=10024)
    e10025 = Edge(n35, n10008, num=10025)
    e10026 = Edge(n10008, n19, num=10026)
    e10027 = Edge(n19, n22, num=10027)
    e10028 = Edge(n38, n10009, num=10028)
    e10029 = Edge(n10009, n17, num=10029)
    e10030 = Edge(n38, n10010, num=10030)
    e10031 = Edge(n10010, n18, num=10031)
    e10032 = Edge(n17, n18, num=10032)
    e10033 = Edge(n16, n10011, num=10033)
    e10034 = Edge(n10011, n29, num=10034)
    e10035 = Edge(n19, n10012, num=10035)
    e10036 = Edge(n10012, n39, num=10036)
    e10037 = Edge(n28, n10013, num=10037)
    e10038 = Edge(n10013, n37, num=10038)
    ge1 = Edge(n0, gn0, num=1)  # Geometric edge
    ge0 = Edge(n25, gn0, num=0)  # Geometric edge
    ge2 = Edge(n1, gn0, num=2)  # Geometric edge
    ge3 = Edge(n21, gn0, num=3)  # Geometric edge
    ge5 = Edge(n0, gn1, num=5)  # Geometric edge
    ge4 = Edge(n25, gn1, num=4)  # Geometric edge
    ge6 = Edge(n3, gn1, num=6)  # Geometric edge
    ge7 = Edge(n4, gn1, num=7)  # Geometric edge
    ge8 = Edge(n10000, gn1, num=8)  # Geometric edge
    ge10 = Edge(n1, gn2, num=10)  # Geometric edge
    ge9 = Edge(n0, gn2, num=9)  # Geometric edge
    ge11 = Edge(n8, gn2, num=11)  # Geometric edge
    ge12 = Edge(n10, gn2, num=12)  # Geometric edge
    ge13 = Edge(n3, gn2, num=13)  # Geometric edge
    ge15 = Edge(n0, gn3, num=15)  # Geometric edge
    ge14 = Edge(n30, gn3, num=14)  # Geometric edge
    ge16 = Edge(n25, gn3, num=16)  # Geometric edge
    ge17 = Edge(n10001, gn3, num=17)  # Geometric edge
    ge19 = Edge(n1, gn4, num=19)  # Geometric edge
    ge18 = Edge(n0, gn4, num=18)  # Geometric edge
    ge20 = Edge(n2, gn4, num=20)  # Geometric edge
    ge21 = Edge(n31, gn4, num=21)  # Geometric edge
    ge22 = Edge(n30, gn4, num=22)  # Geometric edge
    ge24 = Edge(n0, gn5, num=24)  # Geometric edge
    ge23 = Edge(n30, gn5, num=23)  # Geometric edge
    ge25 = Edge(n3, gn5, num=25)  # Geometric edge
    ge26 = Edge(n5, gn5, num=26)  # Geometric edge
    ge27 = Edge(n32, gn5, num=27)  # Geometric edge
    ge29 = Edge(n8, gn6, num=29)  # Geometric edge
    ge28 = Edge(n1, gn6, num=28)  # Geometric edge
    ge30 = Edge(n7, gn6, num=30)  # Geometric edge
    ge31 = Edge(n20, gn6, num=31)  # Geometric edge
    ge32 = Edge(n21, gn6, num=32)  # Geometric edge
    ge34 = Edge(n1, gn7, num=34)  # Geometric edge
    ge33 = Edge(n21, gn7, num=33)  # Geometric edge
    ge35 = Edge(n2, gn7, num=35)  # Geometric edge
    ge36 = Edge(n24, gn7, num=36)  # Geometric edge
    ge38 = Edge(n2, gn8, num=38)  # Geometric edge
    ge37 = Edge(n1, gn8, num=37)  # Geometric edge
    ge39 = Edge(n11, gn8, num=39)  # Geometric edge
    ge40 = Edge(n13, gn8, num=40)  # Geometric edge
    ge41 = Edge(n8, gn8, num=41)  # Geometric edge
    ge43 = Edge(n2, gn9, num=43)  # Geometric edge
    ge42 = Edge(n31, gn9, num=42)  # Geometric edge
    ge44 = Edge(n24, gn9, num=44)  # Geometric edge
    ge45 = Edge(n10002, gn9, num=45)  # Geometric edge
    ge47 = Edge(n2, gn10, num=47)  # Geometric edge
    ge46 = Edge(n24, gn10, num=46)  # Geometric edge
    ge48 = Edge(n11, gn10, num=48)  # Geometric edge
    ge49 = Edge(n37, gn10, num=49)  # Geometric edge
    ge50 = Edge(n10003, gn10, num=50)  # Geometric edge
    ge52 = Edge(n11, gn11, num=52)  # Geometric edge
    ge51 = Edge(n2, gn11, num=51)  # Geometric edge
    ge53 = Edge(n27, gn11, num=53)  # Geometric edge
    ge54 = Edge(n31, gn11, num=54)  # Geometric edge
    ge56 = Edge(n9, gn12, num=56)  # Geometric edge
    ge55 = Edge(n36, gn12, num=55)  # Geometric edge
    ge57 = Edge(n10, gn12, num=57)  # Geometric edge
    ge58 = Edge(n3, gn12, num=58)  # Geometric edge
    ge59 = Edge(n4, gn12, num=59)  # Geometric edge
    ge61 = Edge(n5, gn13, num=61)  # Geometric edge
    ge60 = Edge(n3, gn13, num=60)  # Geometric edge
    ge62 = Edge(n26, gn13, num=62)  # Geometric edge
    ge63 = Edge(n23, gn13, num=63)  # Geometric edge
    ge64 = Edge(n10, gn13, num=64)  # Geometric edge
    ge66 = Edge(n5, gn14, num=66)  # Geometric edge
    ge65 = Edge(n4, gn14, num=65)  # Geometric edge
    ge67 = Edge(n32, gn14, num=67)  # Geometric edge
    ge68 = Edge(n10004, gn14, num=68)  # Geometric edge
    ge70 = Edge(n5, gn15, num=70)  # Geometric edge
    ge69 = Edge(n4, gn15, num=69)  # Geometric edge
    ge71 = Edge(n26, gn15, num=71)  # Geometric edge
    ge72 = Edge(n10005, gn15, num=72)  # Geometric edge
    ge74 = Edge(n6, gn16, num=74)  # Geometric edge
    ge73 = Edge(n15, gn16, num=73)  # Geometric edge
    ge75 = Edge(n7, gn16, num=75)  # Geometric edge
    ge76 = Edge(n20, gn16, num=76)  # Geometric edge
    ge78 = Edge(n9, gn17, num=78)  # Geometric edge
    ge77 = Edge(n6, gn17, num=77)  # Geometric edge
    ge79 = Edge(n36, gn17, num=79)  # Geometric edge
    ge80 = Edge(n15, gn17, num=80)  # Geometric edge
    ge82 = Edge(n7, gn18, num=82)  # Geometric edge
    ge81 = Edge(n6, gn18, num=81)  # Geometric edge
    ge83 = Edge(n8, gn18, num=83)  # Geometric edge
    ge84 = Edge(n10, gn18, num=84)  # Geometric edge
    ge85 = Edge(n9, gn18, num=85)  # Geometric edge
    ge87 = Edge(n6, gn19, num=87)  # Geometric edge
    ge86 = Edge(n34, gn19, num=86)  # Geometric edge
    ge88 = Edge(n15, gn19, num=88)  # Geometric edge
    ge89 = Edge(n10006, gn19, num=89)  # Geometric edge
    ge91 = Edge(n6, gn20, num=91)  # Geometric edge
    ge90 = Edge(n34, gn20, num=90)  # Geometric edge
    ge92 = Edge(n7, gn20, num=92)  # Geometric edge
    ge93 = Edge(n12, gn20, num=93)  # Geometric edge
    ge94 = Edge(n35, gn20, num=94)  # Geometric edge
    ge96 = Edge(n6, gn21, num=96)  # Geometric edge
    ge95 = Edge(n34, gn21, num=95)  # Geometric edge
    ge97 = Edge(n9, gn21, num=97)  # Geometric edge
    ge98 = Edge(n14, gn21, num=98)  # Geometric edge
    ge99 = Edge(n17, gn21, num=99)  # Geometric edge
    ge100 = Edge(n10007, gn21, num=100)  # Geometric edge
    ge102 = Edge(n12, gn22, num=102)  # Geometric edge
    ge101 = Edge(n7, gn22, num=101)  # Geometric edge
    ge103 = Edge(n33, gn22, num=103)  # Geometric edge
    ge104 = Edge(n29, gn22, num=104)  # Geometric edge
    ge105 = Edge(n16, gn22, num=105)  # Geometric edge
    ge106 = Edge(n20, gn22, num=106)  # Geometric edge
    ge108 = Edge(n8, gn23, num=108)  # Geometric edge
    ge107 = Edge(n7, gn23, num=107)  # Geometric edge
    ge109 = Edge(n13, gn23, num=109)  # Geometric edge
    ge110 = Edge(n19, gn23, num=110)  # Geometric edge
    ge111 = Edge(n12, gn23, num=111)  # Geometric edge
    ge113 = Edge(n10, gn24, num=113)  # Geometric edge
    ge112 = Edge(n8, gn24, num=112)  # Geometric edge
    ge114 = Edge(n23, gn24, num=114)  # Geometric edge
    ge115 = Edge(n22, gn24, num=115)  # Geometric edge
    ge116 = Edge(n13, gn24, num=116)  # Geometric edge
    ge118 = Edge(n9, gn25, num=118)  # Geometric edge
    ge117 = Edge(n36, gn25, num=117)  # Geometric edge
    ge119 = Edge(n14, gn25, num=119)  # Geometric edge
    ge120 = Edge(n38, gn25, num=120)  # Geometric edge
    ge122 = Edge(n14, gn26, num=122)  # Geometric edge
    ge121 = Edge(n18, gn26, num=121)  # Geometric edge
    ge123 = Edge(n9, gn26, num=123)  # Geometric edge
    ge124 = Edge(n10, gn26, num=124)  # Geometric edge
    ge125 = Edge(n23, gn26, num=125)  # Geometric edge
    ge127 = Edge(n27, gn27, num=127)  # Geometric edge
    ge126 = Edge(n11, gn27, num=126)  # Geometric edge
    ge128 = Edge(n28, gn27, num=128)  # Geometric edge
    ge129 = Edge(n37, gn27, num=129)  # Geometric edge
    ge131 = Edge(n13, gn28, num=131)  # Geometric edge
    ge130 = Edge(n11, gn28, num=130)  # Geometric edge
    ge132 = Edge(n19, gn28, num=132)  # Geometric edge
    ge133 = Edge(n39, gn28, num=133)  # Geometric edge
    ge134 = Edge(n37, gn28, num=134)  # Geometric edge
    ge136 = Edge(n11, gn29, num=136)  # Geometric edge
    ge135 = Edge(n27, gn29, num=135)  # Geometric edge
    ge137 = Edge(n13, gn29, num=137)  # Geometric edge
    ge138 = Edge(n22, gn29, num=138)  # Geometric edge
    ge140 = Edge(n19, gn30, num=140)  # Geometric edge
    ge139 = Edge(n12, gn30, num=139)  # Geometric edge
    ge141 = Edge(n39, gn30, num=141)  # Geometric edge
    ge142 = Edge(n33, gn30, num=142)  # Geometric edge
    ge144 = Edge(n12, gn31, num=144)  # Geometric edge
    ge143 = Edge(n35, gn31, num=143)  # Geometric edge
    ge145 = Edge(n19, gn31, num=145)  # Geometric edge
    ge146 = Edge(n10008, gn31, num=146)  # Geometric edge
    ge148 = Edge(n14, gn32, num=148)  # Geometric edge
    ge147 = Edge(n38, gn32, num=147)  # Geometric edge
    ge149 = Edge(n17, gn32, num=149)  # Geometric edge
    ge150 = Edge(n10009, gn32, num=150)  # Geometric edge
    ge152 = Edge(n14, gn33, num=152)  # Geometric edge
    ge151 = Edge(n38, gn33, num=151)  # Geometric edge
    ge153 = Edge(n18, gn33, num=153)  # Geometric edge
    ge154 = Edge(n10010, gn33, num=154)  # Geometric edge
    edges = [e0, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16, e17, e18, e19, e20, e21, e22, e23, e24, e25, e26, e27, e28, e29, e30, e31, e32, e33, e34, e35, e36, e37, e38, e39, e40, e41, e42, e43, e44, e45, e46, e47, e48, e49, e50, e51, e52, e53, e54, e55, e10000, e10001, e10002, e10003, e10004, e10005, e10006, e10007, e10008, e10009, e10010, e10011, e10012, e10013, e10014, e10015, e10016, e10017, e10018, e10019, e10020, e10021, e10022, e10023, e10024, e10025, e10026, e10027, e10028, e10029, e10030, e10031, e10032, e10033, e10034, e10035, e10036, e10037, e10038]

    geometric_edges = [ge1, ge0, ge2, ge3, ge5, ge4, ge6, ge7, ge8, ge10, ge9, ge11, ge12, ge13, ge15, ge14, ge16, ge17, ge19, ge18, ge20, ge21, ge22, ge24, ge23, ge25, ge26, ge27, ge29, ge28, ge30, ge31, ge32, ge34, ge33, ge35, ge36, ge38, ge37, ge39, ge40, ge41, ge43, ge42, ge44, ge45, ge47, ge46, ge48, ge49, ge50, ge52, ge51, ge53, ge54, ge56, ge55, ge57, ge58, ge59, ge61, ge60, ge62, ge63, ge64, ge66, ge65, ge67, ge68, ge70, ge69, ge71, ge72, ge74, ge73, ge75, ge76, ge78, ge77, ge79, ge80, ge82, ge81, ge83, ge84, ge85, ge87, ge86, ge88, ge89, ge91, ge90, ge92, ge93, ge94, ge96, ge95, ge97, ge98, ge99, ge100, ge102, ge101, ge103, ge104, ge105, ge106, ge108, ge107, ge109, ge110, ge111, ge113, ge112, ge114, ge115, ge116, ge118, ge117, ge119, ge120, ge122, ge121, ge123, ge124, ge125, ge127, ge126, ge128, ge129, ge131, ge130, ge132, ge133, ge134, ge136, ge135, ge137, ge138, ge140, ge139, ge141, ge142, ge144, ge143, ge145, ge146, ge148, ge147, ge149, ge150, ge152, ge151, ge153, ge154]

    e20000 = Edge(n20000, n10011, num=20000)
    e20001 = Edge(n10011, n10006, num=20001)
    e20002 = Edge(n10006, n20001, num=20002)
    e20003 = Edge(n20010, n10000, num=20003)
    e20004 = Edge(n10000, n20003, num=20004)
    e20005 = Edge(n20003, n10001, num=20005)
    e20006 = Edge(n10001, n10002, num=20006)
    e20007 = Edge(n10002, n20002, num=20007)
    e20008 = Edge(n20002, n10003, num=20008)
    e20009 = Edge(n10003, n20000, num=20009)
    e20010 = Edge(n20004, n10008, num=20010)
    e20011 = Edge(n10008, n10007, num=20011)
    e20012 = Edge(n10007, n20005, num=20012)
    e20013 = Edge(n20005, n10009, num=20013)
    e20014 = Edge(n10009, n10010, num=20014)
    e20015 = Edge(n10010, n10005, num=20015)
    e20016 = Edge(n10005, n20007, num=20016)
    e20017 = Edge(n20007, n20008, num=20017)
    e20018 = Edge(n27, n20006, num=20018)
    e20019 = Edge(n20006, n10013, num=20019)
    e20020 = Edge(n10013, n10012, num=20020)
    e20021 = Edge(n10012, n20004, num=20021)
    e20022 = Edge(n20000, n20009, num=20022)
    e20023 = Edge(n20001, n20010, num=20023)
    e20024 = Edge(n20002, n20006, num=20024)
    e20025 = Edge(n20003, n10004, num=20025)
    e20026 = Edge(n20008, n27, num=20026)
    e20027 = Edge(n20008, n26, num=20027)
    e20028 = Edge(n32, n20008, num=20028)
    e20029 = Edge(n10004, n20007, num=20029)
    e20030 = Edge(n20009, n20004, num=20030)
    e20031 = Edge(n20009, n33, num=20031)
    e20032 = Edge(n20009, n39, num=20032)
    e20033 = Edge(n20001, n20005, num=20033)
    e20034 = Edge(n20010, n36, num=20034)
    e20035 = Edge(n20010, n15, num=20035)

    edges.extend([e20000, e20001, e20002, e20003, e20004, e20005, e20006, e20007, e20008, e20009, e20010, e20011, e20012, e20013, e20014, e20015, e20016, e20017, e20018, e20019, e20020, e20021, e20022, e20023, e20024, e20025, e20026, e20027, e20028, e20029, e20030, e20031, e20032, e20033, e20034, e20035])

    f0 = Face([[-e2, ge1, -ge0], [e0, ge2, -ge1], [e6, ge3, -ge2], [e10000, ge0, -ge3]], num=0)
    f1 = Face([[-e2, ge5, -ge4], [e1, ge6, -ge5], [e10, ge7, -ge6], [-e10002, ge8, -ge7], [-e10001, ge4, -ge8]], num=1)
    f2 = Face([[e0, ge10, -ge9], [e5, ge11, -ge10], [e23, ge12, -ge11], [-e12, ge13, -ge12], [-e1, ge9, -ge13]], num=2)
    f3 = Face([[-e3, ge15, -ge14], [e2, ge16, -ge15], [-e10004, ge17, -ge16], [-e10003, ge14, -ge17]], num=3)
    f4 = Face([[e0, ge19, -ge18], [e4, ge20, -ge19], [e9, ge21, -ge20], [-e52, ge22, -ge21], [-e3, ge18, -ge22]], num=4)
    f5 = Face([[-e3, ge24, -ge23], [e1, ge25, -ge24], [e11, ge26, -ge25], [e15, ge27, -ge26], [e10005, ge23, -ge27]], num=5)
    f6 = Face([[e5, ge29, -ge28], [-e20, ge30, -ge29], [e22, ge31, -ge30], [e44, ge32, -ge31], [-e6, ge28, -ge32]], num=6)
    f7 = Face([[-e6, ge34, -ge33], [e4, ge35, -ge34], [e8, ge36, -ge35], [e10006, ge33, -ge36]], num=7)
    f8 = Face([[e4, ge38, -ge37], [e7, ge39, -ge38], [e29, ge40, -ge39], [-e24, ge41, -ge40], [-e5, ge37, -ge41]], num=8)
    f9 = Face([[-e9, ge43, -ge42], [e8, ge44, -ge43], [-e10008, ge45, -ge44], [-e10007, ge42, -ge45]], num=9)
    f10 = Face([[-e8, ge47, -ge46], [e7, ge48, -ge47], [e31, ge49, -ge48], [-e10010, ge50, -ge49], [-e10009, ge46, -ge50]], num=10)
    f11 = Face([[e7, ge52, -ge51], [e30, ge53, -ge52], [e48, ge54, -ge53], [-e9, ge51, -ge54]], num=11)
    f12 = Face([[-e27, ge56, -ge55], [e25, ge57, -ge56], [-e12, ge58, -ge57], [e10, ge59, -ge58], [e10011, ge55, -ge59]], num=12)
    f13 = Face([[e10, e13, -e11]], num=13)
    f14 = Face([[e11, ge61, -ge60], [e14, ge62, -ge61], [-e46, ge63, -ge62], [-e28, ge64, -ge63], [-e12, ge60, -ge64]], num=14)
    f15 = Face([[e13, ge66, -ge65], [e15, ge67, -ge66], [-e10013, ge68, -ge67], [-e10012, ge65, -ge68]], num=15)
    f16 = Face([[e13, ge70, -ge69], [e14, ge71, -ge70], [-e10015, ge72, -ge71], [-e10014, ge69, -ge72]], num=16)
    f17 = Face([[e14, e47, -e15]], num=17)
    f18 = Face([[-e18, ge74, -ge73], [e16, ge75, -ge74], [e22, ge76, -ge75], [e10016, ge73, -ge76]], num=18)
    f19 = Face([[e17, ge78, -ge77], [e27, ge79, -ge78], [-e40, ge80, -ge79], [-e18, ge77, -ge80]], num=19)
    f20 = Face([[e16, ge82, -ge81], [e20, ge83, -ge82], [e23, ge84, -ge83], [-e25, ge85, -ge84], [-e17, ge81, -ge85]], num=20)
    f21 = Face([[-e19, ge87, -ge86], [e18, ge88, -ge87], [-e10018, ge89, -ge88], [-e10017, ge86, -ge89]], num=21)
    f22 = Face([[-e19, ge91, -ge90], [e16, ge92, -ge91], [e21, ge93, -ge92], [e34, ge94, -ge93], [e10019, ge90, -ge94]], num=22)
    f23 = Face([[-e19, ge96, -ge95], [e17, ge97, -ge96], [e26, ge98, -ge97], [e37, ge99, -ge98], [-e10021, ge100, -ge99], [-e10020, ge95, -ge100]], num=23)
    f24 = Face([[e21, ge102, -ge101], [e33, ge103, -ge102], [-e51, ge104, -ge103], [-e42, ge105, -ge104], [e41, ge106, -ge105], [-e22, ge101, -ge106]], num=24)
    f25 = Face([[e20, ge108, -ge107], [e24, ge109, -ge108], [e35, ge110, -ge109], [-e32, ge111, -ge110], [-e21, ge107, -ge111]], num=25)
    f26 = Face([[e23, ge113, -ge112], [e28, ge114, -ge113], [-e45, ge115, -ge114], [-e36, ge116, -ge115], [-e24, ge112, -ge116]], num=26)
    f27 = Face([[-e27, ge118, -ge117], [e26, ge119, -ge118], [e39, ge120, -ge119], [e10022, ge117, -ge120]], num=27)
    f28 = Face([[-e38, ge122, -ge121], [-e26, ge123, -ge122], [e25, ge124, -ge123], [e28, ge125, -ge124], [e10023, ge121, -ge125]], num=28)
    f29 = Face([[e30, ge127, -ge126], [e49, ge128, -ge127], [e50, ge129, -ge128], [-e31, ge126, -ge129]], num=29)
    f30 = Face([[e29, ge131, -ge130], [e35, ge132, -ge131], [e43, ge133, -ge132], [-e55, ge134, -ge133], [-e31, ge130, -ge134]], num=30)
    f31 = Face([[-e30, ge136, -ge135], [e29, ge137, -ge136], [e36, ge138, -ge137], [e10024, ge135, -ge138]], num=31)
    f32 = Face([[e33, e54, -e34]], num=32)
    f33 = Face([[e32, ge140, -ge139], [e43, ge141, -ge140], [-e53, ge142, -ge141], [-e33, ge139, -ge142]], num=33)
    f34 = Face([[-e34, ge144, -ge143], [e32, ge145, -ge144], [-e10026, ge146, -ge145], [-e10025, ge143, -ge146]], num=34)
    f35 = Face([[-e36, e35, e10027]], num=35)
    f36 = Face([[-e39, ge148, -ge147], [e37, ge149, -ge148], [-e10029, ge150, -ge149], [-e10028, ge147, -ge150]], num=36)
    f37 = Face([[-e39, ge152, -ge151], [e38, ge153, -ge152], [-e10031, ge154, -ge153], [-e10030, ge151, -ge154]], num=37)
    f38 = Face([[-e38, e37, e10032]], num=38)
    f39 = Face([[e42, -e10034, -e10033]], num=39)
    f40 = Face([[e43, -e10036, -e10035]], num=40)
    f41 = Face([[e50, -e10038, -e10037]], num=41)
    faces = [f0, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17, f18, f19, f20, f21, f22, f23, f24, f25, f26, f27, f28, f29, f30, f31, f32, f33, f34, f35, f36, f37, f38, f39, f40, f41]


    f20000 = Face([[e20021, e20010, e10026, e10035]], num=20000)
    f20001 = Face([[e20011, e10021, e10032, -e10023, -e45, -e10027, -e10026]], num=20001)
    f20002 = Face([[e20012, e20013, e10029, -e10021]], num=20002)
    f20003 = Face([[e20014, e10031, -e10032, -e10029]], num=20003)
    f20004 = Face([[e20015, e10015, -e46, e10023, -e10031]], num=20004)
    f20005 = Face([[e20026, -e10024, e45, e46, -e20027]], num=20005)
    f20006 = Face([[e20020, -e10035, e10027, e10024, e49, e10037]], num=20006)
    f20007 = Face([[e20018, e20019, -e10037, -e49]], num=20007)
    f20008 = Face([[e20024, -e20018, e48, e10007, e20007]], num=20008)
    f20009 = Face([[e20006, -e10007, -e52, e10003]], num=20009)
    f20010 = Face([[e20017, e20027, -e10015, e20016]], num=20010)
    f20011 = Face([[e20026, e48, -e52, -e10005, e20028]], num=20011)
    f20012 = Face([[e20028, -e20017, -e20029, e10013]], num=20012)
    f20013 = Face([[e10012, e20029, -e20016, -e10014]], num=20013)
    f20014 = Face([[e20005, -e10003, -e10005, -e10013, -e20025]], num=20014)
    # f20015 = Face([e20029, -e20016, -e10014, e10012], num=20015)
    f20016 = Face([e20004, e20025, -e10012, -e10002], num=20016)
    f20017 = Face([e20008, e10010, -e10038, -e20019, -e20024], num=20017)
    f20018 = Face([-e10011, e10014, -e20015, -e10030, e10022], num=20018)
    f20019 = Face([e10030, -e20014, -e10028], num=20019)
    f20020 = Face([e55, -e10036, -e20020, e10038], num=20020)
    f20021 = Face([e10020, -e20011, -e10025, e10019], num=20021)
    f20022 = Face([e20001, e10018, -e10016, -e41, e10033], num=20022)
    f20023 = Face([e20001, -e10017, -e10019, -e54, -e51, -e10034], num=20023)
    f20024 = Face([e20009, e20000, -e10033, e41, e44, -e10006, e10009], num=20024)
    f20025 = Face([e10009, -e20008, -e20007, e10008], num=20025)
    f20026 = Face([e20006, e10008, e10006, e10000, -e10004], num=20026)
    f20027 = Face([e20004, e20005, e10004, e10001], num=20027)
    f20028 = Face([e20034, -e40, -e20035], num=20028)
    f20029 = Face([e20031, e53, -e20032], num=20029)
    f20030 = Face([e54, e10025, -e20010, -e20030, e20031], num=20030)
    f20031 = Face([e20030, -e20021, e10036, -e20032], num=20031)
    f20032 = Face([e20000, e10034, e51, -e20031, -e20022], num=20032)
    f20033 = Face([e20009, e20022, e20032, -e55, -e10010], num=20033)
    f20034 = Face([e10002, e10011, -e20034, e20003], num=20034)
    f20035 = Face([e20003, -e10001, -e10000, -e44, e10016, -e20035], num=20035)
    f20036 = Face([e20023, e20035, -e10018, e20002], num=20036)
    f20037 = Face([e20023, e20034, -e10022, e10028, -e20013, -e20033], num=20037)
    f20038 = Face([e20002, e20033, -e20012, -e10020, e10017], num=20038)
    f20039 = Face([e20028, e20027, e47], num=20039)

    faces_new = [f20000, f20001, f20002, f20003, f20004, f20005, f20006, f20007, f20008, f20009, f20010, f20011, f20012, f20013, f20014, f20016, f20017, f20018, f20019, f20020, f20021, f20022, f20023, f20024, f20025, f20026, f20027, f20028, f20029, f20030, f20031, f20032, f20033, f20034, f20035, f20036, f20037, f20038, f20039]
    for f in faces_new:
        f.color = tc.TUMRose()

    faces.extend(faces_new)

    v0 = Volume([-f0, f1, f2, -f6, -f12, f18, -f19, -f20, f20034, -f20035, f20028], num=0)
    v1 = Volume([f0, f3, -f4, f7, -f9, f20009, -f20026], num=1)
    v2 = Volume([-f1, -f3, f5, f13, -f15, f20016, f20014, -f20027], num=2)
    v3 = Volume([-f2, f4, -f5, -f8, f11, f14, -f17, f26, f31, f20039, f20005, -f20011], num=3)
    v4 = Volume([f6, -f7, f8, -f10, f24, f25, -f30, f33, f39, -f20024, f20033, f20032, f20029], num=4)
    v5 = Volume([f9, f10, -f11, f29, -f41, f20025, f20008, f20017, f20007], num=5)
    v6 = Volume([f12, -f13, -f14, f16, -f27, -f28, -f37, f20018, f20004], num=6)
    v7 = Volume([f15, -f16, f17, -f20039, f20010, f20013, f20012], num=7)
    v8 = Volume([-f18, -f21, f22, -f24, f32, -f39, -f20022, f20023], num=8)
    v9 = Volume([f19, f21, -f23, f27, f36, -f20036, f20037, f20038, f20002, -f20028], num=9)
    v10 = Volume([f20, -f22, f23, -f25, -f26, f28, -f34, f35, -f38, f20001, f20021], num=10)
    v11 = Volume([-f29, f30, -f31, -f35, -f40, f41, f20020, f20006], num=11)
    v12 = Volume([-f32, -f33, f34, f40, f20030, f20000, f20031, -f20029], num=12)
    v13 = Volume([-f36, f37, f38, f20003, f20019], num=13)





    # v14 = Volume([f39], num=14)
    # v15 = Volume([f41], num=15)
    # volumes = [v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15]

    volumes = [v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13]


    return (nodes, edges, faces, volumes)


if __name__ == "__main__":

    (nodes, edges, faces, volumes) = get_k_cells()

    faces_for_volumes = []

    # for e in geometric_edges:
        # e.color = tc.TUMGreen()

    pc = PrimalComplex3D(nodes, edges, faces, volumes)

    for n in pc.borderNodes:
        n.color = tc.TUMGreen()

    plotly_nodes = NodePlotly(nodes)
    plotly_edges = EdgePlotly(edges)
    plotly_faces = FacePlotly(faces)
    # plotly_faces2 = FacePlotly(faces_for_volumes)
    plotly_volumes = VolumePlotly(volumes)

    plotly_fig_nodes_edges = plotly_nodes.plot_nodes_plotly(show_label=False, show_axes=False, marker_size=20)
    plotly_edges.plot_edges_plotly(plotly_fig_nodes_edges, show_label=False, cone_size=0.25, show_barycenter=False)
    plotly_fig_nodes_edges.show()

    # plotly_fig_edges_faces = plotly_edges.plot_edges_plotly(show_label=False, cone_size=0.05, show_barycenter=False, show_axes=False)
    # plotly_faces.plot_faces_plotly(plotly_fig_edges_faces, show_label=False, cone_size=0.05, show_barycenter=False)
    # plotly_fig_edges_faces.update_layout(
    #     scene={
    #         "camera": {
    #             "up": {"x": -0.234, "y": 0.908, "z": -0.344},
    #             "center": {"x": 0, "y": 0, "z": 0},
    #             "eye": {"x": 1.075, "y": 0.899, "z": 1.648},
    #         },
    #     }
    # )
    # plotly_fig_edges_faces.show()

    # for f in faces:
    #     if f in faces_for_volumes or -f in faces_for_volumes:
    #         f.color = tc.TUMBlue()
    #     else:
    #         f.color = tc.TUMGreen()

    # f39.color = tc.TUMBlack()

    # plotly_fig_faces = plotly_faces.plot_faces_plotly(show_normal_vec=False)
    # plotly_nodes.plot_nodes_plotly(plotly_fig_faces, show_label=True)
    # plotly_fig_faces.show()

    # plotly_fig_faces2 = plotly_faces2.plot_faces_plotly()
    # plotly_fig_faces2.show()

    # plotly_fig_volumes = plotly_volumes.plot_volumes_plotly()
    # plotly_fig_volumes.show()

    # pc = PrimalComplex3D(nodes, edges, faces, volumes)
    # dc = DualComplex3D(pc)




    # for n in nodes:
    #     n.color = tc.TUMBlue()
    # for e in pc.edges:
    #     e.color = tc.TUMBlue()
    # for e in dc.edges:
    #     e.color = tc.TUMBlack()

    # for n in dc.innerNodes:
    #     n.color = tc.TUMOrange()
    # for n in dc.additionalBorderNodes:
    #     n.color = tc.TUMBlack()

    # plotly_nodes_dual = NodePlotly(dc.nodes)
    # plotly_edges_dual = EdgePlotly(dc.edges)
    # plotly_faces_dual = FacePlotly(dc.faces)

    # problem_edge = [e for e in dc.innerEdges if e.num == 39][0]
    # problem_face = problem_edge.dualCell3D
    # _log.critical("edge: %s", problem_edge)
    # _log.critical("face: %s", problem_face)

    # problem_edge.color = tc.TUMRose()
    # plotly_problem_face = FacePlotly([problem_face])




    # plotly_fig_edges_dual = plotly_edges_dual.plot_edges_plotly(show_label=False, show_direction=False, show_barycenter=False)
    # plotly_problem_face.plot_faces_plotly(plotly_fig_edges_dual, show_label=False, cone_size=0.1, show_barycenter=False)
    # plotly_edges.plot_edges_plotly(plotly_fig_edges_dual, show_label=False, show_direction=False, show_barycenter=False)
    # plotly_nodes_dual.plot_nodes_plotly(plotly_fig_edges_dual, show_label=False)
    # plotly_nodes.plot_nodes_plotly(plotly_fig_edges_dual, show_label=False)
    # plotly_fig_edges_dual.show()

    # plotly_fig_faces_dual = plotly_faces_dual.plot_faces_plotly(show_normal_vec=False, show_label=False)
    # plotly_fig_faces_dual.show()

    # dc.checkAllIncidenceMatrices()

    # print(len(pc.borderNodes), len(dc.borderVolumes))

    # Launch interactive Dash visualization
    # To run the Dash app, execute: python dash_node_visualizer.py

    # for f in faces:
    #     _log.info("2D dual of face %s: %s (%s) - %s", f.num, f.dualCell2D, f.dualCell2D.coordinates, len(f.geometricNodes))
