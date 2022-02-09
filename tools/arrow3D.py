# -*- coding: utf-8 -*-
#==============================================================================
# TITLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Dec  8 09:41:03 2017

'''
Source: https://stackoverflow.com/questions/27134567/3d-vectors-in-python

This class is a child  of  FancyArrowPatch from matplotlib.patches
https://matplotlib.org/devdocs/api/_as_gen/matplotlib.patches.Patch.html


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
from matplotlib import pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d




class Arrow3D(FancyArrowPatch):
    '''
    Bla
    
    '''
    
    def __init__(self, v1, v2, *args, **kwargs):
        '''
        :param numpy.ndarray v1: Start vector of the arrow
        :param numpy.ndarray v2: End vector of the arrow
        
        '''
        xs,ys,zs = [v1[0], v2[0]], [v1[1], v2[1]],[v1[2], v2[2]]
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        '''
        
        '''
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)
        
    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))

        return np.min(zs)        



if __name__ == '__main__':
    plt.close("all") 
    
    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111, projection='3d')
    v1 = np.array([0,0,0])
    v2 = np.array([0,0,3])
    
    w1 = np.array([1,0,0])
    w2 = np.array([1,2,3])
    xs,ys,zs = [v1[0], v2[0]], [v1[1], v2[1]],[v1[2], v2[2]]
    
    a = Arrow3D(v1, v2, mutation_scale=20,  lw=3, arrowstyle="-|>", color="r")
    b = Arrow3D(w1, w2, mutation_scale=20,  lw=3, arrowstyle="fancy", color="b")
    ax.add_artist(a)
    ax.add_artist(b)
    ax.set_xlabel('x_values')
    ax.set_ylabel('y_values')
    ax.set_zlabel('z_values')
    
    plt.title('3D Arrows')
    
    plt.draw()  
    plt.show()