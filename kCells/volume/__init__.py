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

if __name__ == '__main__':
    import os
    os.chdir('../../')

# Primal
from kCells.volume.volume import Volume

# Dual
from kCells.volume.dualVolume3D import DualVolume3D