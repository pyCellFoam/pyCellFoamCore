# -*- coding: utf-8 -*-
#==============================================================================
# TITLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu May 28 16:47:23 2020

r'''

===============================================================================
What does this library provide?
===============================================================================  

.. todo ::
    
    picture of dual grids

This library provides a framework to run simulations based on dual grids, it is
especially intended to be used with the cell method.

.. todo::
    
    Cite cell method here.

1.  Define a primal grid.
2.  Automatically construct a dual grid.

===============================================================================
What's the difference to existing code
===============================================================================  


The main extenstion to the most existing simulation libraries is the extension
to non-uniform primal grids, where the boundary of each :math:`n`-cell can have 
an arbitrary number of :math:`(n-1)`-cells.


.. todo ::
    
    picture of a complicated 3-cell


'''


#*******************************************************************************
#Level 2
#*******************************************************************************  
#
#Level 3
#===============================================================================
#
#Level 4
#-------------------------------------------------------------------------------
#
#Level 5
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
#Level 6
#"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

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



if __name__ == '__main__':
    
    with MyLogging('Template'):
        
#==============================================================================
#    SECTION
#==============================================================================
        
        
        
        
#==============================================================================
#    SECTION
#==============================================================================
        
        
        

#-------------------------------------------------------------------------
#    Subsection
#-------------------------------------------------------------------------
       
        
        
        
#-------------------------------------------------------------------------
#    Subsection
#-------------------------------------------------------------------------
    

        
        
        

#-------------------------------------------------------------------------
#    Plotting
#-------------------------------------------------------------------------    
    
        # Choose plotting method. Possible choices: pyplot, VTK, TikZ, animation, doc, None
        plottingMethod = 'None'   
        
        
#    Disabled
#--------------------------------------------------------------------- 
        if plottingMethod is None or plottingMethod == 'None':
            cc.printBlue('Plotting disabled')
        
#    Pyplot
#---------------------------------------------------------------------         
        elif plottingMethod == 'pyplot':
            cc.printBlue('Plot using pyplot')
            (figs,axes) = pf.getFigures()
            cc.printRed('Not implemented')

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
            test.plotDoc()
            
#    Unknown
#---------------------------------------------------------------------             
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))        
        
    

