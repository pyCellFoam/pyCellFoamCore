# -*- coding: utf-8 -*-
#==============================================================================
# TITLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Jul 15 15:55:06 2020

'''
This is the explanation of the whole module and will be printed at the very 
beginning

Use - signs to declare a headline
--------------------------------------------------------------------------

* this is an item
* this is another one

#. numbered lists
#. are also possible


Maths
--------------------------------------------------------------------------

Math can be inline :math:`a^2 + b^2 = c^2` or displayed

.. math::

   (a + b)^2 = a^2 + 2ab + b^2

   (a - b)^2 = a^2 - 2ab + b^2

Always remember that the last line has to be blank

'''
#==============================================================================
#    IMPORTS
#==============================================================================
#-------------------------------------------------------------------------
#    Change to Main Directory
#-------------------------------------------------------------------------
import os
if __name__ == '__main__':
    os.chdir('.')


#-------------------------------------------------------------------------
#    Standard Libraries
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------


#    kCells
#--------------------------------------------------------------------


#    Complex & Grids
#--------------------------------------------------------------------


#    Tools
#--------------------------------------------------------------------
import tools.colorConsole as cc
import tools.placeFigures as pf
from tools import MyLogging


#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class Name:
    '''
    This is the explanation of this class.
    
    '''
    
#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__a',
                 '__b')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,a=0,b=''):
        '''
        This is the explanation of the __init__ method. 
        
        All parameters should be listed:
        
        :param int a: Some Number
        :param str b: Some String
        
        '''
        self.__a = a
        self.__b = b
        
        
    
#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getA(self): return self.__a
    def __setA(self,a): self.__a = a
    a = property(__getA,__setA)

    
#==============================================================================
#    METHODS
#==============================================================================
    
#-------------------------------------------------------------------------
#    Method 1
#-------------------------------------------------------------------------
    def __loadNodesConnectivity(self):
        '''
        Load nodes from the file which consists of the list of nodes and the
        connectivity table.
        
        '''
            
        
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
        
        myPrintInfo('Loading edges')        
        
        nodes = []
            
        with open(self.filepath) as fh:
            read = False
            for l in fh.readlines():
                
                if self.stopLineNode is not None:
                    if l.startswith(self.stopLineNode):
                        read = False
                if read:
#                    cc.printGreen(l.rstrip())
                    data = l.rstrip().split('\t')
                    nodes.append(Node(int(data[1])*self.__scaling,int(data[2])*self.__scaling,int(data[3])*self.__scaling,num=int(data[0])))
#                else:
#                    cc.printRed(l.rstrip())
                    
                if self.startLineNode is not None:
                    if l.startswith(self.startLineNode):
                        read = True
                        
            
                
            for (i,n) in enumerate(nodes):
                if n.num != i:
                    self.logger.error('Nodes are not numbered consistently: {} should have number {}'.format(n,i))
                
                
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
                                
                                
                
            
            
            
    def __loadEdgesConnectivity(self):
        '''
        Load edges from the file which consists of the list of nodes and the
        connectivity table.
        
        '''        
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
            
            
        edges = []
        with open(self.filepath) as fh:
            read = False
            for l in fh.readlines():
                
                if self.stopLineEdge is not None:
                    if l.startswith(self.stopLineEdge):
                        read = False
                        myPrintInfo('Stop reading edges')
                if read:
#                    cc.printGreen(l.rstrip())
                    data = l.rstrip().split('\t')
                    if int(data[0]) in self.__duplicateNodeNumbers:
                        currentNode = self.nodes[self.__duplicateNodeNumbers[int(data[0])]]
                    else:
                        currentNode = self.nodes[int(data[0])]
                    data.pop(0)
                    data.pop(0)
                    nodesToConnect = []
                    for e in data:
                        if int(e) in self.__duplicateNodeNumbers:
                            nodesToConnect.append(self.nodes[self.__duplicateNodeNumbers[int(e)]])
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
#                else:
#                    cc.printRed(l.rstrip())
                    
                if self.startLineEdge is not None:
                    if l.startswith(self.startLineEdge):
                        read = True
                        myPrintInfo('Start reading edges')
                        
                        
            self.edges = edges
        

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
    
    with MyLogging('Template'):

#-------------------------------------------------------------------------
#    Create some examples
#-------------------------------------------------------------------------
        
        
        test = Name()
        test.a = 5
        print('I am a template for object oriented python modules')
        print(test.method2(4,'abc'))
    


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
        
    

