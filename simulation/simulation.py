# -*- coding: utf-8 -*-
#==============================================================================
# TITLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue Apr 21 12:03:47 2020

'''
This is the explanation of the whole module and will be printed at the very 
beginning

Use - signs to declare a headline
--------------------------------------------------------------------------

* this is an item
* this is another one

#. numbered lists
#. are also possible


Maths
--------------------------------------------------------------------------

Math can be inline :math:`a^2 + b^2 = c^2` or displayed

.. math::

   (a + b)^2 = a^2 + 2ab + b^2

   (a - b)^2 = a^2 - 2ab + b^2

Always remember that the last line has to be blank

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
from tools import MyLogging
import tools.myLogging as ml
import tools.colorConsole as cc

#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class Simulation:
    '''
    This is the explanation of this class.
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__logger',
                 '__primalComplex',
                 '__dualComplex',
                 '__startTime',
                 '__endTime',
                 '__initialTimeStep',
                 '__maxNumberOfTimeSteps',
                 '__timeVector',
                 '__numberOfLastTimeStep')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,*,endTime=10,initialTimeStep=0.1,startTime=0,maxNumberOfTimeSteps=10000,**kwargs):
        '''
        This is the explanation of the __init__ method. 
        
        All parameters should be listed:
        
        :param int a: Some Number
        :param str b: Some String
        
        '''
        self.__logger = ml.getLogger('simulation')
        self.__primalComplex = None
        self.__dualComplex = None
        self.__startTime = startTime
        self.__endTime = endTime
        self.__initialTimeStep = initialTimeStep
        self.__maxNumberOfTimeSteps = maxNumberOfTimeSteps
        self.__timeVector = np.zeros(maxNumberOfTimeSteps+1)
        self.__numberOfLastTimeStep = None
        
        
        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getLogger(self): return self.__logger
    logger = property(__getLogger)
    '''
    
    '''

    def __getPrimalComplex(self): return self.__primalComplex
    def __setPrimalComplex(self,p): self.__primalComplex = p
    primalComplex = property(__getPrimalComplex,__setPrimalComplex)
    '''
    
    '''    

    def __getDualComplex(self): return self.__dualComplex
    def __setDualComplex(self,d): self.__dualComplex = d
    dualComplex = property(__getDualComplex,__setDualComplex)
    '''
    
    '''    

    def __getStartTime(self): return self.__startTime
    def __setStartTime(self,s): self.__startTime = s
    startTime = property(__getStartTime,__setStartTime)
    '''
    
    '''    

    def __getEndTime(self): return self.__endTime
    def __setEndTime(self,e): self.__endTime = e
    endTime = property(__getEndTime,__setEndTime)
    '''
    
    '''    

    def __getInitialTimeStep(self): return self.__initialTimeStep
    def __setInitialTimeStep(self,i): self.__initialTimeStep = i
    initialTimeStep = property(__getInitialTimeStep,__setInitialTimeStep)
    '''
    
    '''    

    def __getMaxNumberOfTimeSteps(self): return self.__maxNumberOfTimeSteps
    def __setMaxNumberOfTimeSteps(self,m): 
        self.__maxNumberOfTimeSteps = m
        self.logger.warning('Overwriting time vector')
        self.__timeVector = np.zeros(m+1)
    maxNumberOfTimeSteps = property(__getMaxNumberOfTimeSteps,__setMaxNumberOfTimeSteps)
    '''
    
    '''    

    def __getTimeVector(self): return self.__timeVector
    timeVector = property(__getTimeVector)
    '''
    
    '''    
    
    def __getNumberOfLastTimeStep(self): return self.__numberOfLastTimeStep
    def __setNumberOfLastTimeStep(self,n): self.__numberOfLastTimeStep = n
    numberOfLastTimeStep = property(__getNumberOfLastTimeStep,__setNumberOfLastTimeStep)
    '''
    
    '''




    
#==============================================================================
#    METHODS
#==============================================================================
    
#-------------------------------------------------------------------------
#    Run Simulation
#-------------------------------------------------------------------------
    def simulate(self):
        '''
        
        '''
        currentNumberOfTimeStep = 0
        currentTime = self.startTime
        self.timeVector[0] = self.startTime
        while currentNumberOfTimeStep < self.maxNumberOfTimeSteps and currentTime < self.endTime:
            currentTime += self.initialTimeStep
            currentNumberOfTimeStep += 1
            self.timeVector[currentNumberOfTimeStep] = currentTime
            
        self.numberOfLastTimeStep = currentNumberOfTimeStep
            
            
        
#-------------------------------------------------------------------------
#    Cut Not Used Parts of the Matrices
#-------------------------------------------------------------------------
    def cutVector(self,v):
        '''
        Cut a numpy ndarray at the number of the last time step. 
        
        :param numpy.ndarray v: Vector or matrix that should be cut.
        
        '''
        if self.numberOfLastTimeStep is None:
            self.logger.error('Last time step has not been calculated')
        else:
            return np.delete(v,np.s_[self.numberOfLastTimeStep+1:],axis=0)
        
    def cutVectors(self):
        '''
        Cut time vector at last calculated timestep.
        
        '''
        self.__timeVector = self.cutVector(self.__timeVector)
    


#-------------------------------------------------------------------------
#    Check Initial State Vector
#-------------------------------------------------------------------------
    def checkStateVector(self,v,requiredLength):
        '''
        Check that a given intitial vector fulfills all necessary properties.
        
        '''
        if not isinstance(v,np.ndarray):
            self.logger.error('Inital state vector must be a numpy array')
            return False
        if not len(v.shape) == 1:
            self.logger.error('Initial state vector must be a 1-dimensional array')
            return False
        if not v.shape[0] == requiredLength:
            self.logger.error('Initial state vector must have length {} but has {}'.format(requiredLength,v.shape[0]))
            return False
        return True

    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    with MyLogging('Simulation'):
        cc.printBlue('Create simulation')
        sim = Simulation()
        
        cc.printBlue('Run simulation')
        sim.simulate()
        
        cc.printBlue('Remove unused vector entries')
        sim.cutVectors()
        print(sim.timeVector)
        
        
        

        
        
    

