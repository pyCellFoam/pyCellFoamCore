# -*- coding: utf-8 -*-
#==============================================================================
# DUAL EDGE 3D
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Jul  6 13:23:04 2018

'''
In 3D, an edge is dual to a face. Additional border faces have no dual. For
inner and border faces, the dual edge is calculated as described in the 
following.
The orientation of the dual edge is given by the normal vector of the primal
face.

Inner face
--------------------------------------------------------------------------

An inner face belongs to two volumes. The dual edge connects the dual nodes of
these two volumes.

.. image:: ../../../_static/dualEdge3D_1.png
   :width: 400px
   :alt: 3D dual edge of an inner face
   :align: center


Border face
--------------------------------------------------------------------------

A border face belongs to one volume. The dual edge connects the dual node of 
this volume with the 2D dual node of the face itself.

.. image:: ../../../_static/dualEdge3D_0.png
   :width: 400px
   :alt: 3D dual edge of a border face
   :align: center


'''
#==============================================================================
#    IMPORTS
#==============================================================================
if __name__== '__main__':
    import os
    os.chdir('../../')
    
from kCells.cell import DualCell
from kCells.edge.edge import Edge
from kCells.node import Node, DualNode3D, DualNode2D
import tools.colorConsole as cc
import numpy as np
from tools import MyLogging
import tools.placeFigures as pf

#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class DualEdge3D(Edge,DualCell):
    '''
    Create 3D dual edge of a primal face
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
#    __slots__ = ()

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,face,*args,myPrintDebug=None,myPrintError=None,**kwargs):        
        '''
        
        :param Face face: Primal face
        
        '''

        
        n1 = Node(0,0,0)
        n2 = Node(1,0,0)
        super().__init__(n1,n2,
                         *args,
                         num = face.num,
                         **kwargs)
        
        if True:
            if myPrintDebug is None:
                myPrintDebug = self.logger.debug
            myPrintInfo = self.logger.info
            myPrintWarning = self.logger.warning
            if myPrintError is None:
                myPrintError = self.logger.error
        else:
            self.logger.warning('Using prints instead of logger!')
            myPrintDebug = cc.printGreen
            myPrintInfo = cc.printCyan
            myPrintWarning = cc.printYellow
            myPrintError = cc.printRed
            
        
        
        self.category1 = face.category1
        self.category2 = face.category2
        
        
        
        # If the primal volumes have no 3D duals yet, calculate them
        for v in face.volumes:
            if v.dualCell3D is None:
                myPrintDebug('Calculating dual node of {}'.format(v))
                DualNode3D(v)
        # If the primal face has no 2D dual yet, calculate it
        if face.dualCell2D is None:
            myPrintDebug('Calculating dual node of {}'.format(face))
            DualNode2D(face)                
            myPrintDebug('Finished calculation of dual node of {}'.format(face))
            
               
            
        
    
#-------------------------------------------------------------------------
#    Inner face
#-------------------------------------------------------------------------
        
         
        if face.category1 == 'inner':
            myPrintDebug('\nCreating dual edge for inner face {}'.format(face))
            
            # An inner face must belong to two volumes, check this before going on
            if len(face.volumes) == 2:
                
                myPrintDebug('dualEdge3D: Set start node of {} to node {} at {}'.format(self,face.volumes[0].dualCell3D,face.volumes[0].dualCell3D.coordinates))
                self.startNode = face.volumes[0].dualCell3D
                myPrintDebug('dualEdge3D: Set end node of {} to node {} at {}'.format(self,face.volumes[1].dualCell3D,face.volumes[1].dualCell3D.coordinates))
                self.endNode  = face.volumes[1].dualCell3D
                
                

                    
                # The 2D dual node is set as intermediate point for the 3D dual edge
                self.geometricNodes = face.dualCell2D
                
                # Setup edge to get direction vectors correct
                self.setUp()
                
                # If the direction vectors align, then the geometric node is unneccesary and can be removed
                if np.linalg.norm(self.directionVec[0]-self.directionVec[1])<1e-4:
                    myPrintDebug('dualEdge3D: Removing geometric node of {}'.format(self))
                    self.geometricNodes = []
                    self.setUp()
               
                
#                ################################################################################################################################################
#                # This is some old code, check if this can be deleted
#                ################################################################################################################################################
#                if face.volumes[0].category1 == 'border' and face.volumes[1].category1 == 'border':
#                    cc.printRed('{}: Setting geometric node for dual edge between {} and {}. Check if this is correct!'.format(self.infoText,face.volumes[0],face.volumes[1]))
#                ################################################################################################################################################    
                    
                    
                
                        
                    
            else:
                myPrintError('Face {} is inner and should therefor belong to two volumes, but belongs to {}'.format(face.infoText,len(face.volumes)))
                
                
#-------------------------------------------------------------------------
#    Border face
#-------------------------------------------------------------------------                
                
                
        elif face.category1 == 'border':
            myPrintDebug('\nCreating dual edge for border face {}'.format(face))
            if len(face.volumes) == 1:
                
                
                self.startNode = face.volumes[0].dualCell3D
                self.endNode = face.dualCell2D
                self.setUp()
                
            else:
                myPrintError('Face {} is border and should therefor belong to one volume, but belongs to {}'.format(face.infoText,len(face.volumes)))
                
        else:
            myPrintError('Unknown category {} of face {}'.format(face.category,face.infoText))
            
            
            
        # If the edge was created in the wrong direction (according to the prescribed direction of the primal face), it needs to be swapped
        if np.inner(self.directionVec[0],face.normalVec[0]) < 0:
            myPrintDebug('Swapping edge {} because it is in the wrong direction'.format(self))
            self.swap()            
            
        # Check direction
        if np.inner(self.directionVec[0],face.normalVec[0]) > 0:
            myPrintDebug('{}: direction ok'.format(self.infoText))
        else:
            myPrintError('{}: direction not ok'.format(self.infoText))
            
        
        self.dualCell3D = face
        face.dualCell3D = self
        
        
        
        
        # TODO: If the additional border edges share one face, then they should become one edge. Like this, the dual of the dual is unique again!!!
        if self.category1 == 'inner':
            for e in face.edges:
                if e.category1 == 'additionalBorder':
                    if e.isReverse:
                        e.dualCell2D = -self
                    else:
                        e.dualCell2D = self
                        
                    # TODO change this!!!
                    self.logger.info('Setting {} as dual of edge {}. This should not be done here'.format(self,e))
                    
                    
        myPrintDebug('Initialized DualEdge3D')
            
            
        
        
#==============================================================================
#    METHODS
#==============================================================================
#-------------------------------------------------------------------------
#    Plot for Documentation
#-------------------------------------------------------------------------         
    @classmethod
    def plotDoc(cls):    
        from kCells.face import Face
        from kCells.volume import Volume
    
        with MyLogging('dualEdge3D'):
            
            # Create nodes
            n0 = Node(0,0,0)
            n1 = Node(1,0,0)
            n2 = Node(0,1,0)
            n3 = Node(0,0,1)
            n4 = Node(0.5,0.5,1)
            
            # Create edges
            e0 = Edge(n0,n1)
            e1 = Edge(n0,n2)
            e2 = Edge(n0,n3)
            e3 = Edge(n1,n2)
            e4 = Edge(n1,n3)
            e5 = Edge(n2,n3)
            e6 = Edge(n1,n4)
            e7 = Edge(n2,n4)
            e8 = Edge(n3,n4)
            
            # Create faces
            f0 = Face([e0,e3,-e1])
            f1 = Face([e1,e5,-e2])
            f2 = Face([e0,e4,-e2])
            f3 = Face([e3,e5,-e4])
            f4 = Face([e4,e8,-e6])
            f5 = Face([e5,e8,-e7])
            f6 = Face([e3,e7,-e6])            
            faces = [f0,f1,f2,f3,f4,f5,f6]
            for f in faces:
                if f == f3:
                    f.category = 'inner'
                else:
                    f.category = 'border'

            # Create volumes            
            v1 = Volume([-f0,-f1,f2,f3])
            v2 = Volume([f6,f5,-f4,-f3])
            volumes = [v1,v2]
            for v in volumes:
                v.category = 'inner'
                
            # Create figures
            (figs,ax) = pf.getFigures(2,1)
                
            # Calculate dual edges
            de0 = DualEdge3D(f0)
            de3 = DualEdge3D(f3)
            
            # Plot volumes
            for v in volumes:
                v.showLabel = False
                v.showBarycenter = False
                v.plotVolume(ax[0])
                v.plotVolume(ax[1])
                
                
            # Plot dual edges
            de0.plotEdge(ax [0])
            de3.plotEdge(ax [1])
            
            # Plot primal faces
            f0.plotFace(ax[0])
            f3.plotFace(ax[1])
            
                
            # Plot dual nodes
            for n in de0.topologicNodes:
                n.plotNode(ax[0])
            for n in de3.topologicNodes:
                n.plotNode(ax[1])
                
            # Rotate figure                
            for a in ax:
                a.view_init(17,142)
                
            # Export png files
            for (i,f) in enumerate(figs):
                pf.exportPNG(f,'doc/_static/dualEdge3D_'+str(i))
        
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == "__main__":
    from kCells.face import Face
    from kCells.volume import Volume

    with MyLogging('dualEdge3D'):
        
        n0 = Node(0,0,0)
        n1 = Node(1,0,0)
        n2 = Node(0,1,0)
        n3 = Node(0,0,1)
        n4 = Node(0.5,0.5,1)
        nodes = [n0,n1,n2,n3,n4]
        
        e0 = Edge(n0,n1)
        e1 = Edge(n0,n2)
        e2 = Edge(n0,n3)
        e3 = Edge(n1,n2)
        e4 = Edge(n1,n3)
        e5 = Edge(n2,n3)
        e6 = Edge(n1,n4)
        e7 = Edge(n2,n4)
        e8 = Edge(n3,n4)
        edges = [e0,e1,e2,e3,e4,e5,e6,e7,e8]
        
        f0 = Face([e0,e3,-e1])
        f1 = Face([e1,e5,-e2])
        f2 = Face([e0,e4,-e2])
        f3 = Face([e3,e5,-e4])
        f4 = Face([e4,e8,-e6])
        f5 = Face([e5,e8,-e7])
        f6 = Face([e3,e7,-e6])
        faces = [f0,f1,f2,f3,f4,f5,f6]
        for f in faces:
            if f == f3:
                f.category = 'inner'
            else:
                f.category = 'border'
        
        v1 = Volume([-f0,-f1,f2,f3])
        v2 = Volume([f6,f5,-f4,-f3])
        volumes = [v1,v2]
        for v in volumes:
            v.category = 'inner'
        
        
        (figs,ax) = pf.getFigures(2,2)
        for e in edges:
            e.plotEdge(ax[0])
        for f in faces:
            f.plotFace(ax[0])
            
        for v in volumes:
            v.plotVolume(ax[1])
            
        de0 = DualEdge3D(f0,myPrintDebug=cc.printYellow)
        de3 = DualEdge3D(f3,myPrintDebug=cc.printYellow)
        
        for v in volumes:
            v.showLabel = False
            v.showBarycenter = False
            v.plotVolume(ax[2])
            v.plotVolume(ax[3])
            
            
        de0.plotEdge(ax [2])
        de3.plotEdge(ax [3])
        
        for n in de0.topologicNodes:
            n.plotNode(ax[2])
        
        for n in de3.topologicNodes:
            n.plotNode(ax[3])
            
        for a in ax:
            a.view_init(17,142)
            
        if False:
            DualEdge3D.plotDoc()
            
        
        
