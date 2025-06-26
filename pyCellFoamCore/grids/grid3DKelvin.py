# -*- coding: utf-8 -*-
#==============================================================================
# COMPLEX OF KELVIN CELLS
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Dec  7 14:16:21 2017

r'''

.. todo::
    * Remove prisms from this class (maybe create a child class with these
      prisms) and repace them with the new bounding box.



Example grid using kelvin cells.

The KelvinCell class creates all nodes, edges, faces and the volume for one
kelvin cell. Therefore, there is a local numbering for each cell. The kelvin
cell is split up into 5 layers from top to bottom.


*******************************************************************************
Layer 1
*******************************************************************************

Coordinates of the nodes (center at the origin of the coordinate system):

.. math::

    \mathbf{n_0} &=
        \begin{bmatrix}
            0\\
            -\frac{1}{2} \sqrt{2} a \\
            \sqrt{2} a
        \end{bmatrix} & \quad
    \mathbf{n_1} &=
        \begin{bmatrix}
            \frac{1}{2} \sqrt{2} a \\
            0 \\
            \sqrt{2} a
        \end{bmatrix} & \quad
    \mathbf{n_2} &=
        \begin{bmatrix}
            0\\
            \frac{1}{2} \sqrt{2} a \\
            \sqrt{2} a
        \end{bmatrix} & \quad
    \mathbf{n_3} &=
        \begin{bmatrix}
            -\frac{1}{2} \sqrt{2} a \\
            0 \\
            \sqrt{2} a
        \end{bmatrix}


.. image:: ../../_static/kelvin_layer1.png
       :width: 90%
       :alt: alternate text
       :align: center


*******************************************************************************
Layer 2
*******************************************************************************
Coordinates of the nodes (center at the origin of the coordinate system):

.. math::

    \mathbf{n_4} &=
        \begin{bmatrix}
            0\\
            -\sqrt{2} a \\
            \frac{1}{2} \sqrt{2} a
        \end{bmatrix} & \quad
    \mathbf{n_5} &=
        \begin{bmatrix}
            \sqrt{2} a \\
            0 \\
            \frac{1}{2} \sqrt{2} a
        \end{bmatrix} & \quad
    \mathbf{n_6} &=
        \begin{bmatrix}
            0\\
            \sqrt{2} a \\
            \frac{1}{2} \sqrt{2} a
        \end{bmatrix} & \quad
    \mathbf{n_7} &=
        \begin{bmatrix}
            - \sqrt{2} a \\
            0 \\
            \frac{1}{2} \sqrt{2} a
        \end{bmatrix}


.. image:: ../../_static/kelvin_layer2.png
       :width: 90%
       :alt: alternate text
       :align: center


*******************************************************************************
Layer 3
*******************************************************************************

.. math::

    \mathbf{n_8} &=
        \begin{bmatrix}
            \frac{1}{2} \sqrt{2} a \\
            - \sqrt{2} a \\
            0
        \end{bmatrix} & \quad
    \mathbf{n_9} &=
        \begin{bmatrix}
            \sqrt{2} a \\
            -\frac{1}{2} \sqrt{2} a \\
            0
        \end{bmatrix} & \quad
    \mathbf{n_{10}} &=
        \begin{bmatrix}
            \sqrt{2} a\\
            \frac{1}{2} \sqrt{2} a  a \\
            0
        \end{bmatrix} & \quad
    \mathbf{n_{11}} &=
        \begin{bmatrix}
            \frac{1}{2} \sqrt{2} a  \\
            \sqrt{2} a \\
            0
        \end{bmatrix} \\
    \mathbf{n_{12}} &=
        \begin{bmatrix}
            -\frac{1}{2} \sqrt{2} a  \\
            \sqrt{2} a \\
            0
        \end{bmatrix} & \quad
    \mathbf{n_{13}} &=
        \begin{bmatrix}
            -\sqrt{2} a\\
            \frac{1}{2} \sqrt{2} a \\
            0
        \end{bmatrix} & \quad
    \mathbf{n_{14}} &=
        \begin{bmatrix}
            -\sqrt{2} a \\
            -\frac{1}{2} \sqrt{2} a \\
            0
        \end{bmatrix} & \quad
    \mathbf{n_{15}} &=
        \begin{bmatrix}
            - \frac{1}{2} \sqrt{2} a \\
            - \sqrt{2} a \\
            0
        \end{bmatrix}

.. image:: ../../_static/kelvin_layer3.png
       :width: 90%
       :alt: alternate text
       :align: center


*******************************************************************************
Layer 4
*******************************************************************************
Coordinates of the nodes (center at the origin of the coordinate system):

.. math::

    \mathbf{n_{16}} &=
        \begin{bmatrix}
            0\\
            -\sqrt{2} a \\
            -\frac{1}{2} \sqrt{2} a
        \end{bmatrix} & \quad
    \mathbf{n_{17}} &=
        \begin{bmatrix}
            \sqrt{2} a \\
            0 \\
            -\frac{1}{2} \sqrt{2} a
        \end{bmatrix} & \quad
    \mathbf{n_{18}} &=
        \begin{bmatrix}
            0\\
            \sqrt{2} a \\
            -\frac{1}{2} \sqrt{2} a
        \end{bmatrix} & \quad
    \mathbf{n_{19}} &=
        \begin{bmatrix}
            - \sqrt{2} a \\
            0 \\
            - \frac{1}{2} \sqrt{2} a
        \end{bmatrix}

.. image:: ../../_static/kelvin_layer4.png
       :width: 90%
       :alt: alternate text
       :align: center


*******************************************************************************
Layer 5
*******************************************************************************

.. math::

    \mathbf{n_{20}} &=
        \begin{bmatrix}
            0\\
            -\frac{1}{2} \sqrt{2} a \\
            -\sqrt{2} a
        \end{bmatrix} & \quad
    \mathbf{n_{21}} &=
        \begin{bmatrix}
            \frac{1}{2} \sqrt{2} a \\
            0 \\
            -\sqrt{2} a
        \end{bmatrix} & \quad
    \mathbf{n_{22}} &=
        \begin{bmatrix}
            0\\
            \frac{1}{2} \sqrt{2} a \\
            -\sqrt{2} a
        \end{bmatrix} & \quad
    \mathbf{n_{23}} &=
        \begin{bmatrix}
            -\frac{1}{2} \sqrt{2} a \\
            0 \\
            -\sqrt{2} a
        \end{bmatrix}

.. image:: ../../_static/kelvin_layer5.png
       :width: 90%
       :alt: alternate text
       :align: center


'''


#==============================================================================
#    IMPORTS
#==============================================================================
if __name__ == '__main__':
    import os
    os.chdir('../')

import logging

from kCells import Node
from kCells import Edge
from kCells import Face
from kCells.volume.volume import Volume
import math
import numpy as np
import tools.colorConsole as cc
import tools.tumcolor as tc

import tools.placeFigures as pf
from tools import MyLogging
import matplotlib.pyplot as plt
from complex import PrimalComplex3D,DualComplex3D,Complex3D
plt.switch_backend("Qt5Agg")

import tools.combineImages as ci
import os

from tools.logging_formatter import set_logging_format


_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)

# Length of the edges in the kelvin cells
cubeDim = 40
numCells = 2


#a = cubeDim/2/math.sqrt(2)/numCells
a = cubeDim/2/math.sqrt(2)/4

# Half length of a diagonal in the quadratic faces of the kelvin cell
d = 1/2*math.sqrt(2)*a





#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class KelvinCell:
    '''
    Class to define a single kelvin cell


    '''



#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,x,y,z,n0old = False,
                            n1old = False,
                            n2old = False,
                            n3old = False,
                            n4old = False,
                            n5old = False,
                            n6old = False,
                            n7old = False,
                            n8old = False,
                            n9old = False,
                            n10old = False,
                            n11old = False,
                            n12old = False,
                            n13old = False,
                            n14old = False,
                            n15old = False,
                            n16old = False,
                            n17old = False,
                            n18old = False,
                            n19old = False,
                            n20old = False,
                            n21old = False,
                            n22old = False,
                            n23old = False,
                            n100old = False,
                            n101old = False,
                            n102old = False,
                            n103old = False,
                            n104old = False,
                            n105old = False,
                            n106old = False,
                            createPart = 'all'):
        '''
        Initializing the kelvin cell

        :param int x: x-coordinate of the center of the kelvin cell
        :param int y: y-coordinate of the center of the kelvin cell
        :param int z: z-coordinate of the center of the kelvin cell
        :param Node nXold: old nodes that already exist from previous kelvin
                           cells
        :param str createPart': Determine which part of the kelvin cell is
                                created. 'All' is standard. For cells at the
                                border, other options are available:
                                'upperHalf', 'lowerHalf', ...


        '''

        self.createN0 = True
        self.createN1 = True
        self.createN2 = True
        self.createN3 = True
        self.createN4 = True
        self.createN5 = True
        self.createN6 = True
        self.createN7 = True
        self.createN8 = True
        self.createN9 = True
        self.createN10 = True
        self.createN11 = True
        self.createN12 = True
        self.createN13 = True
        self.createN14 = True
        self.createN15 = True
        self.createN16 = True
        self.createN17 = True
        self.createN18 = True
        self.createN19 = True
        self.createN20 = True
        self.createN21 = True
        self.createN22 = True
        self.createN23 = True


        self.createN100 = False
        self.createN101 = False
        self.createN102 = False
        self.createN103 = False
        self.createN104 = False
        self.createN105 = False
        self.createN106 = False

        self.createE100 = False
        self.createE101 = False
        self.createE102 = False
        self.createE103 = False
        self.createE104 = False
        self.createE105 = False
        self.createE106 = False
        self.createE107 = False
        self.createE108 = False
        self.createE109 = False
        self.createE110 = False
        self.createE111 = False


#-------------------------------------------------------------------------
#    Create nodes
#-------------------------------------------------------------------------




        if createPart == 'all':
            pass

        elif createPart == 'upperHalf':

            self.createN16 = False
            self.createN17 = False
            self.createN18 = False
            self.createN19 = False
            self.createN20 = False
            self.createN21 = False
            self.createN22 = False
            self.createN23 = False
            self.createE100 = True
            self.createE101 = True
            self.createE102 = True
            self.createE103 = True

        elif createPart == 'lowerHalf':

            self.createN0 = False
            self.createN1 = False
            self.createN2 = False
            self.createN3 = False
            self.createN4 = False
            self.createN5 = False
            self.createN6 = False
            self.createN7 = False
            self.createE100 = True
            self.createE101 = True
            self.createE102 = True
            self.createE103 = True

        elif createPart == 'frontHalf':

            self.createN2 = False
            self.createN6 = False
            self.createN10 = False
            self.createN11 = False
            self.createN12 = False
            self.createN13 = False
            self.createN18 = False
            self.createN22 = False
            self.createE104 = True
            self.createE105 = True
            self.createE106 = True
            self.createE107 = True

        elif createPart == 'backHalf':

            self.createN0 = False
            self.createN4 = False
            self.createN8 = False
            self.createN9 = False
            self.createN14 = False
            self.createN15 = False
            self.createN16 = False
            self.createN20 = False

            self.createE104 = True
            self.createE105 = True
            self.createE106 = True
            self.createE107 = True

        elif createPart == 'leftHalf':

            self.createN1 = False
            self.createN5 = False
            self.createN8 = False
            self.createN9 = False
            self.createN10 = False
            self.createN11 = False
            self.createN17 = False
            self.createN21 = False

            self.createE108 = True
            self.createE109 = True
            self.createE110 = True
            self.createE111 = True

        elif createPart == 'rightHalf':

            self.createN3 = False
            self.createN7 = False
            self.createN12 = False
            self.createN13 = False
            self.createN14 = False
            self.createN15 = False
            self.createN19 = False
            self.createN23 = False

            self.createE108 = True
            self.createE109 = True
            self.createE110 = True
            self.createE111 = True

        elif createPart == 'upperFrontQuarter':

            self.createN2 = False
            self.createN6 = False
            self.createN10 = False
            self.createN11 = False
            self.createN12 = False
            self.createN13 = False
            self.createN16 = False
            self.createN17 = False
            self.createN18 = False
            self.createN19 = False
            self.createN20 = False
            self.createN21 = False
            self.createN22 = False
            self.createN23 = False

            self.createN100 = True
            self.createN101 = True

            self.createE100 = True
            self.createE104 = True



        elif createPart == 'upperBackQuarter':

            self.createN0  = False
            self.createN4  = False
            self.createN8  = False
            self.createN9  = False
            self.createN14 = False
            self.createN15 = False
            self.createN16 = False
            self.createN17 = False
            self.createN18 = False
            self.createN19 = False
            self.createN20 = False
            self.createN21 = False
            self.createN22 = False
            self.createN23 = False

            self.createN100 = True
            self.createN101 = True


            self.createE102 = True
            self.createE104 = True



        elif createPart == 'lowerFrontQuarter':

            self.createN0 = False
            self.createN1 = False
            self.createN2 = False
            self.createN3 = False
            self.createN4 = False
            self.createN5 = False
            self.createN6 = False
            self.createN7 = False
            self.createN10 = False
            self.createN11 = False
            self.createN12 = False
            self.createN13 = False
            self.createN18 = False
            self.createN22 = False

            self.createN100 = True
            self.createN101 = True

            self.createE100 = True
            self.createE107 = True



        elif createPart == 'lowerBackQuarter':

            self.createN0 = False
            self.createN1 = False
            self.createN2 = False
            self.createN3 = False
            self.createN4 = False
            self.createN5 = False
            self.createN6 = False
            self.createN7 = False
            self.createN8 = False
            self.createN9 = False
            self.createN14 = False
            self.createN15 = False
            self.createN16 = False
            self.createN20 = False

            self.createN100 = True
            self.createN101 = True

            self.createE102 = True
            self.createE107 = True


        elif createPart == 'upperLeftQuarter':

            self.createN1 = False
            self.createN5 = False
            self.createN8 = False
            self.createN9 = False
            self.createN10 = False
            self.createN11 = False
            self.createN16 = False
            self.createN17 = False
            self.createN18 = False
            self.createN19 = False
            self.createN20 = False
            self.createN21 = False
            self.createN22 = False
            self.createN23 = False

            self.createN102 = True
            self.createN103 = True

            self.createE103 = True
            self.createE108 = True


        elif createPart == 'lowerLeftQuarter':

            self.createN0 = False
            self.createN1 = False
            self.createN2 = False
            self.createN3 = False
            self.createN4 = False
            self.createN5 = False
            self.createN6 = False
            self.createN7 = False
            self.createN8 = False
            self.createN9 = False
            self.createN10 = False
            self.createN11 = False
            self.createN17 = False
            self.createN21 = False

            self.createN102 = True
            self.createN103 = True

            self.createE103 = True
            self.createE111 = True


        elif createPart == 'upperRightQuarter':

            self.createN3 = False
            self.createN7 = False
            self.createN12 = False
            self.createN13 = False
            self.createN14 = False
            self.createN15 = False
            self.createN16 = False
            self.createN17 = False
            self.createN18 = False
            self.createN19 = False
            self.createN20 = False
            self.createN21 = False
            self.createN22 = False
            self.createN23 = False

            self.createN102 = True
            self.createN103 = True

            self.createE101 = True
            self.createE108 = True


        elif createPart == 'lowerRightQuarter':

            self.createN0 = False
            self.createN1 = False
            self.createN2 = False
            self.createN3 = False
            self.createN4 = False
            self.createN5 = False
            self.createN6 = False
            self.createN7 = False
            self.createN12 = False
            self.createN13 = False
            self.createN14 = False
            self.createN15 = False
            self.createN19 = False
            self.createN23 = False

            self.createN102 = True
            self.createN103 = True

            self.createE101 = True
            self.createE111 = True


        elif createPart == 'frontLeftQuarter':

            self.createN1 = False
            self.createN2 = False
            self.createN5 = False
            self.createN6 = False
            self.createN8 = False
            self.createN9 = False
            self.createN10 = False
            self.createN11 = False
            self.createN12 = False
            self.createN13 = False
            self.createN17 = False
            self.createN18 = False
            self.createN21 = False
            self.createN22 = False

            self.createN104 = True
            self.createN105 = True

            self.createE106 = True
            self.createE109 = True


        elif createPart == 'frontRightQuarter':

            self.createN2 = False
            self.createN3 = False
            self.createN6 = False
            self.createN7 = False
            self.createN10 = False
            self.createN11 = False
            self.createN12 = False
            self.createN13 = False
            self.createN14 = False
            self.createN15 = False
            self.createN18 = False
            self.createN19 = False
            self.createN22 = False
            self.createN23 = False

            self.createN104 = True
            self.createN105 = True


            self.createE105 = True
            self.createE109 = True



        elif createPart == 'backLeftQuarter':

            self.createN0 = False
            self.createN1 = False
            self.createN4 = False
            self.createN5 = False
            self.createN8 = False
            self.createN9 = False
            self.createN10 = False
            self.createN11 = False
            self.createN14 = False
            self.createN15 = False
            self.createN16 = False
            self.createN17 = False
            self.createN20 = False
            self.createN21 = False

            self.createN104 = True
            self.createN105 = True

            self.createE106 = True
            self.createE110 = True


        elif createPart == 'backRightQuarter':

            self.createN0 = False
            self.createN3 = False
            self.createN4 = False
            self.createN7 = False
            self.createN8 = False
            self.createN9 = False
            self.createN12 = False
            self.createN13 = False
            self.createN14 = False
            self.createN15 = False
            self.createN16 = False
            self.createN19 = False
            self.createN20 = False
            self.createN23 = False

            self.createN104 = True
            self.createN105 = True

            self.createE105 = True
            self.createE110 = True




        elif createPart == 'upperFrontLeftEighth':

            self.createN1 = False
            self.createN2 = False
            self.createN5 = False
            self.createN6 = False
            self.createN8 = False
            self.createN9 = False
            self.createN10 = False
            self.createN11 = False
            self.createN12 = False
            self.createN13 = False
            self.createN16 = False
            self.createN17 = False
            self.createN18 = False
            self.createN19 = False
            self.createN20 = False
            self.createN21 = False
            self.createN22 = False
            self.createN23 = False

            self.createN101 = True
            self.createN103 = True
            self.createN104 = True
            self.createN106 = True


        elif createPart == 'lowerFrontLeftEighth':


            self.createN0 = False
            self.createN1 = False
            self.createN2 = False
            self.createN3 = False
            self.createN4 = False
            self.createN5 = False
            self.createN6 = False
            self.createN7 = False
            self.createN8 = False
            self.createN9 = False
            self.createN10 = False
            self.createN11 = False
            self.createN12 = False
            self.createN13 = False
            self.createN17 = False
            self.createN18 = False
            self.createN21 = False
            self.createN22 = False

            self.createN101 = True
            self.createN103 = True
            self.createN105 = True
            self.createN106 = True


        elif createPart == 'upperBackLeftEighth':

            self.createN0 = False
            self.createN1 = False
            self.createN4 = False
            self.createN5 = False
            self.createN8 = False
            self.createN9 = False
            self.createN10 = False
            self.createN11 = False
            self.createN14 = False
            self.createN15 = False
            self.createN16 = False
            self.createN17 = False
            self.createN18 = False
            self.createN19 = False
            self.createN20 = False
            self.createN21 = False
            self.createN22 = False
            self.createN23 = False

            self.createN101 = True
            self.createN102 = True
            self.createN104 = True
            self.createN106 = True


        elif createPart == 'lowerBackLeftEighth':

            self.createN0 = False
            self.createN1 = False
            self.createN2 = False
            self.createN3 = False
            self.createN4 = False
            self.createN5 = False
            self.createN6 = False
            self.createN7 = False
            self.createN8 = False
            self.createN9 = False
            self.createN10 = False
            self.createN11 = False
            self.createN14 = False
            self.createN15 = False
            self.createN16 = False
            self.createN17 = False
            self.createN14 = False
            self.createN20 = False
            self.createN21 = False

            self.createN101 = True
            self.createN102 = True
            self.createN105 = True
            self.createN106 = True



        elif createPart == 'upperFrontRightEighth':


            self.createN2 = False
            self.createN3 = False
            self.createN6 = False
            self.createN7 = False
            self.createN10 = False
            self.createN11 = False
            self.createN12 = False
            self.createN13 = False
            self.createN14 = False
            self.createN15 = False
            self.createN16 = False
            self.createN17 = False
            self.createN18 = False
            self.createN19 = False
            self.createN20 = False
            self.createN22 = False
            self.createN21 = False
            self.createN23 = False

            self.createN100 = True
            self.createN103 = True
            self.createN104 = True
            self.createN106 = True



        elif createPart == 'lowerFrontRightEighth':

            self.createN0 = False
            self.createN1 = False
            self.createN2 = False
            self.createN3 = False
            self.createN4 = False
            self.createN5 = False
            self.createN6 = False
            self.createN7 = False
            self.createN10 = False
            self.createN11 = False
            self.createN12 = False
            self.createN13 = False
            self.createN14 = False
            self.createN15 = False
            self.createN18 = False
            self.createN19 = False
            self.createN22 = False
            self.createN23 = False

            self.createN100 = True
            self.createN103 = True
            self.createN105 = True
            self.createN106 = True


        elif createPart == 'upperBackRightEighth':


            self.createN0 = False
            self.createN3 = False
            self.createN4 = False
            self.createN7 = False
            self.createN8 = False
            self.createN9 = False
            self.createN12 = False
            self.createN13 = False
            self.createN14 = False
            self.createN15 = False
            self.createN16 = False
            self.createN17 = False
            self.createN18 = False
            self.createN19 = False
            self.createN20 = False
            self.createN21 = False
            self.createN22 = False
            self.createN23 = False

            self.createN100 = True
            self.createN102 = True
            self.createN104 = True
            self.createN106 = True


        elif createPart == 'lowerBackRightEighth':


            self.createN0 = False
            self.createN1 = False
            self.createN2 = False
            self.createN3 = False
            self.createN4 = False
            self.createN5 = False
            self.createN6 = False
            self.createN7 = False
            self.createN8 = False
            self.createN9 = False
            self.createN12 = False
            self.createN13 = False
            self.createN14 = False
            self.createN15 = False
            self.createN16 = False
            self.createN19 = False
            self.createN20 = False
            self.createN23 = False

            self.createN100 = True
            self.createN102 = True
            self.createN105 = True
            self.createN106 = True


        else:
            cc.printRed('Create part',createPart,'is not known')



        # Layer 1
        self.n0=self.__createNode(x,y-d,z+2*d,self.createN0,n0old)
        self.n1=self.__createNode(x+d,y,z+2*d,self.createN1,n1old)
        self.n2=self.__createNode(x,y+d,z+2*d,self.createN2,n2old)
        self.n3=self.__createNode(x-d,y,z+2*d,self.createN3,n3old)


        # Layer 2
        self.n4=self.__createNode(x,y-2*d,z+d,self.createN4,n4old)
        self.n5=self.__createNode(x+2*d,y,z+d,self.createN5,n5old)
        self.n6=self.__createNode(x,y+2*d,z+d,self.createN6,n6old)
        self.n7=self.__createNode(x-2*d,y,z+d,self.createN7,n7old)


        # Layer 3
        self.n8  = self.__createNode(x+d,y-2*d,z, self.createN8,n8old)
        self.n9  = self.__createNode(x+2*d,y-d,z, self.createN9,n9old)
        self.n10 = self.__createNode(x+2*d,y+d,z,self.createN10,n10old)
        self.n11 = self.__createNode(x+d,y+2*d,z,self.createN11,n11old)
        self.n12 = self.__createNode(x-d,y+2*d,z,self.createN12,n12old)
        self.n13 = self.__createNode(x-2*d,y+d,z,self.createN13,n13old)
        self.n14 = self.__createNode(x-2*d,y-d,z,self.createN14,n14old)
        self.n15 = self.__createNode(x-d,y-2*d,z,self.createN15,n15old)


        # Layer 4
        self.n16=self.__createNode(x,y-2*d,z-d,self.createN16,n16old)
        self.n17=self.__createNode(x+2*d,y,z-d,self.createN17,n17old)
        self.n18=self.__createNode(x,y+2*d,z-d,self.createN18,n18old)
        self.n19=self.__createNode(x-2*d,y,z-d,self.createN19,n19old)


        # Layer 5
        self.n20=self.__createNode(x,y-d,z-2*d,self.createN20,n20old)
        self.n21=self.__createNode(x+d,y,z-2*d,self.createN21,n21old)
        self.n22=self.__createNode(x,y+d,z-2*d,self.createN22,n22old)
        self.n23=self.__createNode(x-d,y,z-2*d,self.createN23,n23old)


        self.n100 = self.__createNode(x+2*d,y,z, self.createN100,n100old)
        self.n101 = self.__createNode(x-2*d,y,z, self.createN101, n101old)
        self.n102 = self.__createNode(x,y+2*d,z, self.createN102, n102old)
        self.n103 = self.__createNode(x,y-2*d,z, self.createN103, n103old)
        self.n104 = self.__createNode(x,y,z+2*d, self.createN104, n104old)
        self.n105 = self.__createNode(x,y,z-2*d, self.createN105, n105old)
        self.n106 = self.__createNode(x,y,z,     self.createN106, n106old)


        self.nodes = [self.n0,  self.n1,  self.n2,  self.n3,  self.n4,
                      self.n5,  self.n6,  self.n7,  self.n8,  self.n9,
                      self.n10, self.n11, self.n12, self.n13, self.n14,
                      self.n15, self.n16, self.n17, self.n18, self.n19,
                      self.n20, self.n21, self.n22, self.n23,
                      self.n100, self.n101, self.n102, self.n103,self.n104,self.n105,self.n106]


#-------------------------------------------------------------------------
#    Create edges
#-------------------------------------------------------------------------

        # Layer 1
        self.e0 = self.__createEdge(self.n0,self.n1)
        self.e1 = self.__createEdge(self.n1,self.n2)
        self.e2 = self.__createEdge(self.n2,self.n3)
        self.e3 = self.__createEdge(self.n3,self.n0)


        # Layer 2
        self.e4 = self.__createEdge(self.n4,self.n0)
        self.e5 = self.__createEdge(self.n5,self.n1)
        self.e6 = self.__createEdge(self.n2,self.n6)
        self.e7 = self.__createEdge(self.n3,self.n7)


        # Layer 3
        self.e8 = self.__createEdge(self.n9,self.n8)
        self.e9 = self.__createEdge(self.n9,self.n5)
        self.e10 = self.__createEdge(self.n5,self.n10)
        self.e11 = self.__createEdge(self.n11,self.n10)
        self.e12 = self.__createEdge(self.n11,self.n6)
        self.e13 = self.__createEdge(self.n6,self.n12)
        self.e14 = self.__createEdge(self.n13,self.n12)
        self.e15 = self.__createEdge(self.n7,self.n13)
        self.e16 = self.__createEdge(self.n14,self.n7)
        self.e17 = self.__createEdge(self.n15,self.n14)
        self.e18 = self.__createEdge(self.n4,self.n15)
        self.e19 = self.__createEdge(self.n8,self.n4)


        # Layer 4
        self.e20 = self.__createEdge(self.n16,self.n15)
        self.e21 = self.__createEdge(self.n8,self.n16)
        self.e22 = self.__createEdge(self.n9,self.n17)
        self.e23 = self.__createEdge(self.n17,self.n10)
        self.e24 = self.__createEdge(self.n11,self.n18)
        self.e25 = self.__createEdge(self.n18,self.n12)
        self.e26 = self.__createEdge(self.n19,self.n13)
        self.e27 = self.__createEdge(self.n14,self.n19)

        # Layer 5
        self.e28 = self.__createEdge(self.n16,self.n20)
        self.e29 = self.__createEdge(self.n17,self.n21)
        self.e30 = self.__createEdge(self.n22,self.n18)
        self.e31 = self.__createEdge(self.n23,self.n19)
        self.e32 = self.__createEdge(self.n20,self.n21)
        self.e33 = self.__createEdge(self.n21,self.n22)
        self.e34 = self.__createEdge(self.n22,self.n23)
        self.e35 = self.__createEdge(self.n23,self.n20)


        self.e100 = self.__createEdge(self.n15,self.n8,self.createE100)
        self.e101 = self.__createEdge(self.n9,self.n10,self.createE101)
        self.e102 = self.__createEdge(self.n12,self.n11,self.createE102)
        self.e103 = self.__createEdge(self.n14,self.n13,self.createE103)


        self.e104 = self.__createEdge(self.n1,self.n3,self.createE104)
        self.e105 = self.__createEdge(self.n5,self.n17,self.createE105)
        self.e106 = self.__createEdge(self.n7,self.n19,self.createE106)
        self.e107 = self.__createEdge(self.n21,self.n23,self.createE107)


        self.e108 = self.__createEdge(self.n0,self.n2,self.createE108)
        self.e109 = self.__createEdge(self.n4,self.n16,self.createE109)
        self.e110 = self.__createEdge(self.n6,self.n18,self.createE110)
        self.e111 = self.__createEdge(self.n20,self.n22,self.createE111)


        self.e112 = self.__createEdge(self.n100,self.n5)
        self.e113 = self.__createEdge(self.n100,self.n9)
        self.e114 = self.__createEdge(self.n101,self.n7)
        self.e115 = self.__createEdge(self.n101,self.n14)
        self.e116 = self.__createEdge(self.n100,self.n101)
        self.e117 = self.__createEdge(self.n100,self.n10)
        self.e118 = self.__createEdge(self.n101,self.n13)
        self.e119 = self.__createEdge(self.n100,self.n17)
        self.e120 = self.__createEdge(self.n101,self.n19)
        self.e121 = self.__createEdge(self.n102,self.n6)
        self.e122 = self.__createEdge(self.n102,self.n12)
        self.e123 = self.__createEdge(self.n103,self.n4)
        self.e124 = self.__createEdge(self.n103,self.n15)
        self.e125 = self.__createEdge(self.n102,self.n103)
        self.e126 = self.__createEdge(self.n102,self.n18)
        self.e127 = self.__createEdge(self.n103,self.n16)
        self.e128 = self.__createEdge(self.n102,self.n11)
        self.e129 = self.__createEdge(self.n103,self.n8)
        self.e130 = self.__createEdge(self.n104,self.n0)
        self.e131 = self.__createEdge(self.n104,self.n3)
        self.e132 = self.__createEdge(self.n105,self.n20)
        self.e133 = self.__createEdge(self.n105,self.n23)
        self.e134 = self.__createEdge(self.n104,self.n105)
        self.e135 = self.__createEdge(self.n104,self.n1)
        self.e136 = self.__createEdge(self.n105,self.n21)
        self.e137 = self.__createEdge(self.n104,self.n2)
        self.e138 = self.__createEdge(self.n105,self.n22)
        self.e139 = self.__createEdge(self.n106,self.n101)
        self.e140 = self.__createEdge(self.n106,self.n103)
        self.e141 = self.__createEdge(self.n106,self.n104)
        self.e142 = self.__createEdge(self.n106,self.n105)
        self.e143 = self.__createEdge(self.n106,self.n102)
        self.e144 = self.__createEdge(self.n106,self.n100)



        self.edges = [self.e0, self.e1, self.e2, self.e3, self.e4,
                      self.e5, self.e6, self.e7, self.e8, self.e9,
                      self.e10,self.e11,self.e12,self.e13,self.e14,
                      self.e15,self.e16,self.e17,self.e18,self.e19,
                      self.e20,self.e21,self.e22,self.e23,self.e24,
                      self.e25,self.e26,self.e27,self.e28,self.e29,
                      self.e30,self.e31,self.e32,self.e33,self.e34,
                      self.e35,
                      self.e100,self.e101,self.e102,self.e103,
                      self.e104,self.e105,self.e106,self.e107,
                      self.e108,self.e109,self.e110,self.e111,
                      self.e112,self.e113,self.e114,self.e115,self.e116,
                      self.e117,self.e118,self.e119,self.e120,
                      self.e121,self.e122,self.e123,self.e124,self.e125,
                      self.e126,self.e127,self.e128,self.e129,
                      self.e130,self.e131,self.e132,self.e133,self.e134,
                      self.e135,self.e136,self.e137,self.e138,
                      self.e139,self.e140,self.e141,self.e142,
                      self.e143,self.e144]


#-------------------------------------------------------------------------
#    Create faces
#-------------------------------------------------------------------------
        # Layer 1
        self.f0  = self.__createFace([  self.e0,  self.e1,  self.e2,  self.e3])

        # Layer 2
        self.f1  = self.__createFace([ -self.e19, -self.e8, self.e9, self.e5, -self.e0, -self.e4])
        self.f2  = self.__createFace([self.e10, -self.e11, self.e12, -self.e6, -self.e1, -self.e5])
        self.f3  = self.__createFace([self.e13, -self.e14, -self.e15, -self.e7, -self.e2, self.e6])
        self.f4  = self.__createFace([-self.e16, -self.e17, -self.e18, self.e4, -self.e3, self.e7])

        # Layer 3
        self.f5  = self.__createFace([-self.e18, -self.e19, self.e21, self.e20])
        self.f6  = self.__createFace([ self.e22, self.e23, -self.e10,-self.e9])
        self.f7  = self.__createFace([ self.e24, self.e25, -self.e13,-self.e12])
        self.f8  = self.__createFace([-self.e15, -self.e16, self.e27, self.e26])


        # Layer 4
        self.f9  = self.__createFace([-self.e21, -self.e8, self.e22, self.e29, -self.e32, -self.e28])
        self.f10 = self.__createFace([self.e23, -self.e11, self.e24, -self.e30, -self.e33, -self.e29])
        self.f11 = self.__createFace([self.e25, -self.e14, -self.e26, -self.e31, -self.e34, self.e30])
        self.f12 = self.__createFace([-self.e27, -self.e17, -self.e20, self.e28, -self.e35, self.e31])

        # Layer 5
        self.f13 = self.__createFace([self.e32, self.e33, self.e34, self.e35])



        self.f100 = self.__createFace([self.e21,self.e20,self.e100])
        self.f101 = self.__createFace([self.e22,self.e23,-self.e101])
        self.f102 = self.__createFace([self.e24,self.e25,self.e102])
        self.f103 = self.__createFace([self.e27,self.e26,-self.e103])
        self.f104 = self.__createFace([self.e9,self.e10,-self.e101])
        self.f105 = self.__createFace([self.e12,self.e13,self.e102])
        self.f106 = self.__createFace([self.e16,self.e15,-self.e103])
        self.f107 = self.__createFace([self.e19,self.e18,self.e100])
        self.f108 = self.__createFace([self.e100,-self.e8,self.e101,-self.e11,-self.e102,-self.e14,-self.e103,-self.e17])

        self.f109 = self.__createFace([self.e104,self.e3,self.e0])
        self.f110 = self.__createFace([self.e105,-self.e22,self.e9])
        self.f111 = self.__createFace([self.e106,-self.e27,self.e16])
        self.f112 = self.__createFace([self.e107,self.e35,self.e32])
        self.f113 = self.__createFace([self.e104,-self.e2,-self.e1])
        self.f114 = self.__createFace([self.e105,self.e23,-self.e10])
        self.f115 = self.__createFace([self.e106,self.e26,-self.e15])
        self.f116 = self.__createFace([-self.e107,self.e33,self.e34])
        self.f117 = self.__createFace([self.e104,self.e7,self.e106,-self.e31,-self.e107,-self.e29,-self.e105,self.e5])

        self.f118 = self.__createFace([self.e108,self.e2,self.e3])
        self.f119 = self.__createFace([self.e109,self.e20,-self.e18])
        self.f120 = self.__createFace([self.e110,self.e25,-self.e13])
        self.f121 = self.__createFace([self.e111,self.e34,self.e35])
        self.f122 = self.__createFace([self.e108,-self.e1,-self.e0])
        self.f123 = self.__createFace([self.e109,-self.e21,self.e19])
        self.f124 = self.__createFace([self.e110,-self.e24,self.e12])
        self.f125 = self.__createFace([self.e111,-self.e33,-self.e32])
        self.f126 = self.__createFace([self.e108,self.e6,self.e110,-self.e30,-self.e111,-self.e28,-self.e109,self.e4])

        self.f127 = self.__createFace([-self.e112,self.e113,self.e9])
        self.f128 = self.__createFace([-self.e114,self.e115,self.e16])
        self.f129 = self.__createFace([self.e112,self.e5,self.e104,self.e7,-self.e114,-self.e116])
        self.f130 = self.__createFace([self.e113,self.e8,-self.e100,self.e17,-self.e115,-self.e116])
        self.f131 = self.__createFace([-self.e114,self.e118,-self.e15])
        self.f132 = self.__createFace([-self.e112,self.e117,-self.e10])
        self.f133 = self.__createFace([self.e117,-self.e11,-self.e102,-self.e14,-self.e118,-self.e116])

        self.f134 = self.__createFace([-self.e119,self.e113,self.e22])
        self.f135 = self.__createFace([-self.e120,self.e115,self.e27])
        self.f136 = self.__createFace([self.e119,self.e29,self.e107,self.e31,-self.e120,-self.e116])
        self.f137 = self.__createFace([-self.e119,self.e117,-self.e23])
        self.f138 = self.__createFace([-self.e120,self.e118,-self.e26])
        self.f139 = self.__createFace([-self.e124,self.e123,self.e18])
        self.f140 = self.__createFace([-self.e122,self.e121,self.e13])
        self.f141 = self.__createFace([self.e122,-self.e14,-self.e103,-self.e17,-self.e124,-self.e125])
        self.f142 = self.__createFace([self.e121,-self.e6,-self.e108,-self.e4,-self.e123,-self.e125])
        self.f143 = self.__createFace([-self.e122,self.e126,self.e25])
        self.f144 = self.__createFace([-self.e124,self.e127,self.e20])
        self.f145 = self.__createFace([self.e126,-self.e30,-self.e111,-self.e28,-self.e127,-self.e125])
        self.f146 = self.__createFace([-self.e129,self.e123,-self.e19])
        self.f147 = self.__createFace([-self.e128,self.e121,-self.e12])
        self.f148 = self.__createFace([self.e128,self.e11,-self.e101,self.e8,-self.e129,-self.e125])
        self.f149 = self.__createFace([-self.e128,self.e126,-self.e24])
        self.f150 = self.__createFace([-self.e129,self.e127,-self.e21])
        self.f151 = self.__createFace([-self.e131,self.e130,-self.e3])
        self.f152 = self.__createFace([-self.e133,self.e132,-self.e35])
        self.f153 = self.__createFace([self.e130,-self.e4,self.e109,self.e28,-self.e132,-self.e134])
        self.f154 = self.__createFace([self.e131,self.e7,self.e106,-self.e31,-self.e133,-self.e134])
        self.f155 = self.__createFace([-self.e135,self.e130,self.e0])
        self.f156 = self.__createFace([-self.e136,self.e132,self.e32])
        self.f157 = self.__createFace([self.e135,-self.e5,self.e105,self.e29,-self.e136,-self.e134])
        self.f158 = self.__createFace([-self.e137,self.e131,-self.e2])
        self.f159 = self.__createFace([-self.e138,self.e133,-self.e34])
        self.f160 = self.__createFace([self.e137,self.e6,self.e110,-self.e30,-self.e138,-self.e134])
        self.f161 = self.__createFace([-self.e135,self.e137,-self.e1])
        self.f162 = self.__createFace([-self.e136,self.e138,-self.e33])
        self.f163 = self.__createFace([self.e140,self.e123,self.e4,-self.e130,-self.e141])
        self.f164 = self.__createFace([self.e141,self.e131,self.e7,-self.e114,-self.e139])
        self.f165 = self.__createFace([self.e139,self.e115,-self.e17,-self.e124,-self.e140])
        self.f166 = self.__createFace([self.e142,self.e132,-self.e28,-self.e127,-self.e140])
        self.f167 = self.__createFace([self.e142,self.e133,self.e31,-self.e120,-self.e139])
        self.f168 = self.__createFace([self.e141,self.e137,self.e6,-self.e121,-self.e143])
        self.f169 = self.__createFace([self.e139,self.e118,self.e14,-self.e122,-self.e143])
        self.f170 = self.__createFace([self.e142,self.e138,self.e30,-self.e126,-self.e143])
        self.f171 = self.__createFace([self.e140,self.e129,-self.e8,-self.e113,-self.e144])
        self.f172 = self.__createFace([self.e141,self.e135,-self.e5,-self.e112,-self.e144])
        self.f173 = self.__createFace([self.e142,self.e136,-self.e29,-self.e119,-self.e144])
        self.f174 = self.__createFace([self.e143,self.e128,self.e11,-self.e117,-self.e144])

        self.faces = [self.f0,self.f1,self.f2,self.f3,self.f4,
                      self.f5,self.f6,self.f7,self.f8,self.f9,
                      self.f10,self.f11,self.f12,self.f13,
                      self.f100,self.f101,self.f102,self.f103,self.f104,
                      self.f105,self.f106,self.f107,self.f108,self.f109,
                      self.f110,self.f111,self.f112,self.f113,self.f114,
                      self.f115,self.f116,self.f117,self.f118,self.f119,
                      self.f120,self.f121,self.f122,self.f123,self.f124,
                      self.f125,self.f126,self.f127,self.f128,self.f129,self.f130,
                      self.f131,self.f132,self.f133,self.f134,self.f135,self.f136,
                      self.f137,self.f138,self.f139,self.f140,self.f141,self.f142,
                      self.f143,self.f144,self.f145,self.f146,self.f147,self.f148,
                      self.f149,self.f150,self.f151,self.f152,self.f153,self.f154,
                      self.f155,self.f156,self.f157,self.f158,self.f159,self.f160,
                      self.f161,self.f162,
                      self.f163,self.f164,self.f165,self.f166,self.f167,self.f168,
                      self.f169,self.f170,self.f171,self.f172,self.f173,self.f174]





#        if createPart == 'upperHalf' or createPart == 'lowerHalf':
#            self.f108 = self.__createFace([])



#-------------------------------------------------------------------------
#    Create volume
#-------------------------------------------------------------------------
        self.volume = False
        if createPart == 'all':
            self.volume = Volume([self.f0,self.f1,self.f2,self.f3,self.f4,-self.f5,self.f6,self.f7,-self.f8,-self.f9,-self.f10,-self.f11,-self.f12,-self.f13])
        elif createPart == 'upperHalf':
#            print([self.f0,self.f1,self.f2,self.f3,self.f4,-self.f104,-self.f105,self.f106,self.f107,-self.f108])
            self.volume = Volume([self.f0,self.f1,self.f2,self.f3,self.f4,-self.f104,-self.f105,self.f106,self.f107,-self.f108])
        elif createPart == 'lowerHalf':
#            print([-self.f13,-self.f12,-self.f11,-self.f10,-self.f9,-self.f100,-self.f101,self.f102,self.f103,self.f108])
            self.volume = Volume([-self.f13,-self.f12,-self.f11,-self.f10,-self.f9,-self.f100,self.f101,self.f102,-self.f103,self.f108])
        elif createPart == 'frontHalf':
            self.volume = Volume([self.f109,self.f1,self.f4,-self.f110,self.f111,-self.f5,-self.f9,-self.f12,-self.f112,-self.f117])
        elif createPart == 'backHalf':
            self.volume = Volume([-self.f113,self.f2,self.f3,self.f7,self.f114,-self.f115,-self.f10,-self.f11,-self.f116,self.f117])
        elif createPart == 'leftHalf':
            self.volume = Volume([self.f118,self.f3,self.f4,-self.f119,self.f120,-self.f8,-self.f12,-self.f11,-self.f121,-self.f126])
        elif createPart == 'rightHalf':
            self.volume = Volume([-self.f122,self.f1,self.f2,self.f123,-self.f124,self.f6,-self.f9,-self.f10,self.f125,self.f126])
        elif createPart == 'upperFrontQuarter':
            self.volume = Volume([self.f109,self.f1,self.f4,self.f128,-self.f127,self.f107,-self.f129,self.f130])
        elif createPart == 'upperBackQuarter':
            self.volume = Volume([-self.f113,self.f2,self.f3,-self.f105,self.f132,-self.f131,-self.f133,self.f129])
        elif createPart == 'lowerFrontQuarter':
            self.volume = Volume([-self.f130,self.f134,-self.f135,-self.f100,-self.f9,-self.f12,-self.f112,self.f136])
        elif createPart == 'lowerBackQuarter':
            self.volume = Volume([self.f133,-self.f137,self.f138,self.f102,-self.f10,-self.f11,-self.f116,-self.f136])
        elif createPart == 'upperLeftQuarter':
            self.volume = Volume([self.f118,self.f3,self.f4,self.f139,self.f106,-self.f140,-self.f141,self.f142])
        elif createPart == 'lowerLeftQuarter':
            self.volume = Volume([self.f141,self.f143,-self.f103,-self.f144,-self.f11,-self.f12,-self.f121,-self.f145])
        elif createPart == 'upperRightQuarter':
            self.volume = Volume([-self.f122,self.f1,self.f2,self.f147,-self.f104,-self.f146,self.f148,-self.f142])
        elif createPart == 'lowerRightQuarter':
            self.volume = Volume([-self.f148,self.f150,self.f101,-self.f149,-self.f9,-self.f10,self.f125,self.f145])
        elif createPart == 'frontLeftQuarter':
            self.volume = Volume([-self.f151,self.f4,-self.f119,self.f111,-self.f12,self.f152,self.f153,-self.f154])
        elif createPart == 'frontRightQuarter':
            self.volume = Volume([self.f155,-self.f153,self.f157,self.f1,-self.f110,self.f123,-self.f9,-self.f156])
        elif createPart == 'backLeftQuarter':
            self.volume = Volume([-self.f158,self.f3,self.f120,-self.f115,self.f154,-self.f11,self.f159,-self.f160])
        elif createPart == 'backRightQuarter':
            self.volume = Volume([-self.f161,self.f2,self.f114,-self.f124,-self.f10,self.f162,self.f160,-self.f157])
        elif createPart == 'upperFrontLeftEighth':
            self.volume = Volume([-self.f151,self.f4,self.f128,self.f139,-self.f163,-self.f164,-self.f165])
        elif createPart == 'lowerFrontLeftEighth':
            self.volume = Volume([self.f165,-self.f135,-self.f144,-self.f12,self.f167,-self.f166,self.f152])
        elif createPart == 'upperBackLeftEighth':
            self.volume = Volume([-self.f158,self.f3,-self.f131,-self.f140,self.f169,self.f164,-self.f168])
        elif createPart == 'lowerBackLeftEighth':
            self.volume = Volume([-self.f169,self.f138,self.f143,-self.f11,-self.f167,self.f159,self.f170])
        elif createPart == 'upperFrontRightEighth':
            self.volume = Volume([self.f155,self.f1,self.f163,self.f172,-self.f146,-self.f127,-self.f171])
        elif createPart == 'lowerFrontRightEighth':
            self.volume = Volume([self.f171,self.f166,-self.f173,-self.f9,self.f134,self.f150,-self.f156])
        elif createPart == 'upperBackRightEighth':
            self.volume = Volume([-self.f161,self.f2,-self.f172,self.f168,self.f132,self.f147,self.f174])
        elif createPart == 'lowerBackRightEighth':
            self.volume = Volume([-self.f174,self.f173,-self.f137,-self.f149,-self.f10,self.f162,-self.f170])

#==============================================================================
#    METHODS
#==============================================================================

#-------------------------------------------------------------------------
#    Create node
#-------------------------------------------------------------------------
    def __createNode(self,x,y,z,createNode,nodeOld):
        '''
        Creating node at given location if it is meant to be created and if it
        is not created yet.

        :param int x: x-Coordinate of the node
        :param int y: y-Coordinate of the node
        :param int z: z-Coordinate of the node
        :param bool createNode: Set to False if the node is not needed in this
                                cell (for example at the border)
        :param nodeOld: old node, if it already existed

        :return: New node

        '''

        if not createNode:
            return False
        else:
            if not nodeOld:
                return Node(x,y,z)
            else:
                return nodeOld

#-------------------------------------------------------------------------
#    Create edge
#-------------------------------------------------------------------------
    def __createEdge(self,n1,n2,createEdge=True):
        '''
        Creating edge between two given nodes. If at least one of the nodes
        does not exist, then the edge is not created.

        :param Node n1: Start node
        :param Node n2: End node
        :return: New edge

        '''
        if n1 == False or n2 == False or not createEdge:
            return False
        else:
            edgeExisted = False
            for e in n1.edges:
                if e.startNode == n2 or e.endNode == n2:
                    edgeExisted = True
                    oldEdge = e
            if not edgeExisted:
                return Edge(n1,n2)
            else:
                return oldEdge
#-------------------------------------------------------------------------
#    Create face
#-------------------------------------------------------------------------
    def __createFace(self,edges):
        '''
        Creating face between given edges. If any of the edges does not exist,
        then the face i not created.

        :param Edge edges: list of edges to define face
        :return: New face

        '''
        if any([e == False for e in edges]):
            return False
        faceExisted = False
        facesOld = []
        for e in edges:
            for f in e.faces:
                if not f in facesOld:
                    facesOld.append(f)
                    facesOld.append(-f)
        for f in facesOld:
            if all([e in edges for e in f.edges]):
                faceExisted = True
                oldFace = f


        if not faceExisted:
            return Face(edges)
        else:
            return oldFace
#-------------------------------------------------------------------------
#    Plot nodes, edges and faces in one figure
#-------------------------------------------------------------------------
    def plotKelvinCell(self,ax):
        for n in self.nodes:
            if n:
                n.plotNode(ax)
        for e in self.edges:
            if e:
                e.plotEdge(ax)
        for f in self.faces:
            if f:
                f.plotFace(ax)

#-------------------------------------------------------------------------
#    Plot nodes and edges with local nomenclature
#-------------------------------------------------------------------------
    def plotNomenclature(self,prefix='temp_'):
        '''
        Plot the different layers of the current kelvin cell to see the
        numbering. A top view and a 3D view are plotted next to each other.

        '''

        for (i,n) in enumerate(self.nodes[:24]):
            if n:
                n.num = i
        for (i,n) in enumerate(self.nodes[24:]):
            if n:
                n.num = i+100
        for (i,e) in enumerate(self.edges[:36]):
            if e:
                e.num = i
        for (i,e) in enumerate(self.edges[36:]):
            if e:
                e.num = i+100

        for (i,f) in enumerate(self.faces[:14]):
            if f:
                f.num = i
        for (i,f) in enumerate(self.faces[14:]):
            if f:
                f.num = i+100

        (figs,ax) = pf.getFigures(numTotal=10)

        if os.getcwd().endswith('doc'):
            imagePath = './_static/'
        else:
            imagePath = './temp/'


        # Layer 1
        self.__setAllColors(tc.TUMGrayMedium())
        axNum = 0
        for n in [self.n0,self.n1,self.n2,self.n3]:
            if n:
                n.color = tc.TUMOrange()
                n.showLabel = True
                n.plotNode(ax[axNum])
        for e in [self.e0,self.e1,self.e2,self.e3]:
            if e:
                e.color = tc.TUMBlue()
                e.showLabel = True
                e.showArrow = True
                e.plotEdge(ax[axNum])

        pf.setLabels(ax[axNum])
        pf.setAxesEqual(ax[axNum])
        ax[axNum].view_init(90,-90)

        plt.figure(axNum+1)
        nameFlat = imagePath+prefix+'kelvin_layer1_flat.png'
        plt.savefig(nameFlat,dpi=300)


        axNum = 1
        for n in self.nodes:
            if n:
                n.plotNode(ax[axNum])
        for e in self.edges:
            if e:
                e.plotEdge(ax[axNum])

        pf.setLabels(ax[axNum])
        pf.setAxesEqual(ax[axNum])

        plt.figure(axNum+1)
        name3D = imagePath+prefix+'kelvin_layer1_3d.png'
        plt.savefig(name3D,dpi=300)

        ci.combineImages([nameFlat,name3D],imagePath+prefix+'kelvin_layer1.png')




        # Layer 2
        self.__setAllColors(tc.TUMGrayMedium())
        axNum = 2
        for n in [self.n0,self.n1,self.n2,self.n3]:
            if n:
                n.color = tc.TUMBlack()
                n.plotNode(ax[axNum])
        for n in [self.n4,self.n5,self.n6,self.n7]:
            if n:
                n.color = tc.TUMOrange()
                n.showLabel = True
                n.plotNode(ax[axNum])
        for e in [self.e4,self.e5,self.e6,self.e7]:
            if e:
                e.color = tc.TUMBlue()
                e.showLabel = True
                e.showArrow = True
                e.plotEdge(ax[axNum])

        pf.setLabels(ax[axNum])
        pf.setAxesEqual(ax[axNum])
        ax[axNum].view_init(90,-90)

        plt.figure(axNum+1)
        nameFlat = imagePath+prefix+'kelvin_layer2_flat.png'
        plt.savefig(nameFlat,dpi=300)

        axNum = 3
        for n in self.nodes:
            if n:
                n.plotNode(ax[axNum])
        for e in self.edges:
            if e:
                e.plotEdge(ax[axNum])

        pf.setLabels(ax[axNum])
        pf.setAxesEqual(ax[axNum])
        plt.figure(axNum+1)
        name3D = imagePath+prefix+'kelvin_layer2_3d.png'
        plt.savefig(name3D,dpi=300)

        ci.combineImages([nameFlat,name3D],imagePath+prefix+'kelvin_layer2.png')




        # Layer 3
        self.__setAllColors(tc.TUMGrayMedium())
        axNum = 4
        for n in [self.n4,self.n5,self.n6,self.n7]:
            if n:
                n.color = tc.TUMBlack()
                n.plotNode(ax[axNum])
        for n in [self.n8,self.n9,self.n10,self.n11,self.n12,self.n13,self.n14,self.n15]:
            if n:
                n.color = tc.TUMOrange()
                n.showLabel = True
                n.plotNode(ax[axNum])
        for e in [self.e8,self.e9,self.e10,self.e11,self.e12,self.e13,self.e14,self.e15,self.e16,self.e17,self.e18,self.e19]:
            if e:
                e.color = tc.TUMBlue()
                e.showLabel = True
                e.showArrow = True
                e.plotEdge(ax[axNum])

        pf.setLabels(ax[axNum])
        pf.setAxesEqual(ax[axNum])
        ax[axNum].view_init(90,-90)

        plt.figure(axNum+1)
        nameFlat = imagePath+prefix+'kelvin_layer3_flat.png'
        plt.savefig(nameFlat,dpi=300)


        axNum = 5
        for n in self.nodes:
            if n:
                n.plotNode(ax[axNum])
        for e in self.edges:
            if e:
                e.plotEdge(ax[axNum])
        pf.setLabels(ax[axNum])
        pf.setAxesEqual(ax[axNum])

        plt.figure(axNum+1)
        name3D = imagePath+prefix+'kelvin_layer3_3d.png'
        plt.savefig(name3D,dpi=300)

        ci.combineImages([nameFlat,name3D],imagePath+prefix+'kelvin_layer3.png')

        # Layer 4
        self.__setAllColors(tc.TUMGrayMedium())
        axNum = 6
        for n in [self.n8,self.n9,self.n10,self.n11,self.n12,self.n13,self.n14,self.n15]:
            if n:
                n.color = tc.TUMBlack()
                n.plotNode(ax[axNum])
        for n in [self.n16,self.n17,self.n18,self.n19]:
            if n:
                n.color = tc.TUMOrange()
                n.showLabel = True
                n.plotNode(ax[axNum])
        for e in [self.e20,self.e21,self.e22,self.e23,self.e24,self.e25,self.e26,self.e27]:
            if e:
                e.color = tc.TUMBlue()
                e.showLabel = True
                e.showArrow = True
                e.plotEdge(ax[axNum])

        pf.setLabels(ax[axNum])
        pf.setAxesEqual(ax[axNum])
        ax[axNum].view_init(90,-90)

        plt.figure(axNum+1)
        nameFlat = imagePath+prefix+'kelvin_layer4_flat.png'
        plt.savefig(nameFlat,dpi=300)


        axNum = 7
        for n in self.nodes:
            if n:
                n.plotNode(ax[axNum])
        for e in self.edges:
            if e:
                e.plotEdge(ax[axNum])
        pf.setLabels(ax[axNum])
        pf.setAxesEqual(ax[axNum])

        plt.figure(axNum+1)
        name3D = imagePath+prefix+'kelvin_layer4_3d.png'
        plt.savefig(name3D,dpi=300)

        ci.combineImages([nameFlat,name3D],imagePath+prefix+'kelvin_layer4.png')

        # Layer 5
        self.__setAllColors(tc.TUMGrayMedium())
        axNum = 8
        for n in [self.n16,self.n17,self.n18,self.n19]:
            if n:
                n.color = tc.TUMBlack()
                n.plotNode(ax[axNum])
        for n in [self.n20,self.n21,self.n22,self.n23]:
            if n:
                n.color = tc.TUMOrange()
                n.showLabel = True
                n.plotNode(ax[axNum])
        for e in [self.e28,self.e29,self.e30,self.e31,self.e32,self.e33,self.e34,self.e35]:
            if e:
                e.color = tc.TUMBlue()
                e.showLabel = True
                e.showArrow = True
                e.plotEdge(ax[axNum])

        pf.setLabels(ax[axNum])
        pf.setAxesEqual(ax[axNum])
        ax[axNum].view_init(90,-90)

        plt.figure(axNum+1)
        nameFlat = imagePath+prefix+'kelvin_layer5_flat.png'
        plt.savefig(nameFlat,dpi=300)



        axNum = 9
        for n in self.nodes:
            if n:
                n.plotNode(ax[axNum])
        for e in self.edges:
            if e:
                e.plotEdge(ax[axNum])
        pf.setLabels(ax[axNum])
        pf.setAxesEqual(ax[axNum])


        plt.figure(axNum+1)
        name3D = imagePath+prefix+'kelvin_layer5_3d.png'
        plt.savefig(name3D,dpi=300)

        ci.combineImages([nameFlat,name3D],imagePath+prefix+'kelvin_layer5.png')


        # Additional
        axNum = 10
        self.__setAllColors(tc.TUMGrayMedium())
        for e in self.edges[36:]:
            if e:
                e.color = tc.TUMBlue()
                e.showLabel = True
                e.showArrow = True

        for n in self.nodes[24:]:
            if n:
                n.color = tc.TUMOrange()
                n.showLabel = True

        for n in self.nodes:
            if n:
                n.plotNode(ax[axNum])
        for e in self.edges:
            if e:
                e.plotEdge(ax[axNum])

        pf.setLabels(ax[axNum])
        pf.setAxesEqual(ax[axNum])

        plt.figure(axNum+1)
        nameAdd = imagePath+prefix+'kelvin_add.png'
        plt.savefig(nameAdd,dpi=300)


        # Faces
        axNum = 11
        self.__setAllColors(tc.TUMGrayMedium())
        for f in self.faces:
            if f:
                f.showNormalVec = True
                f.showLabel = True
                f.plotFace(ax[axNum])
        for e in self.edges:
            if e:
                e.plotEdge(ax[axNum])
        pf.setLabels(ax[axNum])
        pf.setAxesEqual(ax[axNum])

        plt.figure(axNum+1)
        nameAdd = imagePath+prefix+'kelvin_faces.png'
        plt.savefig(nameAdd,dpi=300)

#-------------------------------------------------------------------------
#    Set colors and hide everything
#-------------------------------------------------------------------------
    def __setAllColors(self,color):
        for n in self.nodes:
            if n:
                n.color = color
                n.showLabel = False
        for e in self.edges:
            if e:
                e.color = color
                e.showLabel = False
                e.showArrow = False








class Prism:
    def __init__(self):
        pass


#-------------------------------------------------------------------------
#    Create node
#-------------------------------------------------------------------------
    def createNode(self,x,y,z,node):
        '''
        Creating node at given location if it is meant to be created and if it
        is not created yet.

        :param int x: x-Coordinate of the node
        :param int y: y-Coordinate of the node
        :param int z: z-Coordinate of the node
        :param bool createNode: Set to False if the node is not needed in this
                                cell (for example at the border)
        :param nodeOld: old node, if it already existed

        :return: New node

        '''

#        if not createNode:
#            return False
#        else:
        if not node.projectedNode:
            newNode = Node(x,y,z)
            node.projectedNode = newNode
            return newNode

        else:
#            cc.printYellow('using projected node')
            return node.projectedNode

#-------------------------------------------------------------------------
#    Create edge
#-------------------------------------------------------------------------
    def createEdge(self,n1,n2,createEdge=True):
        '''
        Creating edge between two given nodes. If at least one of the nodes
        does not exist, then the edge is not created.

        :param Node n1: Start node
        :param Node n2: End node
        :return: New edge

        '''
        if n1 == False or n2 == False or not createEdge:
            return False
        else:
            edgeExisted = False
            for e in n1.edges:
                if e.startNode == n2 or e.endNode == n2:
                    edgeExisted = True
                    oldEdge = e
            if not edgeExisted:
                return Edge(n1,n2)
            else:
                if oldEdge.startNode == n1:
                    return oldEdge
                else:
                    return -oldEdge
#-------------------------------------------------------------------------
#    Create face
#-------------------------------------------------------------------------
    def createFace(self,edges):
        '''
        Creating face between given edges. If any of the edges does not exist,
        then the face i not created.

        :param Edge edges: list of edges to define face
        :return: New face

        '''
        if any([e == False for e in edges]):
            return False
        faceExisted = False
        facesOld = []
        for e in edges:
            for f in e.faces:
                if not f in facesOld:
                    facesOld.append(f)
                    facesOld.append(-f)
        for f in facesOld:
            if all([e in edges for e in f.edges]):
                faceExisted = True
                oldFace = f


        if not faceExisted:
            return Face(edges)
        else:
            return oldFace


class Prism4(Prism):
    def __init__(self,n0,n1,n2,n3,disp0,disp1,disp2,disp3):
        super().__init__()
        self.n0 = n0
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3

        coords4 = n0.coordinates+disp0
        coords5 = n1.coordinates+disp1
        coords6 = n2.coordinates+disp2
        coords7 = n3.coordinates+disp3

        self.n4 = self.createNode(*coords4,self.n0)
        self.n5 = self.createNode(*coords5,self.n1)
        self.n6 = self.createNode(*coords6,self.n2)
        self.n7 = self.createNode(*coords7,self.n3)


        self.nodes = [self.n0,self.n1,self.n2,self.n3,self.n4,self.n5,self.n6,self.n7]


        self.e0 = self.createEdge(self.n0,self.n4)
        self.e1 = self.createEdge(self.n1,self.n5)
        self.e2 = self.createEdge(self.n2,self.n6)
        self.e3 = self.createEdge(self.n3,self.n7)

        self.e4 = self.createEdge(self.n0,self.n1)
        self.e5 = self.createEdge(self.n1,self.n2)
        self.e6 = self.createEdge(self.n2,self.n3)
        self.e7 = self.createEdge(self.n3,self.n0)

        self.e8 = self.createEdge(self.n4,self.n5)
        self.e9 = self.createEdge(self.n5,self.n6)
        self.e10 = self.createEdge(self.n6,self.n7)
        self.e11 = self.createEdge(self.n7,self.n4)

        self.edges = [self.e0,self.e1,self.e2,self.e3,self.e4,self.e5,self.e6,self.e7,self.e8,self.e9,self.e10,self.e11]


#        self.e0 = Edge(self.n0,self.n4)
#        e1 = Edge(self.n1,self.n5)
#        e2 = Edge(self.n2,self.n6)
#        e3 = Edge(self.n3,self.n7)


class Prism6(Prism):
    def __init__(self,n0,n1,n2,n3,n4,n5,disp0,disp1,disp2,disp3,disp4,disp5):
        super().__init__()
        self.n0 = n0
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4
        self.n5 = n5

        coords6 = n0.coordinates+disp0
        coords7 = n1.coordinates+disp1
        coords8 = n2.coordinates+disp2
        coords9 = n3.coordinates+disp3
        coords10 = n4.coordinates+disp4
        coords11 = n5.coordinates+disp5


        self.n6 = self.createNode(*coords6,self.n0)
        self.n7 = self.createNode(*coords7,self.n1)
        self.n8 = self.createNode(*coords8,self.n2)
        self.n9 = self.createNode(*coords9,self.n3)
        self.n10 = self.createNode(*coords10,self.n4)
        self.n11 = self.createNode(*coords11,self.n5)


        self.nodes = [self.n0,self.n1,self.n2,self.n3,self.n4,self.n5,self.n6,self.n7,self.n8,self.n9,self.n10,self.n11]


        self.e0 = self.createEdge(self.n0,self.n6)
        self.e1 = self.createEdge(self.n1,self.n7)
        self.e2 = self.createEdge(self.n2,self.n8)
        self.e3 = self.createEdge(self.n3,self.n9)
        self.e4 = self.createEdge(self.n4,self.n10)
        self.e5 = self.createEdge(self.n5,self.n11)

        self.e6 = self.createEdge(self.n0,self.n1)
        self.e7 = self.createEdge(self.n1,self.n2)
        self.e8 = self.createEdge(self.n2,self.n3)
        self.e9 = self.createEdge(self.n3,self.n4)
        self.e10 = self.createEdge(self.n4,self.n5)
        self.e11 = self.createEdge(self.n5,self.n0)

        self.e12 = self.createEdge(self.n6,self.n7)
        self.e13 = self.createEdge(self.n7,self.n8)
        self.e14 = self.createEdge(self.n8,self.n9)
        self.e15 = self.createEdge(self.n9,self.n10)
        self.e16 = self.createEdge(self.n10,self.n11)
        self.e17 = self.createEdge(self.n11,self.n6)


        self.edges = [self.e0,self.e1,self.e2,self.e3,self.e4,self.e5,self.e6,self.e7,self.e8,self.e9,self.e10,self.e11,
                      self.e12,self.e13,self.e14,self.e15,self.e16,self.e17]



class PrismN(Prism):
    def __init__(self,nodes,disp,createVolume=True):
        super().__init__()
        nodes1 = nodes
        nodes2 = []
        for (n,d) in zip(nodes1,disp):
            (x,y,z) = n.coordinates+d
            nodes2.append(self.createNode(x,y,z,n))

        self.nodes = nodes1+nodes2


        edges1 = []
        for (n1,n2) in zip(nodes1,nodes2):
            edges1.append(self.createEdge(n1,n2))


        edges2 = []
        for (n1,n2) in zip(nodes1[:-1],nodes1[1:]):
            edges2.append(self.createEdge(n1,n2))
        edges2.append(self.createEdge(nodes1[-1],nodes1[0]))


        edges3 = []
        for (n1,n2) in zip(nodes2[:-1],nodes2[1:]):
            edges3.append(self.createEdge(n1,n2))
        edges3.append(self.createEdge(nodes2[-1],nodes2[0]))


        self.edges = edges1+edges2+edges3

        self.faces = []

        self.faces.append(self.createFace([-e for e in reversed(edges2)]))
        self.faces.append(self.createFace(edges3))
#
#

        for (e0,e1,e2,e3) in zip(edges2,edges1,edges3,edges1[1:]+[edges1[0],]):
#            pass
#            self.faces.append(self.createFace([-e0,e1,e2,-e3]))
            self.faces.append(self.createFace([e3,-e2,-e1,e0]))

        if createVolume:
            self.volume = Volume(self.faces)
        else:
            self.volume = None



#class Prism2N(Prism):
#    def __init__()


class Combine2Prisms:
    def __init__(self,p1,p2):
        cc.printYellow('combine2Prisms: combining')
        if p1.volume is not None:
            cc.printRed('combine2Prisms: p1 already has a volume, need prism without volume')

        if p2.volume is not None:
            cc.printRed('combine2Prisms: p2 already has a volume, need prism without volume')


        if p1.volume is None and p2.volume is None:
            faces = p1.faces[:]
            for f in p2.faces:
                if -f in faces:
                    faces.remove(-f)
                    f.delete()
                else:
                    faces.append(f)

            commonEdges = []
            for e in p1.edges:
                if e in p2.edges:
                    commonEdges.append(e)

            facesToCombine = []
            for e in commonEdges:
                for f in e.faces:
                    otherFaces = e.faces[:]
                    otherFaces.remove(f)
                    for f2 in otherFaces:
                        if abs(np.linalg.norm(f.normalVec[0]-f2.normalVec[0]))<1e-3 or abs(np.linalg.norm(f.normalVec[0]+f2.normalVec[0]))<1e-3:
                            cc.printYellow('combine2Prisms Found faces to combine:',f,f2)
                            alreadyFound = False
                            for comb in facesToCombine:
                                if f in comb or -f in comb:
                                    alreadyFound = True
                            if not alreadyFound:
                                facesToCombine.append((f,f2))

            cc.printYellow('combine2Prisms',facesToCombine)

#            for




            self.nodes = p1.nodes + p2.nodes
            self.edges = p1.edges+ p2.edges
            self.faces = faces
            self.volume = Volume(faces)

        else:
            self.nodes = []
            self.edegs = []
            self.faces = []
            self.volume = None

    #
#








#        coords6 = n0.coordinates+disp0
#        coords7 = n1.coordinates+disp1
#        coords8 = n2.coordinates+disp2
#        coords9 = n3.coordinates+disp3
#        coords10 = n4.coordinates+disp4
#        coords11 = n5.coordinates+disp5


#        self.n6 = self.createNode(*coords6,self.n0)
#        self.n7 = self.createNode(*coords7,self.n1)
#        self.n8 = self.createNode(*coords8,self.n2)
#        self.n9 = self.createNode(*coords9,self.n3)
#        self.n10 = self.createNode(*coords10,self.n4)
#        self.n11 = self.createNode(*coords11,self.n5)


#        self.nodes = [self.n0,self.n1,self.n2,self.n3,self.n4,self.n5,self.n6,self.n7,self.n8,self.n9,self.n10,self.n11]


#        for
#
#        self.e0 = self.createEdge(self.n0,self.n6)
#        self.e1 = self.createEdge(self.n1,self.n7)
#        self.e2 = self.createEdge(self.n2,self.n8)
#        self.e3 = self.createEdge(self.n3,self.n9)
#        self.e4 = self.createEdge(self.n4,self.n10)
#        self.e5 = self.createEdge(self.n5,self.n11)
#
#        self.e6 = self.createEdge(self.n0,self.n1)
#        self.e7 = self.createEdge(self.n1,self.n2)
#        self.e8 = self.createEdge(self.n2,self.n3)
#        self.e9 = self.createEdge(self.n3,self.n4)
#        self.e10 = self.createEdge(self.n4,self.n5)
#        self.e11 = self.createEdge(self.n5,self.n0)
#
#        self.e12 = self.createEdge(self.n6,self.n7)
#        self.e13 = self.createEdge(self.n7,self.n8)
#        self.e14 = self.createEdge(self.n8,self.n9)
#        self.e15 = self.createEdge(self.n9,self.n10)
#        self.e16 = self.createEdge(self.n10,self.n11)
#        self.e17 = self.createEdge(self.n11,self.n6)
#
#
#        self.edges = [self.e0,self.e1,self.e2,self.e3,self.e4,self.e5,self.e6,self.e7,self.e8,self.e9,self.e10,self.e11,
#                      self.e12,self.e13,self.e14,self.e15,self.e16,self.e17]
#




class Grid3DKelvin(PrimalComplex3D):


    def __init__(self,anzX=0,anzY=None,anzZ=None,fill=True,
                   borderVolumesBottom=False,
                   borderVolumesTop=False,
                   borderVolumesFront=False,
                   borderVolumesBack=False,
                   borderVolumesLeft=False,
                   borderVolumesRight=False,
                   fillCube=True,
                   create_prisms=False,
                   **kwargs):

        if anzY == None:
            anzY = anzX
        if anzZ == None:
            anzZ = anzX

        kelvinCells = []
        kelvinCellsLayer = []
        kelvinCellsLine = []


        # First kelvin cell
        kelvinCellsLine.append(KelvinCell(0,0,0))

        # First line
        for i in range(anzX):
            kelvinCellsLine.append(KelvinCell(4*(i+1)*d,0,0,n14old=kelvinCellsLine[-1].n9,      # predecessor in x
                                                            n7old=kelvinCellsLine[-1].n5,       # predecessor in x
                                                            n13old=kelvinCellsLine[-1].n10,     # predecessor in x
                                                            n19old=kelvinCellsLine[-1].n17))    # predecessor in x
        kelvinCellsLayer.append(kelvinCellsLine)



        # First layer
        for j in range(anzY):
            kelvinCellsLine = []
            #First cell in line
            kelvinCellsLine.append(KelvinCell(0,(j+1)*4*d,0,n8old=kelvinCellsLayer[-1][0].n11,      # predecessor in y
                                                            n4old=kelvinCellsLayer[-1][0].n6,       # predecessor in y
                                                            n15old=kelvinCellsLayer[-1][0].n12,     # predecessor in y
                                                            n16old=kelvinCellsLayer[-1][0].n18))    # predecessor in y
            # Add other cells to line
            for i,c in enumerate(kelvinCellsLayer[-1][1:]):
                kelvinCellsLine.append(KelvinCell(4*(i+1)*d,(j+1)*4*d,0,n8old=c.n11,                        # predecessor in y
                                                                        n4old=c.n6,                         # predecessor in y
                                                                        n15old=c.n12,                       # predecessor in y
                                                                        n16old=c.n18,                       # predecessor in y
                                                                        n14old=kelvinCellsLine[-1].n9,      # predecessor in x
                                                                        n7old=kelvinCellsLine[-1].n5,       # predecessor in x
                                                                        n13old=kelvinCellsLine[-1].n10,     # predecessor in x
                                                                        n19old=kelvinCellsLine[-1].n17))    # predecessor in x
            kelvinCellsLayer.append(kelvinCellsLine)
        kelvinCells.append(kelvinCellsLayer)



        for k in range(anzZ):
            kelvinCellsLayer = []
            kelvinCellsLine = []
        #    k=0

            # first cell in layer
            kelvinCellsLine.append(KelvinCell(0,0,4*(k+1)*d,n20old=kelvinCells[-1][0][0].n0,    # predecessor in z
                                                            n21old=kelvinCells[-1][0][0].n1,    # predecessor in z
                                                            n22old=kelvinCells[-1][0][0].n2,    # predecessor in z
                                                            n23old=kelvinCells[-1][0][0].n3))   # predecessor in z
            # first line in layer
            for i in range(anzX):
                kelvinCellsLine.append(KelvinCell(4*(i+1)*d,0,4*(k+1)*d,n14old=kelvinCellsLine[-1].n9,      # predecessor in x
                                                                        n7old=kelvinCellsLine[-1].n5,       # predecessor in x
                                                                        n13old=kelvinCellsLine[-1].n10,     # predecessor in x
                                                                        n19old=kelvinCellsLine[-1].n17,     # predecessor in x
                                                                        n20old=kelvinCells[-1][0][i+1].n0,  # predecessor in z
                                                                        n21old=kelvinCells[-1][0][i+1].n1,  # predecessor in z
                                                                        n22old=kelvinCells[-1][0][i+1].n2,  # predecessor in z
                                                                        n23old=kelvinCells[-1][0][i+1].n3)) # predecessor in z
            kelvinCellsLayer.append(kelvinCellsLine)

            # Add other lines to layer
            for j in range(anzY):
                kelvinCellsLine = []

                # First cell in line
                kelvinCellsLine.append(KelvinCell(0,(j+1)*4*d,4*(k+1)*d,n8old=kelvinCellsLayer[-1][0].n11,      # predecessor in y
                                                                        n4old=kelvinCellsLayer[-1][0].n6,       # predecessor in y
                                                                        n15old=kelvinCellsLayer[-1][0].n12,     # predecessor in y
                                                                        n16old=kelvinCellsLayer[-1][0].n18,     # predecessor in y
                                                                        n20old=kelvinCells[-1][j+1][0].n0,    # predecessor in z
                                                                        n21old=kelvinCells[-1][j+1][0].n1,    # predecessor in z
                                                                        n22old=kelvinCells[-1][j+1][0].n2,    # predecessor in z
                                                                        n23old=kelvinCells[-1][j+1][0].n3))   # predecessor in z

                # Add other cells to line
                for i,c in enumerate(kelvinCellsLayer[j][1:]):
                    kelvinCellsLine.append(KelvinCell(4*(i+1)*d,(j+1)*4*d,4*(k+1)*d,n14old=kelvinCellsLine[-1].n9,      # predecessor in x
                                                                                    n7old=kelvinCellsLine[-1].n5,       # predecessor in x
                                                                                    n13old=kelvinCellsLine[-1].n10,     # predecessor in x
                                                                                    n19old=kelvinCellsLine[-1].n17,     # predecessor in xn14old=c.n13,
                                                                                    n8old=kelvinCellsLayer[-1][i+1].n11,      # predecessor in y
                                                                                    n4old=kelvinCellsLayer[-1][i+1].n6,       # predecessor in y
                                                                                    n15old=kelvinCellsLayer[-1][i+1].n12,     # predecessor in y
                                                                                    n16old=kelvinCellsLayer[-1][i+1].n18,     # predecessor in y
                                                                                    n20old=kelvinCells[-1][j+1][i+1].n0,    # predecessor in z
                                                                                    n21old=kelvinCells[-1][j+1][i+1].n1,    # predecessor in z
                                                                                    n22old=kelvinCells[-1][j+1][i+1].n2,    # predecessor in z
                                                                                    n23old=kelvinCells[-1][j+1][i+1].n3))   # predecessor in z
                kelvinCellsLayer.append(kelvinCellsLine)
            kelvinCells.append(kelvinCellsLayer)






        addKelvinCells = []
        for i in range(anzX):
            for j in range(anzY):
                for k in range(anzZ):

    #                cc.printBlue('x:',i,i+1)
    #                cc.printBlue('y:',j,j+1)
    #                cc.printBlue('z:',k,k+1)
                    kc1 = kelvinCells[k][j][i]
                    kc2 = kelvinCells[k][j][i+1]
                    kc3 = kelvinCells[k][j+1][i+1]
                    kc4 = kelvinCells[k][j+1][i]
                    kc5 = kelvinCells[k+1][j][i]
                    kc6 = kelvinCells[k+1][j][i+1]
                    kc7 = kelvinCells[k+1][j+1][i+1]
                    kc8 = kelvinCells[k+1][j+1][i]
                    addKelvinCells.append(KelvinCell(0,0,0,  n0old  = kc5.n10,
                                                             n1old  = kc6.n12,
                                                             n2old  = kc7.n14,
                                                             n3old  = kc5.n11,
                                                             n4old  = kc5.n17,
                                                             n5old  = kc6.n18,
                                                             n6old  = kc7.n19,
                                                             n7old  = kc5.n18,
                                                             n8old  = kc2.n3,
                                                             n9old  = kc2.n2,
                                                             n10old = kc3.n0,
                                                             n11old = kc3.n3,
                                                             n12old = kc4.n1,
                                                             n13old = kc4.n0,
                                                             n14old = kc1.n2,
                                                             n15old = kc1.n1,
                                                             n16old = kc1.n5,
                                                             n17old = kc2.n6,
                                                             n18old = kc4.n5,
                                                             n19old = kc1.n6,
                                                             n20old = kc1.n10,
                                                             n21old = kc2.n12,
                                                             n22old = kc4.n9,
                                                             n23old = kc1.n11))



        if fillCube:
            # Top border
            addKelvinCellsUpper = []
            if fill:
                for i in range(anzX):
                    for j in range(anzY):

                        kc1 = kelvinCells[-1][j][i]
                        kc2 = kelvinCells[-1][j][i+1]
                        kc3 = kelvinCells[-1][j+1][i+1]
                        kc4 = kelvinCells[-1][j+1][i]
                        addKelvinCellsUpper.append(KelvinCell(0,0,0,createPart = 'lowerHalf',
                                                                 n8old  = kc2.n3,
                                                                 n9old  = kc2.n2,
                                                                 n10old = kc3.n0,
                                                                 n11old = kc3.n3,
                                                                 n12old = kc4.n1,
                                                                 n13old = kc4.n0,
                                                                 n14old = kc1.n2,
                                                                 n15old = kc1.n1,
                                                                 n16old = kc1.n5,
                                                                 n17old = kc2.n6,
                                                                 n18old = kc4.n5,
                                                                 n19old = kc1.n6,
                                                                 n20old = kc1.n10,
                                                                 n21old = kc2.n12,
                                                                 n22old = kc4.n9,
                                                                 n23old = kc1.n11))

                for k in addKelvinCellsUpper:
                    addKelvinCells.append(k)

                # Bottom border
                addKelvinCellsLower = []
                for i in range(anzX):
                    for j in range(anzY):

                        kc5 = kelvinCells[0][j][i]
                        kc6 = kelvinCells[0][j][i+1]
                        kc7 = kelvinCells[0][j+1][i+1]
                        kc8 = kelvinCells[0][j+1][i]
                        addKelvinCellsLower.append(KelvinCell(0,0,0,createPart = 'upperHalf',
                                                                 n0old  = kc5.n10,
                                                                 n1old  = kc6.n12,
                                                                 n2old  = kc7.n14,
                                                                 n3old  = kc5.n11,
                                                                 n4old  = kc5.n17,
                                                                 n5old  = kc6.n18,
                                                                 n6old  = kc7.n19,
                                                                 n7old  = kc5.n18,
                                                                 n8old  = kc6.n23,
                                                                 n9old  = kc6.n22,
                                                                 n10old = kc7.n20,
                                                                 n11old = kc7.n23,
                                                                 n12old = kc8.n21,
                                                                 n13old = kc8.n20,
                                                                 n14old = kc5.n22,
                                                                 n15old = kc5.n21))
                for k in addKelvinCellsLower:
                    addKelvinCells.append(k)


                # Front border
                addKelvinCellsFront = []
                for i in range(anzX):
                    addKelvinCellsFrontLine = []
                    for k in range(anzZ):

                        kc3 = kelvinCells[k][0][i+1]
                        kc4 = kelvinCells[k][0][i]
                        kc7 = kelvinCells[k+1][0][i+1]
                        kc8 = kelvinCells[k+1][0][i]
                        addKelvinCellsFrontLine.append(KelvinCell(-3*a,0,0,  createPart = 'backHalf',
                                                                 n1old  = kc7.n15,
                                                                 n2old  = kc7.n14,
                                                                 n3old  = kc8.n8,
                                                                 n5old  = kc7.n16,
                                                                 n6old  = kc7.n19,
                                                                 n7old  = kc8.n16,
                                                                 n10old = kc3.n0,
                                                                 n11old = kc3.n3,
                                                                 n12old = kc4.n1,
                                                                 n13old = kc4.n0,
                                                                 n17old = kc3.n4,
                                                                 n18old = kc3.n7,
                                                                 n19old = kc4.n4,
                                                                 n21old = kc3.n15,
                                                                 n22old = kc3.n14,
                                                                 n23old = kc4.n8))
                    addKelvinCellsFront.append(addKelvinCellsFrontLine)

                for line in addKelvinCellsFront:
                    for k in line:
                        addKelvinCells.append(k)
        #
                # Back border
                addKelvinCellsBack = []
                for i in range(anzX):
                    addKelvinCellsBackLine = []
                    for k in range(anzZ):

                        kc1 = kelvinCells[k][-1][i]
                        kc2 = kelvinCells[k][-1][i+1]
                        kc5 = kelvinCells[k+1][-1][i]
                        kc6 = kelvinCells[k+1][-1][i+1]
                        addKelvinCellsBackLine.append(KelvinCell(0,0,0,  createPart = 'frontHalf',
                                                                 n0old  = kc5.n10,
                                                                 n1old  = kc6.n12,
                                                                 n3old  = kc5.n11,
                                                                 n4old  = kc5.n17,
                                                                 n5old  = kc6.n18,
                                                                 n7old  = kc5.n18,
                                                                 n8old  = kc2.n3,
                                                                 n9old  = kc2.n2,
                                                                 n14old = kc1.n2,
                                                                 n15old = kc1.n1,
                                                                 n16old = kc1.n5,
                                                                 n17old = kc2.n6,
                                                                 n19old = kc1.n6,
                                                                 n20old = kc1.n10,
                                                                 n21old = kc2.n12,
                                                                 n23old = kc1.n11))

                    addKelvinCellsBack.append(addKelvinCellsBackLine)

                for line in addKelvinCellsBack:
                    for k in line:
                        addKelvinCells.append(k)


                # Left border
                addKelvinCellsLeft = []
                for j in range(anzY):
                    addKelvinCellsLeftLine = []
                    for k in range(anzZ):

                        kc2 = kelvinCells[k][j][0]
                        kc3 = kelvinCells[k][j+1][0]
                        kc6 = kelvinCells[k+1][j][0]
                        kc7 = kelvinCells[k+1][j+1][0]
                        addKelvinCellsLeftLine.append(KelvinCell(-5*a,0,0,  createPart = 'rightHalf',
                                                                 n0old  = kc6.n13,
                                                                 n1old  = kc6.n12,
                                                                 n2old  = kc7.n14,
                                                                 n4old  = kc6.n19,
                                                                 n5old  = kc6.n18,
                                                                 n6old  = kc7.n19,
                                                                 n8old  = kc2.n3,
                                                                 n9old  = kc2.n2,
                                                                 n10old = kc3.n0,
                                                                 n11old = kc3.n3,
                                                                 n16old = kc2.n7,
                                                                 n17old = kc2.n6,
                                                                 n18old = kc3.n7,
                                                                 n20old = kc2.n13,
                                                                 n21old = kc2.n12,
                                                                 n22old = kc3.n14))
                    addKelvinCellsLeft.append(addKelvinCellsLeftLine)


                for line in addKelvinCellsLeft:
                    for k in line:
                        addKelvinCells.append(k)



                # right border
                addKelvinCellsRight = []
                for j in range(anzY):
                    addKelvinCellsRightLine = []
                    for k in range(anzZ):

                        kc1 = kelvinCells[k][j][-1]
                        kc4 = kelvinCells[k][j+1][-1]
                        kc5 = kelvinCells[k+1][j][-1]
                        kc8 = kelvinCells[k+1][j+1][-1]
                        addKelvinCellsRightLine.append(KelvinCell(-5*a,0,0,  createPart = 'leftHalf',
                                                                 n0old  = kc5.n10,
                                                                 n2old  = kc8.n9,
                                                                 n3old  = kc5.n11,
                                                                 n4old  = kc5.n17,
                                                                 n6old  = kc8.n17,
                                                                 n7old  = kc5.n18,
                                                                 n12old = kc4.n1,
                                                                 n13old = kc4.n0,
                                                                 n14old = kc1.n2,
                                                                 n15old = kc1.n1,
                                                                 n16old = kc1.n5,
                                                                 n18old = kc4.n5,
                                                                 n19old = kc1.n6,
                                                                 n20old = kc1.n10,
                                                                 n21old = kc2.n12,
                                                                 n22old = kc4.n9,
                                                                 n23old = kc1.n11))
                    addKelvinCellsRight.append(addKelvinCellsRightLine)

                for line in addKelvinCellsRight:
                    for k in line:
                        addKelvinCells.append(k)


                # Lower back rim

                addKelvinCellsLowerBack = []
                if anzX > 0:

                    kc5 = kelvinCells[0][-1][0]
                    kc6 = kelvinCells[0][-1][1]
                    addKelvinCellsLowerBack.append(KelvinCell(2*d,(anzY+0.5)*4*d,-2*d,  createPart = 'upperFrontQuarter',
                                                             n0old  = kc5.n10,
                                                             n1old  = kc6.n12,
                                                             n3old  = kc5.n11,
                                                             n4old  = kc5.n17,
                                                             n5old  = kc6.n18,
                                                             n7old  = kc5.n18,
                                                             n8old  = kc6.n23,
                                                             n9old  = kc6.n22,
                                                             n14old = kc5.n22,
                                                             n15old = kc5.n21))

                for i in range(anzX-1):

                    kc5 = kelvinCells[0][-1][i+1]
                    kc6 = kelvinCells[0][-1][i+2]
                    kc9 = addKelvinCellsLowerBack[-1]
                    addKelvinCellsLowerBack.append(KelvinCell((i+1.5)*4*d,(anzY+0.5)*4*d,-2*d,  createPart = 'upperFrontQuarter',
                                                             n0old  = kc5.n10,
                                                             n1old  = kc6.n12,
                                                             n3old  = kc5.n11,
                                                             n4old  = kc5.n17,
                                                             n5old  = kc6.n18,
                                                             n7old  = kc5.n18,
                                                             n8old  = kc6.n23,
                                                             n9old  = kc6.n22,
                                                             n14old = kc5.n22,
                                                             n15old = kc5.n21,
                                                             n101old = kc9.n100))

                for kc in addKelvinCellsLowerBack:
                    addKelvinCells.append(kc)
                    addKelvinCellsLower.append(kc)
        #            addKelvinCellsBack.append(kc)


                # Lower front rim
                addKelvinCellsLowerFront = []
                if anzX > 0:

                    kc7 = kelvinCells[0][0][1]
                    kc8 = kelvinCells[0][0][0]
                    addKelvinCellsLowerFront.append(KelvinCell(2*d,-2*d,-2*d,  createPart = 'upperBackQuarter',
                                                             n1old  = kc7.n15,
                                                             n2old  = kc7.n14,
                                                             n3old  = kc8.n8,
                                                             n5old = kc7.n16,
                                                             n6old  = kc7.n19,
                                                             n7old = kc8.n16,
                                                             n10old = kc7.n20,
                                                             n11old = kc7.n23,
                                                             n12old = kc8.n21,
                                                             n13old = kc8.n20))
                for i in range(anzX-1):

                    kc7 = kelvinCells[0][0][i+2]
                    kc8 = kelvinCells[0][0][i+1]
                    kc9 = addKelvinCellsLowerFront[-1]
                    addKelvinCellsLowerFront.append(KelvinCell((i+1.5)*4*d,-2*d,-2*d,  createPart = 'upperBackQuarter',
                                                             n1old  = kc7.n15,
                                                             n2old  = kc7.n14,
                                                             n3old  = kc8.n8,
                                                             n5old = kc7.n16,
                                                             n6old  = kc7.n19,
                                                             n7old = kc8.n16,
                                                             n10old = kc7.n20,
                                                             n11old = kc7.n23,
                                                             n12old = kc8.n21,
                                                             n13old = kc8.n20,
                                                             n101old = kc9.n100))



                for kc in addKelvinCellsLowerFront:
                    addKelvinCells.append(kc)
                    addKelvinCellsLower.append(kc)
        #            addKelvinCellsFront.append(kc)
        #

                # Upper back rim
                addKelvinCellsUpperBack = []
                if anzX > 0:

                    kc1 = kelvinCells[-1][-1][0]
                    kc2 = kelvinCells[-1][-1][1]
                    addKelvinCellsUpperBack.append(KelvinCell(2*d,(anzY+0.5)*4*d,(anzZ+0.5)*4*d,  createPart = 'lowerFrontQuarter',
                                                             n8old  = kc2.n3,
                                                             n9old  = kc2.n2,
                                                             n14old = kc1.n2,
                                                             n15old = kc1.n1,
                                                             n16old = kc1.n5,
                                                             n17old = kc2.n6,
                                                             n19old = kc1.n6,
                                                             n20old = kc1.n10,
                                                             n21old = kc2.n12,
                                                             n23old = kc1.n11))
                for i in range(anzX-1):

                    kc1 = kelvinCells[-1][-1][i+1]
                    kc2 = kelvinCells[-1][-1][i+2]
                    kc9 = addKelvinCellsUpperBack[-1]
                    addKelvinCellsUpperBack.append(KelvinCell((i+1.5)*4*d,(anzY+0.5)*4*d,(anzZ+0.5)*4*d,  createPart = 'lowerFrontQuarter',
                                                             n8old  = kc2.n3,
                                                             n9old  = kc2.n2,
                                                             n14old = kc1.n2,
                                                             n15old = kc1.n1,
                                                             n16old = kc1.n5,
                                                             n17old = kc2.n6,
                                                             n19old = kc1.n6,
                                                             n20old = kc1.n10,
                                                             n21old = kc2.n12,
                                                             n23old = kc1.n11,
                                                             n101old = kc9.n100))



                for kc in addKelvinCellsUpperBack:
                    addKelvinCells.append(kc)
                    addKelvinCellsUpper.append(kc)
        #            addKelvinCellsBack.append(kc)


                # Upper front rim
                addKelvinCellsUpperFront = []
                if anzX > 0:

                    kc3 = kelvinCells[-1][0][1]
                    kc4 = kelvinCells[-1][0][0]
                    addKelvinCellsUpperFront.append(KelvinCell(2*d,-2*d,(anzZ+0.5)*4*d,  createPart = 'lowerBackQuarter',
                                                             n10old = kc3.n0,
                                                             n11old = kc3.n3,
                                                             n12old = kc4.n1,
                                                             n13old = kc4.n0,
                                                             n17old = kc3.n4,
                                                             n18old = kc4.n5,
                                                             n19old = kc4.n4,
                                                             n21old = kc3.n15,
                                                             n22old = kc4.n9,
                                                             n23old = kc4.n8))



                for i in range(anzX-1):

                    kc3 = kelvinCells[-1][0][i+2]
                    kc4 = kelvinCells[-1][0][i+1]
                    kc9 = addKelvinCellsUpperFront[-1]
                    addKelvinCellsUpperFront.append(KelvinCell((i+1.5)*4*d,-2*d,(anzZ+0.5)*4*d,  createPart = 'lowerBackQuarter',
                                                             n10old = kc3.n0,
                                                             n11old = kc3.n3,
                                                             n12old = kc4.n1,
                                                             n13old = kc4.n0,
                                                             n17old = kc3.n4,
                                                             n18old = kc4.n5,
                                                             n19old = kc4.n4,
                                                             n21old = kc3.n15,
                                                             n22old = kc4.n9,
                                                             n23old = kc4.n8,
                                                             n101old = kc9.n100))


                for kc in addKelvinCellsUpperFront:
                    addKelvinCells.append(kc)
                    addKelvinCellsUpper.append(kc)
        #            addKelvinCellsFront.append(kc)


                # Lower right rim
                addKelvinCellsLowerRight = []
                if anzY > 0:

                    kc5 = kelvinCells[0][0][-1]
                    kc8 = kelvinCells[0][1][-1]
                    addKelvinCellsLowerRight.append(KelvinCell((anzX+0.5)*4*d,2*d,-2*d,  createPart = 'upperLeftQuarter',
                                                             n0old  = kc5.n10,
                                                             n2old  = kc8.n9,
                                                             n3old  = kc5.n11,
                                                             n4old  = kc5.n17,
                                                             n6old  = kc8.n17,
                                                             n7old  = kc5.n18,
                                                             n12old = kc8.n21,
                                                             n13old = kc8.n20,
                                                             n14old = kc5.n22,
                                                             n15old = kc5.n21))


                for j in range(anzY-1):

                    kc5 = kelvinCells[0][j+1][-1]
                    kc8 = kelvinCells[0][j+2][-1]
                    kc9 = addKelvinCellsLowerRight[-1]
                    addKelvinCellsLowerRight.append(KelvinCell((anzX+0.5)*4*d,(j+1.5)*4*d,-2*d,  createPart = 'upperLeftQuarter',
                                                             n0old  = kc5.n10,
                                                             n2old  = kc8.n9,
                                                             n3old  = kc5.n11,
                                                             n4old  = kc5.n17,
                                                             n6old  = kc8.n17,
                                                             n7old  = kc5.n18,
                                                             n12old = kc8.n21,
                                                             n13old = kc8.n20,
                                                             n14old = kc5.n22,
                                                             n15old = kc5.n21,
                                                             n103old = kc9.n102))


                for kc in addKelvinCellsLowerRight:
                    addKelvinCells.append(kc)
                    addKelvinCellsLower.append(kc)
        #            addKelvinCellsRight.append(kc)




                # Upper right rim
                addKelvinCellsUpperRight = []
                if anzY > 0:

                    kc1 = kelvinCells[-1][0][-1]
                    kc4 = kelvinCells[-1][1][-1]
                    addKelvinCellsUpperRight.append(KelvinCell((anzX+0.5)*4*d,2*d,(anzZ+0.5)*4*d,  createPart = 'lowerLeftQuarter',
                                                             n12old = kc4.n1,
                                                             n13old = kc4.n0,
                                                             n14old = kc1.n2,
                                                             n15old = kc1.n1,
                                                             n16old = kc1.n5,
                                                             n18old = kc4.n5,
                                                             n19old = kc1.n6,
                                                             n20old = kc1.n10,
                                                             n22old = kc4.n9,
                                                             n23old = kc1.n11))

                for j in range(anzY-1):

                    kc1 = kelvinCells[-1][j+1][-1]
                    kc4 = kelvinCells[-1][j+2][-1]
                    kc9 = addKelvinCellsUpperRight[-1]
                    addKelvinCellsUpperRight.append(KelvinCell((anzX+0.5)*4*d,(j+1.5)*4*d,(anzZ+0.5)*4*d,  createPart = 'lowerLeftQuarter',
                                                             n12old = kc4.n1,
                                                             n13old = kc4.n0,
                                                             n14old = kc1.n2,
                                                             n15old = kc1.n1,
                                                             n16old = kc1.n5,
                                                             n18old = kc4.n5,
                                                             n19old = kc1.n6,
                                                             n20old = kc1.n10,
                                                             n22old = kc4.n9,
                                                             n23old = kc1.n11,
                                                             n103old = kc9.n102))

                for kc in addKelvinCellsUpperRight:
                    addKelvinCells.append(kc)
                    addKelvinCellsUpper.append(kc)
        #            addKelvinCellsRight.append(kc)



                # Lower left rim
                addKelvinCellsLowerLeft = []
                if anzY > 0:

                    kc6 = kelvinCells[0][0][0]
                    kc7 = kelvinCells[0][1][0]
                    addKelvinCellsLowerLeft.append(KelvinCell(-2*d,2*d,-2*d,  createPart = 'upperRightQuarter',
                                                             n0old  = kc6.n13,
                                                             n1old  = kc6.n12,
                                                             n2old  = kc7.n14,
                                                             n4old  = kc6.n19,
                                                             n5old  = kc6.n18,
                                                             n6old  = kc7.n19,
                                                             n8old  = kc6.n23,
                                                             n9old  = kc6.n22,
                                                             n10old = kc7.n20,
                                                             n11old = kc7.n23))

                for j in range(anzY-1):

                    kc6 = kelvinCells[0][j+1][0]
                    kc7 = kelvinCells[0][j+2][0]
                    kc9 = addKelvinCellsLowerLeft[-1]
                    addKelvinCellsLowerLeft.append(KelvinCell(-2*d,(j+1.5)*4*d,-2*d,  createPart = 'upperRightQuarter',
                                                             n0old  = kc6.n13,
                                                             n1old  = kc6.n12,
                                                             n2old  = kc7.n14,
                                                             n4old  = kc6.n19,
                                                             n5old  = kc6.n18,
                                                             n6old  = kc7.n19,
                                                             n8old  = kc6.n23,
                                                             n9old  = kc6.n22,
                                                             n10old = kc7.n20,
                                                             n11old = kc7.n23,
                                                             n103old = kc9.n102))

                for kc in addKelvinCellsLowerLeft:
                    addKelvinCells.append(kc)
                    addKelvinCellsLower.append(kc)
        #            addKelvinCellsLeft.append(kc)


                # Upper left rim
                addKelvinCellsUpperLeft = []
                if anzY > 0:

                    kc2 = kelvinCells[-1][0][0]
                    kc3 = kelvinCells[-1][1][0]
                    addKelvinCellsUpperLeft.append(KelvinCell(-2*d,2*d,(anzZ+0.5)*4*d,  createPart = 'lowerRightQuarter',
                                                             n8old  = kc2.n3,
                                                             n9old  = kc2.n2,
                                                             n10old = kc3.n0,
                                                             n11old = kc3.n3,
                                                             n16old = kc2.n7,
                                                             n17old = kc2.n6,
                                                             n18old = kc3.n7,
                                                             n20old = kc2.n13,
                                                             n21old = kc2.n12,
                                                             n22old = kc3.n14))
                for j in range(anzY-1):

                    kc2 = kelvinCells[-1][j+1][0]
                    kc3 = kelvinCells[-1][j+2][0]
                    kc9 = addKelvinCellsUpperLeft[-1]
                    addKelvinCellsUpperLeft.append(KelvinCell(-2*d,(j+1.5)*4*d,(anzZ+0.5)*4*d,  createPart = 'lowerRightQuarter',
                                                             n8old  = kc2.n3,
                                                             n9old  = kc2.n2,
                                                             n10old = kc3.n0,
                                                             n11old = kc3.n3,
                                                             n16old = kc2.n7,
                                                             n17old = kc2.n6,
                                                             n18old = kc3.n7,
                                                             n20old = kc2.n13,
                                                             n21old = kc2.n12,
                                                             n22old = kc3.n14,
                                                             n103old = kc9.n102))

                for kc in addKelvinCellsUpperLeft:
                    addKelvinCells.append(kc)
                    addKelvinCellsUpper.append(kc)
        #            addKelvinCellsLeft.append(kc)



                # Back right rim
                addKelvinCellsBackRight = []
                if anzZ > 0:

                    kc1 = kelvinCells[0][-1][-1]
                    kc5 = kelvinCells[1][-1][-1]
                    addKelvinCellsBackRight.append(KelvinCell((anzX+0.5)*4*d,(anzY+0.5)*4*d,2*d,  createPart = 'frontLeftQuarter',
                                                             n0old  = kc5.n10,
                                                             n3old  = kc5.n11,
                                                             n4old  = kc5.n17,
                                                             n7old  = kc5.n18,
                                                             n14old = kc1.n2,
                                                             n15old = kc1.n1,
                                                             n16old = kc1.n5,
                                                             n19old = kc1.n6,
                                                             n20old = kc1.n10,
                                                             n23old = kc1.n11))

                for k in range(anzZ-1):

                    kc1 = kelvinCells[k+1][-1][-1]
                    kc5 = kelvinCells[k+2][-1][-1]
                    kc9 = addKelvinCellsBackRight[-1]
                    addKelvinCellsBackRight.append(KelvinCell((anzX+0.5)*4*d,(anzY+0.5)*4*d,(k+1.5)*4*d,  createPart = 'frontLeftQuarter',
                                                             n0old  = kc5.n10,
                                                             n3old  = kc5.n11,
                                                             n4old  = kc5.n17,
                                                             n7old  = kc5.n18,
                                                             n14old = kc1.n2,
                                                             n15old = kc1.n1,
                                                             n16old = kc1.n5,
                                                             n19old = kc1.n6,
                                                             n20old = kc1.n10,
                                                             n23old = kc1.n11,
                                                             n105old = kc9.n104))


                for kc in addKelvinCellsBackRight:
                    addKelvinCells.append(kc)
        #            addKelvinCellsBack.append(kc)
        #            addKelvinCellsRight.append(kc)



                # Back left rim
                addKelvinCellsBackLeft = []
                if anzZ > 0:


                    kc2 = kelvinCells[0][-1][0]
                    kc6 = kelvinCells[1][-1][0]
                    addKelvinCellsBackLeft.append(KelvinCell(-2*d,(anzY+0.5)*4*d,2*d,  createPart = 'frontRightQuarter',
                                                             n0old  = kc6.n13,
                                                             n1old  = kc6.n12,
                                                             n4old  = kc6.n19,
                                                             n5old  = kc6.n18,
                                                             n8old  = kc2.n3,
                                                             n9old  = kc2.n2,
                                                             n16old = kc2.n7,
                                                             n17old = kc2.n6,
                                                             n20old = kc2.n13,
                                                             n21old = kc2.n12))

                for k in range(anzZ-1):

                    kc2 = kelvinCells[k+1][-1][0]
                    kc6 = kelvinCells[k+2][-1][0]
                    kc9 = addKelvinCellsBackLeft[-1]
                    addKelvinCellsBackLeft.append(KelvinCell(-2*d,(anzY+0.5)*4*d,(k+1.5)*4*d,  createPart = 'frontRightQuarter',
                                                             n0old  = kc6.n13,
                                                             n1old  = kc6.n12,
                                                             n4old  = kc6.n19,
                                                             n5old  = kc6.n18,
                                                             n8old  = kc2.n3,
                                                             n9old  = kc2.n2,
                                                             n16old = kc2.n7,
                                                             n17old = kc2.n6,
                                                             n20old = kc2.n13,
                                                             n21old = kc2.n12,
                                                             n105old = kc9.n104))



                for kc in addKelvinCellsBackLeft:
                    addKelvinCells.append(kc)
        #            addKelvinCellsBack.append(kc)
        #            addKelvinCellsLeft.append(kc)



                # front right rim
                addKelvinCellsFrontRight = []
                if anzZ > 0:



                    kc4 = kelvinCells[0][0][-1]
                    kc8 = kelvinCells[1][0][-1]
                    addKelvinCellsFrontRight.append(KelvinCell((anzX+0.5)*4*d,-2*d,2*d,  createPart = 'backLeftQuarter',
                                                             n2old  = kc8.n9,
                                                             n3old  = kc8.n8,
                                                             n6old  = kc8.n17,
                                                             n7old  = kc8.n16,
                                                             n12old = kc4.n1,
                                                             n13old = kc4.n0,
                                                             n18old = kc4.n5,
                                                             n19old = kc4.n4,
                                                             n22old = kc4.n9,
                                                             n23old = kc4.n8))
                for k in range(anzZ-1):



                    kc4 = kelvinCells[k+1][0][-1]
                    kc8 = kelvinCells[k+2][0][-1]
                    kc9 = addKelvinCellsFrontRight[-1]
                    addKelvinCellsFrontRight.append(KelvinCell((anzX+0.5)*4*d,-2*d,(k+1.5)*4*d,  createPart = 'backLeftQuarter',
                                                             n2old  = kc8.n9,
                                                             n3old  = kc8.n8,
                                                             n6old  = kc8.n17,
                                                             n7old  = kc8.n16,
                                                             n12old = kc4.n1,
                                                             n13old = kc4.n0,
                                                             n18old = kc4.n5,
                                                             n19old = kc4.n4,
                                                             n22old = kc4.n9,
                                                             n23old = kc4.n8,
                                                             n105old = kc9.n104))




                for kc in addKelvinCellsFrontRight:
                    addKelvinCells.append(kc)
        #            addKelvinCellsFront.append(kc)
        #            addKelvinCellsRight.append(kc)



                # front left rim
                addKelvinCellsFrontLeft = []
                if anzZ > 0:

                    kc3 = kelvinCells[0][0][0]
                    kc7 = kelvinCells[1][0][0]
                    addKelvinCellsFrontLeft.append(KelvinCell(-2*d,-2*d,2*d,  createPart = 'backRightQuarter',
                                                             n1old  = kc7.n15,
                                                             n2old  = kc7.n14,
                                                             n5old  = kc7.n16,
                                                             n6old  = kc7.n19,
                                                             n10old = kc3.n0,
                                                             n11old = kc3.n3,
                                                             n17old = kc3.n4,
                                                             n18old = kc3.n7,
                                                             n21old = kc3.n15,
                                                             n22old = kc3.n14))

                for k in range(anzZ-1):

                    kc3 = kelvinCells[k+1][0][0]
                    kc7 = kelvinCells[k+2][0][0]
                    kc9 = addKelvinCellsFrontLeft[-1]
                    addKelvinCellsFrontLeft.append(KelvinCell(-2*d,-2*d,(k+1.5)*4*d,  createPart = 'backRightQuarter',
                                                             n1old  = kc7.n15,
                                                             n2old  = kc7.n14,
                                                             n5old  = kc7.n16,
                                                             n6old  = kc7.n19,
                                                             n10old = kc3.n0,
                                                             n11old = kc3.n3,
                                                             n17old = kc3.n4,
                                                             n18old = kc3.n7,
                                                             n21old = kc3.n15,
                                                             n22old = kc3.n14,
                                                             n105old = kc9.n104))


                for kc in addKelvinCellsFrontLeft:
                    addKelvinCells.append(kc)
        #            addKelvinCellsFront.append(kc)
        #            addKelvinCellsLeft.append(kc)



                # lower back right corner

                kc5 = kelvinCells[0][-1][-1]

                if anzX > 0:
                    n101old = addKelvinCellsLowerBack[-1].n100
                else:
                    n101old = False

                if anzY > 0:
                    n103old = addKelvinCellsLowerRight[-1].n102
                else:
                    n103old = False
                if anzZ > 0:
                    n104old = addKelvinCellsBackRight[0].n105
                else:
                    n104old = False
                addKelvinCellLowerBackRight = KelvinCell((anzX+0.5)*4*d,(anzY+0.5)*4*d,-2*d,  createPart = 'upperFrontLeftEighth',
                                                         n0old  = kc5.n10,
                                                         n3old  = kc5.n11,
                                                         n4old  = kc5.n17,
                                                         n7old  = kc5.n18,
                                                         n14old = kc5.n22,
                                                         n15old = kc5.n21,
                                                         n101old = n101old,
                                                         n103old = n103old,
                                                         n104old = n104old)
                addKelvinCells.append(addKelvinCellLowerBackRight)
                addKelvinCellsLower.append(addKelvinCellLowerBackRight)
        #        addKelvinCellsBack.append(addKelvinCellLowerBackRight)
        #        addKelvinCellsRight.append(addKelvinCellLowerBackRight)



                # upper back right corner


                if anzX > 0:
                    n101old = addKelvinCellsUpperBack[-1].n100
                else:
                    n101old = False

                if anzY > 0:
                    n103old = addKelvinCellsUpperRight[-1].n102
                else:
                    n103old = False

                if anzZ > 0:
                    n105old = addKelvinCellsBackRight[-1].n104
                else:
                    n105old = addKelvinCellLowerBackRight.n104




                kc1 = kelvinCells[-1][-1][-1]
                addKelvinCellUpperBackRight = KelvinCell((anzX+0.5)*4*d,(anzY+0.5)*4*d,(anzZ+0.5)*4*d,  createPart = 'lowerFrontLeftEighth',
                                                         n14old = kc1.n2,
                                                         n15old = kc1.n1,
                                                         n16old = kc1.n5,
            #                                             n18old = kc4.n5,
                                                         n19old = kc1.n6,
                                                         n20old = kc1.n10,
                                                         n23old = kc1.n11,
                                                         n101old = n101old,
                                                         n103old = n103old,
                                                         n105old = n105old)

                addKelvinCells.append(addKelvinCellUpperBackRight)
                addKelvinCellsUpper.append(addKelvinCellUpperBackRight)
        #        addKelvinCellsBack.append(addKelvinCellUpperBackRight)
        #        addKelvinCellsRight.append(addKelvinCellUpperBackRight)





                # lower front right corner


                if anzX > 0:
                    n101old = addKelvinCellsLowerFront[-1].n100
                else:
                    n101old = False

                if anzY > 0:
                    n102old = addKelvinCellsLowerRight[0].n103
                else:
                    n102old = addKelvinCellLowerBackRight.n103

                if anzZ > 0:
                    n104old = addKelvinCellsFrontRight[0].n105
                else:
                    n104old = False

                kc8 = kelvinCells[0][0][-1]
                addKelvinCellLowerFrontRight = KelvinCell((anzX+0.5)*4*d,-2*d,-2*d,  createPart = 'upperBackLeftEighth',
                                                             n2old  = kc8.n9,
                                                             n3old  = kc8.n8,
                                                             n6old  = kc8.n17,
                                                             n7old  = kc8.n16,
                                                             n12old = kc8.n21,
                                                             n13old = kc8.n20,
                                                             n101old = n101old,
                                                             n102old = n102old,
                                                             n104old = n104old)




                addKelvinCells.append(addKelvinCellLowerFrontRight)
                addKelvinCellsLower.append(addKelvinCellLowerFrontRight)
        #        addKelvinCellsFront.append(addKelvinCellLowerFrontRight)
        #        addKelvinCellsRight.append(addKelvinCellLowerFrontRight)



                 # upper front right corner


                if anzX > 0:
                    n101old = addKelvinCellsUpperFront[-1].n100
                else:
                    n101old = False

                if anzY > 0:
                    n102old = addKelvinCellsUpperRight[0].n103
                else:
                    n102old = addKelvinCellUpperBackRight.n103

                if anzZ > 0:
                    n105old = addKelvinCellsFrontRight[-1].n104
                else:
                    n105old = addKelvinCellLowerFrontRight.n104

                kc4 = kelvinCells[-1][0][-1]
                addKelvinCellUpperFrontRight = KelvinCell((anzX+0.5)*4*d,-2*d,(anzZ+0.5)*4*d,  createPart = 'lowerBackLeftEighth',
                                                         n12old = kc4.n1,
                                                         n13old = kc4.n0,
                                                         n18old = kc4.n5,
                                                         n19old = kc4.n4,
                                                         n22old = kc4.n9,
                                                         n23old = kc4.n8,
                                                         n101old = n101old,
                                                         n102old = n102old,
                                                         n105old = n105old)


                addKelvinCells.append(addKelvinCellUpperFrontRight)
                addKelvinCellsUpper.append(addKelvinCellUpperFrontRight)
        #        addKelvinCellsFront.append(addKelvinCellUpperFrontRight)
        #        addKelvinCellsRight.append(addKelvinCellUpperFrontRight)


                # Lower Back Left Corner



                if anzX > 0:
                    n100old = addKelvinCellsLowerBack[0].n101
                else:
                    n100old = addKelvinCellLowerBackRight.n101

                if anzY > 0:
                    n103old = addKelvinCellsLowerLeft[-1].n102
                else:
                    n103old = False

                if anzZ > 0:
                    n104old = addKelvinCellsBackLeft[0].n105
                else:
                    n104old = False

                kc6 = kelvinCells[0][-1][0]
                addKelvinCellLowerBackLeft = KelvinCell(-2*d,(anzY+0.5)*4*d,-2*d,  createPart = 'upperFrontRightEighth',
                                                         n0old  = kc6.n13,
                                                         n1old  = kc6.n12,
                                                         n4old  = kc6.n19,
                                                         n5old  = kc6.n18,
                                                         n8old  = kc6.n23,
                                                         n9old  = kc6.n22,
                                                         n100old = n100old,
                                                         n103old = n103old,
                                                         n104old = n104old)


                addKelvinCells.append(addKelvinCellLowerBackLeft)
                addKelvinCellsLower.append(addKelvinCellLowerBackLeft)
        #        addKelvinCellsBack.append(addKelvinCellLowerBackLeft)
        #        addKelvinCellsLeft.append(addKelvinCellLowerBackLeft)




                # Upper back left Corner



                if anzX > 0:
                    n100old = addKelvinCellsUpperBack[0].n101
                else:
                    n100old = addKelvinCellUpperBackRight.n101

                if anzY > 0:
                    n103old = addKelvinCellsUpperLeft[-1].n102
                else:
                    n103old = False

                if anzZ > 0:
                    n105old = addKelvinCellsBackLeft[-1].n104
                else:
                    n105old = addKelvinCellLowerBackLeft.n104

                kc2 = kelvinCells[-1][-1][0]
                addKelvinCellUpperBackLeft = KelvinCell(-2*d,(anzY+0.5)*4*d,(anzZ+0.5)*4*d,  createPart = 'lowerFrontRightEighth',
                                                             n8old  = kc2.n3,
                                                             n9old  = kc2.n2,
                                                             n16old = kc2.n7,
                                                             n17old = kc2.n6,
                                                             n20old = kc2.n13,
                                                             n21old = kc2.n12,
                                                             n100old = n100old,
                                                             n103old = n103old,
                                                             n105old = n105old)

                addKelvinCells.append(addKelvinCellUpperBackLeft)
                addKelvinCellsUpper.append(addKelvinCellUpperBackLeft)
        #        addKelvinCellsBack.append(addKelvinCellUpperBackLeft)
        #        addKelvinCellsLeft.append(addKelvinCellUpperBackLeft)



                # Lower front left Corner


                if anzX > 0:
                    n100old = addKelvinCellsLowerFront[0].n101
                else:
                    n100old = addKelvinCellLowerFrontRight.n101

                if anzY > 0:
                    n102old = addKelvinCellsLowerLeft[0].n103
                else:
                    n102old = addKelvinCellLowerBackLeft.n103

                if anzZ > 0:
                    n104old = addKelvinCellsFrontLeft[0].n105
                else:
                    n104old = False



                kc7 = kelvinCells[0][0][0]
                addKelvinCellLowerFrontLeft = KelvinCell(-2*d,-2*d,-2*d,  createPart = 'upperBackRightEighth',
                                                         n1old  = kc7.n15,
                                                         n2old  = kc7.n14,
                                                         n5old = kc7.n16,
                                                         n6old  = kc7.n19,
                                                         n10old = kc7.n20,
                                                         n11old = kc7.n23,
                                                         n100old = n100old,
                                                         n102old = n102old,
                                                         n104old = n104old)

                addKelvinCells.append(addKelvinCellLowerFrontLeft)
                addKelvinCellsLower.append(addKelvinCellLowerFrontLeft)
        #        addKelvinCellsFront.append(addKelvinCellLowerFrontLeft)
        #        addKelvinCellsLeft.append(addKelvinCellLowerFrontLeft)

                # Upper front left Corner

                if anzX > 0:
                    n100old = addKelvinCellsUpperFront[0].n101
                else:
                    n100old = addKelvinCellUpperFrontRight.n101

                if anzY > 0:
                    n102old = addKelvinCellsUpperLeft[0].n103
                else:
                    n102old = addKelvinCellUpperBackLeft.n103

                if anzZ > 0:
                    n105old = addKelvinCellsFrontLeft[-1].n104
                else:
                    n105old = addKelvinCellLowerFrontLeft.n104

                kc3 = kelvinCells[-1][0][0]
                addKelvinCellUpperFrontLeft = KelvinCell(-2*d,-2*d,(anzZ+0.5)*4*d,  createPart = 'lowerBackRightEighth',
                                                             n10old = kc3.n0,
                                                             n11old = kc3.n3,
                                                             n17old = kc3.n4,
                                                             n18old = kc3.n7,
                                                             n21old = kc3.n15,
                                                             n22old = kc3.n14,
                                                             n100old = n100old,
                                                             n102old = n102old,
                                                             n105old = n105old)


                addKelvinCells.append(addKelvinCellUpperFrontLeft)
                addKelvinCellsUpper.append(addKelvinCellUpperFrontLeft)
        #        addKelvinCellsFront.append(addKelvinCellUpperFrontLeft)
        #        addKelvinCellsLeft.append(addKelvinCellUpperFrontLeft)



        # Collect all k-cells
        nodes = []
        edges = []
        faces = []
        volumes = []
        for kelvinCellsLayer in kelvinCells:
            for kelvinCellsLine in kelvinCellsLayer:
                for k in kelvinCellsLine:
                    for n in k.nodes:
                        if not n in nodes and n:
                            nodes.append(n)
                    for e in k.edges:
                        if not e in edges and e:
                            edges.append(e)
                    for f in k.faces:
                        mf = -f
                        if not f in faces and f and not mf in faces:
                            faces.append(f)
                    volumes.append(k.volume)

        for k in addKelvinCells:
            for n in k.nodes:
                if not n in nodes and n:
                    nodes.append(n)
            for e in k.edges:
                if not e in edges and e:
                    edges.append(e)
            for f in k.faces:
                mf = -f
                if not f in faces and f and not mf in faces:
                    faces.append(f)
            if k.volume:
                volumes.append(k.volume)








        if create_prisms:
            t = 0.2*a
            prisms = []
            if borderVolumesFront:
                for kelvinCellsLayer in kelvinCells:
                    for k in kelvinCellsLayer[0]:
                        disp = np.array([0,-t,0])
                        prism = PrismN([k.n4,k.n15,k.n16,k.n8],[disp,disp,disp,disp])
                        prisms.append(prism)


                for line in addKelvinCellsFront:
                    for k in line:
                        disp = np.array([0,-t,0])
                        prism = PrismN([k.n3,k.n7,k.n19,k.n23,k.n21,k.n17,k.n5,k.n1],[disp,]*8)
                        prisms.append(prism)



            if borderVolumesBack:
                for kelvinCellsLayer in kelvinCells:
                    for k in kelvinCellsLayer[-1]:
                        disp = np.array([0,t,0])
                        prism = PrismN([k.n11,k.n18,k.n12,k.n6],[disp,disp,disp,disp])
                        prisms.append(prism)

                for line in addKelvinCellsBack:
                    for k in line:
                        disp = np.array([0,t,0])
                        prism = PrismN([k.n1,k.n5,k.n17,k.n21,k.n23,k.n19,k.n7,k.n3],[disp,]*8)
                        prisms.append(prism)


            if borderVolumesLeft:
                for kelvinCellsLayer in kelvinCells:
                    for kelvinCellsLine in kelvinCellsLayer:
                        disp = np.array([-t,0,0])
                        prism = PrismN([kelvinCellsLine[0].n7,kelvinCellsLine[0].n14,kelvinCellsLine[0].n19,kelvinCellsLine[0].n13],[disp,disp,disp,disp])
                        prisms.append(prism)


                for line in addKelvinCellsLeft:
                    for k in line:
                        disp = np.array([-t,0,0])
                        prism = PrismN([k.n2,k.n6,k.n18,k.n22,k.n20,k.n16,k.n4,k.n0],[disp,]*8)
                        prisms.append(prism)




            if borderVolumesRight:
                for kelvinCellsLayer in kelvinCells:
                    for kelvinCellsLine in kelvinCellsLayer:
                        disp = np.array([t,0,0])
                        prism = PrismN([kelvinCellsLine[-1].n5,kelvinCellsLine[-1].n10,kelvinCellsLine[-1].n17,kelvinCellsLine[-1].n9],[disp,disp,disp,disp])
                        prisms.append(prism)

                for line in addKelvinCellsRight:
                    for k in line:
                        disp = np.array([t,0,0])
                        prism = PrismN([k.n0,k.n4,k.n16,k.n20,k.n22,k.n18,k.n6,k.n2],[disp,]*8)
                        prisms.append(prism)


            myKelvinCells = []
            if borderVolumesBack and borderVolumesRight:
                for k in addKelvinCellsBackRight:
                    disp1 = np.array([t,0,0])
                    disp2 = np.array([t,t,0])
                    disp3 = np.array([0,t,0])
                    prism1 = PrismN([k.n104,k.n0,k.n4,k.n16,k.n20,k.n105],[disp2,disp1,disp1,disp1,disp1,disp2])
                    prism2 = PrismN([k.n105,k.n23,k.n19,k.n7,k.n3,k.n104],[disp2,disp3,disp3,disp3,disp3,disp2])
                    prisms.append(prism1)
                    prisms.append(prism2)

            if borderVolumesBack and borderVolumesLeft:
                for k in addKelvinCellsBackLeft:
                    disp1 = np.array([-t,0,0])
                    disp2 = np.array([-t,t,0])
                    disp3 = np.array([0,t,0])
                    prism1 = PrismN([k.n105,k.n20,k.n16,k.n4,k.n0,k.n104],[disp2,disp1,disp1,disp1,disp1,disp2])
                    prism2 = PrismN([k.n104,k.n1,k.n5,k.n17,k.n21,k.n105],[disp2,disp3,disp3,disp3,disp3,disp2])
                    prisms.append(prism1)
                    prisms.append(prism2)


            if borderVolumesFront and borderVolumesRight:
                for k in addKelvinCellsFrontRight:
                    disp1 = np.array([t,0,0])
                    disp2 = np.array([t,-t,0])
                    disp3 = np.array([0,-t,0])
                    prism1 = PrismN([k.n105,k.n22,k.n18,k.n6,k.n2,k.n104],[disp2,disp1,disp1,disp1,disp1,disp2])

                    prism2 = PrismN([k.n104,k.n3,k.n7,k.n19,k.n23,k.n105],[disp2,disp3,disp3,disp3,disp3,disp2])
                    prisms.append(prism1)
                    prisms.append(prism2)

            if borderVolumesFront and borderVolumesLeft:
                for k in addKelvinCellsFrontLeft:
                    disp1 = np.array([-t,0,0])
                    disp2 = np.array([-t,-t,0])
                    disp3 = np.array([0,-t,0])
                    prism1 = PrismN([k.n104,k.n2,k.n6,k.n18,k.n22,k.n105],[disp2,disp1,disp1,disp1,disp1,disp2])

                    prism2 = PrismN([k.n105,k.n21,k.n17,k.n5,k.n1,k.n104],[disp2,disp3,disp3,disp3,disp3,disp2])
                    prisms.append(prism1)
                    prisms.append(prism2)

            if borderVolumesLeft and not borderVolumesTop:
                for k in addKelvinCellsUpperLeft:
                    disp = np.array([-t,0,0])
                    prism = PrismN([k.n102,k.n18,k.n22,k.n20,k.n16,k.n103],[disp,]*6)
                    prisms.append(prism)

            if borderVolumesRight and not borderVolumesTop:
                for k in addKelvinCellsUpperRight:
                    disp = np.array([t,0,0])
                    prism = PrismN([k.n103,k.n16,k.n20,k.n22,k.n18,k.n102],[disp,]*6)
                    prisms.append(prism)

            if borderVolumesFront and not borderVolumesTop:
                for k in addKelvinCellsUpperFront:
                    disp = np.array([0,-t,0])
                    prism = PrismN([k.n101,k.n19,k.n23,k.n21,k.n17,k.n100],[disp,]*6)
                    prisms.append(prism)

            if borderVolumesBack and not borderVolumesTop:
                for k in addKelvinCellsUpperBack:
                    disp = np.array([0,t,0])
                    prism = PrismN([k.n100,k.n17,k.n21,k.n23,k.n19,k.n101],[disp,]*6)
                    prisms.append(prism)

            if borderVolumesLeft and not borderVolumesBottom:
                for k in addKelvinCellsLowerLeft:
                    disp = np.array([-t,0,0])
                    prism = PrismN([k.n103,k.n4,k.n0,k.n2,k.n6,k.n102],[disp,]*6)
                    prisms.append(prism)

            if borderVolumesRight and not borderVolumesBottom:
                for k in addKelvinCellsLowerRight:
                    disp = np.array([t,0,0])
                    prism = PrismN([k.n102,k.n6,k.n2,k.n0,k.n4,k.n103],[disp,]*6)
                    prisms.append(prism)

            if borderVolumesFront and not borderVolumesBottom:
                for k in addKelvinCellsLowerFront:
                    disp = np.array([0,-t,0])
                    prism = PrismN([k.n100,k.n5,k.n1,k.n3,k.n7,k.n101],[disp,]*6)
                    prisms.append(prism)

            if borderVolumesBack and not borderVolumesBottom:
                for k in addKelvinCellsLowerBack:
                    disp = np.array([0,t,0])
                    prism = PrismN([k.n101,k.n7,k.n3,k.n1,k.n5,k.n100],[disp,]*6)
                    prisms.append(prism)


            if not borderVolumesBottom and borderVolumesBack and borderVolumesLeft:
                k = addKelvinCellLowerBackLeft
                disp1 = np.array([-t,0,0])
                disp2 = np.array([-t,t,0])
                disp3 = np.array([0,t,0])
                prism1 = PrismN([k.n106,k.n103,k.n4,k.n0,k.n104],[disp2,disp1,disp1,disp1,disp2])

                prism2 = PrismN([k.n104,k.n1,k.n5,k.n100,k.n106],[disp2,disp3,disp3,disp3,disp2])
                prisms.append(prism1)
                prisms.append(prism2)


            if not borderVolumesBottom and borderVolumesBack and borderVolumesRight:
                k = addKelvinCellLowerBackRight
                disp1 = np.array([t,0,0])
                disp2 = np.array([t,t,0])
                disp3 = np.array([0,t,0])
                prism1 = PrismN([k.n104,k.n0,k.n4,k.n103,k.n106],[disp2,disp1,disp1,disp1,disp2])
                prism2 = PrismN([k.n106,k.n101,k.n7,k.n3,k.n104],[disp2,disp3,disp3,disp3,disp2])
                prisms.append(prism1)
                prisms.append(prism2)

            if not borderVolumesBottom and borderVolumesFront and borderVolumesLeft:
                k = addKelvinCellLowerFrontLeft
                myKelvinCells.append(k)
                disp1 = np.array([-t,0,0])
                disp2 = np.array([-t,-t,0])
                disp3 = np.array([0,-t,0])
                prism1 = PrismN([k.n104,k.n2,k.n6,k.n102,k.n106],[disp2,disp1,disp1,disp1,disp2])
                prism2 = PrismN([k.n106,k.n100,k.n5,k.n1,k.n104],[disp2,disp3,disp3,disp3,disp2])
                prisms.append(prism1)
                prisms.append(prism2)

            if not borderVolumesBottom and borderVolumesFront and borderVolumesRight:
                k = addKelvinCellLowerFrontRight
                myKelvinCells.append(k)
                disp1 = np.array([t,0,0])
                disp2 = np.array([t,-t,0])
                disp3 = np.array([0,-t,0])
                prism1 = PrismN([k.n106,k.n102,k.n6,k.n2,k.n104],[disp2,disp1,disp1,disp1,disp2])
                prism2 = PrismN([k.n104,k.n3,k.n7,k.n101,k.n106],[disp2,disp3,disp3,disp3,disp2])
                prisms.append(prism1)
                prisms.append(prism2)


            if not borderVolumesTop and borderVolumesBack and borderVolumesLeft:
                k = addKelvinCellUpperBackLeft
                disp1 = np.array([-t,0,0])
                disp2 = np.array([-t,t,0])
                disp3 = np.array([0,t,0])
                prism1 = PrismN([k.n105,k.n20,k.n16,k.n103,k.n106],[disp2,disp1,disp1,disp1,disp2])
                prism2 = PrismN([k.n106,k.n100,k.n17,k.n21,k.n105],[disp2,disp3,disp3,disp3,disp2])
                prisms.append(prism1)
                prisms.append(prism2)

            if not borderVolumesTop and borderVolumesBack and borderVolumesRight:
                k = addKelvinCellUpperBackRight
                disp1 = np.array([t,0,0])
                disp2 = np.array([t,t,0])
                disp3 = np.array([0,t,0])
                prism1 = PrismN([k.n106,k.n103,k.n16,k.n20,k.n105],[disp2,disp1,disp1,disp1,disp2])
                prism2 = PrismN([k.n105,k.n23,k.n19,k.n101,k.n106],[disp2,disp3,disp3,disp3,disp2])
                prisms.append(prism1)
                prisms.append(prism2)

            if not borderVolumesTop and borderVolumesFront and borderVolumesLeft:
                disp1 = np.array([-t,0,0])
                disp2 = np.array([-t,-t,0])
                disp3 = np.array([0,-t,0])
                prism1 = PrismN([k.n106,k.n102,k.n18,k.n22,k.n105],[disp2,disp1,disp1,disp1,disp2])
                prism2 = PrismN([k.n105,k.n21,k.n17,k.n100,k.n106],[disp2,disp3,disp3,disp3,disp2])
                prisms.append(prism1)
                prisms.append(prism2)

            if not borderVolumesTop and borderVolumesFront and borderVolumesRight:
                k = addKelvinCellUpperFrontRight
                disp1 = np.array([t,0,0])
                disp2 = np.array([t,-t,0])
                disp3 = np.array([0,-t,0])
                prism1 = PrismN([k.n105,k.n22,k.n18,k.n102,k.n106],[disp2,disp1,disp1,disp1,disp2])
                prism2 = PrismN([k.n106,k.n101,k.n19,k.n23,k.n105],[disp2,disp3,disp3,disp3,disp2])
                prisms.append(prism1)
                prisms.append(prism2)






            for p in prisms:
                p.volume.category = 'border'
                for n in p.nodes:
                    if not n in nodes:
                        n.color = tc.TUMRose()
                        nodes.append(n)

                for e in p.edges:
                    if e.isReverse:
                        e = -e
                    if not e in edges:
                        edges.append(e)

                for f in p.faces:
                    if f.isReverse:
                        f = -f
                    if not f in faces:
                        faces.append(f)
                volumes.append(p.volume)

        else:
            if borderVolumesFront:
                for kelvinCellsLayer in kelvinCells:
                    for k in kelvinCellsLayer[0]:
                        k.volume.category = 'border'


                for line in addKelvinCellsFront:
                    for k in line:
                        k.volume.category = 'border'

                for k in addKelvinCellsFrontLeft:
                    k.volume.category = 'border'

                for k in addKelvinCellsFrontRight:
                    k.volume.category = 'border'

                for k in addKelvinCellsLowerFront:
                    k.volume.category = 'border'

                for k in addKelvinCellsUpperFront:
                    k.volume.category = 'border'

                addKelvinCellLowerFrontLeft.volume.category = 'border'
                addKelvinCellLowerFrontRight.volume.category = 'border'
                addKelvinCellUpperFrontLeft.volume.category = 'border'
                addKelvinCellUpperFrontRight.volume.category = 'border'


        # Check if two nodes were generated at the same location
        for n1 in nodes:
            for n2 in nodes:
                if not n1 == n2:
                    if np.linalg.norm(n1.coordinates-n2.coordinates)<1e-4:
                        cc.printRed('It seems that two nodes were created at the same place')
                        cc.printRed(n1,n2)
                        print()




        cc.printMagenta(volumes)

        super().__init__(
            nodes,edges,faces,volumes,
            volumes_to_combine = [
                (volumes[0], volumes[33]),
                (volumes[1], volumes[29]),
                (volumes[4], volumes[34]),
                (volumes[5], volumes[30]),
            ],
            faces_to_combine = [
                (faces[205], faces[60]),
                (faces[206], faces[57]),
                (faces[207], faces[52]),
                (faces[193], faces[70]),
                (faces[194], faces[65]),
                (faces[195], faces[71]),
                (faces[190], faces[19]),
                (faces[191], faces[20]),
                (faces[192], faces[26]),
                (faces[202], faces[8]),
                (faces[203], faces[5]),
                (faces[204], faces[13]),
            ],
            renumber=False,
            **kwargs
        )


if __name__ == '__main__':
    import random

    set_logging_format(logging.DEBUG)

#        c = getComplex(numCells-1,
#                       borderVolumesRight=True,
#                       borderVolumesLeft=True,
#                       borderVolumesFront=True,
#                       borderVolumesBack=True)

    c = Grid3DKelvin(1,
                     fillCube=True,
#                       borderVolumesBottom=True,
#                       borderVolumesTop = True,
                    borderVolumesLeft = True,
                    borderVolumesRight = True,
                    borderVolumesFront = True,
                    borderVolumesBack=True,
                   )
    for v in c.volumes:
        if v.category == 'inner':
            v.color = tc.TUMBlack()


    if False:
        dc = DualComplex3D(c, createFaces=True, createVolumes=True)
    else:
        dc = False



    if False:

        import pickle,sys
        sys.setrecursionlimit(30000)
        outputFileName = 'test.data'
        fw = open(outputFileName, 'wb')
        pickle.dump(c.volumes, fw)
        fw.close()




    (figs,ax) = pf.getFigures(numTotal=10)
    axNum = -1





    nodes = c.nodes
    edges = c.edges
    faces = c.faces

    c.useCategory = 1
    print(len(c.innerNodes))





#-------------------------------------------------------------------------
#    Figure 1: Nodes and edges of all kelvin cells
#-------------------------------------------------------------------------

    if True:
        axNum += 1
        for n in nodes:
            n.showLabel=False
            if n.category1 == "border":
                n.color = tc.TUMGreen()
            if n.category1 == "additionalBorder":
                n.color = tc.TUMBlack()
            n.plotNode(ax[axNum])
        for e in edges:
            e.showArrow=False
            e.showLabel=False
            if e.num == 17:
                e.showLabel=True
                e.showArrow=True
            e.plotEdge(ax[axNum])


#-------------------------------------------------------------------------
#    Figure 2: Spheres and cylinders around nodes and edges
#-------------------------------------------------------------------------


    if False:
        axNum += 1
        for n in nodes:
            n.color = tc.TUMWhite
            n.radius = random.uniform(0.25,0.5)
            n.plotSphere(ax[axNum])
            n.plotNode(ax[axNum])
#            for e in edges:
#                e.radius = random.uniform(0.07,0.15)
#                e.plotCylinder(ax[axNum])
#                e.plotEdge(ax[axNum])


#-------------------------------------------------------------------------
#    Figure 3: Faces of kelvin cells and inner edges of dual complex
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        for f in faces:
            f.showLabel=False
            f.showNormalVec=False
            f.plotFace(ax[axNum])
        c.setupAxis(ax[axNum])



#-------------------------------------------------------------------------
#    Figure 4: upper half
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell1 = KelvinCell(0,0,0,createPart='upperHalf')
        testCell1.plotKelvinCell(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 5: lower half
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell2 = KelvinCell(0,0,0,createPart='lowerHalf')
        testCell2.plotKelvinCell(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 6: front half
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell3 = KelvinCell(0,0,0,createPart='frontHalf')
        testCell3.plotKelvinCell(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 7: back half
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell4 = KelvinCell(0,0,0,createPart='backHalf')
        testCell4.plotKelvinCell(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 8: left half
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell5 = KelvinCell(0,0,0,createPart='leftHalf')
        testCell5.plotKelvinCell(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 9: right half
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell6 = KelvinCell(0,0,0,createPart='rightHalf')
        testCell6.plotKelvinCell(ax[axNum])


#-------------------------------------------------------------------------
#    Figure 10: upper front quarter
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell7 = KelvinCell(0,0,0,createPart='upperFrontQuarter')
        testCell7.plotKelvinCell(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 11: upper back quarter
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell8 = KelvinCell(0,0,0,createPart='upperBackQuarter')
        testCell8.plotKelvinCell(ax[axNum])


#-------------------------------------------------------------------------
#    Figure 12: lower front quarter
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell9 = KelvinCell(0,0,0,createPart='lowerFrontQuarter')
        testCell9.plotKelvinCell(ax[axNum])


#-------------------------------------------------------------------------
#    Figure 13: lower back quarter
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell10 = KelvinCell(0,0,0,createPart='lowerBackQuarter')
        testCell10.plotKelvinCell(ax[axNum])


#-------------------------------------------------------------------------
#    Figure 14: upper left quarter
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell11 = KelvinCell(0,0,0,createPart='upperLeftQuarter')
        testCell11.plotKelvinCell(ax[axNum])


#-------------------------------------------------------------------------
#    Figure 15: lower left quarter
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell12 = KelvinCell(0,0,0,createPart='lowerLeftQuarter')
        testCell12.plotKelvinCell(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 16: upper right quarter
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell13 = KelvinCell(0,0,0,createPart='upperRightQuarter')
        testCell13.plotKelvinCell(ax[axNum])


#-------------------------------------------------------------------------
#    Figure 17: upper right quarter
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell14 = KelvinCell(0,0,0,createPart='lowerRightQuarter')
        testCell14.plotKelvinCell(ax[axNum])



#-------------------------------------------------------------------------
#    Figure 18: front left quarter
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell15 = KelvinCell(0,0,0,createPart='frontLeftQuarter')
        testCell15.plotKelvinCell(ax[axNum])


#-------------------------------------------------------------------------
#    Figure 19: front right quarter
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell16 = KelvinCell(0,0,0,createPart='frontRightQuarter')
        testCell16.plotKelvinCell(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 20: Back left quarter
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell17 = KelvinCell(0,0,0,createPart='backLeftQuarter')
        testCell17.plotKelvinCell(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 21: Back right quarter
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell18 = KelvinCell(0,0,0,createPart='backRightQuarter')
        testCell18.plotKelvinCell(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 22: Upper front left eighth
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell19 = KelvinCell(0,0,0,createPart='upperFrontLeftEighth')
        testCell19.plotKelvinCell(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 23: Lower front left eighth
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell20 = KelvinCell(0,0,0,createPart='lowerFrontLeftEighth')
        testCell20.plotKelvinCell(ax[axNum])


#-------------------------------------------------------------------------
#    Figure 24: Upper back left eighth
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell21 = KelvinCell(0,0,0,createPart='upperBackLeftEighth')
        testCell21.plotKelvinCell(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 25: Lower back left eighth
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell22 = KelvinCell(0,0,0,createPart='lowerBackLeftEighth')
        testCell22.plotKelvinCell(ax[axNum])



#-------------------------------------------------------------------------
#    Figure 26: Upper front right eighth
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell23 = KelvinCell(0,0,0,createPart='upperFrontRightEighth')
        testCell23.plotKelvinCell(ax[axNum])


#-------------------------------------------------------------------------
#    Figure 27: lower front right eighth
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell24 = KelvinCell(0,0,0,createPart='lowerFrontRightEighth')
        testCell24.plotKelvinCell(ax[axNum])


#-------------------------------------------------------------------------
#    Figure 28: upper back right eighth
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell25 = KelvinCell(0,0,0,createPart='upperBackRightEighth')
        testCell25.plotKelvinCell(ax[axNum])



#-------------------------------------------------------------------------
#    Figure 29: lower back right eighth
#-------------------------------------------------------------------------
    if False:
        axNum += 1
        testCell26 = KelvinCell(0,0,0,createPart='lowerBackRightEighth')
        testCell26.plotKelvinCell(ax[axNum])



#-------------------------------------------------------------------------
#    Figure 30: Dual complex
#-------------------------------------------------------------------------
    if False and dc:
        axNum += 1
        for f in dc.faces:
            f.simplifyFace()
        for f in dc.faces:

            f.showLabel = False
            f.showNormalVec = False
            f.plotFace(ax[axNum])


#-------------------------------------------------------------------------
#    Figure 31: Dual complex
#-------------------------------------------------------------------------
    if True and dc:
        axNum += 1
        for n in dc.nodes:
            n.showLabel = False
            n.plotNode(ax[axNum])
        for e in dc.edges:
            e.showLabel = False
            e.showArrow = False
            e.plotEdge(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 32: Volumes
#-------------------------------------------------------------------------

    if True:
        axNum += 1
        c.plotVolumes(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 33: Border Volumes
#-------------------------------------------------------------------------

    if True:
        axNum += 1
        for v in c.borderVolumes:
            v.plotVolume(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 34: Additional Border Faces
#-------------------------------------------------------------------------
    if True:
        axNum += 1
        for f in c.additionalBorderFaces:
            f.plotFace(ax[axNum], showNormalVec=False, showBarycenter=False)
        c.plotNodes(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 34: Border edges
#-------------------------------------------------------------------------
    if True:
        axNum += 1
        c.borderEdges[0].color = tc.TUMRose()
        for e in c.borderEdges:
            e.plotEdge(ax[axNum], showArrow=False, showLabel=True)

        for f in c.borderEdges[0].faces:
            f.plotFace(ax[axNum])
        c.plotNodes(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 35: Dual faces
#-------------------------------------------------------------------------
    if True and dc:
        axNum += 1
        for f in dc.faces:
            f.showLabel=False
            f.showNormalVec=False
            f.showBarycenter=False
            f.plotFace(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 36: Dual volumes
#-------------------------------------------------------------------------
    if True and dc:
        axNum += 1
        for v in dc.borderVolumes:
            v.showLabel=False
            v.showNormalVec=False
            v.showBarycenter=False
            v.plotVolume(ax[axNum])
        for n in c.borderNodes:
            n.plotNode(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 37: Dual volumes
#-------------------------------------------------------------------------
    if True and dc:
        axNum += 1
        for v in dc.innerVolumes:
            v.showLabel=False
            v.showNormalVec=False
            v.showBarycenter=False
            v.plotVolume(ax[axNum])
        for n in c.innerNodes:
            n.plotNode(ax[axNum])

#-------------------------------------------------------------------------
#    Figure 38: Dual volumes
#-------------------------------------------------------------------------
    if True and dc:
        axNum += 1
        for n in dc.nodes:
            n.showLabel=False
            n.plotNode(ax[axNum])






#-------------------------------------------------------------------------
#    Border volumes test
#-------------------------------------------------------------------------

    if False:
        axNum += 1
#            c.plotComplex(ax[axNum],showLabel=False,showArrow=False)
#            for e in c.borderEdges2:
#                e.plotEdge(ax[axNum],showLabel=False,showArrow=False)


#            dc.useCategory = 2
        axNum += 1
        for f in dc.borderFaces2:
            f.plotFace(ax[axNum],showLabel=False,showNormalVec=False)
            f.dualCell3D.plotEdge(ax[axNum],showLabel=False,showArrow=False)
        dc.plotNodes(ax[axNum],showLabel=False)

    if False:
        axNum += 1
#            c.plotNodes(ax[axNum])
#            volNum = 29

#            dc.plotFaces(ax[axNum],showLabel=False,color=tc.TUMBlack())
        dc.useCategory = 2
        for f in dc.borderFaces:
            f.plotFace(ax[axNum],showLabel=False,showNormalVec=False)




#            dc.innerVolumes[volNum].plotVolume(ax[axNum],showLabel=True)
#
    if False:
        axNum += 1
        c.plotVolumes(ax[axNum],showLabel=False)

        axNum += 1
        for e in c.additionalBorderEdges:
            e.plotEdge(ax[axNum],showLabel=False)


#            axNum += 1
#            for v in [c.borderVolumes[8],c.borderVolumes[83]]:
#                v.plotVolume(ax[axNum])




        axNum += 1
        for f in c.additionalBorderFaces:
            f.plotFace(ax[axNum])

        from kCells import BaseEdge
        axNum += 1
        for cell in c.errorCells:
            if isinstance(cell,Volume):
                cell.plotVolume(ax[axNum])
            if isinstance(cell,BaseEdge):
                cell.plotEdge(ax[axNum])


#            axNum += 1
#            dc.plotEdges(ax[axNum],showLabel=False,showArrow=False)
#
#
#            axNum += 1
#            dc.plotFaces(ax[axNum],showLabel=False,showNormalVec=False)

        axNum += 1
        dc.plotVolumes(ax[axNum],showLabel=False)


        axNum += 1
        for f in dc.additionalBorderFaces:
            f.plotFace(ax[axNum],showLabel=True,showNormalVec=False)
#            axNum += 1
#            for f in dc.innerFaces:
#                f.plotFace(ax[axNum],showLabel=False,showNormalVec=False)
#
#            axNum += 1
##            for n in c.borderNodes:
#
#            for n in dc.additionalBorderNodes:
#                n.plotNode(ax[axNum])
#
#            for f in dc.additionalBorderFaces:
#                f.plotFace(ax[axNum],showNormalVec=False)
#
#
#            axNum += 1
#            dc.plotVolumes(ax[axNum],showLabel=False)
#
#            axNum += 1
#            dc.volumes[0].plotVolume(ax[axNum])
#
##            nodeNum = -1
#            axNum += 1
#            for e in dc.borderEdges:
#                e.plotEdge(ax[axNum],showLabel=False,showNormalVec=False)
#            nodeNum += 1
#            primalNode = c.innerNodes[nodeNum]
#            dualVolume = primalNode.dualCell3D
#            primalNode.plotNode(ax[axNum])
#            dualVolume.plotVolume(ax[axNum])





    if False:
        axNum += 1
#            dc.plotEdges(ax[axNum],showLabel=False,showArrow=False)
        for e in dc.innerEdges:
            e.plotEdge(ax[axNum])

        axNum += 1
        for e in dc.borderEdges:
            e.plotEdge(ax[axNum])

        axNum += 1
#            dc.plotFaces(ax[axNum],showLabel=False,showNormalVec=False)
        for f in dc.innerFaces:
            f.plotFace(ax[axNum],showLabel=False,showNormalVec=False)

        axNum += 1
#            dc.plotFaces(ax[axNum],showLabel=False,showNormalVec=False)
        for f in dc.borderFaces:
            f.plotFace(ax[axNum],showLabel=False,showNormalVec=False)



        testDualBorderFace = dc.borderFaces[0]
        testPrimalBorderEdge = testDualBorderFace.dualCell3D
        testPrimalBorderEdge.plotEdge(ax[axNum],color=tc.TUMRose())
        for f in testPrimalBorderEdge.faces:
            f.plotFace(ax[axNum])
#            for e in dc.borderFaces

        for e in dc.borderFaces[0].edges:
            e.plotEdge(ax[axNum])
#                for sf in f.simpleFaces:



#                    if len(sf.simpleEdges)




#            axNum += 1
#            dc.plotVolumes(ax[axNum],showLabel=False,showNormalVec=False)






#-------------------------------------------------------------------------
#   Create numenclature for documentation
#-------------------------------------------------------------------------

#        if os.getcwd().endswith('doc'):
#            kc = KelvinCell(0,0,0)
#            kc.plotNomenclature(prefix='')




#-------------------------------------------------------------------------
#    Generate video
#-------------------------------------------------------------------------
    if False:
        cc.printBlue('Creating Video')
        (fig,ax,writer) = pf.getVideo(title='Kelvin cells and dual Complex',fps=15)
        with writer.saving(fig,'vid/kelvin.mp4',120):
#                for e in dc.innerEdges:
#                    e.showLabel = False
#                    e.plotEdge(ax)
#                for f in faces:
#                    f.showLabel=False
#                    f.showNormalVec=False
#                    f.plotFace(ax)
#                c.setupAxis(ax)
#            for i in range(50):
#                print(i)
#                writer.grab_frame()
#
            anz = 2
            for j in range(anz):
                print(j)
                ax.clear()
                dc.plotVolumes(ax,showLabel=False,color=tc.TUMBlack())
                dc.volumes[j].plotVolume(ax,showLabel=True)
#                    ax.view_init(30,j*360/anz)
                for i in range(15):
                    print('\t',j,' | ',i)
                    writer.grab_frame()




    if False:
        cc.printBlue('Creating Video')
        (fig,ax,writer) = pf.getVideo(title='Kelvin cells and dual Complex')
        with writer.saving(fig,'vid/kelvin2.mp4',120):
            for i in range(len(dc.innerVolumes[:5])):
                print(i+1,'of',len(dc.innerVolumes))
                ax.clear()
                c.plotGraph(ax,showLabels=False)
                v = dc.volumes[i]
                v.plotVolume(ax)
                for j in range(30):
                    ax.view_init(30,(i*30+j)*360/(len(dc.innerVolumes)*30))
                    writer.grab_frame()


    if False:
        cc.printBlue('Creating Video')
        (fig,ax,writer) = pf.getVideo(title='Kelvin cells and dual Complex')
        with writer.saving(fig,'vid/kelvin2.mp4',120):
            kc = addKelvinCells[0]
            nodesToPlot = []
            for n in kc.nodes:
                if n :
                    nodesToPlot.append(n)

            for i,pn in enumerate(nodesTocPlot):
                print(i+1,'of',len(nodesToPlot))
                ax.clear()
                for n in nodesToPlot:
                    n.plotNode(ax)
                for e in kc.edges:
                    if e:
                        e.plotEdge(ax)
                v = pn.dualCell3D
                v.plotVolume(ax)
                for j in range(30):
                    ax.view_init(30,(i*30+j)*360/(len(nodesToPlot)*30))
                    writer.grab_frame()



    if False:

        res = 130
        for e in c.edges:
            e.radius = 1
        for n in c.nodes:
            n.radius = 1.3
        myVTK1 = c.plotVtkVoxels(resolution = res)




#            if dc:
#                for f in dc.volumes[0].faces:
#                    for p in f.polygons:
#                        myVTK1.addActor(p.vtkActor)
#
        myVTK1.start()

        numberOfCells = myVTK1.extract.GetOutput().GetNumberOfCells()
        cc.printBlueBackground('           Number of solid Cells:       {}      '.format(numberOfCells))
        cc.printBlueBackground('           Total number of voxels      {}      '.format(res*res*res))
        cc.printBlueBackground('           Ratio     {}      '.format(numberOfCells/(res*res*res)))





    if False:
#            for v in c.borderVolumes:
#                v.plotVolume(ax[axNum],showLabel=False,showBarycenter=False)
#                v.dualCell3D.plotNode(ax[axNum],showLabel=False)

#            c.plotEdges(ax[axNum],showLabel=False,showArrow=False)

        cc.printBlue(c.xlim,c.ylim,c.zlim)
        d = c.xlim[1]-c.xlim[0]
        cc.printBlue(d)

#            print(c.incidenceMatrix1)
#            print(c.incidenceMatrix2)
#            print(c.incidenceMatrix3)
#



#            c.plotComplex(ax[axNum],showLabel=False,showArrow=False)

        nodes = []
        edges = []
        faces = []
        for p in prisms:
            for n in p.nodes:
                if not n in nodes:
                    nodes.append(n)

            for e in p.edges:
                if not e in edges:
                    edges.append(e)
            for f in p.faces:
                if not f in faces:
                    faces.append(f)




        axNum += 1
        c.plotEdges(ax[axNum],showLabel=False,showArrow=False)

        k = myKelvinCells[0]
        k.volume.plotVolume(ax[axNum])


        axNum += 1
        c.plotVolumes(ax[axNum],showLabel=False)


        axNum += 1
        dc.plotFaces(ax[axNum],showLabel=False,showNormalVec=False)

#            for n in nodes:
#                n.plotNode(ax[axNum],showLabel=False,showArrow=False)
#            for e in edges:
#                e.plotEdge(ax[axNum],showLabel=False,showArrow=True)
#            for f in faces:
#                f.plotFace(ax[axNum],showLabel=False,showNormalVec=False,showBarycenter=False)
#


#
#            for e in dc.edges:
#                e.plotEdge(ax[axNum],showLabel=False)

#            for n in dc.errorCells:
#                n.plotNode(ax[axNum])
#            for n in dc.nodes:


    if False:
        c.checkIncidenceMatrix(dc.incidenceMatrix1ii,c.incidenceMatrix3ii)
        c.checkIncidenceMatrix(dc.incidenceMatrix1ib,c.incidenceMatrix3bi)
        c.checkIncidenceMatrix(dc.incidenceMatrix1bi,c.incidenceMatrix3ib)
        c.checkIncidenceMatrix(dc.incidenceMatrix1bb,c.incidenceMatrix3bb)

        c.useCategory = 2
        dc.useCategory = 2
#
        c.checkIncidenceMatrix(dc.incidenceMatrix1ii,c.incidenceMatrix3ii)
        c.checkIncidenceMatrix(dc.incidenceMatrix1ib,c.incidenceMatrix3bi)
        c.checkIncidenceMatrix(dc.incidenceMatrix1bi,c.incidenceMatrix3ib)
        c.checkIncidenceMatrix(dc.incidenceMatrix1bb,c.incidenceMatrix3bb)
        #


    if True:
        axNum += 1
        testEdges = []
        # for v in c.borderVolumes:
        #     for f in v.faces:
        #         for e in f.edges:
        #             if e.isReverse:
        #                 e = -e
        #                 if not e in testEdges:
        #                     testEdges.append(e)


        v = c.volumes[14]
        # v.plotVolume(ax[axNum])
        for f in v.faces:
            # f.plotFace(ax[axNum])
            for e in f.edges + f.geometricEdges:
                if e.isReverse:
                    e = -e
                if not e in testEdges:
                    testEdges.append(e)

        for e in testEdges:
            e.showLabel=True
            e.plotEdge(ax[axNum])









    if True:

        # geometricNodesNew = []
        # geometricEdgesNew = []
        # for v in c.volumes:
        #     for f in v.faces:
        #         for sf in f.simpleFaces:
        #             for se in sf.simpleEdges:
        #                 if se.isGeometrical:
        #                     if se.isReverse:
        #                         if not -se in geometricEdgesNew:
        #                             geometricEdgesNew.append(-se)
        #                     else:
        #                         if not se in geometricEdgesNew:
        #                             geometricEdgesNew.append(se)
        #                 for n in [se.startNode, se.endNode]:
        #                     if n.isGeometrical:
        #                         if not n in geometricNodesNew:
        #                             geometricNodesNew.append(n)

        # for v in c.volumes:
        #     for f in v.faces:
        #         for e in

        nodes_in_border_volumes = []



        # edges_new = []

        # for v in c.volumes:
        #     for f in v.faces:
        #         for e in f.edges:
        #             if e.isReverse:
        #                 e = -e
        #             if not e in edges_new:
        #                 edges_new.append(e)

        # Nodes
        all_nodes = c.nodes + c.geometricNodes
        new_nodes = []
        for n in all_nodes:
            in_border_volume = n.num in [172, 168, 169, 173]
            for e in n.edges:
                if in_border_volume:
                    break
                for f in e.faces:
                    if in_border_volume:
                        break
                    for v in f.volumes:
                        if in_border_volume:
                            break
                        if v.category1 == "border":
                            in_border_volume=True

            if in_border_volume:
                print(f"n{n.num} = Node({n.xCoordinate}, {n.yCoordinate}, {n.zCoordinate}, num={n.num})")
                new_nodes.append(n)

        print("nodes = [", end="")
        print(", ".join([f"n{n.num}" for n in new_nodes]), end="")
        print("]")



        # Edges
        new_edges = []
        all_edges = c.edges + c.geometricEdges
        for e in all_edges:
            if e.startNode in new_nodes and e.endNode in new_nodes:
                text_geo_nodes = ""
                geo_node_nums = [f"n{n.num}" for n in e.geometricNodes]
                if geo_node_nums:
                    text_geo_nodes = ", geometricNodes=[" + ", ".join(geo_node_nums) + "]"


                print(f"e{e.num} = Edge(n{e.startNode.num}, n{e.endNode.num}{text_geo_nodes}, num={e.num})")
                new_edges.append(e)

        print("edges = [", end="")
        print(", ".join([f"e{e.num}" for e in new_edges]), end="")
        print("]")

        # Faces
        new_faces = []
        for f in c.faces:
            edges_no_sign = [-e if e.isReverse else e for e in f.edges]
            if all([e in new_edges for e in edges_no_sign]):
                num_edges_text = ""
                num_edges_f = []
                for sf in f.simpleFaces:
                    num_edges_sf = []
                    for se in sf.simpleEdges:
                        if not se.num in num_edges_sf:
                            if se.isReverse:
                                num_edges_sf.append(-0.1 if se.num==0 else -se.num)
                            else:
                                num_edges_sf.append(0.1 if se.num==0 else se.num)
                    num_edges_f.append(", ".join([f"-e{-int(e_num)}" if e_num<0 else f"e{int(e_num)}" for e_num in num_edges_sf]))
                if len(num_edges_f) == 1:
                    num_edges_text = f"[{num_edges_f[0]}]"
                else:
                    num_edges_text = "[" + ", ".join([f"[{num_f}]" for num_f in num_edges_f]) + "]"
                print(f"f{f.num} = Face({num_edges_text}, num={f.num})")
                new_faces.append(f)

        print("faces = [", end="")
        print(", ".join([f"f{f.num}" for f in new_faces]), end="")
        print("]")


        # Volumes
        new_volumes = []
        for v in c.volumes:
            faces_no_sign = [-f if f.isReverse else f for f in v.faces]
            if all([f in new_faces for f in faces_no_sign]):
                print(f"v{v.num} = Volume([{', '.join([str(f).replace("_i","").replace("_b","").replace("_B","") for f in v.faces])}], num={v.num})")
                new_volumes.append(v)

        print("volumes = [", end="")
        print(", ".join([f"v{v.num}" for v in new_volumes]), end="")
        print("]")

        print("volumes_b = [", end="")
        print(", ".join([f"v{v.num}"  for v in new_volumes if v.category1 == "border"]), end="")
        print("]")







#




