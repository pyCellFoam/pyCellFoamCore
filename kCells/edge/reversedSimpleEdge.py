# -*- coding: utf-8 -*-
#==============================================================================
# REVERSED SIMPLE EDGE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue May 22 15:46:32 2018





#==============================================================================
#    IMPORTS
#==============================================================================
if __name__== '__main__':
    import os
    os.chdir('../../')

from kCells.edge.baseSimpleEdge import BaseSimpleEdge
from kCells.cell import ReversedSimpleCell
import numpy as np

#==============================================================================
#    CLASS DEFINITION
#==============================================================================
class ReversedSimpleEdge(BaseSimpleEdge,ReversedSimpleCell):
    '''
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
#    __slots__ = ()
    
#==============================================================================
#    INITIALIZATION
#==============================================================================    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,loggerName=__name__,**kwargs)
        self.logger.debug('Initialized ReversedSimpleEdge')

    
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
        
        
    def __getStartNode(self): return self.myReverse.endNode
    startNode = property(__getStartNode)   
    '''
    The start node is stored in the non-reversed class.
    
    '''
#    
    def __getEndNode(self): return self.myReverse.startNode
    endNode = property(__getEndNode)
    '''
    The end node is stored in the non-reversed class.
    
    '''
    
    
    def __getBarycenter(self): 
        if self.myReverse:
            return self.myReverse.barycenter 
        else:
            self.logger.error('Reversed Simple Edge does not belong to a Simple Edge, cannot return barycenter')
            return np.array([0,0,0])
    barycenter = property(__getBarycenter)  
    '''
    The barycenter is stored in the non-reversed class.
    
    '''
    
    
    def __getDirectionVec(self): 
        if self.myReverse:
            return -self.myReverse.directionVec 
        else:
            self.logger.error('Reversed Simple Edge does not belong to a Simple Edge, cannot return directionVec')
            return np.array([0,0,0])
    directionVec = property(__getDirectionVec)  
    '''
    The direction vector is stored in the non-reversed class, but multplied
    with -1 for the reversed simple edge.
    
    '''
    
    
    

    def __getConnectionVec(self): 
        if self.myReverse:
            return -self.myReverse.connectionVec 
        else:
            self.logger.error('Reversed Simple Edge does not belong to a Simple Edge, cannot return directionVec')
            return np.array([0,0,0])
    connectionVec = property(__getConnectionVec)  
    '''
    The connection vector is stored in the non-reversed class, but multplied
    with -1 for the reversed simple edge.
    
    '''
    
    
    def __getSimpleFaces(self): 
        if self.myReverse:
            return [-sf for sf in self.myReverse.simpleFaces]
        else:
            self.logger.error('Reversed Simple Edge does not belong to a Simple Edge, cannot return simpleFaces')
            return []
    simpleFaces = property(__getSimpleFaces)  
    '''
    The simple faces are stored in the non-reversed class, but multplied
    with -1 for the reversed simple edge and reversed in their order.
    
    '''
    

    
    
#==============================================================================
#    METHODS
#==============================================================================
#-------------------------------------------------------------------------
#    Add a simple face that uses this simple edge
#-------------------------------------------------------------------------           
    def addSimpleFace(self,simpleFace):
        '''
        Add the negative simple face to the non-reversed simple edge.
        
        '''
        if self.myReverse:
            self.myReverse.addSimpleFace(-simpleFace)
        else:
            self.logger.error('Cannot add simple face {} to reversed simple edge {} because it does not belong to a simple edge'.format(simpleFace.infoText,self.infoText))
#-------------------------------------------------------------------------
#    Delete a simple face that uses this simple edge
#-------------------------------------------------------------------------               
    def delSimpleFace(self,simpleFace):
        '''
        Delete the negative simple face from the non-reversed simple edge.
        
        '''
        if self.myReverse:
            self.myReverse.delSimpleFace(-simpleFace)
        else:
            self.logger.error('Cannot delete simple face {} from reversed simple edge {} because it does not belong to a simple edge'.format(simpleFace.infoText,self.infoText))
    
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
    

if __name__ == '__main__':
    rse = ReversedSimpleEdge()
    print(rse)
    print(rse.barycenter)
    print(rse.simpleFaces)
    