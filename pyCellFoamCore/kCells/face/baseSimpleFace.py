# -*- coding: utf-8 -*-
# =============================================================================
# BASE SIMPLE FACE
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue May 22 18:13:01 2018


'''


'''

# =============================================================================
#    IMPORTS
# =============================================================================
if __name__ == '__main__':
    import os
    os.chdir('../../')

import tools.colorConsole as cc
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from tools import Arrow3D
from kCells import BaseSimpleCell
import tools.tumcolor as tc


# =============================================================================
#    CLASS DEFINITION
# =============================================================================


class BaseSimpleFace(BaseSimpleCell):
    '''
    '''

# =============================================================================
#    INITIALIZATION
# =============================================================================

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger.debug('Initialized BaseSimpleFace')

    def deleteFace(self):
        # TODO: check that the face does not belong to a volume before deleting
        for e in self.data.edges:
            e.delFace(self)
        self.data.edges = []
        self.logger.info('Deleted Face %i', self.num)

# =============================================================================
#    SETTER AND GETTER
# =============================================================================

    def __getShowNormalVec(self):
        if self.belongsTo:
            return self.belongsTo.showNormalVec
        else:
            self.logger.warning(
                'Simple fdge does not belong to a real cell, ' +
                'using fixed standard value for showNormalVec')
            return True

    showNormalVec = property(__getShowNormalVec)

    def __getShowBarycenter(self):
        if self.belongsTo:
            return self.belongsTo.showBarycenter
        else:
            self.logger.warning(
                'Simple fdge does not belong to a real cell, ' +
                'using fixed standard value for showBarycenter')
            return True

    showBarycenter = property(__getShowBarycenter)

# =============================================================================
#    METHODS
# =============================================================================

    def printFace(self, printEdges=True, printNodes=False):

        print('=============================================================')
        print('-------------------------------------------------------------')
        cc.printGreenBackground('   ', end='')
        print(' Face Number', self.num, self.infoText)
        print('-------------------------------------------------------------')
        print('=============================================================')
        print()
        print('Label:'+self.labelText)
        print()
        num_edges = []
        for e in self.edges:
            if e.isReverse:
                num_edges.append(-e.num)
            else:
                num_edges.append(e.num)

        print("Includes edges:", num_edges)
        print()
        if printEdges:
            for e in self.edges:
                e.printEdge(printNodes)
        print()
        if len(self.volumes) > 0:
            if len(self.volumes) > 1:
                print('This Face belongs to', len(self.volumes), 'volumes:')
            else:
                print('This Face belongs to', len(self.volumes), 'volume:')
            print([f.num for f in self.volumes])
        else:
            print('This Face does not belong to a volume')
        print()
        print()
        print('-------------------------------------------------------------')
        print('=============================================================')
        print()
        print()
        print()

    def plotFace(self,
                 ax,
                 *args,
                 showNormalVec=None,
                 showLabel=None,
                 color=None,
                 showBarycenter=None,
                 alpha=0.15,
                 dx=0, dy=0, dz=0,
                 **kwargs):

        if showNormalVec is None:
            showNormalVec = self.showNormalVec

        if showLabel is None:
            showLabel = self.showLabel

        if color is None:
            color = self.color

        if showBarycenter is None:
            showBarycenter = self.showBarycenter

        if len(self.coordinates) > 2:
            collection = Poly3DCollection([self.coordinates],
                                          color=color.html,
                                          alpha=alpha)
            collection.set_facecolor(color.html)
            ax.add_collection3d(collection)
            if showBarycenter:
                ax.scatter(self.barycenter[0],
                           self.barycenter[1],
                           self.barycenter[2],
                           c=color.html)
            if showLabel:
                ax.text(self.barycenter[0]+dx,
                        self.barycenter[1]+dy,
                        self.barycenter[2]+dz,
                        self.labelText,
                        color=color.html)
            if showNormalVec:
                a = Arrow3D(self.barycenter,
                            self.barycenter+self.normalVec,
                            mutation_scale=20,
                            lw=2,
                            arrowstyle="-|>",
                            color=color.html)
                ax.add_artist(a)
        else:
            self.logger.error('Cannot Plot Face {} because it is empty'
                              .format(self.infoText))

    def plotFaceVtk(self, myVtk, showNormalVec=False, **kwargs):
        myVtk.addPolygon(self.coordinates)
        if showNormalVec:
            myVtk.addArrowStartEnd(self.barycenter,
                                   self.barycenter+self.normalVec)

    def plotFlowVtk(self, myVtk, length, color=None):
        myVtk.addArrowCenterDirection(self.barycenter,
                                      self.normalVec,
                                      length,
                                      color=color)

    def plotFaceTikZ(self, pic,
                     color=None,
                     showLabel=None,
                     shortLabel=True,
                     showArrow=True,
                     arrowDiameter=0.3,
                     opacity=0.2,
                     grayInTikZ=None,
                     showNormalVec=False,
                     **kwargs):
        '''

        '''

        if color is None:
            color = self.color

        if showLabel is None:
            showLabel = self.showLabel

        if grayInTikZ is None:
            grayInTikZ = self.grayInTikz

        if grayInTikZ:
            color = tc.TUMGrayMedium()

        polygonOptions = []
        arrowOptions = []
        normalVecOptions = ['->', ]

        polygonOptions.append(color.name)
        arrowOptions.append(color.name)
        normalVecOptions.append(color.name)

        if opacity:
            polygonOptions.append('fill opacity = {}'.format(opacity))

        nodes = []
        for e in self.simpleEdges:

            tikZNode = e.startNode.getTikZNode(pic)

            if not tikZNode:
                self.logger.info(
                    '{} has no tikZNode yet, '.format(e.startNode) +
                    'adding it as a simple TikZCoordinate')
                e.startNode.plotNodeTikZ(pic, showInPlot=False)

                newTikZNode = e.startNode.getTikZNode(pic)
                if newTikZNode:
                    nodes.append(newTikZNode)
                else:
                    self.logger.error(
                        'Could not get tikz node of node {}'
                        .format(e.startNode))
            else:
                nodes.append(tikZNode)

        v1 = np.array([0, 0, 0])
        v1[np.argmin(np.abs(self.normalVec))] = 1

        v2 = np.cross(self.normalVec, v1)

        if showLabel:
            if shortLabel:
                tikZLabelText = self.labelTextShort
            else:
                tikZLabelText = self.labelText
        else:
            tikZLabelText = ''

        if grayInTikZ:
            pic.addTikZPolygon(nodes,
                               command='draw',
                               cycle=True,
                               options=polygonOptions)

        else:
            pic.addTikZPolygon(nodes,
                               command='filldraw',
                               cycle=True,
                               options=polygonOptions)

            if pic.dim == 3:
                canv = pic.addTikZCanvas(center=self.barycenter,
                                         directionVecX=v1,
                                         directionVecY=v2)

                n = canv.addTikZNode(self.tikZName,
                                     np.array([0, 0]),
                                     content=tikZLabelText,
                                     options=arrowOptions)

                if showArrow:
                    canv.addTikZCircledArrow(n,
                                             arrowDiameter,
                                             options=arrowOptions)

            elif pic.dim == 2:
                n = pic.addTikZNode(self.tikZName,
                                    self.barycenter[:2],
                                    content=tikZLabelText,
                                    options=arrowOptions)
                if showArrow:
                    pic.addTikZCircledArrow(n,
                                            arrowDiameter,
                                            options=arrowOptions)
            else:
                self.logger.error('TikZPicture has dimension {}'
                                  .format(pic.dim))
            if showNormalVec:
                start = pic.addTikZCoordinate(self.tikZName+'Barycenter',
                                              self.barycenter)
                end = pic.addTikZCoordinate(self.tikZName+'NormalVec',
                                            self.barycenter+self.normalVec)

                pic.addTikZLine(start, end, normalVecOptions)

    def plotFaceTikZOld(self,
                        possibleNodeNames,
                        color=None,
                        fill=False,
                        draw=False,
                        arrowDiameter=0.2,
                        aspect3D=True,
                        showLabel=None,
                        grayInTikz=None,
                        shortLabel=True,
                        showArrow=True,
                        showNormalVec=False,
                        **kwargs):
        if True:
            myPrintDebug = self.logger.debug
            # myPrintInfo = self.logger.info
            # myPrintWarning = self.logger.warning
            myPrintError = self.logger.error
        else:
            self.logger.warning('Using prints instead of logger!')
            myPrintDebug = cc.printGreen
            # myPrintInfo = cc.printCyan
            # myPrintWarning = cc.printYellow
            myPrintError = cc.printRed

        if grayInTikz is None:
            grayInTikz = self.grayInTikz

        if showLabel is None:
            showLabel = self.showLabel

        if showLabel:
            if shortLabel:
                tikzLabelText = self.labelTextShort
            else:
                tikzLabelText = self.labelText
        else:
            tikzLabelText = ''

        v1 = np.array([0, 0, 0])
        v1[np.argmin(np.abs(self.normalVec))] = 1

        v2 = np.cross(self.normalVec, v1)

        o = self.barycenter
        x = self.barycenter+v1
        y = self.barycenter+v2

        optionsNode = []
        optionsCircledarrow = []
        optionsFilldraw = []

        if color is True:
            optionsNode.append(self.color.name)
            optionsCircledarrow.append(self.color.name)
            optionsFilldraw.append(self.color.name)
        elif color:
            optionsNode.append(color.name)
            optionsCircledarrow.append(color.name)
            optionsFilldraw.append(color.name)

        if fill:
            optionsFilldraw.append('fill opacity=0.05')

        optionsNodeText = ''
        if optionsNode:
            optionsNodeText = '['+', '.join(optionsNode)+']'

        optionsCircledarrowText = ''
        if optionsCircledarrow:
            optionsCircledarrowText = ', '.join(optionsCircledarrow)

        optionsFilldrawText = ''
        if optionsFilldraw:
            optionsFilldrawText = '['+', '.join(optionsFilldraw)+']'

        if aspect3D:
            tikzText = '\\begin{{scope}}'
            tikzText += '[canvas is plane={{O({})x({})y({})}}]\n' \
                .format(self.tikzCoords(o),
                        self.tikzCoords(x),
                        self.tikzCoords(y))
            tikzText += '\t\\node{} ({}) at (0, 0) {{{}}};\n' \
                .format(optionsNodeText, self.tikZName, tikzLabelText)
            if showArrow:
                tikzText += '\t\\circledarrow{{{}}}{{{}}}{{{}}}\n' \
                    .format(optionsCircledarrowText,
                            self.tikZName,
                            arrowDiameter)
            tikzText += '\\end{scope}\n'
        else:
            tikzText = '\\node{} ({}) at ({}) {{{}}};\n' \
                .format(optionsNodeText,
                        self.tikZName,
                        self.tikzCoords(o[:2]),
                        tikzLabelText)
            if showArrow:
                tikzText += '\t\\circledarrow{{{}}}{{{}}}{{{}}}\n' \
                    .format(optionsCircledarrowText,
                            self.tikZName,
                            arrowDiameter)

        if showNormalVec:
            tikzText += '\\draw[-stealth, {}] ({}) -- +({});' \
                .format(optionsCircledarrowText,
                        self.tikzCoords(self.barycenter),
                        self.tikzCoords(self.normalVec))

        if fill or draw:
            command = '\\'
            if fill:
                command += 'fill'
            if draw:
                command += 'draw'

            myPrintDebug('Nodes for {}: {}'.format(self, self.nodes))
            currentTikZNames = [x.tikZName for x in self.nodes]
            if all(name in possibleNodeNames for name in currentTikZNames):

                coords = ' -- '.join('('+x+'.center)'
                                     for x in currentTikZNames)
                coords += ' -- cycle'
                tikzText += '{}{} {};\n'.format(command,
                                                optionsFilldrawText,
                                                coords)
            else:
                myPrintError('Cannot find all needed nodes to plot {} in TikZ'
                             .format(self))

        if grayInTikz:
            tikzText = ''

        return tikzText


if __name__ == "__main__":

    bsf = BaseSimpleFace()
    print(bsf.showBarycenter)
    print(bsf.showNormalVec)
