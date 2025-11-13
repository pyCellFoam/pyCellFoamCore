# -*- coding: utf-8 -*-
# =============================================================================
# BASE EDGE
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Dec  7 14:16:21 2017

'''


'''
# =============================================================================
#    IMPORTS
# =============================================================================
if __name__ == '__main__':
    import os
    os.chdir('../../')

# ------------------------------------------------------------------------
#    Standard Libraries
# ------------------------------------------------------------------------

import logging

# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------

from k_cells import BaseCell
import tools.colorConsole as cc

from tools.logging_formatter import set_logging_format


# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class BaseEdge(BaseCell):
    '''


    '''

# =============================================================================
#    SLOTS
# =============================================================================
#    __slots__ = ()

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self, *args, **kwargs):
        '''


        '''

        super().__init__(*args, **kwargs)
        _log.debug('Initialized BaseEdge')

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getBarycenter(self):
        return [se.barycenter for se in self.simpleEdges]

    barycenter = property(__getBarycenter)
    '''
    Returns a list of barycenters of all simple edges that the edge consists
    of.

    '''

    def __getDirectionVec(self):
        return [se.directionVec for se in self.simpleEdges]

    directionVec = property(__getDirectionVec)
    '''
    Returns a list of direction vectors of all simple edges that the edge
    consists of.

    '''

    def __getTopologicNodes(self): return [self.startNode, self.endNode]

    topologicNodes = property(__getTopologicNodes)
    '''

    '''

    def __getLength(self):
        lengths = []
        totalLenth = 0
        for se in self.simpleEdges:
            lengths.append(se.length)
            totalLenth += se.length
        return [lengths, totalLenth]
    length = property(__getLength)
    '''

    '''

# =============================================================================
#    METHODS
# =============================================================================

    def intersectWithBoundingBox(self, *args, **kwargs):
        '''

        '''
        nodes = []
        for se in self.simpleEdges:
            nodes.append(se.intersectWithBoundingBox(*args, **kwargs))
        return nodes

# ------------------------------------------------------------------------
#    Plotting
# ------------------------------------------------------------------------
    def plotEdge(self, *args, **kwargs):
        '''
        Plot all simple edges in a given pyplot axis

        :param ax: pyplot axis

        '''
        if self.showInPlot:

            if not self.simpleEdges:
                _log.warning('Edge {} '.format(self) +
                                    'has no simple edges, ' +
                                    'maybe it was deleted')
            for se in self.simpleEdges:
                se.plotEdge(*args, **kwargs)

        else:
            _log.warning('Plotting of edge {} is disabled'.format(self))

    def plotEdgeVtk(self, *args, **kwargs):
        '''
        Plot all simple edges in a given vtk window.

        :param myVtk: Instance of MyVtk class

        '''
        for se in self.simpleEdges:
            se.plotEdgeVtk(*args, **kwargs)

    def plotEdgeTikZ(self, *args, repeatLabel=True, **kwargs):
        '''

        '''
        if self.showInPlot:
            if repeatLabel:
                for se in self.simpleEdges:
                    se.plotEdgeTikZ(*args, **kwargs)
            else:
                self.simpleEdges[0].plotEdgeTikZ(*args, **kwargs)
                for se in self.simpleEdges[1:]:
                    se.plotEdgeTikZ(*args, showLabel=False, **kwargs)

#    def plotHeatFlow(self, ax, Q, Qmax, lmax):
#        for se in self.simpleEdges:
#            se.plotHeatFlow(ax, Q/len(self.simpleEdges), Qmax, lmax)

    def printEdge(self, printNodes=True):
        '''
        Prints information about the edge in the console including

        * Number
        * Start node and end node
        * Attached faces

        '''
        print('==========================================================')
        cc.printBlueBackground('   ', end='')
        print(' Edge ', self.info_text)
        print('==========================================================')
        print()
        print('Label:'+self.label_text)
        print()
        print('Defined by Node', self.startNode.num, 'and', self.endNode.num)
        print()
        if printNodes:
            print('Start Node:')
            print('-----------')
            self.startNode.printNode()
            print()
            print('End Node:')
            print('-----------')
            self.endNode.printNode()
            print()
        if len(self.faces) > 0:
            if len(self.faces) > 1:
                print('this edge belongs to', len(self.faces), 'Faces:')
            else:
                print('this edge belongs to', len(self.faces), 'Face:')
            print([f.num for f in self.faces])
        else:
            print('This Edge does not belong to a Face')
        print()
        print('==========================================================')
        print()
        print()
        print()


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':
    set_logging_format(logging.DEBUG)
    e1 = BaseEdge()
