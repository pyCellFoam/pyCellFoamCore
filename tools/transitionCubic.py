# -*- coding: utf-8 -*-
#==============================================================================
# TITLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue May 12 13:14:21 2020

r'''
In this class a transition from one value :math:`v_0` to anther value :math:`v_1`
during the time interval :math:`[t_0,t_1]` is implemented.

The transition between these two values is done with a cubic spline

.. math::
    v(t) = 
    \begin{cases}
        v_0, & \text{if } t < t_0 \\
        v_1, & \text{if } t > t_1 \\
        a_0 + a_1 t + a_2 t^2 + a_3 t^3, & \text{else}.
    \end{cases}

With the example values 

.. math::
    
    t_0 &= 3 \\
    v_0 &= 3 \\
    t_1 &= 12 \\
    v_1 &= 5
    
the resulting transtion is given in the following graph:

.. image:: ../../../_static/transitionCubic.png
       :width: 90%
       :alt: Cubic transition from value 1 to value 2
       :align: center  

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
import tools.colorConsole as cc
import tools.placeFigures as pf
from tools import MyLogging


#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class TransitionCubic:
    '''
    This is the explanation of this class.
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__a',
                 '__time0',
                 '__time1')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,time0,time1,value0,value1):
        '''
        Set the transition with the following parameters:        
        
        :param time0: Start time of transition
        :param time1: End time of transition
        :param value0: Value before start time
        :param value1: Value after end time
        
        '''
        self.__time0 = time0
        self.__time1 = time1
        
        M = np.array([[1, time0, time0**2, time0**3  ],
                      [1, time1, time1**2, time1**3  ],
                      [0, 1,     2*time0,  3*time0**2],
                      [0, 1,     2*time1,  3*time1**2]])
    
        v = np.array([value0,value1,0,0])
        
        self.__a = np.linalg.solve(M,v)
        
        
        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getA(self): return self.__a
    a = property(__getA)
    '''
    Vector of all parameters of the cubic spline.
    
    '''
    
    def __getA0(self): return self.__a[0]
    a0 = property(__getA0)
    '''
    Parameter :math:`a_0` of the cubic spline.
    
    '''
    
    def __getA1(self): return self.__a[1]
    a1 = property(__getA1)
    '''
    Parameter :math:`a_1` of the cubic spline.
    
    '''
    
    def __getA2(self): return self.__a[2]
    a2 = property(__getA2)
    '''
    Parameter :math:`a_2` of the cubic spline.
    
    '''
    
    def __getA3(self): return self.__a[3]
    a3 = property(__getA3)
    '''
    Parameter :math:`a_3` of the cubic spline.
    
    '''
    
    def __getTime0(self): return self.__time0
    time0 = property(__getTime0)
    '''
    Start time of the transition.
    
    '''

    def __getTime1(self): return self.__time1
    time1 = property(__getTime1)
    '''
    End time of the transition.
    
    '''



    
#==============================================================================
#    METHODS
#==============================================================================
    
#-------------------------------------------------------------------------
#    Get Value at Given t
#-------------------------------------------------------------------------
    def getValue(self,t):
        '''
        Get a value of the transition.
        
        :param t: time
        
        '''
        if t < self.time0:
            t = self.time0
        if t > self.time1:
            t = self.time1
        
        return self.a0 + self.a1*t + self.a2*t**2 + self.a3*t**3

#-------------------------------------------------------------------------
#    Plot for Documentation
#-------------------------------------------------------------------------         
    @classmethod
    def plotDoc(cls):    
        trans = TransitionCubic(3,12,3,5)
        
        t = np.arange(0,15,0.1)
        v = np.zeros(t.shape)
        
        for i in range(len(v)):
            v[i] = trans.getValue(t[i])
            
        (figs,axes) = pf.getFigures(numTotal=1,aspect3D=False)
        
        ax = axes[0]
        ax.plot(t,v)        
        
        ax.set_xlabel('t')
        ax.set_ylabel('value')
        
        pf.exportPNG(figs[0],'doc/_static/transitionCubic')
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    
    with MyLogging('TranistionCubic'):

#-------------------------------------------------------------------------
#    Create some examples
#-------------------------------------------------------------------------
        
        
        trans = TransitionCubic(3,12,3,5)
        
        t = np.arange(0,15,0.1)
        v = np.zeros(t.shape)
        
        for i in range(len(v)):
            v[i] = trans.getValue(t[i])
            
            
        
    


#-------------------------------------------------------------------------
#    Plotting
#-------------------------------------------------------------------------    
    
        # Choose plotting method. Possible choices: pyplot, VTK, TikZ, animation, doc, None
        plottingMethod = 'doc'   
        
        
#    Disabled
#--------------------------------------------------------------------- 
        if plottingMethod is None or plottingMethod == 'None':
            cc.printBlue('Plotting disabled')
        
#    Pyplot
#---------------------------------------------------------------------         
        elif plottingMethod == 'pyplot':
            cc.printBlue('Plot using pyplot')
            (figs,axes) = pf.getFigures(aspect3D=False)
            
            ax = axes[0]
            ax.plot(t,v)

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
            TransitionCubic.plotDoc()
            
#    Unknown
#---------------------------------------------------------------------             
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))        
        
    

