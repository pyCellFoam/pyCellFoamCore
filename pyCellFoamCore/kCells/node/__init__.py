# -*- coding: utf-8 -*-

#==============================================================================
# NODE INIT FILE
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

# Primal
from kCells.node.node import Node

# Dual
from kCells.node.dualNode0D import DualNode0D
from kCells.node.dualNode1D import DualNode1D
from kCells.node.dualNode2D import DualNode2D
from kCells.node.dualNode3D import DualNode3D