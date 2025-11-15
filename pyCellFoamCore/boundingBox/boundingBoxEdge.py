# -*- coding: utf-8 -*-
#==============================================================================
# BOUNDING BOX EDGE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Mon Feb 24 11:25:58 2020

'''

'''
#==============================================================================
#    IMPORTS
#==============================================================================
import os
if __name__ == '__main__':
    os.chdir('../')

import logging

import numpy as np

from pyCellFoamCore.boundingBox.boundingBoxElement import BoundingBoxElement
from pyCellFoamCore.boundingBox.boundingBoxCorner import BoundingBoxCorner
import pyCellFoamCore.tools.tumcolor as tc
from pyCellFoamCore.tools import set_logging_format


#==============================================================================
#    LOGGING
#==============================================================================
_log = logging.getLogger(__name__)

#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class BoundingBoxEdge(BoundingBoxElement):
    '''

    '''

#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__corner1',
                 '__corner2')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,corner1,corner2,*args,**kwargs):
        '''
        :param BoundingBoxCorner corner1: First point of the edge
        :param BoundingBoxCorner corner2: Second point of the edge
        :param str identifier: A name for the edge

        '''
        super().__init__(*args,**kwargs,loggerName = 'bbEdge')
        testCoords = list(corner1.coordinates == corner2.coordinates)
        if testCoords.count(False) != 1:
            _log.error('Two corners must differ in exactly one coordinate')
            self.__corner1 = None
            self.__corner2 = None
        else:
            self.__corner1 = corner1
            self.__corner2 = corner2
        _log.info('Created BoundingBoxEdge')



#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getCorner1(self): return self.__corner1
    corner1 = property(__getCorner1)
    '''

    '''

    def __getCorner2(self): return self.__corner2
    corner2 = property(__getCorner2)
    '''

    '''

    def __getCorners(self): return [self.__corner1, self.__corner2]
    corners = property(__getCorners)
    '''

    '''


    def __getCoordinates(self): return np.vstack((self.corner1.coordinates,self.corner2.coordinates))
    coordinates = property(__getCoordinates)
    '''

    '''

    def __getDirectionVec(self):
        v = self.corner2.coordinates - self.corner1.coordinates
        return np.abs(v)/np.linalg.norm(v)
    directionVec = property(__getDirectionVec)
    '''

    '''

    def __getCenter(self): return (self.corner1.coordinates + self.corner2.coordinates)/2
    center = property(__getCenter)
    '''

    '''


#==============================================================================
#    MAGIC METHODS
#==============================================================================

    def  __repr__(self):
        '''
        Show info_text in console

        '''
        return 'BBEdge<{}>'.format(self.identifier)

#==============================================================================
#    METHODS
#==============================================================================

#-------------------------------------------------------------------------
#    Print Bounding Box Edge
#-------------------------------------------------------------------------
    def printBoundingBoxEdge(self):
        '''

        '''
        print('bbEdge "{}" between corners "{}" and "{}"'.format(self.identifier,self.corner1,self.corner2))



#-------------------------------------------------------------------------
#    Plot Bounding Box Edge with Matplotlib
#-------------------------------------------------------------------------
    def plotBoundingBoxEdge(self,ax,showLabel=False,color=tc.TUMBlack()):
        '''

        '''
        ax.plot(self.coordinates[:,0],self.coordinates[:,1],self.coordinates[:,2],color=color.html)
        if showLabel:
            center = (self.corner1.coordinates+self.corner2.coordinates)/2
            ax.text(center[0],center[1],center[2],self.identifier)

#-------------------------------------------------------------------------
#    Plot Bounding Box Edge with Visualization Toolkit
#-------------------------------------------------------------------------
    def plotBoundingBoxEdgeVtk(self,myVtk,showLabel=True):
        '''

        '''
        myVtk.addLine(self.corner1.coordinates,self.corner2.coordinates)
        if showLabel:
            myVtk.addTextAnnotationNumpy((self.corner1.coordinates+self.corner2.coordinates)/2,self.identifier)

#-------------------------------------------------------------------------
#    Plot Bounding Box Edge with Visualization Toolkit
#-------------------------------------------------------------------------
    def plotBoundingBoxEdgeTikZ(self,pic):
        '''

        '''
        pic.addTikZLine(self.corner1.getTikZCoordinate(pic),self.corner2.getTikZCoordinate(pic))



#-------------------------------------------------------------------------
#    Calculate Distance Between Bounding Box Edge and some Coordinates
#-------------------------------------------------------------------------
    def distToBoundingBoxEdge(self,coordinates):
        '''

        '''
        projVec = np.ones(3) - self.directionVec
        projMat = np.diag(projVec)
        return np.linalg.norm(projMat @ (self.center - coordinates))

    def get_intermediate_point(self, point1, point2):
        '''
        Get intermediate point on the edge between two given points.

        :param np.array point1: First point
        :param np.array point2: Second point
        :return: Intermediate point on the edge
        :rtype: np.array
        '''
        edge_vec = self.corner2.coordinates - self.corner1.coordinates
        edge_length = np.linalg.norm(edge_vec)
        edge_dir = edge_vec / edge_length

        vec1 = point1 - self.corner1.coordinates
        vec2 = point2 - self.corner1.coordinates

        proj1 = np.dot(vec1, edge_dir)
        proj2 = np.dot(vec2, edge_dir)

        t = (proj1 + proj2) / (2 * edge_length)
        t = np.clip(t, 0, 1)

        intermediate_point = self.corner1.coordinates + t * edge_vec
        return intermediate_point


#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    set_logging_format(logging.DEBUG)

    corner3D1 = BoundingBoxCorner(np.array([0,1,0]),'LeftTopBack')
    corner3D2 = BoundingBoxCorner(np.array([1,1,0]),'RightTopBack')
    edge3D = BoundingBoxEdge(corner3D1,corner3D2,'TopBack')

    testCoordinate1 = np.array([1.2,1.3,1.4])
    testCoordinate2 = np.array([0.8,1.3,0.4])

    intermediate_point = edge3D.get_intermediate_point(testCoordinate1, testCoordinate2)
    print("Intermediate Point:", intermediate_point)

    # from tools import MyLogging
    # import tools.colorConsole as cc
    # from tools.myVTK import MyVTK
    # with MyLogging('BoundingBoxEdge',debug=True):

    #     cc.printBlueBackground(' '*20,'2D',' '*20)
    #     cc.printBlue('Create bbCorner left top')
    #     corner2D1 = BoundingBoxCorner(np.array([0,1]),'LeftTop')
    #     cc.printBlue('Create bbCorner right top')
    #     corner2D2 = BoundingBoxCorner(np.array([1,1]),'RightTop')
    #     cc.printBlue('Create top edge')
    #     edge2D = BoundingBoxEdge(corner2D1,corner2D2,'Top')
    #     cc.printBlue('Check result')
    #     print(edge2D)
    #     edge2D.printBoundingBoxEdge()


    #     cc.printBlueBackground(' '*20,'3D',' '*20)
    #     cc.printBlue('Create bbCorner left top back')
    #     corner3D1 = BoundingBoxCorner(np.array([0,1,0]),'LeftTopBack')
    #     cc.printBlue('Create bbCorner top right')
    #     corner3D2 = BoundingBoxCorner(np.array([1,1,0]),'RightTopBack')
    #     cc.printBlue('Create top back edge')
    #     edge3D = BoundingBoxEdge(corner3D1,corner3D2,'TopBack')
    #     cc.printBlue('Check result')
    #     print(edge3D)
    #     edge3D.printBoundingBoxEdge()

    #     testCoordinate1 = np.array([1.2,1.3,1.4])

    #     print(edge3D.distToBoundingBoxEdge(testCoordinate1))

    #     if False:
    #         myVtk = MyVTK(polygonOpacity=1)
    #         edge3D.plotBoundingBoxEdgeVtk(myVtk,showLabel=False)
    #         myVtk.start()

    #     else:
    #         import tools.placeFigures as pf
    #         (figs,axes) = pf.getFigures()
    #         edge3D.plotBoundingBoxEdge(axes[0],showLabel=True)
    #         ax = axes[0]
    #         ax.scatter(testCoordinate1[0],testCoordinate1[1],testCoordinate1[2])
