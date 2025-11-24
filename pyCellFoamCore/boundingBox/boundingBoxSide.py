# -*- coding: utf-8 -*-
#==============================================================================
# BOUNDING BOX SIDE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Mon Feb 24 11:57:28 2020

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
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


from pyCellFoamCore.boundingBox.boundingBoxElement import BoundingBoxElement
from pyCellFoamCore.boundingBox.boundingBoxEdge import BoundingBoxEdge
import pyCellFoamCore.tools.tumcolor as tc
from pyCellFoamCore.tools.arrow3D import Arrow3D

import pyCellFoamCore.tools.colorConsole as cc

#==============================================================================
#    LOGGING
#==============================================================================

_log = logging.getLogger(__name__)

#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class BoundingBoxSide(BoundingBoxElement):
    '''

    '''

#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = (
        '__corners',
        '__edges',
        '__normalVec',
        '__rotationWXYZ',
        '__translationXYZ',
        "__k_cell_edges",
        "__faces",
    )

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,edge1,edge2,edge3,edge4,normalVec,*args,rotationWXYZ=[0,1,0,0],translationXYZ=[0,0,0],**kwargs):
        '''

        :param BoundingBoxEdge edge1: First edge
        :param BoundingBoxEdge edge2: Second edge
        :param BoundingBoxEdge edge3: Third edge
        :param BoundingBoxEdge edge4: Fourth edge
        :param numpy.array normalVec: Normalized normal vec
        :param numpy.array rotationWXYZ: Rotation of the label in VTK
        :param numpy.array translationXYZ: Translation of the label in VTK
        :param str identifier: A name for the edge
        '''
        super().__init__(*args,**kwargs,loggerName='bbFace')
        self.__corners = []
        corners = []
        self.__edges = [edge1,edge2,edge3,edge4]
        for e in self.__edges:
            for c in e.corners:
                if not c in corners:
                    corners.append(c)

        if len(corners) != 4:
            _log.error('A bounding box face must have exactly four corners, but this face has {}'.format(len(corners)))


        self.__corners = corners[:1]
        corners.pop(0)


        # Sort corners so that they can be plotted correctly
        counter = 10
        while corners and  counter > 0:
            counter -= 1
            for c in corners:
                if list((self.__corners[-1].coordinates == c.coordinates)).count(True) == 2:
                    self.__corners.append(c)
                    corners.remove(c)
                    break




        self.__rotationWXYZ = rotationWXYZ
        self.__translationXYZ = translationXYZ

        if np.linalg.norm(normalVec) != 1:
            _log.warning('Normal vector was normalized, it had length {}'.format(np.linalg.norm(normalVec)))
            normalVec = normalVec/np.linalg.norm(normalVec)


        self.__normalVec = normalVec
        if not list((self.__normalVec == np.array([0,0,0]))).count(True) == 2:
            _log.error('Normal vector for a bounding box side must be parallel to a coordinate axis')


        self.__k_cell_edges = []
        self.__faces = []




        _log.info('Created BoundingBoxSide')





#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getCorners(self): return self.__corners
    corners = property(__getCorners)
    '''

    '''


    def __getEdges(self): return self.__edges
    edges = property(__getEdges)
    '''

    '''

    def __getRotationWXYZ(self): return self.__rotationWXYZ
    rotationWXYZ = property(__getRotationWXYZ)
    '''

    '''

    def __getCenter(self):
        coordinates = np.array([c.coordinates for c in self.corners])
        return coordinates.sum(axis=0)/len(self.corners)
    center = property(__getCenter)
    '''

    '''

    def __getRotationWXYZ(self): return self.__rotationWXYZ
    rotationWXYZ = property(__getRotationWXYZ)
    '''

    '''

    def __getTranslationXYZ(self): return self.__translationXYZ
    translationXYZ = property(__getTranslationXYZ)
    '''

    '''

    def __getCoordinates(self): return np.vstack(tuple([c.coordinates for c in self.corners]))
    coordinates = property(__getCoordinates)
    '''

    '''

    def __getNormalVec(self): return self.__normalVec
    normalVec = property(__getNormalVec)
    '''

    '''

    def __getKCellEdges(self):
        return self.__k_cell_edges
    k_cell_edges = property(__getKCellEdges)
    '''

    '''

    def __getFaces(self):
        return self.__faces
    faces = property(__getFaces)
    '''

    '''


#==============================================================================
#    MAGIC METHODS
#==============================================================================

    def  __repr__(self):
        '''
        Show info_text in console

        '''
        return 'BBFace<{}>'.format(self.identifier)
#==============================================================================
#    METHODS
#==============================================================================

    def add_k_cell_edge(self,edge):
        '''

        '''
        if edge in self.__k_cell_edges:
            _log.error('This k-cell edge is already associated with this bounding box side')
        else:
            self.k_cell_edges.append(edge)


    def add_face(self,face):
        '''

        '''
        if face in self.__faces:
            _log.error('This face is already associated with this bounding box side')
        else:
            self.__faces.append(face)

#-------------------------------------------------------------------------
#    Print Bounding Box Side
#-------------------------------------------------------------------------
    def printBoundingBoxSide(self):
        '''

        '''
        print('bbFace "{}" between edges "{}", "{}", "{}" and "{}"'.format(self.identifier,*[e.identifier for e in self.edges]))
#-------------------------------------------------------------------------
#    Plot Bounding Box Side with Matplotlib
#-------------------------------------------------------------------------
    def plotBoundingBoxSide(self,ax,showLabel=True,showNormalVec=False,color=tc.TUMBlack()):
        '''

        '''
        collection = Poly3DCollection([self.coordinates],color=color.html,alpha=0.2)
        collection.set_facecolor(color.html)
        ax.add_collection3d(collection)
        if showLabel:
            xCoordText = self.center[0]+self.translationXYZ[0]
            yCoordText = self.center[1]+self.translationXYZ[1]
            zCoordText = self.center[2]+self.translationXYZ[2]
            ax.text(xCoordText,yCoordText,zCoordText,self.identifier,color=color.html)

        if showNormalVec:
            a = Arrow3D(self.center,self.center+self.normalVec, mutation_scale=20, lw=2, arrowstyle="-|>", color=color.html)
            ax.add_artist(a)

#-------------------------------------------------------------------------
#    Plot Bounding Box Side with Visualization Toolkit
#-------------------------------------------------------------------------
    def plotBoundingBoxSideVtk(self,myVtk,showLabel=True,showNormalVec=False,**kwargs):
        '''

        '''
        myVtk.addPolygon([c.coordinates for c in self.corners])
        if showLabel:
            xCoordText = self.center[0]+self.translationXYZ[0]
            yCoordText = self.center[1]+self.translationXYZ[1]
            zCoordText = self.center[2]+self.translationXYZ[2]
            myVtk.addText3DNew(xCoordText,yCoordText,zCoordText,self.identifier,rotationWXYZ=self.rotationWXYZ,**kwargs)

        if showNormalVec:
            myVtk.addArrowStartEnd(self.center,self.center+self.normalVec)


    def plotBoundingBoxSideTikZ(self,tikZPicture):
        '''

        '''
        tikZCoords = [c.getTikZCoordinate(tikZPicture) for c in self.corners]
        tikZPicture.addTikZPolygon(tikZCoords,command='fill',options=['fill opacity=0.2',])


    def projectOnBoundingBoxSide(self,coordinates):
        '''

        '''
        M1 = np.diag(np.ones(3)-np.abs(self.normalVec))
        M2 = np.diag(np.abs(self.normalVec))

        projectedCoordinates = M1 @ coordinates+ M2 @ self.center
        return projectedCoordinates

#-------------------------------------------------------------------------
#    Calcualte Distance Between Bounding Box Side and some Coordinates
#-------------------------------------------------------------------------
    def distToBoundingBoxSide(self,coordinates):
        '''

        '''

        return self.normalVec.transpose() @ (self.center - coordinates)



    def intersectLineWithBoundingBoxSide(self,point1,point2):
        '''
        https://stackoverflow.com/questions/8812073/ray-and-square-rectangle-intersection-in-3d

        '''
        # Check if both points lie on the same side of the plane:
        if self.distToBoundingBoxSide(point1) * self.distToBoundingBoxSide(point2) < 0:
            d = point2-point1
            d = d / np.linalg.norm(d)
            a = ((self.center-point1).transpose() @ self.normalVec) / (d.transpose() @ self.normalVec)

            p = point1 + a * d




#            cc.printYellow(self.coordinates[:,0])
            ranges = np.array([[min(self.coordinates[:,0]),max(self.coordinates[:,0])],
                               [min(self.coordinates[:,1]),max(self.coordinates[:,1])],
                               [min(self.coordinates[:,2]),max(self.coordinates[:,2])]])
#            xRange = np.array([min(self.coordinates[:,0]),max(self.coordinates[:,0])])
#            yRange = np.array([min(self.coordinates[:,1]),max(self.coordinates[:,1])])
#            zRange = np.array([min(self.coordinates[:,2]),max(self.coordinates[:,2])])

#            cc.printYellow('Intersection point:')
#            cc.printYellow(p)
#            cc.printYellow()
#            cc.printYellow('Ranges:')
#            cc.printYellow(ranges)
#            cc.printYellow()
#            cc.printYellow('Inside ranges?')
#            cc.printYellow(p-ranges[:,0] > -1e-5)
#            cc.printYellow(p-ranges[:,1] < 1e-5)


            if np.all(p-ranges[:,0] > -1e-5) and np.all(p-ranges[:,1] < 1e-5):
                return p
            else:
                return None


#            cc.printYellow(p,ranges,p>ranges[:,0])


#            return ranges







        else:
            return None




#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    from tools import MyLogging
    from boundingBox.boundingBoxCorner import BoundingBoxCorner
    import tools.colorConsole as cc
    from tools.myVTK import MyVTK
    with MyLogging('BoundingBoxEdge',debug=True):
        cc.printBlue('Create bbCorner left top back')
        ltb = BoundingBoxCorner(np.array([0,2,0]),'LeftTopBack')
        cc.printBlue('Create bbCorner right top back')
        rtb = BoundingBoxCorner(np.array([1,2,0]),'RightTopBack')
        cc.printBlue('Create bbCorner left bottom back')
        lbb = BoundingBoxCorner(np.array([0,0,0]),'LeftBottomBack')
        cc.printBlue('Create bbCorner right bottom back')
        rbb = BoundingBoxCorner(np.array([1,0,0]),'RightBottomBack')

        cc.printBlue('Create top back edge')
        tb = BoundingBoxEdge(rtb,ltb,'TopBack')
        cc.printBlue('Create bottom back edge')
        bb = BoundingBoxEdge(rbb,lbb,'BottomBack')
        cc.printBlue('Create right back edge')
        rb = BoundingBoxEdge(rtb,ltb,'TopBack')
        cc.printBlue('Create left back edge')
        lb = BoundingBoxEdge(rbb,lbb,'BottomBack')

        cc.printBlue('Create back face')
        back = BoundingBoxSide(tb,bb,rb,lb,np.array([0,0,-1]),'Back',translationXYZ = [0,0,0.01])
        print(back.corners)

        back.printBoundingBoxSide()


        testCoordinate = np.array([0.3,0.4,0.5])

        print(back.distToBoundingBoxSide(testCoordinate))



        if False:
            myVtk = MyVTK(polygonOpacity=1)
            back.plotBoundingBoxSideVtk(myVtk,scale=0.1,color=tc.TUMLightBlue().rgb01,showNormalVec=True)
            myVtk.start()
        else:
            import tools.placeFigures as pf
            (figs,axes) = pf.getFigures()
            back.plotBoundingBoxSide(axes[0],showNormalVec=True)

            ax = axes[0]
            ax.scatter(testCoordinate[0],testCoordinate[1],testCoordinate[2],color=tc.TUMBlue().html)



            proj = back.projectOnBoundingBoxSide(testCoordinate)
            ax.scatter(proj[0],proj[1],proj[2],color=tc.TUMGreen().html)


            point1 = np.array([0.5,-2,-1])
            point2 = np.array([1,1,1])

            line = np.vstack((point1,point2))

            print(back.intersectLineWithBoundingBoxSide(point1,point2))

            intersection = back.intersectLineWithBoundingBoxSide(point1,point2)

            ax.plot(line[:,0],line[:,1],line[:,2])

            if intersection is not None:
                ax.scatter(intersection[0],intersection[1],intersection[2],color=tc.TUMRose().html)




#            point
#
