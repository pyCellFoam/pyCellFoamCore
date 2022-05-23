# -*- coding: utf-8 -*-
#==============================================================================
# TITLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Feb  9 19:42:47 2022

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
    os.chdir('.')


#-------------------------------------------------------------------------
#    Standard Libraries
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------


#    kCells
#--------------------------------------------------------------------
from kCells import Node, Edge, Face

#    Complex & Grids
#--------------------------------------------------------------------
from complex import PrimalComplex2D, DualComplex2D

#    Tools
#--------------------------------------------------------------------
import tools.colorConsole as cc
import tools.placeFigures as pf
from tools import MyLogging


    
#==============================================================================
#    EXAMPLE
#==============================================================================
if __name__ == '__main__':
    
    with MyLogging('Test'):
        
        extraEdge = True

#-------------------------------------------------------------------------
#    Create face example
#-------------------------------------------------------------------------

        n0 = Node(0,0,0)
        n1 = Node(1,0,0)
        n2 = Node(0,1,0)
        n3 = Node(1,1,0)
        n4 = Node(1.5,0,0)
        n5 = Node(0,1.5,0)
        n6 = Node(0.5,1.5,0)
        n7 = Node(1.5,1.5,0)
        
        
        nodes = [n0,n1,n2,n3,n4,n5,n6,n7]
        
        e0 = Edge(n0,n1)
        e1 = Edge(n1,n3)
        e2 = Edge(n3,n2)
        e3 = Edge(n2,n0)
        e4 = Edge(n1,n4)
        e5 = Edge(n4,n7)
        e6 = Edge(n7,n6)
        e7 = Edge(n6,n5)
        e8 = Edge(n5,n2)
        e9 = Edge(n6,n3)
        
        
        
        edges = [e0,e1,e2,e3,e4,e5,e6,e7,e8,e9]
        
        if extraEdge:
            e10 = Edge(n7,n3)
            edges.append(e10)
        
        
        
        f0 = Face([e0,e1,e2,e3])
        
        if extraEdge:
            f1 = Face([e4,e5,e10,-e1])
            f3 = Face([e6,e9,-e10])
            f3.category1 = 'border'
        else:
            f1 = Face([e4,e5,e6,e9,-e1])
            
        f2 = Face([e8,-e2,-e9,e7])
        
        f1.category1 = 'border'
        f2.category1 = 'border'
        
        faces = [f0,f1,f2]
        
        if extraEdge:
            faces.append(f3)
        
        
        pc = PrimalComplex2D(nodes,edges,faces)
        dc = DualComplex2D(pc)
        
        
        
        
        
        
        
        
    


#-------------------------------------------------------------------------
#    Plotting
#-------------------------------------------------------------------------    
    
        # Choose plotting method. Possible choices: pyplot, VTK, TikZ, animation, doc, None
        plottingMethod = 'pyplot'   
        
        
#    Disabled
#--------------------------------------------------------------------- 
        if plottingMethod is None or plottingMethod == 'None':
            cc.printBlue('Plotting disabled')
        
#    Pyplot
#---------------------------------------------------------------------         
        elif plottingMethod == 'pyplot':
            cc.printBlue('Plot using pyplot')
            (figs,axes) = pf.getFigures()
            
            for n in nodes:
                n.plotNode(axes[0])
                
            for e in edges:
                e.plotEdge(axes[0])
                e.plotEdge(axes[1])
                
            for f in faces:
                f.plotFace(axes[1])
                
            dc.plotComplex(axes[2])
            
            # f0.plotFace(axes[0])

#    VTK
#--------------------------------------------------------------------- 
        elif plottingMethod == 'VTK' :
            cc.printBlue('Plot using VTK')
            cc.printRed('Not implemented')

#    TikZ
#--------------------------------------------------------------------- 
        elif plottingMethod == 'TikZ' :
            cc.printBlue('Plot using TikZ')            
            cc.printRed('Not implemented')
            
#    Animation
#--------------------------------------------------------------------- 
        elif plottingMethod == 'animation':
            cc.printBlue('Creating animation')
            cc.printRed('Not implemented')
            
#    Documentation
#--------------------------------------------------------------------- 
        elif plottingMethod == 'doc':
            cc.printBlue('Creating plots for documentation')
            test.plotDoc()
            
#    Unknown
#---------------------------------------------------------------------             
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))        
        
    
