# -*- coding: utf-8 -*-
#==============================================================================
# IMPORH INTERFACE FOR PLATEAU GRAPH
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Nov 18 14:54:11 2020

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


#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------


#    kCells
#--------------------------------------------------------------------
from pyCellFoamCore.k_cells.node.node import NodePlotly
from pyCellFoamCore.k_cells.edge.baseEdge import EdgePlotly
from pyCellFoamCore.k_cells.face.baseFace import FacePlotly

#    Complex & Grids
#--------------------------------------------------------------------
from pyCellFoamCore.grids.iMorphInterface import IMorphInterface


#    Tools
#--------------------------------------------------------------------
import pyCellFoamCore.tools.colorConsole as cc
import pyCellFoamCore.tools.placeFigures as pf


#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class IMorphInterfacePlateauGraph(IMorphInterface):
    '''
    This is the explanation of this class.

    '''

#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__subPathToGraphFile',
                 '__subPathToNodeThroatsFile')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,*args,
                 subPathToGraphFile = r'\Graphs\network_balls_plateauGraph.txt',
                 subPathToNodeThroatsFile = r'\OutputFiles\node_throats.txt',
                 **kwargs):
        '''


        '''
        self.__subPathToGraphFile = subPathToGraphFile
#        self.__subPathToTubesFile = subPathToTubesFile
        self.__subPathToNodeThroatsFile = subPathToNodeThroatsFile
#        self.__boundingBox = BoundingBox([0,1],[0,1],[0,1])
#        self.__addBorderCellFaceTypeNodes = addBorderCellFaceTypeNodes

        super().__init__(*args,**kwargs)



#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getPathToGraphFile(self): return self.pathToPorousFolder + self.__subPathToGraphFile
    pathToGraphFile = property(__getPathToGraphFile)
    '''

    '''

    def __getPathToNodeThroatsFile(self): return self.pathToPorousFolder +  self.__subPathToNodeThroatsFile
    pathToNodeThroatsFile = property(__getPathToNodeThroatsFile)
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
            error = self.loadNodesGraph(self.pathToGraphFile,'indice	i','connectivity table')

        error = True

        if not error:
            error = self.loadEdgesGraph(self.pathToGraphFile,'indice	nbNeighbors')

        if not error:
            error = self.loadFaces(self.pathToNodeThroatsFile)

        error = True
#
#        if not error:
#            error = self.__loadFaces()
#
#
#        if not error:
#            error = self.__loadVolumes()
#
#
#        if not error:
#            super().setUp()



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

    with MyLogging('iMorphInterfacePlateauGraph'):

#-------------------------------------------------------------------------
#    Create some examples
#-------------------------------------------------------------------------


        # interface = IMorphInterfacePlateauGraph(r'D:\iMorph\06_iMorph_October_20\data\Sample18\Div6\Roi1\original\Porous')
        # interface = IMorphInterfacePlateauGraph(r'H:\iMorphTemp\Sample18\Div6\Roi1\original\Porous')
        interface = IMorphInterfacePlateauGraph(r'D:\iMorph\06_iMorph_October_20\database\data\Sample01\Div6\Cutout2\original\Porous')



#-------------------------------------------------------------------------
#    Plotting
#-------------------------------------------------------------------------

        # Choose plotting method. Possible choices: pyplot, VTK, TikZ, animation, doc, None
        plottingMethod = 'plotly'


#    Disabled
#---------------------------------------------------------------------
        if plottingMethod is None or plottingMethod == 'None':
            cc.printBlue('Plotting disabled')

#    Pyplot
#---------------------------------------------------------------------
        elif plottingMethod == 'pyplot':
            cc.printBlue('Plot using pyplot')
            (figs,axes) = pf.getFigures()
            interface.plotComplex(axes[0],showLabel=False,showArrow=False,showNormalVec=False,showBarycenter=False)
            for f in interface.faces:
                f.plotFace(axes[0],showLabel=False,showBarycenter=False,showNormalVec = False)
            # pf.exportPNG(figs[0],'export/')

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

        elif plottingMethod == 'plotly':
            cc.printBlue('Plot using plotly')

            node_plotly = NodePlotly(interface.nodes)
            plotly_fig_nodes = node_plotly.plot_nodes_plotly(show_label=False)
            plotly_fig_nodes.show()

            edge_plotly = EdgePlotly(interface.edges)
            plotly_fig_edges = edge_plotly.plot_edges_plotly(show_label=True, show_barycenter=False)
            plotly_fig_edges.show()

            face_plotly = FacePlotly(interface.faces)
            plotly_fig_faces = face_plotly.plot_faces_plotly(show_label=True, show_barycenter=False)
            plotly_fig_faces.show()


#    Unknown
#---------------------------------------------------------------------
        else:
            cc.printRed('Unknown plotting method {}'.format(plottingMethod))
