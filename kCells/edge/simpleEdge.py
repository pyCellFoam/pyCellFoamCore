# -*- coding: utf-8 -*-
#==============================================================================
# SIMPLE EDGE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Dec  7 14:16:21 2017



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
    os.chdir('../../')


#-------------------------------------------------------------------------
#    Standard Libraries
#-------------------------------------------------------------------------
import numpy as np

#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------


#    kCells
#--------------------------------------------------------------------
from kCells.cell import SimpleCell
from kCells.edge.baseSimpleEdge import BaseSimpleEdge
from kCells.edge.reversedSimpleEdge import ReversedSimpleEdge

#    Complex & Grids
#--------------------------------------------------------------------


#    Tools
#--------------------------------------------------------------------


import tools.colorConsole as cc
# from geometricObjects import Cylinder




#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class SimpleEdge(BaseSimpleEdge,SimpleCell):
    '''
    
    '''

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,start,end,*args,belongsTo=None,**kwargs):
        '''
        Defines the edge and prepares further properties.        
        
        :param Node start: start node
        :param Node end: end node
        :param int num: number of the edge
        :param str label: text the edge is labelled with when plotted
        :param bool isAdditional: Should be changed!
        :param bool isDual: Does this edge belong to a dual complex
        
        '''
        if belongsTo == None:
            belongsToRev = None
        else:
            belongsToRev = belongsTo.myReverse
        super().__init__(*args,
                         myReverse=ReversedSimpleEdge(myReverse=self,belongsTo=belongsToRev),
                         belongsTo=belongsTo,
                         loggerName=__name__,
                         **kwargs)
        
        self.__startNode = start
        self.__endNode = end
        self.__createDirVec()
        self.__calcBarycenter()
        self.__startNode.addSimpleEdge(self)
        self.__endNode.addSimpleEdge(self)
        
        self.__simpleFaces = []
        self.__cylinder = None
        
        self.logger.debug('Initialized SimpleEdge')
        
        
        
        
        
        
#==============================================================================
#    GETTER AND SETTER
#==============================================================================
    def __getStartNode(self): return self.__startNode
    startNode = property(__getStartNode)
    '''
    Node that defines the start of the simple edge.
    
    '''
    
    def __getEndNode(self): return self.__endNode
    endNode = property(__getEndNode)
    '''
    Node that defines the end of the simple edge.
    
    '''
    
    def __getDirectionVec(self): return self.__directionVec
    directionVec = property(__getDirectionVec)
    '''
    Normalized vector in the direction of the simple edge.
    
    '''
    
    def __getConnectionVec(self): return self.__connectionVec
    connectionVec = property(__getConnectionVec)
    '''
    Unnormalized vector between start node and end node.
    
    '''
    
    def __getBarycenter(self): return self.__barycenter
    barycenter = property(__getBarycenter)
    '''
    Barycenter (= middle) of the simple edge
    
    '''
    
    def __getSimpleFaces(self): return self.__simpleFaces
    simpleFaces = property(__getSimpleFaces)
    '''
    All simple faces that this simple edge belongs to.
    
    '''
    
    def __getCylinder(self):
        if not self.__cylinder:
            self.__cylinder = Cylinder(1,self.startNode.coordinates,self.endNode.coordinates)
        return self.__cylinder
    cylinder = property(__getCylinder)
    '''
    Geometric object that represents the volume of the simple edge
    
    '''
    
    def __getRadius(self): return self.cylinder.radius
    def __setRadius(self,r): self.cylinder.radius = r
    radius = property(__getRadius,__setRadius)
    '''
    Radius of the simple or respectively a cylinder with the identical volume.
    
    '''
        
    
    
#==============================================================================
#    METHODS
#==============================================================================
    
#-------------------------------------------------------------------------
#    Calculate barycenter of simple edge
#-------------------------------------------------------------------------        
    def __calcBarycenter(self):
        '''
        Calculate the barycenter of the simple edge
        
        '''
        v1 = self.__startNode.coordinates
        v2 = self.__endNode.coordinates
        self.__barycenter = (v1+v2)/2
  
#-------------------------------------------------------------------------
#    Create direction vector
#-------------------------------------------------------------------------        
    def __createDirVec(self):
        '''
        Calculate the direction vector (normalized) and connection vector 
        (unnormalized).
        
        '''
        v = self.__endNode.coordinates-self.__startNode.coordinates
        if np.linalg.norm(v) > self.tolerance:
            self.__directionVec = v/np.linalg.norm(v)
            self.__connectionVec = v
        else:
            self.__directionVec = np.array([0,0,0])
            self.__connectionVec = np.array([0,0,0])
            self.logger.error('Cannot calculate direction vector of {} norm is too small, it is only {}'.format(self,np.linalg.norm(v)))
            self.logger.error('Start node {}: {} end node {}: {}'.format(self.startNode,self.startNode.coordinates,self.endNode,self.endNode.coordinates))
        
#-------------------------------------------------------------------------
#    Add a simple face that uses this simple edge
#-------------------------------------------------------------------------           
    def addSimpleFace(self,simpleFace):
        '''
        Register a new simple face that is created by using this simple edge.
        
        '''
        if simpleFace in self.__simpleFaces:
            self.logger.error('Simple face {} already belongs to simiple edge {}!'.format(simpleFace.infoText,self.infoText))
        else:
            self.__simpleFaces.append(simpleFace)
#-------------------------------------------------------------------------
#    Delete a simple face that uses this simple edge
#-------------------------------------------------------------------------               
    def delSimpleFace(self,simpleFace):
        '''
        Unregister a simple face that used this simple edge.
        
        '''
        if simpleFace in self.__simpleFaces:
            self.__simpleFaces.remove(simpleFace)
            self.logger.info('Removed simple face {} from simple edge {}'.format(simpleFace.infoText,self.infoText))
        else:
            self.logger.error('Cannot remove simple face {} from simple edge {}!'.format(simpleFace.infoText,self.infoText))
            
#-------------------------------------------------------------------------
#    Delete this simple edge
#-------------------------------------------------------------------------  
    def delete(self):
        '''
        Delete this simple edge and unregister it from the nodes.
        
        '''
        self.__startNode.delSimpleEdge(self)
        self.__endNode.delSimpleEdge(self)
        super().delete()




#==============================================================================
# TEST FUNCTIONS
#==============================================================================
        
if __name__ == '__main__':
    from kCells.node import Node
    import tools.placeFigures as pf
    from tools import MyLogging
    
    with MyLogging('Edge',debug=True) as ml:
        
        
        
        # Create some figures on second screen
        (fig,ax) = pf.getFigures(numTotal=2)
        
        # Create some nodes
        n1 = Node(1,2,-3,num=1)
        ml.logger.debug('')
        n2 = Node(2,2,4,num=2)    
        ml.logger.debug('')
        n3 = Node(1,2,5,num=3)
        ml.logger.debug('')
        n4 = Node(0,2,1,num=4)
        ml.logger.debug('')
#        
        nodes = [n1,n2,n3,n4]
#        
#        # Create SimpleEdge
        se1 = SimpleEdge(n1,n2)
#        
        cc.printBlue(se1)
#        
        se1.plotEdge(ax[0])
        
        cc.printBlue(se1.directionVec)
        cc.printBlue(se1.barycenter)
        
        mse1 = -se1
        mse1.plotEdge(ax[1])
        
        
        cc.printBlue(mse1.directionVec)
        cc.printBlue(mse1.barycenter)
        
        
        # import tools.myVTK as myv
        # myVTK = myv.MyVTK()
        # se1.plotEdgeVtk(myVTK)
#        myVTK.addActor(se1.cylinder.vtkActor)
        # myVTK.start()
        
        
        

    
    
        

    
