# -*- coding: utf-8 -*-
#==============================================================================
# IMPORH INTERFACE FOR PLATEAU CELL GRAPH
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Jul 15 15:55:32 2020

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
from collections import deque
import itertools
import numpy as np

#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------


#    kCells
#--------------------------------------------------------------------
from kCells import Node, Edge
from pyCellFoamCore.kCells.face.face import Face
from pyCellFoamCore.kCells.volume.volume import Volume

#    Complex & Grids
#--------------------------------------------------------------------
from grids.iMorphInterface import IMorphInterface

#    Tools
#--------------------------------------------------------------------
import tools.colorConsole as cc
import tools.placeFigures as pf
from tools import MyLogging
#import tools.tumcolor as tc
from boundingBox import BoundingBox


#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class IMorphInterfacePlateauCellGraph(IMorphInterface):
    '''
    This is the explanation of this class.

    '''

#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__subPathToNodesFile',
                 '__subPathToTubesFile',
                 '__subPathToNodeThroatsFile',
                 '__boundingBox',
#                 '__addBorderCellFaceTypeNodes',
                 )

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,*args,
                 subPathToNodesFile = r'\Graphs\network_balls_plateauCellGraph_Nodes.txt',
                 subPathToTubesFile = r'\Graphs\network_balls_plateauCellGraph_Tubes.txt',
                 subPathToNodeThroatsFile = r'\OutputFiles\node_throatsFromPlateauCell.txt',
#                 addBorderCellFaceTypeNodes = False,
                 **kwargs):
        '''
        This is the explanation of the __init__ method.

        All parameters should be listed:

        :param int a: Some Number
        :param str b: Some String

        '''

        self.__subPathToNodesFile = subPathToNodesFile
        self.__subPathToTubesFile = subPathToTubesFile
        self.__subPathToNodeThroatsFile = subPathToNodeThroatsFile
        # self.__boundingBox = BoundingBox([0,1],[0,1],[0,1])
#        self.__addBorderCellFaceTypeNodes = addBorderCellFaceTypeNodes

        super().__init__(*args,**kwargs)



#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getPathToNodesFile(self): return self.pathToPorousFolder + self.__subPathToNodesFile
    pathToNodesFile = property(__getPathToNodesFile)
    '''

    '''

    def __getPathToTubesFile(self): return self.pathToPorousFolder +  self.__subPathToTubesFile
    pathToTubesFile = property(__getPathToTubesFile)
    '''

    '''

    def __getPathToNodeThroatsFile(self): return self.pathToPorousFolder +  self.__subPathToNodeThroatsFile
    pathToNodeThroatsFile = property(__getPathToNodeThroatsFile)
    '''

    '''

    def __getBoundingBox(self): return self.__boundingBox
    boundingBox = property(__getBoundingBox)
    '''

    '''

    def __getAddBorderCellFaceTypeNodes(self): return self.__addBorderCellFaceTypeNodes
    addBorderCellFaceTypeNodes = property(__getAddBorderCellFaceTypeNodes)
    '''

    '''




#==============================================================================
#    METHODS
#==============================================================================


#-------------------------------------------------------------------------
#    Set Up
#-------------------------------------------------------------------------

    def setUp(self):
        '''

        '''

        error = False

        if not error:
            error = self.loadNodesGraphNodes(self.pathToNodesFile)


        self.__boundingBox = BoundingBox(self.xLim, self.yLim, self.zLim)

        if not error:
            error = self.loadEdgesGraphTubes(self.pathToTubesFile)



        if not error:
            error = self.loadFaces(self.pathToNodeThroatsFile)

        error = True

        if not error:
            error = self.__loadVolumes()





        if not error:
            super().setUp()


#-------------------------------------------------------------------------
#    Load Faces
#-------------------------------------------------------------------------

    def __loadFacesOld(self):
        '''

        '''
        #    Logging
        #---------------------------------------------------------------------
        if False:
            myPrintDebug = self.logger.debug
            myPrintInfo = self.logger.info
            myPrintWarning = self.logger.warning
            myPrintError = self.logger.error
        else:
            self.logger.warning('Using prints instead of logger!')
            myPrintDebug = cc.printGreen
            myPrintInfo = cc.printCyan
            myPrintWarning = cc.printYellow
            myPrintError = cc.printRed

        myPrintInfo('Loading faces')


        #    Prepare lists
        #---------------------------------------------------------------------
        faces = []
        throats = []

        self.__boundingBox = BoundingBox(self.xLim,self.yLim,self.zLim)
#


        #    Check source file
        #---------------------------------------------------------------------

        error = False

        if os.path.isfile(self.pathToNodeThroatsFile):
            myPrintInfo('Found file containing faces')
        else:
            myPrintError('File containing nodes cannot be found')
            error = True


        #    Read faces
        #---------------------------------------------------------------------
        readFaces = False
        maxNumberOfLines = float('inf')
#        maxNumberOfLines = 2

        currentLineNumber = 0
        if not error:
            with open(self.pathToNodeThroatsFile) as fh:
                for l in fh.readlines():
                    if readFaces and currentLineNumber < maxNumberOfLines:
                        currentLineNumber += 1
                        data = l.rstrip().split('\t')
                        if len(data)>1:     # filter out empty lines (mostly at the end of the file)
                            indexNode = int(data[0])
                            numberOfThroats = int(data[1])
                            position = 2

                            myPrintDebug('Creating {} throats that contain node {}'.format(numberOfThroats,self.nodes[indexNode]))
                            for i in range(numberOfThroats):
                                myPrintDebug('')
                                throatStr = data[position+1:position+1+int(data[position])]
                                throat = [int(t) for t in throatStr]



#                                removedNode = False
                                if throat[0] == throat [-1]:
                                    throat.pop()
#                                    completeCircle = True
#                                else:
#                                    completeCircle = False
#                                else:
#                                    firstNode = self.nodes[throat[0]]
#                                    lastNode = self.nodes[throat[1]]
#                                    myPrintDebug('First node of throat {} and last node of throat {} are not connected'.format(firstNode,lastNode))



#                                    (distOfFirstNode,sideOfFirstNode) =  firstNode.distToBoundingBox(self.boundingBox)
#                                    (distOfLastNode,sideOfLastNode) =  lastNode.distToBoundingBox(self.boundingBox)
#                                    myPrintDebug('First node is {} away from {} - Last node is {} away from {}'.format(distOfFirstNode,sideOfFirstNode,distOfLastNode,sideOfLastNode))
#                                    firstNode.color = tc.TUMGreen()
#                                    lastNode.color = tc.TUMGreen()




#                                    myPrintWarning(')
#                                    removedNode = True
                                throatExistsAlready = False
                                throatDeque = deque(throat)
                                for i in range(len(throat)):
                                    if list(throatDeque) in throats or list(reversed(throatDeque)) in throats:
                                        throatExistsAlready = True
                                    throatDeque.rotate()
                                position += int(data[position])+1
                                if throatExistsAlready:
                                    myPrintDebug('Throat with nodes {} already exists'.format(throat))
                                else:
                                    throats.append(throat)
                                    myPrintDebug('Nodes in current throat: {}'.format(throat))
                                    if len(throat) > 2:
                                        foundAllEdges = True
                                        edgesForFace = []
                                        cycleThroat = throat[:]
                                        if not cycleThroat[0] == cycleThroat [-1]:
                                            cycleThroat.append(throat[0])
                                        for numStart,numEnd in zip(cycleThroat[:-1],cycleThroat[1:]):
                                            found = False
                                            n = self.nodes[numStart]
                                            # IMPORTANT: Must check if edge is part of the edges defined by iMorph, because due to triangulation new edges with unknown numbers are created
                                            for e in n.edges:
                                                if e.startNode.num == numStart and e.endNode.num ==numEnd and e in self.edges:
                                                    found = True
                                                    edgesForFace.append(e)
                                                if e.startNode.num == numEnd and e.endNode.num ==numStart and e in self.edges:
                                                    found = True
                                                    edgesForFace.append(-e)
                                            if found:
                                                myPrintDebug('Found edge {} that connects node {} and {}. So far found: {}'.format(edgesForFace[-1],numStart,numEnd,edgesForFace))

                                            else:
                                                myPrintWarning('Could not find an edge that connects node {} and {}'.format(numStart,numEnd))

                                                newEdge = Edge(self.nodes[numStart],self.nodes[numEnd])
                                                myPrintWarning('Creating new edge {} from {} to {}'.format(newEdge,self.nodes[numStart],self.nodes[numEnd]))
                                                self.edges.append(newEdge)
                                                edgesForFace.append(newEdge)
                                                foundAllEdges=True

#                                                if self.__addBorderCellFaceTypeNodes:
#
#                                                    firstNode = self.nodes[numStart]
#                                                    lastNode = self.nodes[numEnd]
#                                                    myPrintDebug('First node of throat {} and last node of throat {} are not connected'.format(firstNode,lastNode))
#                                                    (distOfFirstNode,sideOfFirstNode) =  firstNode.distToBoundingBox(self.boundingBox)
#                                                    (distOfLastNode,sideOfLastNode) =  lastNode.distToBoundingBox(self.boundingBox)
#    #                                                myPrintDebug('First node is {} away from {} - Last node is {} away from {}'.format(distOfFirstNode,sideOfFirstNode,distOfLastNode,sideOfLastNode))
#                                                    myPrintDebug('iMorph type of nodes: "{}" and "{}"'.format(firstNode.iMorphType,lastNode.iMorphType))
#                                                    if  firstNode.iMorphType == 'border_cell' and lastNode.iMorphType == 'border_cell':
#                                                        pass
#                                                        cellFaceNodesFirst = [n for n in firstNode.connectedNodes if n.iMorphType == 'border_cell_face']
#                                                        cellFaceNodesLast = [n for n in lastNode.connectedNodes if n.iMorphType == 'border_cell_face']
#                                                        if len(cellFaceNodesFirst) == 1 and len(cellFaceNodesLast) == 1:
#                                                            myPrintDebug('Adding edges for border_cell_face type nodes')
#    ##
#                                                            edgesForFace.append(cellFaceNodesFirst[0].edges[0])
#                                                            edgesForFace.append(cellFaceNodesLast[0].edges[0])
#    ##
#    ##
#    ##
#                                                            newEdge = Edge(cellFaceNodesFirst[0],cellFaceNodesLast[0])
#                                                            newEdge.color = tc.TUMMustard()
#                                                            edgesForFace.append(newEdge)
#                                                            self.edges.append(newEdge)
#                                                            myPrintDebug('Created new edge {} from {} to {}'.format(newEdge,cellFaceNodesFirst[0],cellFaceNodesLast[0]))
#
#
#
#
#                                                        else:
#                                                            myPrintError('Both border_cell type nodes need to be connected to a border_cell_face')
#                                                            foundAllEdges = False







    #                                                    myPrintDebug('Numbers of cell face type nodes connected to first and last node: {} - {}'.format(len(cellFaceNodesFirst),len(cellFaceNodesLast)))


    #                                                    pairIterator = list(itertools.product(cellFaceNodesFirst,cellFaceNodesLast))
    #                                                    distances = np.array([np.linalg.norm(n1.coordinates - n2.coordinates) for (n1,n2) in pairIterator])
    #                                                    indexOfMinDistance = np.argmin(distances)
    #                                                    closestNodes = pairIterator[indexOfMinDistance]
    #                                                    myPrintWarning('Closest nodes: {}'.format(closestNodes))
    #                                                    newEdge = None
    #                                                    for e in closestNodes[0].edges:
    #                                                        if e.startNode == closestNodes[1] or e.endNode == closestNodes[1]:
    #                                                            newEdge = e

    #                                                    if not newEdge:
    #                                                        newEdge = Edge(closestNodes[0],closestNodes[1])
    #                                                        newEdge.color = tc.TUMMustard()
    #                                                        newEdge.showLabel=False
    #                                                        self.edges.append(newEdge)

    #                                                    edgesForFace.append(newEdge)





#
#                                                    else:
#                                                        myPrintError('Unconnected nodes are of type "{}" and "{}"'.format(firstNode.iMorphType,lastNode.iMorphType))
#                                                        foundAllEdges = False





                                        if foundAllEdges:
                                            myPrintDebug('Found all edges {}'.format(edgesForFace))
                                            newFace = Face(edgesForFace,triangulate=True,sortEdges=True)
                                            faces.append(newFace)
                                            if newFace.isDeleted:
                                                myPrintError('Face creation was not succesful')
#                                                for e in edgesForFace:
#                                                    e.color = tc.TUMBlack()

                                        else:
                                            myPrintError('Could not find all edges')


                                    else:
                                        myPrintError('Need 3 or more nodes in a throat, only have {}: {}'.format(len(throat),throat))
                        else:
                            myPrintDebug('Skipping empty line')
                    if l.startswith('indice node'):
                        readFaces  = True
                        myPrintDebug('Found start for throats')


            for f1 in faces:
                if f1.edges:
                    for f2 in faces:
                        if not f1 is f2 and f1.isIdenticalTo(f2):
                            myPrintError('Found duplicate faces {} and {}'.format(f1,f2))


        self.faces = faces
        return error




#-------------------------------------------------------------------------
#    Load Volumes
#-------------------------------------------------------------------------

    def __loadVolumes(self):
        '''

        '''
        #    Logging
        #---------------------------------------------------------------------
        if False:
            myPrintDebug = self.logger.debug
            myPrintInfo = self.logger.info
            myPrintWarning = self.logger.warning
            myPrintError = self.logger.error
        else:
            self.logger.warning('Using prints instead of logger!')
            myPrintDebug = cc.printGreen
            myPrintInfo = cc.printCyan
            myPrintWarning = cc.printYellow
            myPrintError = cc.printRed

        myPrintInfo('Loading volumes')


        #    Prepare lists
        #---------------------------------------------------------------------
        volumes = []
        throats = []



        #    Check source file
        #---------------------------------------------------------------------

        error = False

        if os.path.isfile(self.pathToNodeThroatsFile):
            myPrintInfo('Found file containing volumes')
        else:
            myPrintError('File containing volumes cannot be found')
            error = True
#
#
#        #    Read faces
#        #---------------------------------------------------------------------
#        readVolumes = False
##        maxNumberOfLines = float('inf')
#        maxNumberOfLines = 10
#
#        currentLineNumber = 0
#        if not error:
#            with open(self.pathToNodeThroatsFile) as fh:
#                for l in fh.readlines():
#                    if readVolumes and currentLineNumber < maxNumberOfLines:
#                        currentLineNumber += 1
#                        print(l.rstrip())
#
#
#                    if l.startswith('indice\ti'):
#                        readVolumes  = True
#                        myPrintDebug('Found start for cells')
#
#
#
        error = True
        return error


#-------------------------------------------------------------------------
#    Plot for Documentation
#-------------------------------------------------------------------------
    @classmethod
    def plotDoc(cls):
        cc.printRed('Not implemented')

#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':

    with MyLogging('IMorphInterfacePlateauCellGraph'):

#-------------------------------------------------------------------------
#    Create some examples
#-------------------------------------------------------------------------


#        interface = IMorphInterfaceTubes(r'D:\iMorph\05_iMorph_July_20\data\data\Kelvin\Div 6\Roi2\original\Porous',addBorderCellFaceTypeNodes=True)
#        interface1 = IMorphInterfaceTubes(r'D:\iMorph\06_iMorph_October_20\data\Sample01\Div6\Roi2\original\Porous')
#        interface1 = IMorphInterfaceTubes(r'D:\iMorph\06_iMorph_October_20\data\Compare\Div 6\Roi1\original\Porous')
        # interface1 = IMorphInterfacePlateauCellGraph(r'D:\iMorph\06_iMorph_October_20\data\Sample18\Div6\Roi1\original\Porous')
#        interface2 = IMorphInterfaceTubes(r'D:\iMorph\06_iMorph_October_20\data\Compare\Div 6\Roi1\original\Porous')
#        interface = IMorphInterfaceTubes(r'D:\iMorph\06_iMorph_October_20\data\Sample01\Div6\Roi2\original\Porous',addBorderCellFaceTypeNodes=True)
#        print(interface.pathToNodesFile)
#        print(interface.pathToTubesFile)
#        print(interface.pathToNodeThroatsFile)
        #

        interface1 = IMorphInterfacePlateauCellGraph(r'D:\iMorph\06_iMorph_October_20\database\data\Sample01\Div6\Cutout2\original\Porous')




#        print(interface.faces[4].edges)

#        for n in interface.nodes:
##            print(n.iMorphType)
#            if n.iMorphType == 'border_cell':
#                cellFaceNodes = [x for x in n.connectedNodes if x.iMorphType == 'border_cell_face']
#                print(len(cellFaceNodes))
#






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
            interface1.plotComplex(axes[0],showArrow=False,showLabel=False)
            names = ['graphNoBoundingBox']

            interface1.plotComplex(axes[1],showArrow=False,showLabel=False)
            interface1.boundingBox.plotBoundingBox(axes[1])
            names.append('graphWithBoundingBox')

            interface1.plotComplex(axes[2],showArrow=False,showLabel=False)
            for f in interface1.faces[20:25]:
                f.plotFace(axes[2],showNormalVec=False,showBarycenter=False,showLabel=False)
            names.append('graphWithSomeFaces')

            interface1.plotComplex(axes[3],showArrow=False,showLabel=False)
            interface1.plotFaces(axes[3],showNormalVec=False,showLabel=False,showBarycenter=False)
            names.append('graphWithAllFaces')







            # interface1.plotFaces(axes[0],showNormalVec=False,showLabel=False,showBarycenter=False)

            # interface1.plotComplex(axes[1],showArrow=False,showLabel=False)
            # interface1.plotFaces(axes[1],showNormalVec=False,showLabel=False,showBarycenter=False)

            # interface1.plotComplex(axes[2],showArrow=False,showLabel=False)
            # interface1.boundingBox.plotBoundingBox(axes[2])


            for i in range(4):
                axes[i].view_init(120,-90)
                pf.setAxesEqual(axes[i])
                pf.exportPNG(figs[i],'export/python_large_{}'.format(names[i]))
                pf.exportPNG(figs[i],'export/python_small_{}'.format(names[i]),width_mm=240,height_mm=200)

            # pf.exportPNG(figs[0],'export/pyhton0')
            # pf.exportPNG(figs[1],'export/pyhton1')
            # pf.exportPNG(figs[2],'export/pyhton2')


#            interface2.plotComplex(axes[2],showArrow=False,showLabel=False)
#            interface2.plotFaces(axes[3],showNormalVec=False,showLabel=False,showBarycenter=False)
#            interface.boundingBox.plotBoundingBox(axes[1])
#            pf.exportPNG(figs[0],filename='graphicExport/iMorph/pic2')

#    VTK
#---------------------------------------------------------------------
        elif plottingMethod == 'VTK' :
            cc.printBlue('Plot using VTK')
            cc.printRed('Not implemented')

#    TikZ
#---------------------------------------------------------------------
        elif plottingMethod == 'TikZ' :
            cc.printBlue('Plot using TikZ')
            cc.printRed('Not implemented')

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



