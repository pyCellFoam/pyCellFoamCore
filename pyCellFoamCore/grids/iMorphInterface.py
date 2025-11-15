# -*- coding: utf-8 -*-
#==============================================================================
# IMORPH INTERFACE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Dec  6 09:59:12 2019

'''


'''

#==============================================================================
#    IMPORTS
#==============================================================================

#-------------------------------------------------------------------------
#    Standard Libraries
#-------------------------------------------------------------------------
import os
import numpy as np
from collections import deque
import logging

#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------


#    kCells
#--------------------------------------------------------------------
from pyCellFoamCore.k_cells.node.node import Node
from pyCellFoamCore.k_cells.edge.edge import Edge
from pyCellFoamCore.k_cells.face.face import Face

#    Complex & Grids
#--------------------------------------------------------------------
from pyCellFoamCore.complex.primalComplex3D import PrimalComplex3D

#    Tools
#--------------------------------------------------------------------
import pyCellFoamCore.tools.colorConsole as cc
import pyCellFoamCore.tools.placeFigures as pf
import pyCellFoamCore.tools.tumcolor as tc
#from tools import MyVTK

#==============================================================================
#    LOGGING
#==============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class IMorphInterface(PrimalComplex3D):
    '''
    This is the explanation of this class.

    '''

#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__pathToPorousFolder',
                 '__scaling',
                 '__iMorphTypes')
#                 '__duplicateNodeNumbers')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,pathToPorousFolder,scaling=0.03):
        '''
        :param str filepath: path to iMorph output file

        '''
        _log.info("Initialize iMorphInterface")
        self.__pathToPorousFolder = pathToPorousFolder
#        self.__filepathNodes = folderpath + r'\Graphs\network_balls_plateauCellGraph_Nodes.txt'
#        self.__filepathEdges = folderpath + r'\Graphs\network_balls_plateauCellGraph_Tubes.txt'
#        self.__filepathNodeThroats = folderpath
        self.__scaling = scaling
        self.__iMorphTypes = {0: 'border_cell',
                              2: 'cell',
                              3: 'border_cell_face'}

#        self.__duplicateNodeNumbers = {}

        super().__init__()


















#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getPathToPorousFolder(self): return self.__pathToPorousFolder
    pathToPorousFolder = property(__getPathToPorousFolder)
    '''

    '''

    def __getScaling(self): return self.__scaling
    scaling = property(__getScaling)
    '''

    '''

    def __getIMorphTypes(self): return self.__iMorphTypes
    iMorphTypes = property(__getIMorphTypes)
    '''

    '''











#==============================================================================
#    METHODS
#==============================================================================


#-------------------------------------------------------------------------
#    Set up
#-------------------------------------------------------------------------

    def setUp(self):

        super().setUp()



#-------------------------------------------------------------------------
#    Load nodes from graph file
#-------------------------------------------------------------------------
    def loadNodesGraph(self,filename,startLine,stopLine,printLogToConsole=False):
        '''
        Load nodes from the file which consists of the list of nodes and the
        connectivity table.

        '''



        _log.info('Loading edges')

        #    Prepare lists
        #---------------------------------------------------------------------
        nodes = []

        #    Check source file
        #---------------------------------------------------------------------
        error = False

        if os.path.isfile(filename):
            _log.info('Found file containing nodes')
        else:
            _log.error('File containing nodes cannot be found')
            error = True


        #    Read nodes
        #---------------------------------------------------------------------
        if not error:
            with open(filename) as fh:
                read = False
                for l in fh.readlines():

                    if l.startswith(stopLine):
                        read = False
                    if read:
                        data = l.rstrip().split('\t')
                        print(data)
                        newNode = Node(int(data[1])*self.__scaling,int(data[2])*self.__scaling,int(data[3])*self.__scaling,num=int(data[0]))
                        nodes.append(newNode)
                        _log.debug('Added node {}'.format(newNode))

                    if l.startswith(startLine):
                        read = True




                for (i,n) in enumerate(nodes):
                    if n.num != i:
                        _log.error('Nodes are not numbered consistently: {} should have number {}'.format(n,i))


                for n1 in nodes:
                    for n2 in nodes[n1.num:]:
                        if not n1 == n2:
                            if np.linalg.norm(n1.coordinates-n2.coordinates)<1e-4:
                                _log.info('Found duplicate nodes {} and {}'.format(n1,n2))

                                if n2.num in self.__duplicateNodeNumbers:
                                    if n1.num in self.__duplicateNodeNumbers:
                                        if self.__duplicateNodeNumbers[n1.num] == self.__duplicateNodeNumbers[n2.num]:
                                            _log.debug('Found double duplicate: {} is a duplicate of {}, both are duplicates of  {}'.format(n2,n1,self.__duplicateNodeNumbers[n2.num]))
                                        else:
                                            _log.error('{} and {} should be a duplicate of the same node, but are not, they are duplicates of: {} and {}'.format(n1,n2,self.__duplicateNodeNumbers[n1.num],self.__duplicateNodeNumbers[n2.num]))
                                    else:
                                        _log.error('Expected double duplicate, but {} is not a duplicate yet'.format(n1))
                                else:
                                    self.__duplicateNodeNumbers[n2.num] = n1.num
                                    _log.warning('Added duplicate node. Current list: {}'.format(self.__duplicateNodeNumbers))


        self.nodes = nodes

#-------------------------------------------------------------------------
#    Load nodes from graph_nodes file
#-------------------------------------------------------------------------

    def loadNodesGraphNodes(self,filename):
        '''

        '''

        _log.info('Loading nodes')

        #    Prepare lists
        #---------------------------------------------------------------------
        nodes = []

        #    Check source file
        #---------------------------------------------------------------------
        error = False

        if os.path.isfile(filename):
            _log.info('Found file containing nodes')
        else:
            _log.error('File containing nodes cannot be found')
            error = True


        #    Read nodes
        #---------------------------------------------------------------------
        if not error:
            with open(filename) as fh:
                for l in fh.readlines()[6:]:
                    lineEntries = l.split('\t')
                    coordinates = lineEntries[1].split(',')
                    nodeNum = int(lineEntries[0])
                    _log.debug('Creating node {} at {}'.format(nodeNum,coordinates))
                    newNode = Node(int(coordinates[0])*self.__scaling,int(coordinates[1])*self.__scaling,int(coordinates[2])*self.__scaling,num=nodeNum)
                    nodes.append(newNode)

                    nodeType = lineEntries[2]
                    newNode.iMorphType = nodeType
                    if nodeType == 'cell':
                        _log.debug('Node {} is of type "cell"'.format(newNode))
                    elif nodeType == 'border_cell':
                        _log.debug('Node {} is of type "border_cell"'.format(newNode))
                        newNode.color = tc.TUMGreen()
                    elif nodeType == 'border_cell_face':
                        _log.debug('Node {} is of type "border_cell"'.format(newNode))
                        newNode.color = tc.TUMRose()
                    elif nodeType == 'throat':
                        _log.debug('Node {} is of type "throat"'.format(newNode))
                        newNode.color = tc.TUMBlack()
                    elif nodeType == 'border_throat':
                        _log.debug('Node {} is of type "border_throat"'.format(newNode))
                        newNode.color = tc.TUMGrayMedium()

                    else:
                        _log.error('Unknown Node Type "{}"'.format(nodeType))


        for n in nodes:
            n.showLabel=False
        self.nodes = nodes

        return error




#-------------------------------------------------------------------------
#    Load edges from graph file
#-------------------------------------------------------------------------



    def loadEdgesGraph(self,filename,startLine,printLogToConsole=False):
        '''
        Load edges from the file which consists of the list of nodes and the
        connectivity table.

        '''

        #    Prepare lists
        #---------------------------------------------------------------------
        edges = []


        #    Check source file
        #---------------------------------------------------------------------
        error = False

        if os.path.isfile(filename):
            _log.info('Found file containing edges')
        else:
            _log.error('File containing nodes cannot be found')
            error = True


        #    Read edges
        #---------------------------------------------------------------------
        if not error:
            duplicateNodeNumbers = []
            with open(filename) as fh:
                read = False
                for l in fh.readlines():

                    if read:
                        data = l.rstrip().split('\t')
                        if int(data[0]) in duplicateNodeNumbers:
                            currentNode = self.nodes[self.__duplicateNodeNumbers[int(data[0])]]
                        else:
                            currentNode = self.nodes[int(data[0])]
                        data.pop(0)
                        data.pop(0)
                        nodesToConnect = []
                        for e in data:
                            if int(e) in duplicateNodeNumbers:
                                nodesToConnect.append(self.nodes[duplicateNodeNumbers[int(e)]])
                            else:
                                nodesToConnect.append(self.nodes[int(e)])
                        for n in nodesToConnect:
                            if not n in currentNode.connectedNodes:
                                if currentNode == n:
                                    _log.warning('Ignoring edge between identical nodes: {} - {}'.format(currentNode,n))
                                else:
                                    newEdge = Edge(currentNode,n)
                                    edges.append(newEdge)
                                    _log.debug('Added edge {} between {} and {}'.format(newEdge,newEdge.startNode,newEdge.endNode))

                    if l.startswith(startLine):
                        read = True
                        _log.info('Start reading edges')


                self.edges = edges


#-------------------------------------------------------------------------
#    Load edges from graph_tubes file
#-------------------------------------------------------------------------


    def loadEdgesGraphTubes(self,filename):
        '''

        '''
        #    Logging
        #---------------------------------------------------------------------


        _log.info('Loading edges')


        #    Prepare lists
        #---------------------------------------------------------------------
        edges = []


        #    Check source file
        #---------------------------------------------------------------------
        error = False

        if os.path.isfile(filename):
            _log.info('Found file containing edges')
        else:
            _log.error('File containing nodes cannot be found')
            error = True


        #    Read edges
        #---------------------------------------------------------------------
        if not error:
            with open(filename) as fh:
                for l in fh.readlines()[7:]:
                    lineEntries = l.split('\t')
                    edgeNum = int(lineEntries[0])
                    startNodeNum = int(lineEntries[1])
                    endNodeNum = int(lineEntries[2])
                    _log.debug('Creating edge {} from node {} to {}'.format(edgeNum,startNodeNum,endNodeNum))
                    edges.append(Edge(self.nodes[startNodeNum],self.nodes[endNodeNum],num=edgeNum))


        #    Store results
        #---------------------------------------------------------------------
        for e in edges:
            e.showLabel=False


        self.edges = edges
        return error





#-------------------------------------------------------------------------
#    Load faces from
#-------------------------------------------------------------------------

    def loadFaces(self,filename):
        '''

        '''

        _log.info('Loading faces')


        #    Prepare lists
        #---------------------------------------------------------------------
        faces = []
        openThroats = []
        closedThroats = []

#        self.__boundingBox = BoundingBox(self.xLim,self.yLim,self.zLim)
#        6


        #    Check source file
        #---------------------------------------------------------------------

        error = False

        if os.path.isfile(filename):
            _log.info('Found file containing faces')
        else:
            _log.error('File containing nodes cannot be found')
            error = True


        #    Read faces
        #---------------------------------------------------------------------
        readFaces = False
        maxNumberOfLines = float('inf')
        # maxNumberOfLines = 5
        # max_number_of_open_throats = 5

        numberOfClosedThroats = 0
        numberOfUniqueClosedThroats = 0
        numberOfOpenThroats = 0
        number_of_throats_not_same_side = 0
        number_of_throats_neighbouring_sides = 0
        number_of_throats_side_not_found = 0

        numberOfThroatsWithLessThan2Nodes = 0

        idx_add_nodes = 10000

        createClosedThroats = True
        createOpenThroats = True



        currentLineNumber = 0
        if not error:
            with open(self.pathToNodeThroatsFile) as fh:

                # Loop over lines in file
                for l in fh.readlines():
                    if readFaces and currentLineNumber < maxNumberOfLines:  # and numberOfOpenThroats < max_number_of_open_throats:
                        currentLineNumber += 1
                        data = l.rstrip().split('\t')
                        if len(data)>1:     # filter out empty lines (mostly at the end of the file)
                            indexNode = int(data[0])
                            numberOfThroats = int(data[1])
                            position = 2

                            _log.debug('Creating {} throats that contain node {}'.format(numberOfThroats,self.nodes[indexNode]))


                            # Loop over throats the current node is part of
                            for i in range(numberOfThroats):
                                # if numberOfOpenThroats >= max_number_of_open_throats:
                                #     break
                                throatStr = data[position+1:position+1+int(data[position])]
                                throat = [int(t) for t in throatStr]
                                position += int(data[position])+1
                                _log.debug('Checking throat {} that consists of {} nodes: {}'.format(i,len(throat),throat))

                                if throat[0] == throat [-1]:

                                    numberOfClosedThroats += 1
                                    _log.debug("Checking closed throat %s with nodes: %s", numberOfClosedThroats, throat)

                                    throatNodes = throat[:-1]





#             ##########################################################################################################################



                                    # throatExistsAlready = False
                                    # throatDeque = deque(throatNodes)
                                    # for i in range(len(throatNodes)):
                                    #     if list(throatDeque) in closedThroats or list(reversed(throatDeque)) in closedThroats:
                                    #         throatExistsAlready = True
                                    #         break
                                    #     throatDeque.rotate()

                                    throatExistsAlready = self.__checkExists(throatNodes,closedThroats)

                                    if throatExistsAlready:
                                        _log.debug('Throat with nodes {} already exists'.format(throat))
                                    else:
                                        _log.info('Creating closed throat with nodes {}'.format(throat))
                                        numberOfUniqueClosedThroats += 1
                                        closedThroats.append(throatNodes)
                                        # _log.debug('Nodes in current throat: {}'.format(throat))
                                        if len(throat) > 2:
                                            _log.debug('A face with {} nodes is possible'.format(len(throat)))

                                            edgesForFace = self.__findEdgesFromNodeNumbers(throat)


                                            if edgesForFace is not None and createClosedThroats:
                                                newFace = Face(edgesForFace,triangulate=True,sortEdges=True)
                                                faces.append(newFace)


#                                             foundAllEdges = True
#                                             edgesForFace = []
#                                             cycleThroat = throat[:]
#                                             if not cycleThroat[0] == cycleThroat [-1]:
#                                                 cycleThroat.append(throat[0])
#                                             for numStart,numEnd in zip(cycleThroat[:-1],cycleThroat[1:]):
#                                                 found = False
#                                                 n = self.nodes[numStart]
#                                                 # IMPORTANT: Must check if edge is part of the edges defined by iMorph, because due to triangulation new edges with unknown numbers are created
#                                                 for e in n.edges:
#                                                     if e.startNode.num == numStart and e.endNode.num ==numEnd and e in self.edges:
#                                                         found = True
#                                                         edgesForFace.append(e)
#                                                     if e.startNode.num == numEnd and e.endNode.num ==numStart and e in self.edges:
#                                                         found = True
#                                                         edgesForFace.append(-e)
#                                                 if found:
#                                                     _log.debug('Found edge {} that connects node {} and {}. So far found: {}'.format(edgesForFace[-1],numStart,numEnd,edgesForFace))

#                                                 else:
#                                                     _log.warning('Could not find an edge that connects node {} and {}'.format(numStart,numEnd))

#                                                     newEdge = Edge(self.nodes[numStart],self.nodes[numEnd])
#                                                     _log.warning('Creating new edge {} from {} to {}'.format(newEdge,self.nodes[numStart],self.nodes[numEnd]))
#                                                     self.edges.append(newEdge)
#                                                     edgesForFace.append(newEdge)
#                                                     foundAllEdges=True





#                                             if foundAllEdges:
#                                                 _log.debug('Found all edges {}'.format(edgesForFace))
#                                                 newFace = Face(edgesForFace,triangulate=True,sortEdges=True)
#                                                 faces.append(newFace)
#                                                 if newFace.is_deleted:
#                                                     _log.error('Face creation was not succesful')
# #                                                for e in edgesForFace:
# #                                                    e.color = tc.TUMBlack()




                                        else:
                                            _log.warning('A face with {} nodes is not possible'.format(len(throat)))
                                            numberOfThroatsWithLessThan2Nodes += 1






                ##########################################################################################################################








                                else:

                                    numberOfOpenThroats += 1
                                    _log.debug("Checking open throat %s with nodes: %s", numberOfOpenThroats, throat)





                                    throatExistsAlready = self.__checkExists(throat,openThroats)

                                    if throatExistsAlready:
                                        _log.debug('Open throat with nodes {} already exists'.format(throat))
                                    else:
                                        _log.info('Creating open throat with nodes {}'.format(throat))
                                        openThroats.append(throat)



                                        edgesForFace = self.__findEdgesFromNodeNumbers(throat)

                                        # cc.printYellow(self.nodes[throat[0]].iMorphType,self.nodes[throat[-1]].iMorphType)

                                        # cc.printYellow(edgesForFace[0].startNode.iMorphType)

                                        nodeStart = self.nodes[throat[0]]
                                        nodeEnd = self.nodes[throat[-1]]

                                        (dist1,side1) = self.boundingBox.distToBoundingBox(nodeStart.coordinates)
                                        (dist2,side2) = self.boundingBox.distToBoundingBox(nodeEnd.coordinates)

                                        if dist1 < 0.2 and dist2 < 0.2:
                                            cc.printYellow(side1,side2)

                                            if side1 == side2:
                                                _log.critical("Nearest sides are the same: %s", side1)
                                                newEdge = Edge(nodeEnd,nodeStart)
                                                edgesForFace.append(newEdge)
                                                newEdge.color = tc.TUMBlack()
                                                self.edges.append(newEdge)



                                                if edgesForFace is not None and createOpenThroats:
                                                    if len(edgesForFace) > 2:
                                                        newFace = Face(edgesForFace,triangulate=True,sortEdges=True)
                                                        newFace.color = tc.TUMRose()
                                                        faces.append(newFace)
                                                    else:
                                                        for e in edgesForFace:
                                                            e.color = tc.TUMRose()

                                            else:
                                                number_of_throats_not_same_side += 1
                                                _log.critical("Nearest sides are not the same")

                                                touching_edge = self.boundingBox.check_neighbouring_sides(side1, side2)
                                                if touching_edge is not None:
                                                    _log.critical("Nearest sides are neighbours touching in edge %s", touching_edge)
                                                    number_of_throats_neighbouring_sides += 1

                                                    intermediateNodeCoordinates = touching_edge.get_intermediate_point(nodeStart.coordinates, nodeEnd.coordinates)
                                                    intermediateNode = Node(intermediateNodeCoordinates[0], intermediateNodeCoordinates[1], intermediateNodeCoordinates[2], num=idx_add_nodes)
                                                    idx_add_nodes += 1
                                                    intermediateNode.color = tc.TUMBlack()
                                                    _log.critical("Creating intermediate node at %s", intermediateNode.coordinates)

                                                    self.nodes.append(intermediateNode)

                                                    new_edge1 = Edge(nodeStart, intermediateNode)
                                                    new_edge2 = Edge(intermediateNode, nodeEnd)
                                                    new_edge1.color = tc.TUMMustard()
                                                    new_edge2.color = tc.TUMMustard()

                                                    self.edges.append(new_edge1)
                                                    self.edges.append(new_edge2)

                                                    edgesForFace.append(new_edge1)
                                                    edgesForFace.append(new_edge2)

                                                    if edgesForFace is not None and createOpenThroats:
                                                        if len(edgesForFace) > 2:
                                                            newFace = Face(edgesForFace,triangulate=True,sortEdges=True)
                                                            newFace.color = tc.TUMLightBlue()
                                                            faces.append(newFace)
                                                        else:
                                                            for e in edgesForFace:
                                                                e.color = tc.TUMRose()



                                                else:
                                                    _log.critical("Nearest sides are not neighbours")
                                        else:
                                            number_of_throats_side_not_found +=1
                                            _log.critical("Could not find nearby sides. dist1 = %s, dist2 = %s", dist1, dist2)



                                        # cc.printYellow(dist,side)
                                        # if dist > 0.5:
                                        #     edgesForFace[0].startNode.color = tc.TUMRose()

                                        if numberOfOpenThroats == -1:
                                            for e in edgesForFace:
                                                e.color = tc.TUMRose()





                    if l.startswith('indice node'):
                        readFaces  = True
                        _log.debug('Found start for throats')

        self.faces = faces

        cc.printMagenta()
        cc.printMagenta()
        cc.printMagenta('='*80)
        cc.printMagenta()
        cc.printMagenta('FACE CREATION SUMMARY')
        cc.printMagenta('-'*40)
        cc.printMagenta()
        cc.printMagenta('Found {} closed throats, of which {} are unique and {} have two or less nodes'.format(numberOfClosedThroats,numberOfUniqueClosedThroats,numberOfThroatsWithLessThan2Nodes))
        cc.printMagenta('Found {} open throats'.format(numberOfOpenThroats))
        cc.printMagenta()
        cc.printMagenta('Found {} throats where the nearest boundaries are not on the same side'.format(number_of_throats_not_same_side))
        cc.printMagenta('Found {} throats that are on neighbouring sides'.format(number_of_throats_neighbouring_sides))
        cc.printMagenta('Found {} throats where the nearest boundary could not be found'.format(number_of_throats_side_not_found))
        cc.printMagenta()
        cc.printMagenta('X: {}'.format(self.xLim))
        cc.printMagenta('Y: {}'.format(self.yLim))
        cc.printMagenta('Z: {}'.format(self.zLim))
        cc.printMagenta()
        cc.printMagenta('='*80)




#-------------------------------------------------------------------------
#    Check if list already exists in list of lists
#-------------------------------------------------------------------------
    def __checkExists(self,currentList,listOfLists):

        _log.debug("Checking list %s for existence", currentList)
        # _log.debug("Existing lists: %s", listOfLists)

        entryExistsAlready = False

        currentDeque = deque(currentList)

        for _ in range(len(currentList)):
            if list(currentDeque) in listOfLists or list(reversed(currentDeque)) in listOfLists:
                entryExistsAlready = True
                break
            currentDeque.rotate()


        # current_list_sorted = currentList[:]
        # current_list_sorted.sort()

        # entry_exists_already_new = False
        # for list_to_check in listOfLists:
        #     list_to_check_sorted = list_to_check[:]
        #     list_to_check_sorted.sort()
        #     if current_list_sorted == list_to_check_sorted:
        #         _log.warning("%s == %s", currentList, list_to_check)
        #         entry_exists_already_new = True
        #         break


        # if entryExistsAlready != entry_exists_already_new:
        #     _log.error("Got different results for new and old method. Old: %s, New: %s", entryExistsAlready, entry_exists_already_new)

        # _log.warning("Old: %s", entryExistsAlready)
        # _log.warning("New: %s", entry_exists_already_new)

        return entryExistsAlready



#-------------------------------------------------------------------------
#    Find edges
#-------------------------------------------------------------------------
    def __findEdgesFromNodeNumbers(self,nodeNumbers,logToFile=True):



        #    Preparation
        #---------------------------------------------------------------------
        _log.debug('Searching for edges that connect nodes {}'.format(nodeNumbers))
        foundAllEdges = True
        edgesForFace = []

        #    Cycle through node number pairs
        #---------------------------------------------------------------------
        for numStart,numEnd in zip(nodeNumbers[:-1],nodeNumbers[1:]):
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
                _log.debug('Found edge {} that connects node {} and {}. So far found: {}'.format(edgesForFace[-1],numStart,numEnd,edgesForFace))

            else:
                _log.warning('Could not find an edge that connects node {} and {}'.format(numStart,numEnd))
                foundAllEdges = False

        #    Check results
        #---------------------------------------------------------------------
        for e in edgesForFace:
            if not e in self.edges and not -e in self.edges:
                _log.error('Edge {} is needed to connect nodes {} and {}, but is not part of the actual edges'.format(e,e.startNode,e.endNode))


        if foundAllEdges:
            return edgesForFace
        else:
            return None











#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    with MyLogging('Interface'):



        interface1 = IMorphInterface(r'D:\iMorph\05_iMorph_July_20\data\data\Kelvin\Div 6\Roi1\original\Porous')
        interface2 = IMorphInterface(r'D:\iMorph\05_iMorph_July_20\data\data\Kelvin\Div 6\Roi1\original\Porous',scaling=5)
        print(interface1,'- scaling:',interface1.scaling)
        print(interface2,'- scaling:',interface2.scaling)









#-------------------------------------------------------------------------
#    Plotting
#-------------------------------------------------------------------------

        # Choose plotting method. Possible choices: pyplot, VTK, TikZ, animation, doc, None
        plottingMethod = 'None'


#    Disabled
#---------------------------------------------------------------------
        if plottingMethod is None or plottingMethod == 'None':
            cc.printBlue('Plotting disabled')

#    Pyplot
#---------------------------------------------------------------------
        elif plottingMethod == 'pyplot':
            cc.printBlue('Plot using pyplot')
            (figs,axes) = pf.getFigures()
            cc.printRed('Not implemented')
#            for n in interface1.nodes:
#                n.plotNode(axes[0],showLabel=False)
#            for e in interface1.edges:
#                e.plotEdge(axes[0],showLabel=False,showArrow=False)
#
#
#            for n in interface2.nodes:
#                n.plotNode(axes[1],showLabel=False)
#            for e in interface2.edges:
#                e.plotEdge(axes[1],showLabel=False,showArrow=False)

#    VTK
#---------------------------------------------------------------------
        elif plottingMethod == 'VTK':
            cc.printBlue('Plot using VTK')
            cc.printRed('Not implemented')
#            myVTK = MyVTK()
#            for n in interface.nodes:
#                n.plotNodeVtk(myVTK,showLabel=False)
#            for e in interface.edges:
#                e.plotEdgeVtk(myVTK,showLabel=False)
#            myVTK.start()

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
            cc.printRed('Not implemented')
#            test.plotDoc()

#    Unknown
#---------------------------------------------------------------------
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))
