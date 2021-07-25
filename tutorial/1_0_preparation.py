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


Working directory
-------------------------------------------------------------------------------  

You have to make sure that python can import all classes of the library.
Best practice is to collect all your simulations in a personal folder and at
the beginning of each file change your working directory to the top level 
folder. This is done by

.. code-block:: python

    import os
    if __name__ == '__main__':
        os.chdir('../')
        
Documentation
------------------------------------------------------------------------------- 

This documentation is created with the use of sphinx. You can add your own
files to this documentation. 

To prevent your code from being executed during the compilation process of the
documentation, make sure that your implementations are always masked by the 
following if-clause:

.. code-block:: python

    if __name__ == '__main__':
        pass
        # your code goes here
        
        
        





Logging
-------------------------------------------------------------------------------  

The logging module is used to create a log of the computations. In the tools,
a logger with two streams (one for the console and on for a file output) is 
prepared. To use it, first import the module:

.. code-block:: python 

    import tools.myLogging as mylog
    
    
then secondly use the following decorator:
   
.. code-block:: python    
    
    with mylog.MyLogging('filename_of_the_log',debug=True):
        

        
and thirdly you can use it to write your own logging messages:
    
.. code-block:: python    
    
    
    logger = mylog.getLogger('MyLogger')
    
    logger.debug('Test debug message')
    logger.info('Test info message')
    logger.warning('Test warning mesage')
    logger.error('Test error message')
    

Colored Printing
-------------------------------------------------------------------------------

Although logging is the preferable way to print messages to the console, it 
sometimes comes in handy to use the standard print function. However, this
function is very limited when it comes to the possible colors. Therefor, you 
find some tools to print in different colors. First, you need to import the 
functions:
    
.. code-block:: python

    import tools.colorConsole as cc
    
Then, you can use different predefined colors, e.g.

.. code-block:: python    

    cc.printRed('Red text')
    cc.printGreen('Green text')
    cc.printBlue('Blue text')
    
    cc.printRedBackground('Text with red background')
    cc.printGreenBackground('Text with green background')
    cc.printBlueBackground('Text with blue background')
    

Pyplot 
-------------------------------------------------------------------------------

You will typically need quite a number of pyplot axis, that usually pop up
somewhere on your screen so that the overlap. Another tool is provided to 
distribute them without overlapping. This tool also needs to be imported:

.. code-block:: python  
    
    import tools.placeFigures as pf
    
Now you can generate the desired number of figures:

.. code-block:: python     
    
    (figs,axes) = pf.getFigures(numTotal=4)    
    


Minimal Example
-------------------------------------------------------------------------------

A minimal working example could look like that:

.. code-block:: python

    #==============================================================================
    # IMPORTS
    #==============================================================================
    import os
    if __name__ == '__main__':
        os.chdir('../')
    import tools.myLogging as mylog  
    import tools.colorConsole as cc
    import tools.placeFigures as pf
    
    
    
    #==============================================================================
    # MY CODE
    #==============================================================================  
    
    if __name__ == '__main__':
        with mylog.MyLogging('MWE',debug=False):
            cc.printBlue('Prepare the plots')
            (figs,axes) = pf.getFigures(numTotal=4)    






Local Configuration 
-------------------------------------------------------------------------------

If you executed the lines from the previous example, you should have gotten a 
message that the local configuration file could not be found.
In the local configuration file, the area on which the pyplot figures are 
spread, is defined. To get rid of this message (and configure your output for 
example in a way that the figures are created on a second screen), create a 
file with the name ``localConfig.py`` in the parent folder this repository.
This file should contain the following four variables:
    
.. code-block:: python   

    pyplotWindowSize = (1920,1000)
    pyplotTopLeftCorner = (2560,380)
    
    vtkWindowSize = (2520,1350)
    vtkTopLeftCorner = (0,0)
    
the first two lines are used for the pyplot figures, the last two lines for a 
visualization with the "visualization toolkit", which we will see later.


Template 
-------------------------------------------------------------------------------

All of the above is already prepared in a template which you can use to write
your own classes or scripts.





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
import tools.myLogging as mylog


if __name__ == '__main__':

#==============================================================================
#    LOGGER
#==============================================================================
    
    with mylog.MyLogging('1_0_preparation',debug=True):
        
        logger = mylog.getLogger('MyLogger')
        
        logger.debug('Test debug message')
        logger.info('Test info message')
        logger.warning('Test warning mesage')
        logger.error('Test error message')
        
        
        
        
        
#==============================================================================
#    PRINT
#==============================================================================
        
        cc.printRed('Red text')
        cc.printGreen('Green text')
        cc.printBlue('Blue text')
        
        cc.printRedBackground('Text with red background')
        cc.printGreenBackground('Text with green background')
        cc.printBlueBackground('Text with blue background')
        
        
        
        

#==============================================================================
#    Plotting
#==============================================================================   
    
        # Choose plotting method. Possible choices: pyplot, None
        plottingMethod = 'pyplot'   
        
        
#    Disabled
#--------------------------------------------------------------------- 
        if plottingMethod is None or plottingMethod == 'None':
            cc.printBlue('Plotting disabled')
        
#    Pyplot
#---------------------------------------------------------------------         
        elif plottingMethod == 'pyplot':
            cc.printBlue('Plot using pyplot')
            (figs,axes) = pf.getFigures(numTotal=4)
            cc.printRed('Not implemented')

#    Unknown
#---------------------------------------------------------------------             
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))        
        
    

