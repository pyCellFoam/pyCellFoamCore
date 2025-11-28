# -*- coding: utf-8 -*-
#==============================================================================
# TITLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Jul 15 15:54:16 2020

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
from k_cells import Node, Edge

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
    def __method1(self,a=0,b=''):
        '''
        This is the explanation of the private method 1

        All parameters should be listed, as well as the output values:

        :param int a: Some Number
        :param str b: Some String
        :return: Returns maybe something

        '''

        return -1
#-------------------------------------------------------------------------
#    Method 2
#-------------------------------------------------------------------------
    def method2(self,a,b):
        '''
        This is the explanation of the public method 2

        All parameters should be listed, as well as the output values:

        :param int a: Some Number
        :param str b: Some String
        :return: Returns maybe something

        '''

        c = a*b
        return c

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
