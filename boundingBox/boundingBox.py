# -*- coding: utf-8 -*-
#==============================================================================
# BOUNDING BOX
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue Feb 25 13:17:36 2020

'''

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


#    Bounding Box
#--------------------------------------------------------------------
from boundingBox.boundingBoxElement import BoundingBoxElement
from boundingBox.boundingBoxCorner import BoundingBoxCorner
from boundingBox.boundingBoxEdge import BoundingBoxEdge
from boundingBox.boundingBoxSide import BoundingBoxSide



#    Tools
#--------------------------------------------------------------------
import tools.colorConsole as cc
import tools.placeFigures as pf
from tools import MyLogging
# from tools.myVTK import MyVTK
import tools.tumcolor as tc

#==============================================================================
#    IMPORTS
#==============================================================================

    



#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class BoundingBox(BoundingBoxElement):
    '''
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__xRange',
                 '__yRange',
                 '__zRange',
                 '__corners',
                 '__edges',
                 '__sides')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,xRange,yRange,zRange,preset=None,xMinName=None,xMaxName=None,yMinName=None,yMaxName=None,zMinName=None,zMaxName=None,**kwargs):
        '''
        :param list xRange: List with numbers: minimum and maximum value in x-direction
        :param list yRange: List with numbers: minimum and maximum value in y-direction
        :param list zRange: List with numbers: minimum and maximum value in z-direction
        :param str preset: Possible options are None,'vtk' or 'pyplot'
        :param str xMinName: String with the name of the side at min x value - do not use with preset
        :param str xMaxName: String with the name of the side at min x value - do not use with preset
        :param str yMinName: String with the name of the side at min x value - do not use with preset
        :param str yMaxName: String with the name of the side at min x value - do not use with preset
        :param str zMinName: String with the name of the side at min x value - do not use with preset
        :param str zMaxName: String with the name of the side at min x value - do not use with preset
        
        '''
        super().__init__(**kwargs,loggerName='boundingBox',identifier='BoundingBox')
        
        error = False
        for r in [xRange,yRange,zRange]:
            if type(r) is list:
                if len(r) == 2:
                    if r[1] <= r[0]:
                        self.logger.error('The second value of the range must be larger than the first, but {} is smaller than {}'.format(r[1],r[0]))
                else:
                    error = True
                    self.logger.error('range must be a list with length 2 but has length {}'.format(len(r)))
            else:
                error = True
                self.logger.error('range must be a list with 2 entries, but {} is given'.format(r))
        
        
        
        
        limitNames = [xMinName, xMaxName, yMinName, yMaxName, zMinName, zMaxName]
        
        
        if preset is None and all([n is None for n in limitNames]):
            self.logger.info('No preset and no limit names are given. Using standard preset "vtk"')
            preset = 'vtk'
        
        
        
        if not preset:
            if not all([type(n) is str for n in limitNames]):
                error = True
                self.logger.error('All names for limits must be strings')
                for n in limitNames:
                    if type(n) is str:
                        self.logger.info('{} is ok'.format(n))
                    else:
                        self.logger.error('{} is not ok'.format(n))
                
            
        
        elif preset in ['vtk','pyplot']:
            if not all([n is None for n in limitNames]):
                self.logger.warning('A preset and custom names for limits are given. The prest overwrites the given names.')
                
            if preset == 'vtk':
                xMinName='Left'
                xMaxName='Right'
                yMinName='Bottom'
                yMaxName='Top'
                zMinName='Back'
                zMaxName='Front'
            elif preset == 'pyplot':
                xMinName='Left'
                xMaxName='Right'
                yMinName='Front'
                yMaxName='Back'
                zMinName='Bottom'
                zMaxName='Top'
            
        else:
            error = True
            self.logger.error('Unknown preset "{}"'.format(preset))
          
            
            
        if error:
            self.__xRange = []
            self.__yRange = []
            self.__zRange = []
            self.__corners = []
            self.__edges = []
            self.__sides = []
            
            self.logger.error('An error occured, bounding box is not defined correctly')
        else:
            self.__xRange = xRange
            self.__yRange = yRange
            self.__zRange = zRange
            
            corner000 = BoundingBoxCorner(np.array([self.xMin,self.yMin,self.zMin]),xMinName+yMinName+zMinName)
            corner001 = BoundingBoxCorner(np.array([self.xMin,self.yMin,self.zMax]),xMinName+yMinName+zMaxName)
            corner010 = BoundingBoxCorner(np.array([self.xMin,self.yMax,self.zMin]),xMinName+yMaxName+zMinName)
            corner011 = BoundingBoxCorner(np.array([self.xMin,self.yMax,self.zMax]),xMinName+yMaxName+zMaxName)
            corner100 = BoundingBoxCorner(np.array([self.xMax,self.yMin,self.zMin]),xMaxName+yMinName+zMinName)
            corner101 = BoundingBoxCorner(np.array([self.xMax,self.yMin,self.zMax]),xMaxName+yMinName+zMaxName)
            corner110 = BoundingBoxCorner(np.array([self.xMax,self.yMax,self.zMin]),xMaxName+yMaxName+zMinName)
            corner111 = BoundingBoxCorner(np.array([self.xMax,self.yMax,self.zMax]),xMaxName+yMaxName+zMaxName)
            
            self.__corners = [corner000,corner001,corner010,corner011,corner100,corner101,corner110,corner111]
            
            edgeY0 = BoundingBoxEdge(corner000,corner010,xMinName+zMinName)
            edgeY1 = BoundingBoxEdge(corner001,corner011,xMinName+zMaxName)
            edgeY2 = BoundingBoxEdge(corner100,corner110,xMaxName+zMinName)
            edgeY3 = BoundingBoxEdge(corner101,corner111,xMaxName+zMaxName)
            
            edgeZ0 = BoundingBoxEdge(corner000,corner001,xMinName+yMinName)
            edgeZ1 = BoundingBoxEdge(corner010,corner011,xMinName+yMaxName)
            edgeZ2 = BoundingBoxEdge(corner100,corner101,xMaxName+yMinName)
            edgeZ3 = BoundingBoxEdge(corner110,corner111,xMaxName+yMaxName)
            
            
            
            edgeX0 = BoundingBoxEdge(corner000,corner100,yMinName+zMinName)
            edgeX1 = BoundingBoxEdge(corner001,corner101,yMinName+zMaxName)
            edgeX2 = BoundingBoxEdge(corner010,corner110,yMaxName+zMinName)
            edgeX3 = BoundingBoxEdge(corner011,corner111,yMaxName+zMaxName)
            
            
            self.__edges = [edgeX0,edgeX1,edgeX2,edgeX3,edgeY0,edgeY1,edgeY2,edgeY3,edgeZ0,edgeZ1,edgeZ2,edgeZ3]
            
            
            
            sideXY0 = BoundingBoxSide(edgeX0,edgeX2,edgeY0,edgeY2,np.array([0,0,-1]),zMinName,rotationWXYZ=[180,0,1,0],translationXYZ=[0,0,-0.01])
            sideXY1 = BoundingBoxSide(edgeX1,edgeX3,edgeY1,edgeY3,np.array([0,0,1]),zMaxName,translationXYZ=[0,0,0.01])
            sideXZ0 = BoundingBoxSide(edgeX0,edgeX1,edgeZ0,edgeZ2,np.array([0,-1,0]),yMinName,rotationWXYZ=[90,1,0,0],translationXYZ=[0,-0.01,0])
            sideXZ1 = BoundingBoxSide(edgeX2,edgeX3,edgeZ1,edgeZ3,np.array([0,1,0]),yMaxName,rotationWXYZ=[-90,1,0,0],translationXYZ=[0,0.01,0])
            sideYZ0 = BoundingBoxSide(edgeY0,edgeY1,edgeZ0,edgeZ1,np.array([-1,0,0]),xMinName,rotationWXYZ=[-90,0,1,0],translationXYZ=[-0.01,0,0])
            sideYZ1 = BoundingBoxSide(edgeY2,edgeY3,edgeZ2,edgeZ3,np.array([1,0,0]),xMaxName,rotationWXYZ=[90,0,1,0],translationXYZ=[0.01,0,0])
            
            
            # The order of the sides is imortant for distance calculation!!!
            self.__sides = [sideYZ0,sideXZ0,sideXY0,sideYZ1,sideXZ1,sideXY1]

            self.logger.info('Created BoundingBox')
        
        
        
        

        

        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getXMin(self): return self.__xRange[0]
    xMin = property(__getXMin)
    '''
    
    '''

    def __getXMax(self): return self.__xRange[1]
    xMax = property(__getXMax)
    '''
    
    '''
    
    def __getXLength(self): return self.xMax - self.xMin
    xLength = property(__getXLength)
    '''
    
    '''
    
    def __getYMin(self): return self.__yRange[0]
    yMin = property(__getYMin)
    '''
    
    '''

    def __getYMax(self): return self.__yRange[1]
    yMax = property(__getYMax)    
    '''
    
    '''
    
    def __getYLength(self): return self.yMax - self.yMin
    yLength = property(__getYLength)
    '''
    
    '''
    
    def __getZMin(self): return self.__zRange[0]
    zMin = property(__getZMin)
    '''
    
    '''

    def __getZMax(self): return self.__zRange[1]
    zMax = property(__getZMax)  
    '''
    
    '''
    
    def __getZLength(self): return self.zMax - self.zMin
    zLength = property(__getZLength)
    '''
    
    '''
   
    def __getCorners(self): return self.__corners
    corners = property(__getCorners)
    '''
    
    '''

    def __getEdges(self): return self.__edges
    edges = property(__getEdges)
    '''
    
    '''
    
    def __getSides(self): return self.__sides
    sides = property(__getSides)
    '''
    
    '''
    
    
    def __getMinCorner(self): return np.array([self.xMin, self.yMin, self.zMin])
    minCorner = property(__getMinCorner)
    '''
    
    '''
    
    def __getMaxCorner(self): return np.array([self.xMax, self.yMax, self.zMax])
    maxCorner = property(__getMaxCorner)
    '''
    
    '''
    
    
    
#==============================================================================
#    METHODS
#==============================================================================
    
#-------------------------------------------------------------------------
#    Calcualte Distance Between Bounding Box and some Coordinates and Give Closest Side
#-------------------------------------------------------------------------
    def distToBoundingBox(self,v):
        '''
        
        '''
        
        dist = np.concatenate((v-self.minCorner,self.maxCorner-v))
        if any(dist<0):
            return((float('-Inf'),None))
        else:
            return (np.min(dist),self.sides[np.argmin(dist)])
        
        
        
#-------------------------------------------------------------------------
#    Calcualte Intersection Point of a Line Segment and the Bounding Box
#-------------------------------------------------------------------------        
    def intersectLineWithBoundingBox(self,point1,point2):
        '''
        Check if a line defined by two points intersects with the bounding box.
        
        The bounding box can be intersected either somewhere inside a side,
        or by chance exactly on an edge or even at a corner. Therefore, the
        intersected element, as well as the intersection point is returned.
        
        
        '''
        
        # Find all sides that intersect with the line
        intersections = []
        for s in self.sides:
            intersection = s.intersectLineWithBoundingBoxSide(point1,point2)
            if intersection is not None:
                intersections.append((s,intersection))
                
                
                
        
                
                
        
        # Line does not intersect with the bounding box
        if len(intersections) == 0:
            return None
        
        
        # Line intersects with one side: return side and intersection point
        elif len(intersections) == 1:
            return intersections[0]
        
        
        # Line intersects with two sides: find the edge connecting both sides 
        # and return edge and intersection point
        elif len(intersections) == 2:
            edges0 = intersections[0][0].edges
            edges1 = intersections[1][0].edges
            
            edge =  list(set(edges0).intersection(set(edges1)))
            
            if len(edge) == 1 and np.allclose(intersections[0][1],intersections[1][1]):
                return (edge[0],intersections[0][1])
            else:
                if len(edge) != 1:
                    self.logger.error('{} and {} do not share an edge, an error must have occured'.format(*intersections))
                if not np.allclose(intersections[0][1],intersections[1][1]):
                    self.logger.error('Got different intersection points {} and {} for line {} to {}'.format(intersections[0][1],intersections[1][1],point1,point2))
                return None
            
        
        
        # Line intersects with three sides: find the corner connecting all sides
        # and return corner and intersection point
        
        elif len(intersections) == 3:
            corners0 = intersections[0][0].corners
            corners1 = intersections[1][0].corners
            corners2 = intersections[2][0].corners
            
            corner =  list(set(corners0).intersection(set(corners1)).intersection(set(corners2)))
            
            if len(corner) == 1 and np.allclose(intersections[0][1],intersections[1][1]) and np.allclose(intersections[0][1],intersections[2][1]):
                return (corner[0],intersections[0][1])
            else:
                self.logger.error('{}, {} and {} do not share an edge, an error must have occured'.format(*intersections))
                return None
            
        else:
            self.logger.error('Cannot have {} intersections'.format(len(intersections)))
            
        
        
        
#-------------------------------------------------------------------------
#    Plot Bounding Box with Matplotlib
#-------------------------------------------------------------------------
    def plotBoundingBox(self,ax,
                        showCorners=True,showCornersLabel=False,
                        showEdges=True,showEdgesLabel=False,
                        showSides=True,showSidesLabel=False,showSidesNormalVec=False):
        '''
        
        '''
        if showCorners:
            for c in self.corners:
                c.plotBoundingBoxCorner(ax,showLabel=showCornersLabel)
                
        if showEdges:
            for e in self.edges:
                e.plotBoundingBoxEdge(ax,showLabel=showEdgesLabel)
                
        if showSides:
            for f in self.sides:
                f.plotBoundingBoxSide(ax,showLabel=showSidesLabel,showNormalVec=showSidesNormalVec)
#-------------------------------------------------------------------------
#    Plot Bounding Box  with Visualization Toolkit
#-------------------------------------------------------------------------
    def plotBoundingBoxVtk(self,myVtk=None,
                           showCorners=True,showCornersLabel=False,
                           showEdges=True,showEdgesLabel=False,
                           showSides=True,showSidesLabel=False,showSidesNormalVec=False,
                           showCoordinateSystem=False):
        '''
        
        '''
        if myVtk is None:
            myVtk = MyVTK(polygonOpacity=1)
            
            
        if showCoordinateSystem:
            myVtk.addCoordinateSystem()
        
        if showCorners:
            for c in self.corners:
                c.plotBoundingBoxCornerVtk(myVtk,showLabel=showCornersLabel)
            
        if showEdges:
            for e in self.edges:
                e.plotBoundingBoxEdgeVtk(myVtk,showLabel=showEdgesLabel)
            
            
        
        if showSides:
            scale = min(self.xLength,self.yLength,self.zLength)*0.1
            textColor = tc.TUMGreen().rgb01
            for f in self.sides:
                f.plotBoundingBoxSideVtk(myVtk,showLabel=showSidesLabel,showNormalVec=showSidesNormalVec,scale=scale,color=textColor)
        return myVtk
    
#-------------------------------------------------------------------------
#    Plot Bounding Box  with TikZ
#-------------------------------------------------------------------------    
    def plotBoundingBoxTikZ(self,tikZPicture,showEdges=True,showSides=False):
        for c in self.corners:
            c.plotBoundingBoxCornerTikZ(tikZPicture)
        if showEdges:
            for e in self.edges:
                e.plotBoundingBoxEdgeTikZ(tikZPicture)
                
        if showSides:
            for s in self.sides:
                s.plotBoundingBoxSideTikZ(tikZPicture)
                
    
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    with MyLogging('BoundingBox'):     
        
        
#-------------------------------------------------------------------------
#    Create some examples
#-------------------------------------------------------------------------        
        
        cc.printBlue('Try to create bounding box with non-lists as ranges')
        bb = BoundingBox(1,2,3)
        
        cc.printBlue('Try to create bounding box with lists of wrong length')
        bb = BoundingBox([1,],[1,2,],[1,2,3])
        
        cc.printBlue('Try to create bounding box with wrong definition of ranges')
        bb = BoundingBox([5,0],[0,6],[0,7],preset='bla')
        
        cc.printBlue('Try to create bounding box with undefined preset')
        bb = BoundingBox([0,5],[0,6],[0,7],preset='bla')
        
        cc.printBlue('Try to create bounding box with missing names')
        bb = BoundingBox([0,5],[0,6],[0,7],xMinName='left',xMaxName='right')
        
        cc.printBlue('Creating bounding box with names and a preset')
        bb = BoundingBox([0,5],[0,6],[0,7],preset='vtk',xMinName='a',xMaxName='b',yMinName='c',yMaxName='d',zMinName='e',zMaxName='f')
        
        cc.printBlue('Creating standard bounding box')
        bb = BoundingBox([0,5],[0,6],[0,7],preset='pyplot')
        
        cc.printWhite(bb.corners)
        cc.printWhite(bb.edges)
        
        
        testPoint1 = np.array([-1,-1,-1])
        testPoint2 = np.array([1,1,1])
        

        
        
        cc.printYellow(bb.distToBoundingBox(testPoint1))
        cc.printYellow(bb.distToBoundingBox(testPoint2))
        
        
        bbTest = BoundingBox([1,14],[1,14],[1,14])
        bbTestPoint1 = np.array([15,10,12.5])
        bbTestPoint2 = np.array([12.5,10,15])
        bbTestLine = np.vstack((bbTestPoint1,bbTestPoint2))
        interstectionTest = bb.intersectLineWithBoundingBox(bbTestPoint1,bbTestPoint2)
        
        
        
        
            
            

#-------------------------------------------------------------------------
#    Plotting
#-------------------------------------------------------------------------    
    
        # Choose plotting method. Possible choices: pyplot, VTK, TikZ, animation, doc, None
        plottingMethod = 'pyplot'   
        
        
#    Disabled
#--------------------------------------------------------------------- 
        if plottingMethod is None or plottingMethod == 'None':
            cc.printBlue('Plotting disabled')
        
#    Pyplot
#---------------------------------------------------------------------         
        elif plottingMethod == 'pyplot':
            cc.printBlue('Plot using pyplot')
            (figs,axes) = pf.getFigures()
            bb.plotBoundingBox(axes[0],showCornersLabel=True)
            bb.plotBoundingBox(axes[1],showEdgesLabel=True)
            bb.plotBoundingBox(axes[2],showSidesLabel=True)
            
            bb.plotBoundingBox(axes[3])
            
            
            
            
            # Check intersections
            p0 = np.array([2,2,2])
            p1 = np.array([-1,-1,-1])
            p2 = np.array([-1,-1,1])
            p3 = np.array([-1,1,1])
            p4 = np.array([3,4,5])
            p5 = np.array([2,2,8])
            
            
            intersection1 = bb.intersectLineWithBoundingBox(p0,p1)
            intersection2 = bb.intersectLineWithBoundingBox(p0,p2)
            intersection3 = bb.intersectLineWithBoundingBox(p0,p3)
            intersection4 = bb.intersectLineWithBoundingBox(p0,p4)
            intersection4 = bb.intersectLineWithBoundingBox(p3,p5)
            
#            cc.printMagenta(intersection)
            
            intersections = [intersection1,intersection2,intersection3]
          
            for i in intersections:
                if i is not None:
                    axes[3].scatter(i[1][0],i[1][1],i[1][2],color=tc.TUMRose().html)
                
                
            
            
            
                        
            line1 = np.vstack((p0,p1))
            line2 = np.vstack((p0,p2))
            line3 = np.vstack((p0,p3))
            line4 = np.vstack((p0,p4))
            line5 = np.vstack((p3,p5))
            
            lines = [line1,line2,line3,line4,line5]
            
            for l in lines:
                axes[3].plot(l[:,0],l[:,1],l[:,2],color=tc.TUMBlue().html)
                
                
                
            
            
            bbTest.plotBoundingBox(axes[4])
            axes[4].plot(bbTestLine[:,0],bbTestLine[:,1],bbTestLine[:,2],color=tc.TUMBlue().html)
            pf.setLabels(axes[3])
            
            

#    VTK
#--------------------------------------------------------------------- 
        elif plottingMethod == 'VTK' :
            cc.printBlue('Plot using VTK')
            myVtk = bb.plotBoundingBoxVtk(showCoordinateSystem=True,showCornersLabel=True,showSidesLabel=True)
            myVtk.addScatterPointNumpy(testPoint1)
            myVtk.addScatterPointNumpy(testPoint2)            
            myVtk.start()
#    TikZ
#--------------------------------------------------------------------- 
        elif plottingMethod == 'TikZ' :
            cc.printBlue('Plot using TikZ')            
            from tools.tikZPicture.tikZPicture3D import TikZPicture3D
            tikZPic = TikZPicture3D()
            origin = tikZPic.addTikZCoordinate('origin',np.array([0,0,0]))
            tikZPic.addTikZCoSy3D(origin)
            bb.plotBoundingBoxTikZ(tikZPic,showSides=True)
            tikZPic.writeLaTeXFile('latex','boundingBox',compileFile=True,openFile=True)
            
            
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
            
    

