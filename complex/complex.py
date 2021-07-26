# -*- coding: utf-8 -*-
#==============================================================================
# COMPLEX
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Oct 30 15:35:04 2019

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
import numpy as np

#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------


#    kCells
#--------------------------------------------------------------------


#    Complex & Grids
#--------------------------------------------------------------------


#    Tools
#--------------------------------------------------------------------
from tools import myLogging
import tools.colorConsole as cc

#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class Complex:
    '''
    This is the explanation of this class.
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__logger')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,loggerName = __name__):
        '''
        
        :param str loggerName: Name for the logger, passed from the lowest child  class
        
        '''
        self.__logger = myLogging.getLogger(loggerName)
        
        self.setUp()

        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getLogger(self): return self.__logger
    logger = property(__getLogger)
    '''
    
    '''
    
    
    
    def __getUseCategory(self):
        self.logger.warning('Using standard value for "useCategory". This should only be used in child classes')
        return 1
    useCategory = property(__getUseCategory)
    '''
    
    '''
    
    def __getChangedNumbering(self):
        self.logger.info('Using standard value for "changedNumbering".')
    changedNumbering = property(__getChangedNumbering)
    '''
    
    '''
    
    
    
#==============================================================================
#    METHODS
#==============================================================================
  
    
    
#-------------------------------------------------------------------------
#    Adapted min/max
#-------------------------------------------------------------------------     
    
    def myMin(self,iteratable):
        '''
        Returns -1 if the given list is empty, otherwise the minimal entry of
        the list.
        
        :param iteratable: A list with sortabable elements 
        
        '''        
        if len(iteratable) == 0:
            return -1
        else:
            return min(iteratable)
        
    def myMax(self,iteratable):
        '''
        Returns 1 if the given list is empty, otherwise the maximal entry of
        the list.
        
        :param iteratable: A list with sortabable elements 
        
        '''             
        if len(iteratable) == 0:
            return 1
        else:
            return max(iteratable)    
    
#-------------------------------------------------------------------------
#    Set up complex
#-------------------------------------------------------------------------        
    
    
    def setUp(self):
        '''
        
        '''
        self.logger.info('Called "Set Up" in Complex class')
        
#-------------------------------------------------------------------------
#    Add a k-cell to a list, if it is not in there yet
#-------------------------------------------------------------------------    
    def addToList(self,cell,listOfCells):
        '''
        
        '''
        if cell in listOfCells:
            self.logger.error('Cannot add {} because it is already in the list'.format(cell))
        else:
            listOfCells.append(cell)
            
            
    
#-------------------------------------------------------------------------
#    Pick the category according to the current choice of useCategory
#-------------------------------------------------------------------------     
    def pickCategory(self,opt1,opt2):
        '''
        
        '''
        if self.changedNumbering:
            self.renumber()
        if self.useCategory == 1:
            return opt1
        elif self.useCategory == 2:
            return opt2
        else:
            self.logger.error('useCategory is set to {} - this is not ok: only 1 and 2 is allowed')
            return None    
  
    
#-------------------------------------------------------------------------
#    Renumber a list (e.g. of kCells)
#-------------------------------------------------------------------------  
    def renumber(self):    
        '''
        This function should be implemented in child classes.
        
        '''
        self.logger.warning('Renumbering is not implemented')

#-------------------------------------------------------------------------
#    Renumber a list (e.g. of kCells)
#-------------------------------------------------------------------------  
    def renumberList(self,myList):
        '''
        
        '''
        for (i,c) in enumerate(myList):
            c.num = i
            

#-------------------------------------------------------------------------
#    Calculate incidence matrix 1 between nodes and edges
#-------------------------------------------------------------------------
    def calcIncidence1(self,nodes,edges):
        '''
        
        '''
        dim1 = len(nodes)
        dim2 = len(edges)
        incidenceMatrix = np.zeros((dim1,dim2))
        for e in edges:
            if e.startNode in nodes:
                entry1 = e.startNode.num
                entry2 = e.num
                if entry1<dim1 and entry2<dim2:
                    incidenceMatrix[entry1,entry2] = -1    
                else:
                    self.logger.error('Cannot assign value [{},{}] in matrix of dimension ({},{})'.format(entry1,entry2,dim1,dim2))
            if e.endNode in nodes:
                entry1 = e.endNode.num
                entry2 = e.num
                if entry1<dim1 and entry2<dim2:
                    incidenceMatrix[entry1,entry2] = 1   
                else:
                    self.logger.error('Cannot assign value [{},{}] in matrix of dimension ({},{})'.format(entry1,entry2,dim1,dim2))
        return incidenceMatrix
    
#-------------------------------------------------------------------------
#    Calculate incidence matrix 2 between edges and faces
#-------------------------------------------------------------------------    
    def calcIncidence2(self,edges,faces):
        '''
        
        '''
        dim1 = len(edges)
        dim2 = len(faces)
        incidenceMatrix = np.zeros((dim1,dim2))
        for f in faces:
            for e in f.edges:
                if e in edges:
                    entry1 = e.num
                    entry2 = f.num
                    if entry1<dim1 and entry2<dim2:
                        incidenceMatrix[entry1,entry2] = 1
                    else:
                        self.logger.error('Cannot assign value [{},{}] in matrix of dimension ({},{})'.format(entry1,entry2,dim1,dim2))
                elif -e in edges:
                    entry1 = e.num
                    entry2 = f.num
                    if entry1<dim1 and entry2<dim2:
                        incidenceMatrix[entry1,entry2] = -1
                    else:
                        self.logger.error('Cannot assign value [{},{}] in matrix of dimension ({},{})'.format(entry1,entry2,dim1,dim2))
        return incidenceMatrix


#-------------------------------------------------------------------------
#    Calculate incidence matrix 2 between faces and volumes
#-------------------------------------------------------------------------     
    def calcIncidence3(self,faces,volumes):
        '''
        
        '''
        dim1 = len(faces)
        dim2 = len(volumes)
        incidenceMatrix = np.zeros((dim1,dim2))
        for v in volumes:
            for f in v.faces:
                if f in faces:
                    entry1 = f.num
                    entry2 = v.num
                    if entry1<dim1 and entry2<dim2:
                        incidenceMatrix[entry1,entry2] = 1
                    else:
                        self.logger.error('Cannot assign value [{},{}] in matrix of dimension ({},{})'.format(entry1,entry2,dim1,dim2))
                elif -f in faces:
                    entry1 = f.num
                    entry2 = v.num
                    if entry1<dim1 and entry2<dim2:
                        incidenceMatrix[entry1,entry2] = -1
                    else:
                        self.logger.error('Cannot assign value [{},{}] in matrix of dimension ({},{})'.format(entry1,entry2,dim1,dim2))
        return incidenceMatrix
                
    
#-------------------------------------------------------------------------
#    Check that d1 = ± d2
#-------------------------------------------------------------------------    
    def checkIncidenceMatrixEqual(self,matrix1,matrix2,description1=None,description2=None,doPrints=True):
        '''
        
        '''
        if doPrints:
            if all([d is not None for d in [description1,description2]]):
                cc.printBlue('Check {} = {}^T ... '.format(description1,description2),end='')
        
        try:
            if (matrix1-matrix2.transpose()).any():
                if doPrints:
                    cc.printRed('Not ok')
                return False
            else:
                if doPrints:
                    cc.printGreen('Ok')
                return True
        except Exception as e:
            cc.printRed('Error occured: {}'.format(e))    
            
            
            
#-------------------------------------------------------------------------
#    Check that d = 0
#-------------------------------------------------------------------------    
    def checkIncidenceMatrixZero(self,matrix,description=None,doPrints=True):
        '''
        
        '''
        if doPrints:
            if description is not None:
                cc.printBlue('Check {} = 0 ... '.format(description),end='')
        
        try:
            if (matrix).any():
                if doPrints:
                    cc.printRed('Not ok')
                return False
            else:
                if doPrints:
                    cc.printGreen('Ok')
                return True
            
        except Exception as e:
            cc.printRed('Error occured: {}'.format(e))        
            
            
            
    def printHeadline(self,text,myPrint,symbol='#'):
        '''
        
        '''
        myPrint(symbol*(len(text)+4))
        myPrint(symbol + ' ' + text + ' ' + symbol)
        myPrint(symbol*(len(text)+4))            
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    
    with myLogging.MyLogging('Complex',debug=True):
        c = Complex()

