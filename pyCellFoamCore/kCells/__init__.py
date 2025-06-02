# -*- coding: utf-8 -*-

#==============================================================================
# KCELLS INIT FILE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue May 22 15:16:19 2018

'''
Import all files


'''

#if __name__ == '__main__':
#    import os
#    os.chdir('../')
#
#
#==============================================================================
#    CELL
#==============================================================================

# Super
from kCells.cell.superBaseCell import SuperBaseCell    
from kCells.cell.superCell import SuperCell  
from kCells.cell.superReversedCell import SuperReversedCell 

# Simple
from kCells.cell.baseSimpleCell import BaseSimpleCell
from kCells.cell.simpleCell import SimpleCell
from kCells.cell.reversedSimpleCell import ReversedSimpleCell

# Primal
from kCells.cell.baseCell import BaseCell
from kCells.cell.cell import Cell
from kCells.cell.reversedCell import ReversedCell

# Dual
from kCells.cell.dualCell import DualCell



#==============================================================================
#    NODE
#==============================================================================

# Primal
from kCells.node.node import Node

# Dual
from kCells.node import DualNode0D
from kCells.node import DualNode1D
from kCells.node import DualNode2D
from kCells.node import DualNode3D



#==============================================================================
#    EDGE
#==============================================================================

# Simple
from kCells.edge import BaseSimpleEdge
from kCells.edge import SimpleEdge
from kCells.edge import ReversedSimpleEdge


# Primal
from kCells.edge import BaseEdge
from kCells.edge import Edge
from kCells.edge import ReversedEdge
    
# Dual
from kCells.edge import DualEdge1D
from kCells.edge import DualEdge2D
from kCells.edge import DualEdge3D



#==============================================================================
#    FACE
#==============================================================================

# Simple
from kCells.face import BaseSimpleFace
from kCells.face import SimpleFace
from kCells.face import ReversedSimpleFace
    
# Primal
from kCells.face import BaseFace
from kCells.face import Face
from kCells.face import ReversedFace
    
# Dual
from kCells.face import DualFace2D
from kCells.face import DualFace3D



#==============================================================================
#    VOLUME
#==============================================================================

# # Primal
# from kCells.volume import Volume

# # Dual
# from kCells.volume import DualVolume3D