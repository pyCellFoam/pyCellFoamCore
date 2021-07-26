# -*- coding: utf-8 -*-
#==============================================================================
# BASE FACE
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

if __name__== '__main__':
    import os
    os.chdir('../../')
    
    
#from kCells import Cell
#import tools.tumcolor as tumcolor
#import numpy as np
#import tools.colorConsole as cc

from kCells.cell import BaseCell


#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class BaseFace(BaseCell):
    '''
    This is the explanation of this class.
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
#    __slots__ = ()

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,*args,**kwargs):
        '''
        This is the explanation of the __init__ method. 

        '''
        super().__init__(*args,**kwargs)
        self.logger.debug('Initialized BaseFace')
        
#        Cell.__init__(self,**kwargs)
#        self.__showNormalVec = True
#        self.color = tumcolor.TUMGreen
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getSimpleEdges(self):
        simpleEdges = []
        for e in self.edges:
            for se in e.simpleEdges:
                simpleEdges.append(se)
        return simpleEdges
    simpleEdges = property(__getSimpleEdges)
#    def __getGeometricEdges(self): return self.data.geometricEdges
#    geometricEdges = property(__getGeometricEdges)
#    
#    
#    def __getVolumes(self): return self.data.volumes
#    volumes = property(__getVolumes)
#    
#    def __getShowNormalVec(self): return self.__showNormalVec
#    def __setShowNormalVec(self,s): self.__showNormalVec = s
#    showNormalVec = property(__getShowNormalVec,__setShowNormalVec)
#    
    def __getBarycenter(self): return [sf.barycenter for sf in self.simpleFaces]
    barycenter = property(__getBarycenter)
    
    
    
#    
#    
#    def __getSimpleEdges(self):
#        simpleEdges = []
#        for sf in self.simpleFaces:
#            for se in sf.edges:
#                mse = -se
#                if mse in simpleEdges:
#                    simpleEdges.remove(mse)
#                else:
#                    simpleEdges.append(se)
#        return(simpleEdges)
#    simpleEdges = property(__getSimpleEdges)
#    
#    
    def __getNormalVec(self): return [sf.normalVec for sf in self.simpleFaces]
    normalVec = property(__getNormalVec)


    def __getArea(self):
        areas = []
        totalArea = 0
        for sf in self.simpleFaces:
            areas.append(sf.area)
            totalArea+=sf.area[1]
        area = [areas,totalArea]
        return area
    area = property(__getArea)

    
#    def __getFaces(self): return [self,]
#    faces = property(__getFaces)
    
    
    
    
    
#==============================================================================
#    METHODS
#==============================================================================
    def plotFace(self,*arg,**kwarg):
        if self.geometryChanged:
            self.setUp()
        
        if self.showInPlot:
            
            if not self.simpleFaces:
                self.logger.warning('Face {} has no simple faces, maybe it was deleted'.format(self))
            for sf in self.simpleFaces:
                sf.plotFace(*arg,**kwarg) 
        else:
            self.logger.warning('Plotting of face {} is disabled'.format(self))  
            
    def plotFaceVtk(self,*arg,**kwarg):
        if self.geometryChanged:
            self.setUp()
        
        
        
        if not self.simpleFaces:
            self.logger.warning('Face {} has no simple faces, maybe it was deleted'.format(self))
        for sf in self.simpleFaces:
            sf.plotFaceVtk(*arg,**kwarg) 
            
    def plotFlowVtk(self,*arg,**kwarg):
        if self.geometryChanged:
            self.setUp()
        if not self.simpleFaces:
            self.logger.warning('Face {} has no simple faces, maybe it was deleted'.format(self))
        for sf in self.simpleFaces:
            sf.plotFlowVtk(*arg,**kwarg) 
        
        
    def plotFaceTikZ(self,*args,**kwargs):
#        tikzText = ''
        if self.showInPlot:
            for sf in self.simpleFaces:
                sf.plotFaceTikZ(*args,**kwargs)
#        return tikzText
            
            
            
    
    def isIdenticalTo(self,other):
        '''
        Two faces are seen as identical, if they consist of the same edges. 
        The orientation is neglected.
        
        Remark: It is of course not possible that only some of the edges are 
        flipped, because then one of the faces would not be defined correctly.
        
        '''
        return (all([e in other.edges for e in self.edges]) and all([e in self.edges for e in other.edges])) or (all([-e in other.edges for e in self.edges])  and all([-e in self.edges for e in other.edges]))





    
    
    
    
    
#    def updateFace(self):
#        self.geometryChanged = True
#        self.logger.debug('Update Face{}'.format(self.infoText))
#        for v in self.volumes:
#            v.updateVolume()
            
            
            

            
#    def deleteFace(self):
#        self.logger.debug('Delete Face {}'.format(self.infoText))
#        if len(self.volumes) != 0:
#            self.logger.error('Cannot delete face {} because it belongs to a volume'.format(self.infoText))
#        else:
##            for e in self.edges:
##                e.delFace(self)
##            for e in self.geometricEdges:
##                e.delFace(self)
#            self.data.rawEdges = []
#            self.num = -1
#            self.setUp()
        

        
    
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == "__main__":
    bf = BaseFace()

