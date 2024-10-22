# -*- coding: utf-8 -*-
#==============================================================================
# DUAL COMPLEX 3D
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Mar  1 15:14:05 2019

'''

'''
#==============================================================================
#    IMPORTS
#==============================================================================
if __name__ == '__main__':
    import os
    os.chdir('../')

from complex.complex3D import Complex3D
from complex.primalComplex3D import PrimalComplex3D

from kCells import Node,DualNode3D,DualNode2D
from kCells import Edge,DualEdge3D,DualEdge2D
from kCells import Face,DualFace3D,DualFace2D
from kCells import Volume,DualVolume3D
import tools.colorConsole as cc


#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class DualComplex3D(Complex3D):
    '''
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__primalComplex',
                 '__createNodes',
                 '__createEdges',
                 '__createFaces',
                 '__createVolumes')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,primalComplex,createNodes=True,createEdges=True,createFaces=True,createVolumes=True):
        '''
        
        :param PrimalComplex primalComplex: The primal complex of which the
            dual shall be constructed.
        
        '''
        
     
        self.__primalComplex = primalComplex
        primalComplex.dualComplex = self
        self.__createNodes = createNodes
        self.__createEdges = createEdges
        self.__createFaces = createFaces
        self.__createVolumes = createVolumes
        super().__init__(loggerName=__name__)
        
        
#        self.__primalComplex = primalComplex
#        
#        (nodes,edges,faces,volumes) = self.__createDualCells(primalComplex)
#        
#        super().__init__(nodes,
#                         edges,
#                         faces,
#                         volumes)
#        
#        
#        
#        
#        
#        primalComplex.dualComplex = self
#        for f in self.faces:
#            for n in f.geometricNodes:
#                if not n in self.geometricNodes:
#                    self.geometricNodes.append(n)
#            for e in f.geometricEdges:
#                if not e in self.geometricEdges:
#                    self.geometricEdges.append(e)
#                    
#                    
#        self.renumberList(self.geometricNodes)
##        self.logger.warning(self.geometricNodes)
#                    
#            
#                    
#        
#        
#        self.sortPrimal()
##        self.__checkCategory2()
#        self.sortDual()
        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getPrimalComplex(self): return self.__primalComplex
    primalComplex = property(__getPrimalComplex)
    '''
    
    '''

    def __getUseCategory(self): 
        if self.__primalComplex:
            return self.__primalComplex.useCategory
        else:
            self.logger.error('Cannot get useCategory: no dual defined')
            return None
    def __setUseCategory(self,u): 
        if self.__primalComplex:
            self.__primalComplex.useCategory = u
        else:
            self.logger.error('Cannot set useCategory: no dual defined')
    useCategory = property(__getUseCategory,__setUseCategory)
    '''
    
    '''
    
    
    def __getChangedNumbering(self): 
        if self.primalComplex:
            return self.primalComplex.changedNumbering
        else:
            self.logger.error('Cannot get changedNumbering: no primalComplex defined')
            return False
    changedNumbering = property(__getChangedNumbering)
    '''
    
    '''    
    
    






#==============================================================================
#    MAGIC METHODS
#==============================================================================
    def  __repr__(self):
        return 'DualComplex3D with {} nodes, {} edges, {} faces and {} volumes'.format(len(self.nodes),len(self.edges),len(self.faces),len(self.volumes))
    
#==============================================================================
#    METHODS
#==============================================================================
  


    def setUp(self):
        '''
        
        '''
        self.logger.info('Called "Set Up" in DualComplex2D class')
        self.__construct()
        self.sortPrimal()
        self.sortDual()
        super().setUp()

 




#-------------------------------------------------------------------------
#    Method 1
#-------------------------------------------------------------------------
    def __construct(self):
#        cc.printMagenta('Dual Complex 3D: Creating dual cells')
        dualNodes = []
        dualEdges = []
        dualFaces = []
        dualVolumes = []
        
        
        # Dual nodes
        if self.__createNodes:
            for v in self.__primalComplex.volumes:
                dualNodes.append(DualNode3D(v))
            for f in self.__primalComplex.borderFaces1:
                dualNodes.append(DualNode2D(f))
        else:
            self.logger.warning('Creation of nodes has been disabled')
            
            
        # Dual edges
        if self.__createEdges and self.__createNodes:
            for f in self.__primalComplex.innerFaces1 + self.__primalComplex.borderFaces1:
                dualEdges.append(DualEdge3D(f))
            for e in self.__primalComplex.borderEdges1:
                dualEdges.append(DualEdge2D(e))
        else:
            self.logger.warning('Creation of edges has been disabled')                  
            
        # Dual faces
        if self.__createFaces and self.__createEdges and self.__createNodes:
            for e in self.__primalComplex.innerEdges1 +  self.__primalComplex.borderEdges1:
                dualFaces.append(DualFace3D(e))
            for n in self.__primalComplex.borderNodes1:
                dualFaces.append(DualFace2D(n))     
            for f in dualFaces:
                f.simplifyFace()
        else:
            self.logger.warning('Creation of faces has been disabled')     


        # Dual volumes
        if self.__createVolumes and self.__createFaces and self.__createEdges and self.__createNodes:
            for n in self.__primalComplex.borderNodes1+self.__primalComplex.innerNodes1:
                dualVolumes.append(DualVolume3D(n))
        else:
            self.logger.warning('Creation of volumes has been disabled')                     
                
            
            
            
        # Geometric nodes
        
        geometricNodes = []
        
        for e in dualEdges:
            for n in e.geometricNodes:
                if not n in geometricNodes:
                    geometricNodes.append(n)
        for f in dualFaces:
            for n in f.geometricNodes:
                if not n in geometricNodes:
                    geometricNodes.append(n)
                    
                    
        self.renumberList(geometricNodes)
            
            
            
            
            
            
#        
#        
#                        
#                                    
##                            cc.printMagenta('Dual Complex 3D: finished simplification of faces')
#                                    
#                            if True:
#                                # Dual volumes
#                                for n in primalComplex.borderNodes+primalComplex.innerNodes:
#                                    volumes.append(DualVolume3D(n))
#                                    
#                                    
        self.nodes = dualNodes
        self.edges = dualEdges
        self.faces = dualFaces
        self.volumes = dualVolumes
        self.geometricNodes = geometricNodes


     
    
#    def reOrderAll(self):
#        if self.useCategory == 1:
#            super().innerNodes1.sort(key = lambda x: x.num)
#            super().borderNodes1.sort(key = lambda x: x.num)
#            super().additionalBorderNodes1.sort(key = lambda x: x.num)
#            super().innerEdges1.sort(key = lambda x: x.num)
#            super().borderEdges1.sort(key = lambda x: x.num)
#            super().additionalBorderEdges1.sort(key = lambda x: x.num)
#            super().innerFaces1.sort(key = lambda x: x.num)
#            super().borderFaces1.sort(key = lambda x: x.num)
#            super().additionalBorderFaces1.sort(key = lambda x: x.num)
#            super().innerVolumes1.sort(key = lambda x: x.num)
#            super().borderVolumes1.sort(key = lambda x: x.num)
#        elif self.useCategory == 2:
#            super().innerNodes2.sort(key = lambda x: x.num)
#            super().borderNodes2.sort(key = lambda x: x.num)
#            super().additionalBorderNodes2.sort(key = lambda x: x.num)
#            super().innerEdges2.sort(key = lambda x: x.num)
#            super().borderEdges2.sort(key = lambda x: x.num)
#            super().additionalBorderEdges2.sort(key = lambda x: x.num)
##            self.logger.warning('Reactivate the line above!!')
#            super().innerFaces2.sort(key = lambda x: x.num)
#            super().borderFaces2.sort(key = lambda x: x.num)
#            super().additionalBorderFaces2.sort(key = lambda x: x.num)
#            super().innerVolumes2.sort(key = lambda x: x.num)
#            super().borderVolumes2.sort(key = lambda x: x.num)    
#        else:
#            self.logger.error('Unknown useCategory {}'.format(self.useCategory))    
 
    
    
    
    
    def renumber(self):
        '''
        
        '''
        if self.primalComplex:
            self.primalComplex.renumber()
        else:
            self.logger.error('Cannot renumber: no primalComplex defined')    
    
    
    
#-------------------------------------------------------------------------
#    Check category 2
#-------------------------------------------------------------------------   
    
    
    def checkCategory2(self):
        
        if False:
            myPrintDebug = self.logger.debug
            myPrintInfo = self.logger.info
            myPrintWarning = self.logger.warning
            myPrintError = self.logger.error
        else:
            self.logger.warning('Using prints instead of logger!')
            myPrintDebug = cc.printGreen
            myPrintInfo = cc.printCyan
            myPrintWarning = cc.printYellow
            myPrintError = cc.printRed
        
  
#    Check volumes
#------------------------------------------------------------------------- 
        
        if True:
            myPrintInfo('Checking volumes')
            
            # Go through all faces
            for v in super().volumes:
                
                if v.category2 == 'undefined':
                    myPrintError('Category2 of {} was not set'.format(v))
        
        
       
#    Check faces
#------------------------------------------------------------------------- 
        
        if True:
            myPrintInfo('Checking faces')
            
            # Go through all faces
            for f in super().faces:
#                f.useCategory = 2
#                
                if f.category2 == 'undefined':
                    myPrintError('Category2 of {} was not set'.format(f))
#                
                # Uncategorized faces are categorized automatically
                if len(f.volumes) == 0:
                    myPrintError('Face {} does not belong to a volume'.format(f))
                
                # Faces that belong to only one volume must be at some kind of border
                elif len(f.volumes) == 1:
                                        
                    
                    # If the face belongs to a single inner volume, it is a border face
                    if f.volumes[0].category2 == 'inner':
                        if f.category2 == 'border':
                            myPrintDebug('Face {} is categorized correctly'.format(f))
                        else:
                            myPrintError('Category2 of  {} is wrong it is {} but should be border'.format(f,f.category2))
                        
                    # If the face belongs to a single border volume, it is an additional border face
                    elif f.volumes[0].category2 == 'border':
                        if f.category2 == 'additionalBorder':
                            myPrintDebug('Face {} is categorized correctly'.format(f))
                        else:
                            myPrintError('Category2 of  {} is wrong it is {} but should be additionalBorder'.format(f,f.category2))
                        
#                        f.category1 = 'additionalBorder'
#                        myPrintDebug('Face {} is an additional border face'.format(f.infoText))
#                        
#                    # Anything else is not knwon
                    else:
                        myPrintError('Unknown category of volume %s',f.volumes[0].infoText)
#                    
                # Faces that belong to two volumes are inner faces
                elif len(f.volumes) == 2:
                    if f.category2 == 'inner':
                        myPrintDebug('Face {} is categorized correctly'.format(f))
                    else:
                        myPrintError('Category2 of  {} is wrong it is {} but should be inner'.format(f,f.category2))
#                
#                # Faces cannot belong to more than 2 volumes - at least in 3 dimensions ;)
#                elif len(f.volumes) > 2:
#                    myPrintError('Face {} belongs to too many volumes'.format(f))
#                        
#                    
                    
#    Check edges
#------------------------------------------------------------------------- 
        
        if True:
            myPrintInfo('Checking edges')
            
            for e in super().edges:
                
                if e.category2 == 'undefined':
                     myPrintError('Category2 of {} was not set'.format(e))
                
                # Edges that belong to a border face are border edges
                if any([f.category2 == 'border' for f in e.faces]):
                    if e.category2 == 'border':
                        myPrintDebug('Edge {} is categorized correctly'.format(e))
                    else:
                        myPrintError('Category2 of  {} is wrong it is {} but should be border'.format(e,e.category2))
#                
                
                # Edges that  belong to additional border faces are additional border edges
                elif any([f.category2 == 'additionalBorder' for f in e.faces]):
                    if e.category2 == 'additionalBorder':
                        myPrintDebug('Edge {} is categorized correctly'.format(e))
                    else:
                        myPrintError('Category2 of  {} is wrong it is {} but should be additionalBorder'.format(e,e.category2))
#                    
                # Edges that are not categorized so far are inner edges
                else:
                    if e.category2 == 'inner':
                        myPrintDebug('Edge {} is categorized correctly'.format(e))
                    else:
                        myPrintError('Category2 of  {} is wrong it is {} but should be inner'.format(e,e.category2))
            
    
#    Check nodes
#-------------------------------------------------------------------------    
        if True:
                    
            myPrintInfo('Checking nodes')
            
            for n in super().nodes:
                if n.category2 == 'undefined':
                     myPrintError('Category2 of {} was not set'.format(n))
                
                
                # Nodes that belong to border edges are border nodes
                if any([e.category2 == 'border' for e in n.edges]):
                    if n.category2 == 'border':
                        myPrintDebug('Node {} is categorized correctly'.format(n))
                    else:
                        myPrintError('Category2 of  {} is wrong it is {} but should be border'.format(n,n.category2))
#                 
                # Nodes that belong to additional border edges are additional border nodes
                elif any([e.category2 == 'additionalBorder' for e in n.edges]):
                    if n.category2 == 'additionalBorder':
                        myPrintDebug('Node {} is categorized correctly'.format(n))
                    else:
                        myPrintError('Category2 of  {} is wrong it is {} but should be additionalBorder'.format(n,n.category2))                    
#                    n.category2 = 'additionalBorder'
#                    myPrintDebug('Node {} is an additional border node'.format(n))
                
                # Nodes that are not categorized so far are inner nodes
                else:
                    if n.category2 == 'inner':
                        myPrintDebug('Node {} is categorized correctly'.format(n))
                    else:
                        myPrintError('Category2 of  {} is wrong it is {} but should be inner'.format(n,n.category2))                       
#                    n.category1 = 'inner'
#                    myPrintDebug('Node {} is an inner node'.format(n))    
#    
                        
                 
                    
#    Check dualities
#-------------------------------------------------------------------------  
        if True:
            myPrintInfo('Checking dual complex')
            for v in super().volumes:
                if v.category2 == v.dualCell3D.category2:
                    myPrintDebug('{} and {} are ok'.format(v,v.dualCell3D))
                else:
                    myPrintError('Category2 of {} is not set correctly'.format(v.dualCell3D))
            
            for f in super().faces:
                if f.category2 == 'additionalBorder':
                    pass
#                    if f.category2 == f.dualCell2D.category2:
#                        myPrintDebug('{} and {} are ok'.format(f,f.dualCell2D))
#                    else:
#                        myPrintError('Category2 of {} (2D dual of {}) is not set correctly it is {} but should be '.format(f.dualCell2D,f))
                else:
                    if f.category2 == f.dualCell3D.category2:
                        myPrintDebug('{} and {} are ok'.format(f,f.dualCell3D))
                    else:
                        myPrintError('Category2 of {} is not set correctly'.format(f.dualCell3D))
            
            for e in super().edges:
#                myPrintDebug('Cell: {} - 3D dual: {} - 2D dual:  {}'.format(e,e.dualCell3D,e.dualCell2D))
                if e.category2 == 'additionalBorder':
                    pass
#                    if e.category2 == e.dualCell2D.category2:
#                        myPrintDebug('{} and {} are ok'.format(e,e.dualCell2D))
#                    else:
#                        myPrintError('Category2 of {} (2D dual of {}) is not set correctly'.format(e.dualCell2D,e))
                else:
                    if e.category2 == e.dualCell3D.category2:
                        myPrintDebug('{} and {} are ok'.format(e,e.dualCell3D))
                    else:
                        myPrintError('Category2 of {} is not set correctly'.format(e.dualCell3D))
            
            for n in super().nodes:
#                myPrintDebug('Cell: {} - 3D dual: {} - 2D dual:  {}'.format(n,n.dualCell3D,n.dualCell2D))
                if n.category2 == 'additionalBorder':
                    pass
#                    if n.category2 == n.dualCell2D.category2:
#                        myPrintDebug('{} and {} are ok'.format(n,n.dualCell2D))
#                    else:
#                        myPrintError('Category2 of {} (2D dual of {}) is not set correctly'.format(n.dualCell2D,n))
                else:
                    if n.category2 == n.dualCell3D.category2:
                        myPrintDebug('{} and {} are ok'.format(n,n.dualCell3D))
                    else:
                        myPrintError('Category2 of {} is not set correctly'.format(n.dualCell3D))
                        
                        
        if True:
            myPrintInfo('Checking primal complex')
            for v in self.__primalComplex.volumes:
                if v.category2 == v.dualCell3D.category2:
                    myPrintDebug('{} and {} are ok'.format(v,v.dualCell3D))
                else:
                    myPrintError('Category2 of {} is not set correctly'.format(v.dualCell3D))
            
            for f in self.__primalComplex.faces:
                if f.category2 == 'additionalBorder':
                    pass
#                    if f.category2 == f.dualCell2D.category2:
#                        myPrintDebug('{} and {} are ok'.format(f,f.dualCell2D))
#                    else:
#                        myPrintError('Category2 of {} (2D dual of {}) is not set correctly'.format(f.dualCell2D,f))
                else:
                    if f.category2 == f.dualCell3D.category2:
                        myPrintDebug('{} and {} are ok'.format(f,f.dualCell3D))
                    else:
                        myPrintError('Category2 of {} is not set correctly'.format(f.dualCell3D))
            
            for e in self.__primalComplex.edges:
                if e.category2 == 'additionalBorder':
                    pass
#                    if e.category2 == e.dualCell2D.category2:
#                        myPrintDebug('{} and {} are ok'.format(e,e.dualCell2D))
#                    else:
#                        myPrintError('Category2 of {} (2D dual of {}) is not set correctly'.format(e.dualCell2D,e))
                else:
                    if e.dualCell3D:
                        if e.category2 == e.dualCell3D.category2:
                            myPrintDebug('{} and {} are ok'.format(e,e.dualCell3D))
                        else:
                            myPrintError('Category2 of {} is not set correctly'.format(e.dualCell3D))
                    else:
                         myPrintError('3D dual of {} is defined'.format(e))
            
            for n in self.__primalComplex.nodes:
                if n.category2 == 'additionalBorder':
                    pass
#                    if n.dualCell2D:
#                        if n.category2 == n.dualCell2D.category2:
#                            myPrintDebug('{} and {} are ok'.format(n,n.dualCell2D))
#                        else:
#                            myPrintError('Category2 of {} (2D dual of {}) is not set correctly'.format(n.dualCell2D,n))
#                    else:
#                         myPrintError('2D dual of {} is not defined'.format(n))
                        
                else:
                    if n.category2 == n.dualCell3D.category2:
                        myPrintDebug('{} and {} are ok'.format(n,n.dualCell3D))
                    else:
                        myPrintError('Category2 of {} is not set correctly'.format(n.dualCell3D))                        
                        
                        
                        
#        for c in super().nodes + super().edges + super().faces + super().volumes + self.__primalComplex.nodes+self.__primalComplex.edges+self.__primalComplex.faces+self.__primalComplex.volumes:
#            c.useCategory = 1                        
                    
                        
                        
    

    
    
    
   



    def checkAllIncidenceMatrices(self,doPrints=True):
        '''
        
        '''
        checks = []
        
        self.useCategory = 1
        if doPrints:
            cc.printBlue()
            cc.printBlue('Checking incidence matrix dualities')
            cc.printBlue('='*35)
            cc.printBlue()
            cc.printBlue('Using category 1')
            cc.printBlue('-'*15)
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix3ii,-self.__primalComplex.incidenceMatrix1ii,'d̂3ii','-d1ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix3ib,-self.__primalComplex.incidenceMatrix1bi,'d̂3ib','-d1bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix3bi,-self.__primalComplex.incidenceMatrix1ib,'d̂3bi','-d1ib',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix3bb,-self.__primalComplex.incidenceMatrix1bb,'d̂3bb','-d1bb',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2ii,self.__primalComplex.incidenceMatrix2ii,'d̂2ii','d2ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2ib,self.__primalComplex.incidenceMatrix2bi,'d̂2ib','d2bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2bi,self.__primalComplex.incidenceMatrix2ib,'d̂2bi','d2ib',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2bb,self.__primalComplex.incidenceMatrix2bb,'d̂2bb','d2bb',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1ii,-self.__primalComplex.incidenceMatrix3ii,'d̂1ii','-d3ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1ib,-self.__primalComplex.incidenceMatrix3bi,'d̂1ib','-d3bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1bi,-self.__primalComplex.incidenceMatrix3ib,'d̂1bi','-d3ib',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1bb,-self.__primalComplex.incidenceMatrix3bb,'d̂1bb','-d3bb',doPrints))        
        
#        checks.append(self.checkIncidenceMatrixZero(self.incidenceMatrix1bb,'d̂1bb',doPrints))
#        checks.append(self.checkIncidenceMatrixZero(self.__primalComplex.incidenceMatrix1bb,'d1bb',doPrints))
        
        
        if doPrints:
            cc.printBlue()
            cc.printBlue('Using category 2')
            cc.printBlue('-'*15)
        
        self.useCategory = 2
        
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix3ii,-self.__primalComplex.incidenceMatrix1ii,'d̂3ii','-d1ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix3ib,-self.__primalComplex.incidenceMatrix1bi,'d̂3ib','-d1bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix3bi,-self.__primalComplex.incidenceMatrix1ib,'d̂3bi','-d1ib',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix3bb,-self.__primalComplex.incidenceMatrix1bb,'d̂3bb','-d1bb',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2ii,self.__primalComplex.incidenceMatrix2ii,'d̂2ii','d2ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2ib,self.__primalComplex.incidenceMatrix2bi,'d̂2ib','d2bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2bi,self.__primalComplex.incidenceMatrix2ib,'d̂2bi','d2ib',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2bb,self.__primalComplex.incidenceMatrix2bb,'d̂2bb','d2bb',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1ii,-self.__primalComplex.incidenceMatrix3ii,'d̂1ii','-d3ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1ib,-self.__primalComplex.incidenceMatrix3bi,'d̂1ib','-d3bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1bi,-self.__primalComplex.incidenceMatrix3ib,'d̂1bi','-d3ib',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1bb,-self.__primalComplex.incidenceMatrix3bb,'d̂1bb','-d3bb',doPrints))  


        
        
        if doPrints:
            cc.printGreen()
            
            if all(checks):
                cc.printGreen('-'*50)
                cc.printGreen('All incidence matrix dualities are correct')
                cc.printGreen('-'*50)
            else:
                cc.printRed('-'*50)
                cc.printRed('Not all incidence matrix dualities are correct')
                cc.printRed('-'*50)
            cc.printGreen()
        return checks
     
   
    

    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    import tools.placeFigures as pf
    import tools.colorConsole as cc
    from tools.myLogging import MyLogging
    
#    from kCells import Node, Edge, Face, Volume
    
    
    with MyLogging('DualComplex3D'):
        cc.printBlue('Create nodes')
        n0 = Node(0,0,0)
        n1 = Node(1,0,0)
        n2 = Node(1.5,0,0)
        n3 = Node(0,1,0)
        n4 = Node(1,1,0)
        n5 = Node(0,1.5,0)
        n6 = Node(1.5,1.5,0)
        n7 = Node(0,0,1)
        n8 = Node(1,0,1)
        n9 = Node(0,1,1)
        n10 = Node(1,1,1)
        n11 = Node(0,0,1.5)
        n12 = Node(1.5,0,1.5)
        n13 = Node(0,1.5,1.5)
        n14 = Node(1.5,1.5,1.5)
        
        
        nodes = [n0,n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14]
        
        
        cc.printBlue('Create edges')
        e0 = Edge(n0,n1)
        e1 = Edge(n1,n2)
        e2 = Edge(n3,n4)
        e3 = Edge(n5,n6)
        e4 = Edge(n0,n3)
        e5 = Edge(n1,n4)
        e6 = Edge(n2,n6)
        e7 = Edge(n3,n5)
        e8 = Edge(n4,n6)
        e9 = Edge(n7,n8)
        e10 = Edge(n8,n10)
        e11 = Edge(n10,n9)
        e12 = Edge(n9,n7)
        e13 = Edge(n11,n12)
        e14 = Edge(n12,n14)
        e15 = Edge(n14,n13)
        e16 = Edge(n13,n11)
        e17 = Edge(n0,n7)
        e18 = Edge(n1,n8)
        e19 = Edge(n4,n10)
        e20 = Edge(n3,n9)
        e21 = Edge(n2,n12)
        e22 = Edge(n6,n14)
        e23 = Edge(n5,n13)
        e24 = Edge(n7,n11)
        e25 = Edge(n8,n12)
        e26 = Edge(n10,n14)
        e27 = Edge(n9,n13)
        
        edges = [e0,e1,e2,e3,e4,e5,e6,e7,e8,e9,e10,e11,e12,e13,e14,e15,e16,e17,e18,e19,e20,e21,e22,e23,e24,e25,e26,e27]
        
        cc.printBlue('Create faces')
        f0 = Face([e0,e5,-e2,-e4])
        f1 = Face([e1,e6,-e8,-e5])
        f2 = Face([e2,e8,-e3,-e7])
        f3 = Face([e0,e18,-e9,-e17])
        f4 = Face([e5,e19,-e10,-e18])
        f5 = Face([e2,e19,e11,-e20])
        f6 = Face([e4,e20,e12,-e17])
        f7 = Face([e9,e10,e11,e12])
        f8 = Face([e9,e25,-e13,-e24])
        f9 = Face([e1,e21,-e25,-e18])
        f10 = Face([e6,e22,-e14,-e21])
        f11 = Face([e25,e14,-e26,-e10])
        f12 = Face([e8,e22,-e26,-e19])
        f13 = Face([e3,e22,e15,-e23])
        f14 = Face([e26,e15,-e27,-e11])
        f15 = Face([e7,e23,-e27,-e20])
        f16 = Face([e27,e16,-e24,-e12])
        f17 = Face([e13,e14,e15,e16])
        
        
        faces = [f0,f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17]
        
        
        cc.printBlue('Create volumes')
        
        v0 = Volume([-f0,f3,f4,-f5,-f6,f7])
        v1 = Volume([-f1,-f4,f9,f10,f11,-f12])
        v2 = Volume([-f2,f5,f12,-f13,f14,-f15])
        v3 = Volume([-f7,f8,-f11,-f14,-f16,f17])
        
        facesForVolume = [-f7,f8,-f11,-f14,-f16,f17]
        
        volumes = [v0,v1,v2,v3]
        
        for v in [v1,v2,v3]:
            v.category1 = 'border'
        
        pc = PrimalComplex3D(nodes,edges,faces,volumes)
        dc = DualComplex3D(pc,
                           createNodes=True,
                           createEdges=True,
                           createFaces=True,
                           createVolumes=True)




        
        dc.checkAllIncidenceMatrices()
        
        pc.printDualities()
        
        


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
            pc.useCategory=2
            pc.plotComplex(axes[0])
            pc.plotFaces(axes[0],showLabel=False,showNormalVec=False,showBarycenter=False)
            axes[0].set_title('Primal')
            axes[0].axis('off')
            figs[0].set_size_inches(4,4)
            figs[0].savefig('img/3D_primal.png',dpi=150)            
            pc.plotFaces(axes[1])
            pc.plotVolumes(axes[2])
            dc.plotComplex(axes[3])
            dc.plotFaces(axes[3],showLabel=False,showNormalVec=False,showBarycenter=False)
            axes[3].set_title('Primal')
            axes[3].axis('off')
            figs[3].set_size_inches(4,4)
            figs[3].savefig('img/3D_dual.png',dpi=150)              
            dc.plotFaces(axes[4])
            dc.plotVolumes(axes[5])
            
            

#    VTK
#--------------------------------------------------------------------- 
        elif plottingMethod == 'VTK' :
            cc.printBlue('Plot using VTK')
            cc.printRed('Not implemented')

#    TikZ
#--------------------------------------------------------------------- 
        elif plottingMethod == 'TikZ' :
            cc.printBlue('Plot using TikZ')            
            pic = pc.plotComplexTikZ()
            pic.scale = 5
            file = True
            pic.writeLaTeXFile('latex','primalComplex3D',compileFile=file,openFile=file)  
            
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
    
    


    

