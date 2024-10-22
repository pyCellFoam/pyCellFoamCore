# -*- coding: utf-8 -*-
# =============================================================================
# TIKZ ENVIRONMENT
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue Feb 11 11:59:03 2020

'''


'''
# =============================================================================
#    IMPORTS
# =============================================================================
import os
if __name__ == '__main__':
    os.chdir('../../')

import numpy as np

import tools.myLogging as ml
import tools.colorConsole as cc
from tools.tikZPicture.tikZCoordinate import TikZCoordinate
from tools.tikZPicture.tikZNode import TikZNode
from tools.tikZPicture.tikZPolygon import TikZPolygon
from tools.tikZPicture.tikZLine import TikZLine
from tools.tikZPicture.tikZCoSy2D import TikZCoSy2D
from tools.tikZPicture.tikZCircledArrow import TikZCircledArrow


# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class TikZEnvironment:
    '''

    '''

# =============================================================================
#    SLOTS
# =============================================================================
    __slots__ = ('__name',
                 '__tikZCoordinates',
                 '__tikZNodes',
                 '__tikZPolygons',
                 '__tikZLines',
                 '__tikZCoSys',
                 '__tikZCircledArrows',
                 '__logger',
                 '__tikZNames',
                 '__tikZNamesChanged',
                 '__tikZPrefix',
                 '__additionaTikZCodePre',
                 '__additionaTikZCodePost')

# =============================================================================
#    INITIALIZATION
# =============================================================================

    def __init__(self, name=None):
        '''
        :param str name: A name for the environment. Makes it easier to
            identify different environments if multiple are used.

        '''
        if name is None:
            self.__name = 'GenericTikZEnvironment'
        else:
            self.__name = name
        self.__logger = ml.getLogger(__name__)
        self.__tikZCoordinates = []
        self.__tikZNodes = []
        self.__tikZPolygons = []
        self.__tikZLines = []
        self.__tikZCoSys = []
        self.__tikZCircledArrows = []
        self.__tikZNamesChanged = True
        self.__tikZPrefix = ''
        self.__additionaTikZCodePre = ''
        self.__additionaTikZCodePost = ''
        self.__logger.info('Created TikZEnvironment "{}"'.format(self.name))

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getName(self): return self.__name

    def __setName(self, n): self.__name = n

    name = property(__getName, __setName)

    def __getLogger(self): return self.__logger

    logger = property(__getLogger)

    def __getTikZCircledArrows(self): return self.__tikZCircledArrows

    tikZCircledArrows = property(__getTikZCircledArrows)

    def __getTikZCoordinates(self): return self.__tikZCoordinates

    tikZCoordinates = property(__getTikZCoordinates)

    def __getTikZNodes(self): return self.__tikZNodes

    tikZNodes = property(__getTikZNodes)

    def __getTikZPolygons(self): return self.__tikZPolygons

    tikZPolygons = property(__getTikZPolygons)

    def __getTikZLines(self): return self.__tikZLines

    tikZLines = property(__getTikZLines)

    def __getTikZCoSys(self): return self.__tikZCoSys

    tikZCoSys = property(__getTikZCoSys)

    def __getTikZNames(self):
        if self.__tikZNamesChanged:
            self.__calcTikZNames()
        return self.__tikZNames

    tikZNames = property(__getTikZNames)

    def __getTikZPrefix(self): return self.__tikZPrefix

    def __setTikZPrefix(self, t): self.__tikZPrefix = t

    tikZPrefix = property(__getTikZPrefix, __setTikZPrefix)

    def __getTikZText(self):
        text = ''
        text += self.__additionaTikZCodePre
        for t in self.__tikZCoordinates+self.__tikZNodes:
            text += t.tikZText
        for p in self.__tikZPolygons:
            text += p.tikZText

        for l in self.__tikZLines:
            text += l.tikZText
        for c in self.__tikZCoSys:
            text += c.tikZText
        for a in self.__tikZCircledArrows:
            text += a.tikZText
        text += self.__additionaTikZCodePost
        return text
    tikZText = property(__getTikZText)

    def __getDim(self): return 2

    dim = property(__getDim)

    def __getAdditionaTikZCodePre(self): return self.__additionaTikZCodePre

    def __setAdditionaTikZCodePre(self, a):
        if type(a) is str:
            self.__additionaTikZCodePre = a
        else:
            self.logger.error('Additional TikZ code must be a string')

    additionaTikZCodePre = property(__getAdditionaTikZCodePre,
                                    __setAdditionaTikZCodePre)

    def __getAdditionaTikZCodePost(self): return self.__additionaTikZCodePost

    def __setAdditionaTikZCodePost(self, a):
        if type(a) is str:
            self.__additionaTikZCodePost = a
        else:
            self.logger.error('Additional TikZ code must be a string')

    additionaTikZCodePost = property(__getAdditionaTikZCodePost,
                                     __setAdditionaTikZCodePost)

# =============================================================================
#    MAGIC METHODS
# =============================================================================
    def __repr__(self):
        '''
        Show infoText in console

        '''
        return 'TikZEnvironment "{}" '.format(self.name)

# =============================================================================
#    METHODS
# =============================================================================
# ------------------------------------------------------------------------
#    Transform coordinates into TikZ form
# ------------------------------------------------------------------------
    def numpy2TikZ(self, v, precission=3):
        '''
        Transform given coordinates from a vector into a string that is used
        in the TikZ plot.

        '''
        # Give a template for the format of the coordinate.
        # Example: '{:.3}'
        # In the later join function, the braces are replaced by the number
        coordFormat = r'{:.' + str(precission) + r'}'

        # Use join function to concatenate all coordinates in the wanted format
        return ','.join([coordFormat.format(float(x)) for x in v])

# ------------------------------------------------------------------------
#    Update names used in this environment
# ------------------------------------------------------------------------
    def __calcTikZNames(self):
        '''

        '''
        self.__tikZNames = [
            x.name for x in self.__tikZCoordinates+self.__tikZNodes]
        self.__tikZNamesChanged = False
        self.logger.debug('Updated TikZNames')

# ------------------------------------------------------------------------
#    Add a coordinate
# ------------------------------------------------------------------------
    def addTikZCoordinate(self, name, coordinates, *args, **kwargs):
        '''

        '''

        error = False
        if name in self.tikZNames:
            error = True
            self.logger.error('Cannot add TikZCoordinate, because ' +
                              'name "{}" is already in use'.format(name))

        try:
            if not coordinates.shape == (self.dim,):
                error = True
                self.logger.error(
                    'Wrong dimension: coordinates must be a ' +
                    '{}-dimensional vector, but its dimension is {}'
                    .format(self.dim, coordinates.shape))
        except:
            self.logger.error(
                'Could not check dimensions of coordinates "{}"'
                .format(coordinates))
            error = True

        if not error:
            self.logger.info('Adding TikZCoordinate {}'.format(name))
            tikZCoordinate = TikZCoordinate(
                name,
                coordinates,
                *args,
                tikZPicture=self,
                **kwargs)
            self.__tikZCoordinates.append(tikZCoordinate)
            self.__tikZNamesChanged = True
            return tikZCoordinate

# ------------------------------------------------------------------------
#    Add a node
# ------------------------------------------------------------------------
    def addTikZNode(self, name, coordinates, *args, **kwargs):
        '''

        '''

        error = False
        if name in self.tikZNames:
            error = True
            self.logger.error('Cannot add TikZNode, because name ' +
                              '"{}" is already in use'.format(name))

        try:
            if not coordinates.shape == (self.dim,):
                error = True
                self.logger.error(
                    'Wrong dimension: coordinates must be a ' +
                    '{}-dimensional vector, but its dimension is {}'
                    .format(self.dim, coordinates.shape))
        except:
            self.logger.error(
                'Could not check dimensions of coordinates "{}"'
                .format(coordinates))
            error = True

        if not error:
            self.logger.info('Adding TikZNode {}'.format(name))
            tikZNode = TikZNode(
                name,
                coordinates,
                *args,
                tikZPicture=self,
                **kwargs)
            self.__tikZNodes.append(tikZNode)
            self.__tikZNamesChanged = True
            return tikZNode

# ------------------------------------------------------------------------
#    Add a polygon
# ------------------------------------------------------------------------
    def addTikZPolygon(self, coordinates, *args, **kwargs):
        '''

        '''
        error = False
        for c in coordinates:
            if c not in self.__tikZCoordinates+self.__tikZNodes:
                error = True
                self.logger.error(
                    '{} is not a coordinate in this TikZPicture'.format(c))

        if error:
            self.logger.error('Cannot create TikZPolygon from coordinates {}'
                              .format([c.name for c in coordinates]))
        else:
            self.__tikZPolygons.append(
                TikZPolygon(coordinates,
                            *args,
                            **kwargs,
                            tikZEnvironment=self))
            self.logger.info('Adding TikZPolygon with coordinates {}'
                             .format([c.name for c in coordinates]))

# ------------------------------------------------------------------------
#    Add a line
# ------------------------------------------------------------------------
    def addTikZLine(self, start, end, *args, **kwargs):
        '''

        '''
        error = False
        for c in [start, end]:
            if c not in self.__tikZCoordinates+self.__tikZNodes:
                error = True
                self.logger.error('{} is not a coordinate in this TikZPicture'
                                  .format(c))

        if error:
            self.logger.error('Cannot create TikZPolygon from coordinates {}'
                              .format([c.name for c in [start, end]]))
        else:
            self.__tikZLines.append(
                TikZLine(start, end, *args, **kwargs, tikZEnvironment=self))
            self.logger.info('Adding TikZLine with coordinates {}'
                             .format([c.name for c in [start, end]]))

# ------------------------------------------------------------------------
#    Add a 2D coordinate system
# ------------------------------------------------------------------------
    def addTikZCoSy2D(self, center, *args, **kwargs):
        '''

        '''
        coSy = TikZCoSy2D(center, *args, tikZEnvironment=self, **kwargs)
        if center in self.__tikZCoordinates+self.__tikZNodes:
            self.__tikZCoSys.append(coSy)
            return coSy
        else:
            self.logger.error('{} is not a coordinate in this TikZPicture'
                              .format(center))

# ------------------------------------------------------------------------
#    Add a circled arrow
# ------------------------------------------------------------------------
    def addTikZCircledArrow(self, center, *args, **kwargs):
        '''

        '''
        circledArrow = TikZCircledArrow(
            center,
            *args,
            tikZEnvironment=self,
            **kwargs)
        if center in self.__tikZCoordinates+self.__tikZNodes:
            self.__tikZCircledArrows.append(circledArrow)
            return circledArrow
        else:
            self.logger.error('{} is not a coordinate in this TikZPicture'
                              .format(center))


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================

if __name__ == '__main__':
    import logging
    with ml.MyLogging('TikZEvironment', shLevel=logging.DEBUG):
        cc.printBlue('Create environment')
        env = TikZEnvironment()

        cc.printBlue('Add a coordinate')
        c1 = env.addTikZCoordinate('c1', np.array([0, 0]))

        cc.printBlue('Add a node')
        n1 = env.addTikZNode('n1', np.array([0, 0]))

        cc.printBlue('Add a polygon')
        env.addTikZPolygon([c1, n1])

        cc.printBlue('Add a 2D coordinate system')
        env.addTikZCoSy2D(c1)

        cc.printBlue('All names that are in use:')
        print(env.tikZNames)

        n1.tikZPrefix = '_'
        env.tikZPrefix = '%'
        cc.printBlue('TikZ commands:')
        print(env.tikZText)
