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

Create New Nodes
------------------------------------------------------------------------------- 

Let us start constructing our complex with the 0-cells, or nodes. The minimal
input variables are the :math:`x`-, :math:`y`- and :math:`z`-coordinates of the
node:

.. code-block:: python

    n0 = Node(1,2,3)
    
Nodes are numbered automatically in the order that they were created (starting
with 0), and are (of course) independent from the numbers used in the variable 
name. If you want to use other numbering, you can give it as an optional 
argument:

.. code-block:: python

    nWithArbitraryNumber = Node(1,2,3,num=25)
    

It is recommended to put all created nodes into a list to make further handling
easier:
    
.. code-block:: python

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
        
        
        




Plot Nodes
-------------------------------------------------------------------------------   

Several plotting methods are implemented which we will go through in this
section.


Plot Nodes with Pyplot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For a small number of nodes and a quick result, pyplot is very useful. After
creating the pyplot figure, we can just use the implemented plot function of 
the node:
 
.. code-block:: python
    
    (figs,axes) = pf.getFigures(numTotal=1)
    for n in nodes:
        n.plotNode(axes[0])


Plot Nodes with VTK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For a larger number of nodes, the visualization toolkit gives a nice speed 
boost. Some functions have also been prepared in the tools folder, which need
to be imported
  
.. code-block:: python
    
    from tools import MyVTK
    
and can then be used.
    
.. code-block:: python
    
    myVTK = MyVTK()
    for n in nodes:
        n.plotNodeVtk(myVTK)
    myVTK.start()
    
    
Note, that the vtk environment must be created before plotting nodes in it and
it must be started manually. Plot commands that appear after the start command
will not be included in the vtk window.
    


Plot Nodes with TikZ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A tikz export is also available, which comes in handy, when it should be used
in a latex document.
Again, a tool collects the most basic operations and must be imported:

.. code-block:: python
    
    from tools.tikZPicture import TikZPicture3D
    
Similar to the vtk plotting, a tikzpicture must be created before the nodes are
plotted and needs to be compiled afterwards.

.. code-block:: python

    tikzpic = TikZPicture3D(name='1_1_nodes',scale=5)
    for n in nodes:
        n.plotNodeTikZ(tikzpic)
        
    tikzpic.writeLaTeXFile(compileFile=True,openFile=True)

    






FULL WORKING EXAMPLE
-------------------------------------------------------------------------------   

The following example covers all shown methods:
    
.. code-block:: python    

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
    #    Local Libraries
    #-------------------------------------------------------------------------
    
    
    #    kCells
    #--------------------------------------------------------------------
    from kCells import Node
    
    
    #    Tools
    #--------------------------------------------------------------------
    import tools.colorConsole as cc
    import tools.placeFigures as pf
    from tools import MyLogging
    from tools import MyVTK
    from tools.tikZPicture import TikZPicture3D


    if __name__ == '__main__':
        with MyLogging('1_1_nodes'):
            
    
      
            
    #==============================================================================
    #    NODES
    #==============================================================================
    
            
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
            
     
            
    
    #==============================================================================
    #    PLOTTING
    #==============================================================================
        
            # Choose plotting method. Possible choices: pyplot, VTK, TikZ,  None
            plottingMethod = 'pyplot'   
            
            
    #    Disabled
    #--------------------------------------------------------------------- 
            if plottingMethod is None or plottingMethod == 'None':
                cc.printBlue('Plotting disabled')
            
    #    Pyplot
    #---------------------------------------------------------------------         
            elif plottingMethod == 'pyplot':
                cc.printBlue('Plot using pyplot')
                (figs,axes) = pf.getFigures(numTotal=1)
                for n in nodes:
                    n.plotNode(axes[0])
    
    #    VTK
    #--------------------------------------------------------------------- 
            elif plottingMethod == 'VTK' :
                cc.printBlue('Plot using VTK')
                myVTK = MyVTK()
                for n in nodes:
                    n.plotNodeVtk(myVTK)
                myVTK.start()
                
    
    #    TikZ
    #--------------------------------------------------------------------- 
            elif plottingMethod == 'TikZ' :
                cc.printBlue('Plot using TikZ')      
                tikzpic = TikZPicture3D(name='1_1_nodes',scale=5)
                for n in nodes:
                    n.plotNodeTikZ(tikzpic)
                    
                tikzpic.writeLaTeXFile(compileFile=True,openFile=True)
                    
    #    Unknown
    #---------------------------------------------------------------------             
            else:
                cc.printRed('Unknown plotting method {}'.format(plottingMethod))        



The result resulting plot with pyplot should look like that:
    
.. image:: ../../_static/tutorial/1_1_nodes.png
   :width: 400px
   :alt: alternate text
   :align: center




Level 4
-------------------------------------------------------------------------------

Level 5
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Level 6
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""




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



#    kCells
#--------------------------------------------------------------------
from kCells import Node


#    Complex & Grids
#--------------------------------------------------------------------


#    Tools
#--------------------------------------------------------------------
import tools.colorConsole as cc
import tools.placeFigures as pf
from tools import MyLogging
# from tools import MyVTK
from tools.tikZPicture import TikZPicture3D






#==============================================================================
#    PLOTS FOR DOCUMENTATION
#==============================================================================

def plotDoc():
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
    
    (figs,axes) = pf.getFigures(numTotal=1)
    for n in nodes:
        n.plotNode(axes[0])
        
        
    pf.exportPNG(figs[0],'doc/_static/tutorial/1_1_nodes.png')
        
    
        




#==============================================================================
#    TEST CODE FOR TUTORIAL
#==============================================================================


if __name__ == '__main__':
    with MyLogging('1_1_nodes'):
        

  
        
#==============================================================================
#    NODES
#==============================================================================

        
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
        
 
        

#==============================================================================
#    PLOTTING
#==============================================================================
    
        # Choose plotting method. Possible choices: pyplot, VTK, TikZ,  None
        plottingMethod = 'doc'   
        
        
#    Disabled
#--------------------------------------------------------------------- 
        if plottingMethod is None or plottingMethod == 'None':
            cc.printBlue('Plotting disabled')
        
#    Pyplot
#---------------------------------------------------------------------         
        elif plottingMethod == 'pyplot':
            cc.printBlue('Plot using pyplot')
            (figs,axes) = pf.getFigures(numTotal=1)
            for n in nodes:
                n.plotNode(axes[0])

#    VTK
#--------------------------------------------------------------------- 
        elif plottingMethod == 'VTK' :
            cc.printBlue('Plot using VTK')
            myVTK = MyVTK()
            for n in nodes:
                n.plotNodeVtk(myVTK)
            myVTK.start()
            

#    TikZ
#--------------------------------------------------------------------- 
        elif plottingMethod == 'TikZ' :
            cc.printBlue('Plot using TikZ')      
            tikzpic = TikZPicture3D(name='1_1_nodes',scale=5)
            for n in nodes:
                n.plotNodeTikZ(tikzpic)
                
            tikzpic.writeLaTeXFile(compileFile=True,openFile=True)
                
            
#    Documentation
#--------------------------------------------------------------------- 
        elif plottingMethod == 'doc':
            cc.printBlue('Creating plots for documentation')
            plotDoc()
            
#    Unknown
#---------------------------------------------------------------------             
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))        
        
    

