# -*- coding: utf-8 -*-
#==============================================================================
# EDGE INIT
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue May 22 15:16:19 2018     



'''
The edge module is implemented under following requirements:
    
* Edges are represented by instances of the Edge class.
* For each edge, there is a reverse edge.
* The reverse edge is an object by itself.
* Any changes to the edge or the reverse edge affect both of them.
* Several methods (like plotting etc.) shoul only be implemented once.

Due to these requirements it is necessary to use a certain data structure shown
below.

.. todo:: Draw this structure!!!

'''

if __name__== '__main__':
    import os
    os.chdir('../../')


# Simple
from kCells.edge.baseSimpleEdge import BaseSimpleEdge
from kCells.edge.simpleEdge import SimpleEdge
from kCells.edge.reversedSimpleEdge import ReversedSimpleEdge


# Primal
from kCells.edge.baseEdge import BaseEdge
from kCells.edge.edge import Edge
from kCells.edge.reversedEdge import ReversedEdge
    
# Dual
from kCells.edge.dualEdge1D import DualEdge1D
from kCells.edge.dualEdge2D import DualEdge2D
from kCells.edge.dualEdge3D import DualEdge3D

