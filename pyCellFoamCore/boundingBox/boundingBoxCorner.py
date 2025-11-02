# -*- coding: utf-8 -*-
#==============================================================================
# BOUNDING BOX CORNER
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Mon Feb 24 11:22:53 2020

'''

'''
#==============================================================================
#    IMPORTS
#==============================================================================
import os
if __name__ == '__main__':
    os.chdir('../')

import numpy as np
import logging

from boundingBox.boundingBoxElement import BoundingBoxElement
import tools.tumcolor as tc

#==============================================================================
#    LOGGING
#==============================================================================

_log = logging.getLogger(__name__)

#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class BoundingBoxCorner(BoundingBoxElement):
    '''

    '''

#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__coordinates',
                 '__node',
                 '__tikZCoordinates')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,coordinates,*args,**kwargs):
        '''
        :param numpy.array coordinates: Coordinates of the bounding box
        :param str identifier: A name for the corner

        '''
        super().__init__(*args,**kwargs,loggerName = 'bbCorner')
        self.__coordinates = coordinates
        self.__node = None
        self.__tikZCoordinates = {}
        _log.info('Created BoundingBoxCorner')



#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getCoordinates(self): return self.__coordinates
    coordinates = property(__getCoordinates)
    '''

    '''

    def __getTikZCoordinates(self): return self.__tikZCoordinates
    tikZCoordinates = property(__getTikZCoordinates)
    '''

    '''


#    def __getNode(self): return self.__node
#    def __setNode(self,n):
#        if self.__node is None:
#            self.__node = n
#            _log.info('Associated {} with node {}'.format(self,n))
#        else:
#            _log.error('This corner already belongs to a node')
#    node = property(__getNode,__setNode)
#    '''
#
#    '''



#==============================================================================
#    MAGIC METHODS
#==============================================================================

    def  __repr__(self):
        '''
        Show infoText in console

        '''
        return 'BBCorner<{}>'.format(self.identifier)


#==============================================================================
#    METHODS
#==============================================================================


    def getTikZCoordinate(self,tikZPicture):
        '''

        '''
        if tikZPicture in self.tikZCoordinates:
            return self.tikZCoordinates[tikZPicture]
        else:
            _log.info('This node does not belong to the given tikzpicture')
            return None

    def __setTikZCoordinate(self,tikZPicture,tikZCoordinate):
        '''

        '''
        if tikZPicture in self.tikZCoordinates:
            _log.error('This node already belongs to the given tikzpicture')
        else:
            self.tikZCoordinates[tikZPicture] = tikZCoordinate

#-------------------------------------------------------------------------
#    Print Bounding Box Corner
#-------------------------------------------------------------------------
    def printBoundingBoxCorner(self):
        '''

        '''
        print('bbCorner "{}" at {}'.format(self.identifier,self.coordinates))

#-------------------------------------------------------------------------
#    Plot Bounding Box Corner with Matplotlib
#-------------------------------------------------------------------------
    def plotBoundingBoxCorner(self,ax,showLabel=False,color=tc.TUMBlack()):
        '''

        '''
        ax.scatter(self.coordinates[0],self.coordinates[1],self.coordinates[2],'o',color=color.html)
        if showLabel:
            ax.text(self.coordinates[0],self.coordinates[1],self.coordinates[2],self.identifier,color=color.html)


#-------------------------------------------------------------------------
#    Plot Bounding Box Corner with Visualization Toolkit
#-------------------------------------------------------------------------
    def plotBoundingBoxCornerVtk(self,myVtk,showLabel=True):
        '''

        '''
        myVtk.addScatterPointNumpy(self.coordinates)
        if showLabel:
            myVtk.addTextAnnotationNumpy(self.coordinates,self.identifier)


#-------------------------------------------------------------------------
#    Plot Bounding Box Corner with Visualization Toolkit
#-------------------------------------------------------------------------
    def plotBoundingBoxCornerTikZ(self,tikZPicture):
        '''

        '''
        coord = tikZPicture.addTikZCoordinate('BBCorner{}'.format(self.identifier),self.coordinates)
        self.__setTikZCoordinate(tikZPicture,coord)

#-------------------------------------------------------------------------
#    Calculate Distance Between Bounding Box Corner and some Coordinates
#-------------------------------------------------------------------------
    def distToBoundingBoxCorner(self,coordinates):
        return np.linalg.norm(self.coordinates - coordinates)



#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    from tools import MyLogging
    from tools.myVTK import MyVTK
    import tools.colorConsole as cc
    with MyLogging('BoundingBoxCorner',debug=True):
        cc.printBlue('Create bbCorner')
        coords = np.array([1,2,3])
        corner = BoundingBoxCorner(coords,'testCorner1')
        cc.printBlue('Check resulut')
        print(corner)
        corner.printBoundingBoxCorner()


        cc.printBlue('Create another bbCorner')
        coords2 = np.array([2,2,3])
        corner2 = BoundingBoxCorner(coords2,'testCorner2')


        # Choose plotting method. Possible choices: pyplot, VTK, TikZ, None
        plottingMethod = 'TikZ'

        if plottingMethod is None or plottingMethod == 'None':
            cc.printBlue('Plotting disabled')

        elif plottingMethod == 'pyplot':
            cc.printBlue('Plot using pyplot')
            import tools.placeFigures as pf
            (figs,axes) = pf.getFigures()
            corner.plotBoundingBoxCorner(axes[0])
            corner2.plotBoundingBoxCorner(axes[0],showLabel=True)
            print(corner.coordinates[0])



        elif plottingMethod == 'VTK' :
            cc.printBlue('Plot using VTK')
            myVtk = MyVTK(polygonOpacity=1)
            corner.plotBoundingBoxCornerVtk(myVtk,showLabel=False)
            corner2.plotBoundingBoxCornerVtk(myVtk)
            myVtk.start()

        elif plottingMethod == 'TikZ' :
            cc.printBlue('Plot using TikZ')
            from tools.tikZPicture.tikZPicture3D import TikZPicture3D
            tikZPic = TikZPicture3D()
            origin = tikZPic.addTikZCoordinate('origin',np.array([0,0,0]))
            tikZPic.addTikZCoSy3D(origin)
            corner.plotBoundingBoxCornerTikZ(tikZPic)
            tikZPic.writeLaTeXFile('latex','boundingBoxCorner',compileFile=True,openFile=True)

        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))


