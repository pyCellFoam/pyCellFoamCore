# -*- coding: utf-8 -*-
# =============================================================================
# DUAL NODE 0D
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Jul  6 15:30:48 2018

'''
A 0 dimensional dual of a node is another node at the exact location. However,
this class is necessery, since these two nodes are not exactly the same, but
only located at the same geometrical position.

.. image:: ../../../_static/dualNode0D_0.png
   :width: 400px
   :alt: primal node
   :align: center

.. image:: ../../../_static/dualNode0D_1.png
   :width: 400px
   :alt: 0D dual node
   :align: center

'''
# =============================================================================
#    IMPORTS
# =============================================================================
# ------------------------------------------------------------------------
#    Change to Main Directory
# ------------------------------------------------------------------------
import os
if __name__ == '__main__':
    os.chdir('../../')

# ------------------------------------------------------------------------
#    Standard Libraries
# ------------------------------------------------------------------------

import logging

# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------

#    kCells
# -------------------------------------------------------------------
from k_cells.node.node import Node
from k_cells.cell import DualCell

#    Tools
# -------------------------------------------------------------------
import tools.placeFigures as pf
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


class DualNode0D(Node, DualCell):
    '''


    '''

# =============================================================================
#    INITIALIZATION
# =============================================================================
    def __init__(self,
                 node,
                 *args,
                 myPrintDebug=None,
                 myPrintError=None,
                 edge=None,
                 face=None,
                 volume=None,
                 **kwargs):
        '''
        :param Node node: Primal node to which a 0D dual is wanted to be
            calculated
        :param myPrintDebug: alternate printing function to redirect debug
            messages.
        :param myPrintError: alternate printing function to redirect error
            messages.
        :param Edge edge: If this dual node is generated as a special case of
            a higher dimension, the duality is stored also in the edge.
        :param Face face: If this dual node is generated as a special case of
            a higher dimension, the duality is stored also in the face.
        :param Volume volume: If this dual node is generated as a special case
            of a higher dimension, the duality is stored also in the volume.


        '''

        category = None
        if volume:
            num = volume.num
            category = volume.category
        elif face:
            num = face.num
            category = face.category
        elif edge:
            num = edge.num
            category = edge.category
        else:
            num = node.num
            if node.category == 'border':
                category = 'additionalBorder'

        super().__init__(node.xCoordinate,
                         node.yCoordinate,
                         node.zCoordinate,
                         *args,
                         num=num,
                         category=category,
                         **kwargs)

        if True:
            if myPrintDebug is None:
                myPrintDebug = _log.debug
            # myPrintInfo = _log.info
            # myPrintWarning = _log.warning
            if myPrintError is None:
                myPrintError = _log.error
        else:
            _log.warning('Using prints instead of logger!')
            myPrintDebug = cc.printGreen
            # myPrintInfo = cc.printCyan
            # myPrintWarning = cc.printYellow
            myPrintError = cc.printRed

        myPrintDebug('Calculting 0D dual of {}'.format(node))
        myPrintDebug('volume: {}, face: {}, edge: {}'.format(volume,
                                                             face,
                                                             edge))

        self.dualCell0D = node
        node.dualCell0D = self

        # If this dual node is created as the 1D dual of an edge, add this
        # information to the edge
        if edge:
            if type(edge) is list:
                self.dualCell1D = edge
                for e in edge:
                    e.dualCell1D = self
            else:
                edge.dualCell1D = self

        if face:
            face.dualCell2D = self
            self.dualCell2D = face

        if volume:
            volume.dualCell3D = self
            self.dualCell3D = volume

        myPrintDebug('Initialized DualNode0D')

# =============================================================================
#    METHODS
# =============================================================================
# ------------------------------------------------------------------------
#    Plot for Documentation
# ------------------------------------------------------------------------
    @classmethod
    def plotDoc(cls):
        '''
        Create the plots used in documentation

        '''
        # Create node
        n0 = Node(1, 2, 3)

        # Create dual node do node defined before
        dn0 = DualNode0D(n0)

        # Create figures
        (figs, ax) = pf.getFigures(2, 1)

        # Plot primal node
        n0.plotNode(ax[0])

        # Plot dual node
        dn0.plotNode(ax[1])

        # Make sure that export directory exists
        if not os.path.isdir('doc/_static'):
            os.mkdir('doc/_static')

        # Create image files
        for i in range(2):
            pf.exportPNG(figs[i], filename='doc/_static/dualNode0D_'+str(i))


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================


if __name__ == '__main__':
    set_logging_format(logging.DEBUG)
    n0 = Node(1, 2, 3)
    dn0 = DualNode0D(n0)
    n0.xCoordinate = 5
    (figs, ax) = pf.getFigures(2, 1)
    n0.plotNode(ax[0])
#        dn0.plotNode(ax[0])

    pf.setLabels(ax[0])
    if False:
        DualNode0D.plotDoc()
