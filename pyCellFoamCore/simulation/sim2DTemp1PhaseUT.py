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
Simulate temperature on a solid plate of length :math:`l` and width :math:`w`
with constant height :math:`h`. 
The heat capacity :math:`c_\mathrm{V}` and thermal conductivity :math:`\lambda`
are assumed to be constant on the plate.

Balance equations:
    
.. math::
    
    \begin{bmatrix}
        \frac{\partial}{\partial t} \Ui \\
        \mathbf{F_\mathrm{T}^\mathrm{i}}
    \end{bmatrix}
    &=
    \begin{bmatrix}
        0 & \mathbf{\hat{d}^2_\mathrm{ii}} \\
        \mathbf{d^1_\mathrm{ii}} & 0
    \end{bmatrix}
    \begin{bmatrix}
        \mathbf{T^\mathrm{i}} \\
        \mathbf{J_\mathrm{Q}^\mathrm{i}}
    \end{bmatrix}
    +
    \begin{bmatrix}
        0 & \mathbf{\hat{d}^2_\mathrm{ib}} \\
        \mathbf{d^1_\mathrm{ib}} & 0
    \end{bmatrix}
    \begin{bmatrix}
        \mathbf{T^\mathrm{b}} \\
        \mathbf{J_\mathrm{Q}^\mathrm{b}}
    \end{bmatrix}

Constitutive laws:

.. math::
    
    \mathbf{U^\mathrm{i}} &= c_\mathrm{V} h \mathbf{\hat{A}^\mathrm{i}} \mathbf{T^\mathrm{i}}  \\
    \mathbf{J_\mathrm{Q}^\mathrm{i}} &= \lambda h \mathbf{\hat{L}^\mathrm{i}}  \left(\mathbf{L^\mathrm{i}}\right)^{-1} \mathbf{F_\mathrm{T}^\mathrm{i}}

        
with 

.. math::
    
    \mathbf{\hat{L}^\mathrm{i}} &= \mathrm{diag}(|\hat{e}_{\mathrm{i},j}|), \quad j = 1 ... |\mathcal{\hat{E}}_i| \\
    \mathbf{\hat{A}^\mathrm{i}} &= \mathrm{diag}(|\hat{f}_{\mathrm{i},j}|), \quad j = 1 ... |\mathcal{\hat{F}}_i| \\
    \mathbf{L^\mathrm{i}} &= \mathrm{diag}(|e_{\mathrm{i},j}|), \quad j = 1 ... |\mathcal{E}_i| \\
    \mathbf{\hat{d}^2_\mathrm{ii}} &= \left(\boldsymbol{\hat{\partial}^2_\mathrm{ii}}\right)^\mathrm{T}\\
    \mathbf{\hat{d}^2_\mathrm{ib}} &= \left(\boldsymbol{\hat{\partial}^2_\mathrm{bi}}\right)^\mathrm{T} \\
    \mathbf{d^1_\mathrm{ii}} &= \left(\boldsymbol{\partial^1_\mathrm{ii}} \right)^\mathrm{T} \\
    \mathbf{d^1_\mathrm{ib}} &= \left(\boldsymbol{\partial^1_\mathrm{bi}} \right)^\mathrm{T} \\
    
    
This time continuous equation is discretized and integrated with a forward 
Euler scheme. 
The snapshots

.. math::
    
    {_m}\Ui &= \Ui(t_m)\\
    {_m}\Ti &= \Ti(t_m)\\
    {_m}\FTi &= \FTi(t_m)\\
    {_m}\JQi &= \JQi(t_m)\\
    
are stored in matrices.

Note that for example

.. code-block:: python

    Ui[0]

returns all values at timestep 0, i.e. :math:`{_0}\Ui`. 
To get the transient for the co-chain on :math:`\fdij{0}`, i.e. :math:`\Uij{0}`, use

.. code-block:: python

    Ui[:,0]

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
from scipy import interpolate

#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------


#    kCells
#--------------------------------------------------------------------


#    Complex & Grids
#--------------------------------------------------------------------
from grids import Grid2DRectangular
from complex import DualComplex2D

#    Tools
#--------------------------------------------------------------------
from simulation.simulation import Simulation
from tools import MyLogging
import tools.placeFigures as pf
import tools.colorConsole as cc
import tools.tumcolor as tc
from tools.transitionCubic import TransitionCubic

#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class Sim2DTemp1PhaseUT(Simulation):
    '''
    This is the explanation of this class.
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__Ui',
                 '__Ui0',
                 '__Ji',
                 '__Jb',
                 '__Fi',
                 '__Ti',
                 '__Tb',
                 '__TbTop',
                 '__TbBottom',
                 '__h',
                 '__rho',
                 '__cV',
                 '__LiPrimal',
                 '__LiPrimalInv',                  
                 '__LiDual',                 
                 '__LiDualInv',
                 '__Ai',
                 '__AiInv',
                 '__lambda',
                 '__plotColor')
    

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,*,h=1,w=8,l=10,
                 TbTop=lambda x: 293,
                 TbBottom=lambda x: 273,
                 Ti0 = 273,
                 **kwargs):
        '''
        
        :param float h: Height of the plate
        :param float w: Width of the plate
        :param float l: Length of the plate
        
        '''
        self.__h = h
        
        self.__Ui = None
        self.__Ji = None
        self.__Fi = None
        self.__Ti = None
        
        self.__TbTop = TbTop
        self.__TbBottom = TbBottom

        
        self.__rho = 2700 # kg/m^3 for aluminium
        self.__rho /= 1E9 # change to mm^3
        self.__cV = 897. # J / (kg K) for aluminium        
        self.__lambda = 200 # W / (m K) for aluminium
        self.__lambda /= 1E3 # change to mm
        
        
        super().__init__(**kwargs)
        self.primalComplex = Grid2DRectangular(xNum=4,xLen=l,yLen=w,borderFacesLeft=True,borderFacesRight=True)
        self.dualComplex = DualComplex2D(self.primalComplex)
        
        self.primalComplex.useCategory = 2
        
        self.__Ai = np.diag([f.area[1] for f in self.dualComplex.innerFaces])
        self.__AiInv = np.diag([1/f.area[1] for f in self.dualComplex.innerFaces])
        self.__LiDual = np.diag([e.length[1] for e in self.dualComplex.innerEdges])
        self.__LiDualInv = np.diag([1/e.length[1] for e in self.dualComplex.innerEdges])
        self.__LiPrimal = np.diag([e.length[1] for e in self.primalComplex.innerEdges])
        self.__LiPrimalInv = np.diag([1/e.length[1] for e in self.primalComplex.innerEdges])        
        
        self.__Ui0 = self.__cV * self.__rho * self.__h * self.__Ai @ np.ones(len(self.dualComplex.innerFaces)) * Ti0
        
        
        self.__Jb = np.zeros((self.maxNumberOfTimeSteps+1,len(self.dualComplex.borderEdges)))
        self.__plotColor = tc.TUMBlue()
        
        
            
            
            
        
        
        
        
        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getUi(self): return self.__Ui
    Ui = property(__getUi)
    r'''
    Matrix containing :math:`\Ui(t)` for every calculated timestep.
    
    '''
    
    def __getJi(self): return self.__Ji
    r'''
    Matrix containing :math:`\JQi(t)` for every calculated timestep.
    
    '''
    
    def __getFi(self): return self.__Fi
    Fi = property(__getFi)
    r'''
    Matrix containing :math:`\FTi(t)` for every calculated timestep.
    
    '''
    
    
    def __getTi(self): return self.__Ti
    Ti = property(__getTi)    
    r'''
    Matrix containing :math:`\Ti(t)` for every calculated timestep.
    
    '''
    
    def __getTb(self): return self.__Tb
    Tb = property(__getTi)    
    
    r'''
    Matrix containing :math:`\Tb(t)` for every calculated timestep.
    
    '''   
    
    
    def __getT(self): return np.hstack((self.Ti,self.Tb))
    T = property(__getT)
    r'''
    Matrix containing :math:`\T(t)=\begin{bmatrix}\Ti(t)\\Tb(t)\end{bmatrix}` for every calculated timestep.
    
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
    
        
        self.__Ui = np.zeros((self.maxNumberOfTimeSteps+1,len(self.dualComplex.innerFaces)))
        self.__Ji = np.zeros((self.maxNumberOfTimeSteps+1,len(self.dualComplex.innerEdges)))
        self.__Fi = np.zeros((self.maxNumberOfTimeSteps+1,len(self.primalComplex.innerEdges)))
        self.__Ti = np.zeros((self.maxNumberOfTimeSteps+1,len(self.primalComplex.innerNodes)))
        self.__Tb = np.zeros((self.maxNumberOfTimeSteps+1,len(self.primalComplex.borderNodes)))
        
        
        TbTopAlloc = np.array([1 if x in self.primalComplex.boundaryNodesTop else 0 for x in self.primalComplex.borderNodes])
        TbBottomAlloc = np.array([1 if x in self.primalComplex.boundaryNodesBottom else 0 for x in self.primalComplex.borderNodes])
        
        if not np.allclose(TbTopAlloc+TbBottomAlloc,np.ones(len(self.primalComplex.borderNodes))):
            self.logger.error('The allocation does not cover all border Nodes')
        
        
        
        
        self.__Ui[0] = self.__Ui0
        
        
        currentNumberOfTimeStep = 0
        currentTime = self.startTime
        self.timeVector[0] = self.startTime
        currentTimeStep = self.initialTimeStep
        
        
        while currentNumberOfTimeStep < self.maxNumberOfTimeSteps and currentTime < self.endTime:
            
            

            UiNow = self.__Ui[currentNumberOfTimeStep]
            
            TiNow = 1/(self.__cV*self.__rho*self.__h) * self.__AiInv @ UiNow
            TbNow = self.__TbTop(currentTime) * TbTopAlloc + self.__TbBottom(currentTime)  * TbBottomAlloc
            
            FiNow = -self.primalComplex.incidenceMatrix1ii.transpose() @ TiNow  - self.primalComplex.incidenceMatrix1bi.transpose() @ TbNow
            JiNow =  self.__lambda * self.__h * self.__LiDual @ self.__LiPrimalInv @ FiNow
            
            UiDot = -self.dualComplex.incidenceMatrix2ii.transpose() @ JiNow  - self.dualComplex.incidenceMatrix2bi.transpose() @ self.__Jb[currentNumberOfTimeStep]
            
            
            
            
            
            # Save current timestep
            self.__Ji[currentNumberOfTimeStep] = JiNow
            self.__Fi[currentNumberOfTimeStep] = FiNow
            self.__Ti[currentNumberOfTimeStep] = TiNow
            self.__Tb[currentNumberOfTimeStep] = TbNow
            
            
            # Integrate new timestep
            
            
            
            
            currentNumberOfTimeStep += 1
            
            currentNumberOfStepLengthSearch = 0
            precisionOK = False
            if currentTimeStep < self.initialTimeStep * 5:
                currentTimeStep = currentTimeStep*2
            self.logger.info('Timestep {}'.format(currentNumberOfTimeStep))
            while currentNumberOfStepLengthSearch < 50 and not precisionOK:
                self.logger.info('Step length iteration {} with steplength {}'.format(currentNumberOfStepLengthSearch,currentTimeStep))
                UiNext1 = UiNow + UiDot * currentTimeStep
                UiNext2 = UiNow + UiDot * currentTimeStep * 2
                
                relErr = np.linalg.norm(((UiNext2-UiNext1)/UiNext1))
                
                if relErr < 1E-4:
                    precisionOK = True
                else:
                    currentTimeStep = currentTimeStep/2
                
                currentNumberOfStepLengthSearch += 1
                
                

                
                
            if currentNumberOfStepLengthSearch >= 50:
                self.logger.error('Could not find a suitable step length')
                currentNumberOfTimeStep = self.maxNumberOfTimeSteps
            
            
            currentTime += currentTimeStep
            self.timeVector[currentNumberOfTimeStep] = currentTime
            self.__Ui[currentNumberOfTimeStep] = UiNext1
            
            
            
            
        self.numberOfLastTimeStep = currentNumberOfTimeStep-1
    
    
    
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
        
        
    def plotTransientTLimit(self,ax,timePoints):
        '''
        
        '''
        T = interpolate.interp1d(self.timeVector,self.T.transpose())(timePoints)
        
        ax.plot(timePoints,T.transpose())      
        
        
        
    def plotTimePoint(self,ax,timePoint,valMin,valMax):
        '''
        
        '''
        
        colorMin = tc.TUMcolor([0,0,255],'blue')
        colorMax = tc.TUMcolor([255,0,0],'red')
        
        if timePoint > self.timeVector[-1]:
            self.logger.warning('Requested time point is above upper limit')
            timePoint = self.timeVector[-1]
                
                
                
        if timePoint < self.timeVector[0]:
            self.logger.warning('Requested time point is below lower limit')
            timePoint = self.timeVector[0]
            
        Ti = interpolate.interp1d(self.timeVector,self.Ti.transpose())(timePoint)
        Tb = interpolate.interp1d(self.timeVector,self.Tb.transpose())(timePoint)
        
        for (f,val) in zip(self.dualComplex.innerFaces,Ti):
            color = colorMin*(1-(val-valMin)/(valMax-valMin))+colorMax*((val-valMin)/(valMax-valMin))
            f.plotFace(ax,color=color,showLabel=False,showNormalVec=False,showBarycenter=False)
            
        for (f,val) in zip(self.dualComplex.borderFaces,Tb):
            color = colorMin*(1-(val-valMin)/(valMax-valMin))+colorMax*((val-valMin)/(valMax-valMin))
            f.plotFace(ax,color=color,showLabel=False,showNormalVec=False,showBarycenter=False)
            
            
        pf.setAxesEqual(ax)
        ax.set_xlim(self.dualComplex.xLim)
        ax.set_ylim(self.dualComplex.yLim)
        ax.view_init(90,-90)
        
        
        
        
        
        
        
        
        
        


#-------------------------------------------------------------------------
#    Cut Not Used Parts of the Matrices
#------------------------------------------------------------------------- 
    def cutVectors(self):
        '''
        Cut all matrices containing calculated vectors at last timestep.
        
        '''
        super().cutVectors()
        self.__Tb = self.cutVector(self.__Tb)
        self.__Ti = self.cutVector(self.__Ti)
        self.__Fi = self.cutVector(self.__Fi)
        self.__Ji = self.cutVector(self.__Ji)
        self.__Ui = self.cutVector(self.__Ui)
        
        
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    with MyLogging('Sim2DTempUT'):
        
        
        
        tran = TransitionCubic(3,10,273,292.5)
        
        

        
        sim = Sim2DTemp1PhaseUT(
                h = 10,
                w = 100,
                l = 100,
                endTime = 50,
                initialTimeStep = 0.1,
                TbTop=tran.getValue)
        
        

        
        
        

        
        sim.simulate()
        sim.cutVectors()
        
        
        # Choose plotting method. Possible choices: pyplot, VTK, TikZ, animation, None
        plottingMethod = 'pyplot'   
        
        if plottingMethod is None or plottingMethod == 'None':
            cc.printBlue('Plotting disabled')
        
        elif plottingMethod == 'pyplot':
            cc.printBlue('Plot using pyplot')
            (figs,axes) = pf.getFigures()
            sim.primalComplex.plotComplex(axes[0],showLabel=False)
            sim.dualComplex.plotComplex(axes[1],showLabel=True)
            sim.plotTransientT(figs[2])
            sim.plotTimePoint(axes[3],49,273,293)
            
            ax = pf.returnTo2D(figs[4])
            numAnimationSteps = 30
            animationTimeVector = np.arange(sim.timeVector[0],sim.timeVector[-1],(sim.timeVector[-1]-sim.timeVector[0])/numAnimationSteps)
            
            sim.plotTransientTLimit(ax,animationTimeVector[:10])
            ax.set_xlim([animationTimeVector[0],animationTimeVector[-1]])
            ax.set_ylim([273,293])
            
            
        elif plottingMethod == 'VTK' :
            cc.printBlue('Plot using VTK')
            cc.printRed('Not implemented')

        elif plottingMethod == 'TikZ' :
            cc.printBlue('Plot using TikZ')            
            cc.printRed('Not implemented')
            
            
        elif plottingMethod == 'animation':
            cc.printBlue('Creating animation')
            
            (fig,[ax1,ax2],writer) = pf.getVideo2(title = '2D Temp',fps=15)
            numAnimationSteps = 300
            animationTimeVector = np.arange(sim.timeVector[0],sim.timeVector[-1],(sim.timeVector[-1]-sim.timeVector[0])/numAnimationSteps)
            
            with writer.saving(fig,'simulations/sim2DTemp1PhaseUT.mp4',120):
                for (i,now) in enumerate(animationTimeVector):
                    print('Visualizing timestep {} of {}: t = {}'.format(i+1,numAnimationSteps,now))
                    
                    ax1.clear()
                    sim.plotTimePoint(ax1,now,273,293)
                    ax1.set_title('t = {:.2f}'.format(now))
                    
                    ax2.clear()
                    sim.plotTransientTLimit(ax2,animationTimeVector[:i+1])
                    ax2.set_xlim([animationTimeVector[0],animationTimeVector[-1]])
                    ax2.set_ylim([273,293])
                    
                    
                    writer.grab_frame()
                    
            
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))        
        
        
        
        

