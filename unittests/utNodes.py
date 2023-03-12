# -*- coding: utf-8 -*-
#==============================================================================
# UNITTEST OF NODE CLASSES
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue May 22 16:00:47 2018
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
import unittest
import numpy as np


#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------


#    kCells
#--------------------------------------------------------------------
from kCells import Node, Edge, Face, Volume
from kCells import DualNode0D, DualNode1D, DualNode2D, DualNode3D


#    Tools
#--------------------------------------------------------------------
from boundingBox.boundingBox import BoundingBox



#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class TestNodeMethods(unittest.TestCase):


#-------------------------------------------------------------------------
#    Node
#-------------------------------------------------------------------------   
    
    def testNode(self):
        
        # Create a Node
        n0 = Node(1,2,3)
        
        
        # Check the coordinates
        self.assertIsInstance(n0.coordinates,np.ndarray)
        self.assertEqual(len(n0.coordinates),3)
        self.assertTrue(np.allclose(n0.coordinates,np.array([1,2,3])))
        
        
        
        # Create another Node
        n1 = Node(4.9,5,6)
        
        # Create an Edge with the two nodes
        e0 = Edge(n0,n1)
    
        # Check, that the edges is registered correctly
        self.assertIs(n0.edges[0],e0)
        self.assertIs(n1.edges[0],e0)
        
        # CHeck that the simpleEdge is also registered correctly
        self.assertIs(n0.simpleEdges[0],e0.simpleEdges[0])
        self.assertIs(n1.simpleEdges[0],e0.simpleEdges[0])
        
        
        # Create another Node
        n2 = Node(0,0,0)
        
        # Create an Edge with a geometric Node
        e1 = Edge(n0,n1,geometricNodes = n2)
        
        # Check that the node has now become geometric
        self.assertTrue(n2.isGeometrical)
        self.assertIs(e1.geometricNodes[0],n2)

        
        # Create a BoundingBox
        bb = BoundingBox([0,5],[0,6],[0,7])
        
        # Calculate and check distance to the BoundingBox
        (dist,side) = n0.distToBoundingBox(bb)
        self.assertEqual(dist,1)
        
        # Move to a given side of the BoundingBox
        n0.moveToBoundingBoxSide(side)
        self.assertEqual(n0.xCoordinate,0)
        self.assertIs(n0.onBoundingBoxSides[0],side)
        
        
        # Move node to closes BoundingBoxSide
        n1.moveToBoundingBox(bb)
        self.assertEqual(n1.xCoordinate,5)
        
  
#-------------------------------------------------------------------------
#    Dual Node 0D
#-------------------------------------------------------------------------   
    def testDualNode0D(self):
        # Create a Node
        n0 = Node(1,1,1)
        
        # Create a 0D dual to the node
        dn0 = DualNode0D(n0)
        
        # Check that the coordinates coincide
        self.assertTrue(np.allclose(n0.coordinates,dn0.coordinates))
        
        
#-------------------------------------------------------------------------
#    Dual Node 1D
#-------------------------------------------------------------------------         
    def testDualNode1D(self):
        
        # Create some Nodes
        n0 = Node(0,0,0,category='inner')
        n1 = Node(0,1,0,category='inner')
        n2 = Node(1,1,0,category='border')
        n3 = Node(1,0,1,category='border')
        n4 = Node(1,0,0,category='border')
        n5 = Node(2,0,0,category='inner')
        n6 = Node(2,1,0,category='additionalBorder')
        
        
        #Create a standard edge
        e0 = Edge(n0,n1)
        
        # Create an edge with a geometric node
        e1 = Edge(n2,n3,geometricNodes=n4)
        
        # Create an edge with one additionalBorderNode
        e2 = Edge(n5,n6)
        
        
        # Create DualNodes
        dn0 = DualNode1D(e0)
        dn1 = DualNode1D(e1)
        dn2 = DualNode1D(e2)
        
        # Check that the dual nodes have been created at the correct place
        self.assertTrue(np.allclose(dn0.coordinates,e0.barycenter[0]))
        self.assertTrue(np.allclose(dn1.coordinates,n4.coordinates))
        self.assertTrue(np.allclose(dn2.coordinates,n6.coordinates))
        
        # Check that the 0D-duals have also been set correctly
        self.assertEqual(n4.dualCell0D,dn1)
        self.assertEqual(n6.dualCell0D,dn2)
        
        
        
#-------------------------------------------------------------------------
#    Dual Node 2D
#-------------------------------------------------------------------------       
        
    def testDualNode2D(self):
        
        # Create some nodes
        n0 = Node(0,0,0)
        n1 = Node(1,0,0)
        n2 = Node(0,1,0)
        n3 = Node(0,0,1)
        n4 = Node(1,0,1)
        n5 = Node(1,1,2)
        n6 = Node(0,1,1)
        n7 = Node(0,0,2)
        n8 = Node(1,0,2)
        n9 = Node(0,1,2)
        n10 = Node(0,0,3)
        n11 = Node(0,0,4)
        n12 = Node(1,0,4)
        n13 = Node(0,1,4)
        
        # Create some edges
        e0 = Edge(n0,n1)
        e1 = Edge(n1,n2)
        e2 = Edge(n2,n0)
        e3 = Edge(n3,n4)
        e4 = Edge(n4,n5)
        e5 = Edge(n5,n6)
        e6 = Edge(n6,n3)
        e7 = Edge(n4,n6)
        e8 = Edge(n7,n8)
        e9 = Edge(n8,n9)
        e10 = Edge(n9,n7)
        e11 = Edge(n8,n10)
        e12 = Edge(n10,n7)
        e13 = Edge(n10,n9)
        e14 = Edge(n11,n12,category='additionalBorder')
        e15 = Edge(n12,n13,category='inner')
        e16 = Edge(n13,n11,category='inner')
        
        # Create a standard face with one simple face
        f0 = Face([e0,e1,e2])
        
        # Create a face with two simple face
        f1 = Face([[e3,e7,e6],[e5,-e7,e4]])
        
        # Create a face with three simple faces
        f2 = Face([[e8,e9,e10],[-e8,-e12,-e11],[-e10,-e13,e12]])
        
        # Create a face that contains an additonal border edge
        f3 = Face([e14,e15,e16])
        
        # Create DualNodes
        dn0 = DualNode2D(f0)
        dn1 = DualNode2D(f1)
        dn2 = DualNode2D(f2)
        dn3 = DualNode2D(f3)
        
        # Check that the dual nodes have been created at the correct place
        self.assertTrue(np.allclose(dn0.coordinates,f0.barycenter[0]))
        self.assertTrue(np.allclose(dn1.coordinates,e7.barycenter[0]))
        self.assertTrue(np.allclose(dn2.coordinates,n7.coordinates))
        self.assertTrue(np.allclose(dn3.coordinates,e14.barycenter[0]))
        
        # Check that the 0D-duals have also been set correctly
        self.assertEqual(n7.dualCell0D,dn2)
        
        # Check that the 1D-duals have also been set correctly
        self.assertEqual(e7.dualCell1D,dn1)
        self.assertEqual(e14.dualCell1D,dn3)
        
 
#-------------------------------------------------------------------------
#    Dual Node 3D
#-------------------------------------------------------------------------     

    def testDualNode3D(self):
#    Inner volume
#--------------------------------------------------------------------
        n100 = Node(0,0,0)
        n101 = Node(1,0,0)
        n102 = Node(0,1,0)
        n103 = Node(0,0,1)
        
        e100 = Edge(n100,n101,num=0)
        e101 = Edge(n100,n102,num=1)
        e102 = Edge(n100,n103,num=2)
        e103 = Edge(n101,n102,num=3)
        e104 = Edge(n101,n103,num=4)
        e105 = Edge(n102,n103,num=5)
        
        
        f100 = Face([e100,e103,-e101])
        f101 = Face([e101,e105,-e102])
        f102 = Face([e100,e104,-e102])
        f103 = Face([e103,e105,-e104])
        
        faces100 = [f100,f101,f102,f103]
        for f in faces100:
            f.category1 = 'inner'
        
        v100 = Volume([-f100,-f101,f102,f103],num=100)
        v100.category1 = 'inner'
        
        
        dn100 = DualNode3D(v100)
        
        self.assertTrue(np.allclose(v100.barycenter[0],dn100.coordinates))
        
        

#    Border volume with one additional border face
#--------------------------------------------------------------------        
        
        
        n200 = Node(0,0,0,num=0)
        n201 = Node(1,0,0,num=1)
        n202 = Node(0,1,0,num=2)
        n203 = Node(0,0,1,num=3)
        
        e200 = Edge(n200,n201,num=0)
        e201 = Edge(n200,n202,num=1)
        e202 = Edge(n200,n203,num=2)
        e203 = Edge(n201,n202,num=3)
        e204 = Edge(n201,n203,num=4)
        e205 = Edge(n202,n203,num=5)
        
        
        f200 = Face([e200,e203,-e201],num=0)
        f201 = Face([e201,e205,-e202],num=1)
        f202 = Face([e200,e204,-e202],num=2)
        f203 = Face([e203,e205,-e204],num=3)
        
        
        f202.category1 = 'additionalBorder'
        for f in [f200,f201,f203]:
            f.category1 = 'inner'
        
        v200 = Volume([-f200,-f201,f202,f203],num=200)
        v200.category1 = 'border'
        
        
        dn200 = DualNode3D(v200)
        
        self.assertTrue(np.allclose(f202.barycenter[0],dn200.coordinates))
        


        
#    Border Volume with two additional border faces
#--------------------------------------------------------------------        
        
        
        n300 = Node(0,0,0,num=0)
        n301 = Node(1,0,0,num=1)
        n302 = Node(0,1,0,num=2)
        n303 = Node(0,0,1,num=3)
        
        e300 = Edge(n300,n301,num=0)
        e301 = Edge(n300,n302,num=1)
        e302 = Edge(n300,n303,num=2)
        e303 = Edge(n301,n302,num=3)
        e304 = Edge(n301,n303,num=4)
        e305 = Edge(n302,n303,num=5)
        
        
        f301 = Face([e301,e305,-e302],num=1)
        f302 = Face([[e300,e304,-e302],[e301,-e303,-e300]],num=300)
        f303 = Face([e303,e305,-e304],num=3)
        
        
        f302.category1 = 'additionalBorder'
        for f in [f301,f303]:
            f.category1 = 'inner'
        
        v300 = Volume([-f301,f302,f303],num=1)
        v300.category1 = 'border'
        
        
        dn300 = DualNode3D(v300)
        
        self.assertTrue(np.allclose(e300.barycenter,dn300.coordinates))
        
        
#    Border Volume with three additional border faces
#--------------------------------------------------------------------        
        
        
        n400 = Node(0,0,0,num=0)
        n401 = Node(1,0,0,num=1)
        n402 = Node(0,1,0,num=2)
        n403 = Node(0,0,1,num=3)
        
        e400 = Edge(n400,n401,num=0)
        e401 = Edge(n400,n402,num=1)
        e402 = Edge(n400,n403,num=2)
        e403 = Edge(n401,n402,num=3)
        e404 = Edge(n401,n403,num=4)
        e405 = Edge(n402,n403,num=5)
        
        
        f402 = Face([[e400,e404,-e402],[e401,-e403,-e400],[e402,-e405,-e401]],num=2)
        f403 = Face([e403,e405,-e404],num=3)
        
        
        f402.category1 = 'additionalBorder'
        f403.category1 = 'inner'
        v400 = Volume([f402,f403],num=400)
        v400.category1 = 'border'
        dn400 = DualNode3D(v400)
        
        self.assertTrue(np.allclose(n400.coordinates,dn400.coordinates))
        
        
#    Border Volume with three additional border faces and more than one 
#    additional border node
#--------------------------------------------------------------------  

        n500 = Node(0,0,0,num=0)
        n501 = Node(1,0,0,num=1)
        n502 = Node(1,1,0,num=2)
        n503 = Node(0,1,0,num=3)
        n504 = Node(0,0,1,num=4)
        n505 = Node(1,0,1,num=5)
        n506 = Node(1,1,1,num=6)
        n507 = Node(0,1,1,num=7)
        
        e500 = Edge(n500,n501,num=0)
        e501 = Edge(n505,n502,num=1,geometricNodes=n501)
        e502 = Edge(n502,n507,num=2,geometricNodes=n503)
        e503 = Edge(n503,n500,num=3)
        e504 = Edge(n504,n505,num=4)
        e505 = Edge(n505,n506,num=5)
        e506 = Edge(n506,n507,num=6)
        e507 = Edge(n507,n504,num=7)
        e508 = Edge(n500,n504,num=8)
        e509 = Edge(n502,n506,num=9)
        
        
        f500 = Face([[e500,e501,e502,e503],[-e500,e508,e504,e501],[-e503,e502,e507,-e508]],num=0,category='additionalBorder')
        f501 = Face([e504,e505,e506,e507],num=1)
        f502 = Face([e501,e509,-e505],num=2)
        f503 = Face([-e502,e509,e506,],num=3)
        
        v500 = Volume([-f500,f501,f502,-f503],num=500)
        v500.category1 = 'border'
        
        dn500 = DualNode3D(v500)
        
        self.assertTrue(np.allclose(n500.coordinates,dn500.coordinates))
  
        
        
        

if __name__ == '__main__':
    from tools.myLogging import MyLogging
    
    with MyLogging('unittestNodes'):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestNodeMethods)
        unittest.TextTestRunner(verbosity=2).run(suite)