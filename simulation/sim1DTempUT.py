# -*- coding: utf-8 -*-
#==============================================================================
# TITLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Apr 24 15:36:09 2020

r'''
Simulate temperature on a solid beam of length :math:`l` with constant height 
:math:`h` and width :math:`w`.
The heat capacity :math:`c_\mathrm{V}` and thermal conductivity :math:`\lambda`
are assumed to be constant on the beam.

Balance equations:
    
.. math::
    
    \begin{bmatrix}
        \frac{\partial}{\partial t} \mathbf{U^\mathrm{i}} \\
        \mathbf{F_\mathrm{T}^\mathrm{i}}
    \end{bmatrix}
    &=
    \begin{bmatrix}
        0 & -\mathbf{\hat{d}^1_\mathrm{ii}} \\
        -\mathbf{d^1_\mathrm{ii}} & 0
    \end{bmatrix}
    \begin{bmatrix}
        \mathbf{T^\mathrm{i}} \\
        \mathbf{J_\mathrm{Q}^\mathrm{i}}
    \end{bmatrix}
    +
    \begin{bmatrix}
        0 & -\mathbf{\hat{d}^1_\mathrm{ib}} \\
        -\mathbf{d^1_\mathrm{ib}} & 0
    \end{bmatrix}
    \begin{bmatrix}
        \mathbf{T^\mathrm{b}} \\
        \mathbf{J_\mathrm{Q}^\mathrm{b}}
    \end{bmatrix}

Constitutive laws:

.. math::
    
    \mathbf{U^\mathrm{i}} &= c_\mathrm{V} h w \mathbf{\hat{L}^\mathrm{i}} \mathbf{T^\mathrm{i}}  \\
    \mathbf{J_\mathrm{Q}^\mathrm{i}} &= \lambda h w \left(\mathbf{L^\mathrm{i}}\right)^{-1} \mathbf{F_\mathrm{T}^\mathrm{i}}

        
with 

.. math::
    
    \mathbf{\hat{L}^\mathrm{i}} &= \mathrm{diag}(|\hat{e}_{\mathrm{i},j}|), \quad j = 1 ... |\mathcal{\hat{E}}_i| \\
    \mathbf{L^\mathrm{i}} &= \mathrm{diag}(|e_{\mathrm{i},j}|), \quad j = 1 ... |\mathcal{E}_i| \\
    \mathbf{\hat{d}^1_\mathrm{ii}} &= \left(\boldsymbol{\hat{\partial}^1_\mathrm{ii}}\right)^\mathrm{T}\\
    \mathbf{\hat{d}^1_\mathrm{ib}} &= \left(\boldsymbol{\hat{\partial}^1_\mathrm{bi}}\right)^\mathrm{T} \\
    \mathbf{d^1_\mathrm{ii}} &= \left(\boldsymbol{\partial^1_\mathrm{ii}} \right)^\mathrm{T} \\
    \mathbf{d^1_\mathrm{ib}} &= \left(\boldsymbol{\partial^1_\mathrm{bi}} \right)^\mathrm{T} \\
    
    
    

'''
#        &= c_\mathrm{V}hw\mathbf{\hat{L}}

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
from grids.grid1DEquidistant import Grid1DEquidistant
from complex import DualComplex1D

#    Tools
#--------------------------------------------------------------------
from simulation.simulation import Simulation
from tools import MyLogging
import tools.placeFigures as pf
import tools.colorConsole as cc
import tools.tumcolor as tc

#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class Sim1DTemp(Simulation):
    '''
    This is the explanation of this class.
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__Ui',
                 '__JQb',
                 '__Tb',
                 '__Ui0',
                 '__height',
                 '__width',
                 '__rho',
                 '__cV',
                 '__LiDual',
                 '__LiDualInv',
                 '__LiPrimal',
                 '__LiPrimalInv',
                 '__lambda',
                 '__plotColor')
    

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,*,primalComplex=None,width=1,height=1,length=None,**kwargs):
        '''
        
        :param float h: Height of the beam
        :param float w: Width of the beam
        :param float l: Length of the beam
        
        '''
        self.__height = height
        self.__width = width
        self.__Ui = None

        
        self.__rho = 2700. # kg/m^3 for aluminium
        self.__cV = 897. # J / (kg K) for aluminium        
        self.__lambda = 200 # W / (m K) for aluminium
        
        super().__init__(**kwargs)
        if primalComplex is None:
            self.primalComplex = Grid1DEquidistant(xMin=0,xMax=length,**kwargs)
            
        self.dualComplex = DualComplex1D(self.primalComplex)
        
        self.__LiDual = np.diag([e.length[1] for e in self.dualComplex.innerEdges])
        self.__LiDualInv = np.diag([1/e.length[1] for e in self.dualComplex.innerEdges])
        self.__LiPrimal = np.diag([e.length[1] for e in self.primalComplex.innerEdges])
        self.__LiPrimalInv = np.diag([1/e.length[1] for e in self.primalComplex.innerEdges])
        
        
        self.__Ui0 = self.__cV*self.__rho*self.__height*self.__width * self.__LiDual @ np.ones(len(self.dualComplex.innerEdges)) * 273
        
        
        self.__Tb = np.ones((self.maxNumberOfTimeSteps+1,len(self.primalComplex.borderNodes))) * 293.0
        self.__JQb = np.zeros((self.maxNumberOfTimeSteps+1,len(self.dualComplex.borderNodes)))
        self.__plotColor = tc.TUMBlue()
        
        
            
            
            
        
        
        
        
        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getUi(self): return self.__Ui
    Ui = property(__getUi)
    '''
    
    '''
    
    def __getFi(self): return self.__Fi
    Fi = property(__getFi)
    '''
    
    '''
    
    def __getTi(self): 
        Ti = np.zeros(self.Ui.shape)
        for (num,Ui) in enumerate(self.Ui):
            Ti[num] = 1/(self.__cV*self.__rho*self.__height*self.__width) * self.__LiDualInv @ Ui
        return Ti
    Ti = property(__getTi)    
    '''
    
    '''
    
    def __getTb(self): return self.__Tb
    Tb = property(__getTb)
    '''
    
    '''
    
    
    
    def __getT(self): return np.hstack((self.Ti,self.Tb))
    T = property(__getT)
    '''
    
    '''
    
    def __getXPrimalNodes(self):
        return np.array([n.xCoordinate for n in self.primalComplex.innerNodes+self.primalComplex.borderNodes])
    xPrimalNodes = property(__getXPrimalNodes)
    
    

    def __getWidth(self):
        return self.__width
    width = property(__getWidth)
    '''
    
    '''
    
    def __getLength(self):
        return self.__length
    length = property(__getLength)
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
        
        self.__Ui = np.zeros((self.maxNumberOfTimeSteps+1,len(self.dualComplex.innerEdges)))
        
        
        
        self.__Ui[0] = self.__Ui0
        
        
        currentNumberOfTimeStep = 0
        currentTime = self.startTime
        self.timeVector[0] = self.startTime
        while currentNumberOfTimeStep < self.maxNumberOfTimeSteps and currentTime < self.endTime:
            
            

            Ui = self.__Ui[currentNumberOfTimeStep]
            
            Ti = 1/(self.__cV*self.__rho*self.__height*self.__width) * self.__LiDualInv @ Ui
            
            Fi = -self.primalComplex.incidenceMatrix1ii.transpose() @ Ti  - self.primalComplex.incidenceMatrix1bi.transpose() @ self.__Tb[currentNumberOfTimeStep]
            JQi =  self.__lambda * self.__width * self.__height * self.__LiPrimalInv @ Fi
            UiDot = -self.dualComplex.incidenceMatrix1ii.transpose() @ JQi  - self.dualComplex.incidenceMatrix1bi.transpose() @ self.__JQb[currentNumberOfTimeStep]
            
            
            
            
            
            
            currentTime += self.initialTimeStep
            currentNumberOfTimeStep += 1
            self.timeVector[currentNumberOfTimeStep] = currentTime
            
            self.__Ui[currentNumberOfTimeStep] = Ui + UiDot * self.initialTimeStep
            
            
            
            
        self.numberOfLastTimeStep = currentNumberOfTimeStep
    
    
    
#-------------------------------------------------------------------------
#    Plotting
#-------------------------------------------------------------------------   
        
    def plotTransient(self,fig,var):
        '''
        
        '''
        ax = pf.returnTo2D(fig)
        ax.plot(self.timeVector,var)
        
        
    def plotTransientUi(self,fig):
        '''
        
        '''
        self.plotTransient(fig,self.__Ui)
        
        
    def plotTransientTi(self,fig):
        '''
        
        '''
        self.plotTransient(fig,self.Ti)
        
    def plotTransientT(self,fig):
        '''
        
        '''
        self.plotTransient(fig,self.T)
        
        
        
    def plotTimeStep(self,ax,x,physicalVariables,timeStep,yZero=0):
        '''
        
        '''
        for (currentX,currentVar) in zip(x,physicalVariables[timeStep]):
            ax.plot([currentX, currentX],[yZero,currentVar],c=self.__plotColor.html)
            
            
            
    def plotTimeStepT(self,ax,timeStep,yZero=0):
        '''
        
        '''
        self.plotTimeStep(ax,self.xPrimalNodes,self.T,timeStep,yZero)
        
        
        


#-------------------------------------------------------------------------
#    Cut Not Used Parts of the Matrices
#------------------------------------------------------------------------- 
        
    def cutVectors(self):
        '''
        
        '''
        super().cutVectors()
        self.__Tb = self.cutVector(self.__Tb)
        self.__Ui = self.cutVector(self.__Ui)
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    with MyLogging('Sim1DTemp'):
        
        
        
        sim1 = Sim1DTemp(
                height = 0.01,
                width = 0.01,
                length = 0.5,
                endTime = 1000,
                initialTimeStep = 1,
                numberOfNodes=20)
        
        
        sim2 = Sim1DTemp(
                height = 0.01,
                width = 0.01,
                length = 0.5,
                endTime = 10000,
                initialTimeStep = 1,
                numberOfNodes=40,
                maxNumberOfTimeSteps = 1000)
        
        
        
        

        
        sim1.simulate()
        sim1.cutVectors()
        
        sim2.simulate()
        sim2.cutVectors()
        
        
        # Choose plotting method. Possible choices: pyplot, VTK, TikZ, animation, None
        plottingMethod = 'animation'   
        
        if plottingMethod is None or plottingMethod == 'None':
            cc.printBlue('Plotting disabled')
        
        elif plottingMethod == 'pyplot':
            cc.printBlue('Plot using pyplot')
            (figs,axes) = pf.getFigures()
#            sim.primalComplex.plotComplex(axes[0],showLabel=False)
#            sim.dualComplex.plotComplex(axes[1],showLabel=False)
#            sim.plotTransientT(figs[2])
            ax = pf.returnTo2D(figs[0])
            sim1.plotTimeStepT(ax,100,yZero=250)
            
            ax = pf.returnTo2D(figs[1])
            sim2.plotTimeStepT(ax,100,yZero=250)
            
            
            pf.exportPNG(figs[0],'Temp20')
            pf.exportPNG(figs[1],'Temp40')
            
            
        elif plottingMethod == 'VTK' :
            cc.printBlue('Plot using VTK')
            cc.printRed('Not implemented')

        elif plottingMethod == 'TikZ' :
            cc.printBlue('Plot using TikZ')            
            cc.printRed('Not implemented')
            
            
        elif plottingMethod == 'animation':
            cc.printBlue('Creating animation')
            (fig,ax,writer) = pf.getVideo(title = '1D Temp',aspect3D = False,fps=30)
            numSteps = len(sim2.timeVector)
            
            with writer.saving(fig,'animations/sim1DTempUT.mp4',120):
                for (i,now) in enumerate(sim1.timeVector):
                    print('Visualizing timestep {} of {}'.format(i+1,numSteps))
                    ax.clear()
                    sim1.plotTimeStepT(ax,i,yZero=250)
                    writer.grab_frame()

            
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))        
        
        
        
        

