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
#    Change to Main Directory
#-------------------------------------------------------------------------
import os
if __name__ == '__main__':
    os.chdir('../')


#-------------------------------------------------------------------------
#    Standard Libraries
#-------------------------------------------------------------------------
import numpy as np
from collections import deque
    
#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------


#    kCells
#--------------------------------------------------------------------
from kCells import Node, Edge, Face

#    Complex & Grids
#--------------------------------------------------------------------
from complex import PrimalComplex3D

#    Tools
#--------------------------------------------------------------------
import tools.colorConsole as cc
import tools.placeFigures as pf
from tools import MyLogging
import tools.tumcolor as tc
#from tools import MyVTK




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
        if True:
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
            
        super().setUp()
            
        
        
#-------------------------------------------------------------------------
#    Load nodes from graph file
#-------------------------------------------------------------------------        
    def loadNodesGraph(self,filename,startLine,stopLine,printLogToConsole=False):
        '''
        Load nodes from the file which consists of the list of nodes and the
        connectivity table.
        
        '''
            
        
        if not printLogToConsole:
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
        
        myPrintInfo('Loading edges')        
        
        #    Prepare lists
        #---------------------------------------------------------------------               
        nodes = []
 
        #    Check source file
        #---------------------------------------------------------------------         
        error = False
        
        if os.path.isfile(filename):
            myPrintInfo('Found file containing nodes')
        else:
            myPrintError('File containing nodes cannot be found')
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
                        myPrintDebug('Added node {}'.format(newNode))
                        
                    if l.startswith(startLine):
                        read = True
                        
                            
                
                    
                for (i,n) in enumerate(nodes):
                    if n.num != i:
                        myPrintError('Nodes are not numbered consistently: {} should have number {}'.format(n,i))
                    
                    
                for n1 in nodes:
                    for n2 in nodes[n1.num:]:
                        if not n1 == n2:
                            if np.linalg.norm(n1.coordinates-n2.coordinates)<1e-4:
                                myPrintInfo('Found duplicate nodes {} and {}'.format(n1,n2))
                                
                                if n2.num in self.__duplicateNodeNumbers:
                                    if n1.num in self.__duplicateNodeNumbers:
                                        if self.__duplicateNodeNumbers[n1.num] == self.__duplicateNodeNumbers[n2.num]:
                                            myPrintDebug('Found double duplicate: {} is a duplicate of {}, both are duplicates of  {}'.format(n2,n1,self.__duplicateNodeNumbers[n2.num]))
                                        else:
                                            myPrintError('{} and {} should be a duplicate of the same node, but are not, they are duplicates of: {} and {}'.format(n1,n2,self.__duplicateNodeNumbers[n1.num],self.__duplicateNodeNumbers[n2.num]))
                                    else:
                                        myPrintError('Expected double duplicate, but {} is not a duplicate yet'.format(n1))
                                else:
                                    self.__duplicateNodeNumbers[n2.num] = n1.num
                                    myPrintWarning('Added duplicate node. Current list: {}'.format(self.__duplicateNodeNumbers))
                                
                                
        self.nodes = nodes

#-------------------------------------------------------------------------
#    Load nodes from graph_nodes file
#-------------------------------------------------------------------------     
       
    def loadNodesGraphNodes(self,filename):
        '''
        
        '''
        #    Logging
        #---------------------------------------------------------------------        
        if True:
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
        
        myPrintInfo('Loading nodes')
        
        #    Prepare lists
        #---------------------------------------------------------------------               
        nodes = []
 
        #    Check source file
        #---------------------------------------------------------------------         
        error = False
        
        if os.path.isfile(filename):
            myPrintInfo('Found file containing nodes')
        else:
            myPrintError('File containing nodes cannot be found')
            error = True
            
  
        #    Read nodes
        #---------------------------------------------------------------------                   
        if not error:
            with open(filename) as fh:
                for l in fh.readlines()[6:]:
                    lineEntries = l.split('\t')
                    coordinates = lineEntries[1].split(',')
                    nodeNum = int(lineEntries[0])
                    myPrintDebug('Creating node {} at {}'.format(nodeNum,coordinates))
                    newNode = Node(int(coordinates[0])*self.__scaling,int(coordinates[1])*self.__scaling,int(coordinates[2])*self.__scaling,num=nodeNum)
                    nodes.append(newNode)
                    
                    nodeType = lineEntries[2]
                    newNode.iMorphType = nodeType
                    if nodeType == 'cell':
                        myPrintDebug('Node {} is of type "cell"'.format(newNode))
                    elif nodeType == 'border_cell':
                        myPrintDebug('Node {} is of type "border_cell"'.format(newNode))
                        newNode.color = tc.TUMGreen()
                    elif nodeType == 'border_cell_face':
                        myPrintDebug('Node {} is of type "border_cell"'.format(newNode))
                        newNode.color = tc.TUMRose()
                    elif nodeType == 'throat':
                        myPrintDebug('Node {} is of type "throat"'.format(newNode))
                        newNode.color = tc.TUMBlack()
                    elif nodeType == 'border_throat':
                        myPrintDebug('Node {} is of type "border_throat"'.format(newNode))
                        newNode.color = tc.TUMGrayMedium()
                        
                    else:
                        myPrintError('Unknown Node Type "{}"'.format(nodeType))
        
        
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
        if not printLogToConsole:
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
            
            
        #    Prepare lists
        #---------------------------------------------------------------------         
        edges = []
        
  
        #    Check source file
        #---------------------------------------------------------------------       
        error = False
        
        if os.path.isfile(filename):
            myPrintInfo('Found file containing edges')
        else:
            myPrintError('File containing nodes cannot be found')
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
                                    myPrintWarning('Ignoring edge between identical nodes: {} - {}'.format(currentNode,n))
                                else:
                                    newEdge = Edge(currentNode,n)
                                    edges.append(newEdge)
                                    myPrintDebug('Added edge {} between {} and {}'.format(newEdge,newEdge.startNode,newEdge.endNode))
                        
                    if l.startswith(startLine):
                        read = True
                        myPrintInfo('Start reading edges')
                            
                            
                self.edges = edges


#-------------------------------------------------------------------------
#    Load edges from graph_tubes file
#-------------------------------------------------------------------------     
        

    def loadEdgesGraphTubes(self,filename):
        '''
        
        '''
        #    Logging
        #--------------------------------------------------------------------- 
        
        if True:
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
        
        myPrintInfo('Loading edges')


        #    Prepare lists
        #---------------------------------------------------------------------         
        edges = []
        
  
        #    Check source file
        #---------------------------------------------------------------------       
        error = False
        
        if os.path.isfile(filename):
            myPrintInfo('Found file containing edges')
        else:
            myPrintError('File containing nodes cannot be found')
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
                    myPrintDebug('Creating edge {} from node {} to {}'.format(edgeNum,startNodeNum,endNodeNum))
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
        #    Logging
        #---------------------------------------------------------------------         
        if True:
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
        openThroats = []
        closedThroats = []
        
#        self.__boundingBox = BoundingBox(self.xLim,self.yLim,self.zLim)
#        6
        
        
        #    Check source file
        #---------------------------------------------------------------------       
        
        error = False
        
        if os.path.isfile(filename):
            myPrintInfo('Found file containing faces')
        else:
            myPrintError('File containing nodes cannot be found')
            error = True
         
            
        #    Read faces
        #---------------------------------------------------------------------     
        readFaces = False
        maxNumberOfLines = float('inf')
        # maxNumberOfLines = 5
        
        numberOfClosedThroats = 0
        numberOfUniqueClosedThroats = 0
        numberOfOpenThroats = 0
        
        numberOfThroatsWithLessThan2Nodes = 0
        
        
        
        createClosedThroats = True
        createOpenThroats = True        
        
        currentLineNumber = 0
        if not error:
            with open(self.pathToNodeThroatsFile) as fh:
                
                # Loop over lines in file
                for l in fh.readlines():
                    if readFaces and currentLineNumber < maxNumberOfLines:
                        currentLineNumber += 1
                        data = l.rstrip().split('\t')
                        if len(data)>1:     # filter out empty lines (mostly at the end of the file)
                            indexNode = int(data[0])
                            numberOfThroats = int(data[1])
                            position = 2
                            
                            myPrintDebug('Creating {} throats that contain node {}'.format(numberOfThroats,self.nodes[indexNode])) 
                            
                            
                            # Loop over throats the current node is part of
                            for i in range(numberOfThroats):
                                throatStr = data[position+1:position+1+int(data[position])]
                                throat = [int(t) for t in throatStr]
                                position += int(data[position])+1
                                myPrintDebug('Checking throat {} that consists of {} nodes: {}'.format(i,len(throat),throat))
                                
                                if throat[0] == throat [-1]:
                                    myPrintInfo('Closed Throat')
                                    numberOfClosedThroats += 1
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
                                        myPrintDebug('Throat with nodes {} already exists'.format(throat))
                                    else:
                                        myPrintDebug('Creating throat with nodes {}'.format(throat))
                                        numberOfUniqueClosedThroats += 1
                                        closedThroats.append(throatNodes)
                                        # myPrintDebug('Nodes in current throat: {}'.format(throat))
                                        if len(throat) > 2:
                                            myPrintDebug('A face with {} nodes is possible'.format(len(throat)))
                                            
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
#                                                     myPrintDebug('Found edge {} that connects node {} and {}. So far found: {}'.format(edgesForFace[-1],numStart,numEnd,edgesForFace))
                                                    
#                                                 else:
#                                                     myPrintWarning('Could not find an edge that connects node {} and {}'.format(numStart,numEnd))
                                                    
#                                                     newEdge = Edge(self.nodes[numStart],self.nodes[numEnd])
#                                                     myPrintWarning('Creating new edge {} from {} to {}'.format(newEdge,self.nodes[numStart],self.nodes[numEnd]))
#                                                     self.edges.append(newEdge)
#                                                     edgesForFace.append(newEdge)
#                                                     foundAllEdges=True
                                                    
                                                    
                                                    
                                                    
                                                    
#                                             if foundAllEdges:
#                                                 myPrintDebug('Found all edges {}'.format(edgesForFace))
#                                                 newFace = Face(edgesForFace,triangulate=True,sortEdges=True)
#                                                 faces.append(newFace)
#                                                 if newFace.isDeleted:
#                                                     myPrintError('Face creation was not succesful')
# #                                                for e in edgesForFace:
# #                                                    e.color = tc.TUMBlack()
                                    
                                    
                                            
                                            
                                        else:
                                            myPrintWarning('A face with {} nodes is not possible'.format(len(throat)))
                                            numberOfThroatsWithLessThan2Nodes += 1
                                            
                                            
                                            
                                            
                                    
                                    
                ##########################################################################################################################                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                    
                                else:
                                    myPrintInfo('Open Throat')
                                    numberOfOpenThroats += 1
                                    
                                    myPrintDebug('Open throat: {}'.format(throat))
                                    
                                    throatExistsAlready = self.__checkExists(throat,openThroats)
                                    
                                    if throatExistsAlready:
                                        myPrintDebug('Throat with nodes {} already exists'.format(throat))
                                    else:
                                        myPrintDebug('Creating throat with nodes {}'.format(throat))                                    
                                    
                                    
                                    
                                    edgesForFace = self.__findEdgesFromNodeNumbers(throat)
                                    
                                    # cc.printYellow(self.nodes[throat[0]].iMorphType,self.nodes[throat[-1]].iMorphType)
                                    
                                    # cc.printYellow(edgesForFace[0].startNode.iMorphType)
                                    
                                    nodeStart = self.nodes[throat[0]]
                                    nodeEnd = self.nodes[throat[-1]]
                                    
                                    (dist1,side1) = self.boundingBox.distToBoundingBox(nodeStart.coordinates)
                                    (dist2,side2) = self.boundingBox.distToBoundingBox(nodeEnd.coordinates)
                                    
                                    if dist1 < 0.1 and dist2 < 0.1:
                                        cc.printYellow(side1,side2)
                                        
                                        if side1 == side2:
                                            newEdge = Edge(nodeEnd,nodeStart)
                                            edgesForFace.append(newEdge)
                                            
                                                                                        
                                            if edgesForFace is not None and createOpenThroats:
                                                if len(edgesForFace) > 2:
                                                    newFace = Face(edgesForFace,triangulate=True,sortEdges=True)
                                                    faces.append(newFace)                                            
                                                else:
                                                    for e in edgesForFace:
                                                        e.color = tc.TUMRose()
                                            
                                            
                                        
                                    # cc.printYellow(dist,side)
                                    # if dist > 0.5:
                                    #     edgesForFace[0].startNode.color = tc.TUMRose()
                                    
                                    if numberOfOpenThroats == -1:
                                        for e in edgesForFace:
                                            e.color = tc.TUMRose()
                                    
                                    
                                    
                            
                            
                    if l.startswith('indice node'):
                        readFaces  = True
                        myPrintDebug('Found start for throats')            
                        
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
        cc.printMagenta('X: {}'.format(self.xLim))
        cc.printMagenta('Y: {}'.format(self.yLim))
        cc.printMagenta('Z: {}'.format(self.zLim))
        cc.printMagenta()
        cc.printMagenta('='*80)
        
       


#-------------------------------------------------------------------------
#    Check if list already exists in list of lists
#-------------------------------------------------------------------------  
    def __checkExists(self,currentList,listOfLists):
        
        entryExistsAlready = False
        
        currentDeque = deque(currentList)
        
        for _ in range(len(currentList)):
            if list(currentDeque) in listOfLists or list(reversed(currentDeque)) in listOfLists:
                entryExistsAlready = True
                break
            currentDeque.rotate()    
            
        return entryExistsAlready
       


#-------------------------------------------------------------------------
#    Find edges
#-------------------------------------------------------------------------  
    def __findEdgesFromNodeNumbers(self,nodeNumbers,logToFile=True):
        
        #    Logging
        #---------------------------------------------------------------------         
        if logToFile:
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
            
        
        #    Preparation
        #---------------------------------------------------------------------   
        myPrintDebug('Searching for edges that connect nodes {}'.format(nodeNumbers))
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
                myPrintDebug('Found edge {} that connects node {} and {}. So far found: {}'.format(edgesForFace[-1],numStart,numEnd,edgesForFace))
                
            else:
                myPrintWarning('Could not find an edge that connects node {} and {}'.format(numStart,numEnd))
                foundAllEdges = False
                
        #    Check results
        #---------------------------------------------------------------------        
        for e in edgesForFace:
            if not e in self.edges and not -e in self.edges:
                myPrintError('Edge {} is needed to connect nodes {} and {}, but is not part of the actual edges'.format(e,e.startNode,e.endNode))
                
        
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
        elif plottingMethod == 'VTK' :
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
                
        
    
    

