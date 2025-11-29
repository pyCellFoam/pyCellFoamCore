# -*- coding: utf-8 -*-
#==============================================================================
# DUAL COMPLEX 3D
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Mar  1 15:14:05 2019

'''

'''
# =============================================================================
#    IMPORTS
# =============================================================================

# ------------------------------------------------------------------------
#    Standard Libraries
# ------------------------------------------------------------------------
import logging

# ------------------------------------------------------------------------
#    Third-Party Libraries
# ------------------------------------------------------------------------

# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------

#    k-Cells
# -------------------------------------------------------------------
from pyCellFoamCore.k_cells.node.node import Node
from pyCellFoamCore.k_cells.node.dualNode2D import DualNode2D
from pyCellFoamCore.k_cells.node.dualNode3D import DualNode3D
from pyCellFoamCore.k_cells.edge.edge import Edge
from pyCellFoamCore.k_cells.edge.dualEdge2D import DualEdge2D
from pyCellFoamCore.k_cells.edge.dualEdge3D import DualEdge3D
from pyCellFoamCore.k_cells.face.face import Face
from pyCellFoamCore.k_cells.face.dualFace2D import DualFace2D
from pyCellFoamCore.k_cells.face.dualFace3D import DualFace3D
from pyCellFoamCore.k_cells.volume.volume import Volume
from pyCellFoamCore.k_cells.volume.dualVolume3D import DualVolume3D

#    Complex
# -------------------------------------------------------------------
from pyCellFoamCore.complex.complex3D import Complex3D
from pyCellFoamCore.complex.primalComplex3D import PrimalComplex3D

#    Grids
# -------------------------------------------------------------------

#    Bounding Box
# -------------------------------------------------------------------

#    Tools
# -------------------------------------------------------------------
from pyCellFoamCore.tools.logging_formatter import set_logging_format

import pyCellFoamCore.tools.colorConsole as cc



# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class DualComplex3D(Complex3D):
    '''

    '''

#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__primalComplex',
                 '__createNodes',
                 '__createEdges',
                 '__createFaces',
                 '__createVolumes')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,primalComplex,createNodes=True,createEdges=True,createFaces=True,createVolumes=True):
        '''

        :param PrimalComplex primalComplex: The primal complex of which the
            dual shall be constructed.

        '''


        self.__primalComplex = primalComplex
        primalComplex.dualComplex = self
        self.__createNodes = createNodes
        self.__createEdges = createEdges
        self.__createFaces = createFaces
        self.__createVolumes = createVolumes
        super().__init__()


#        self.__primalComplex = primalComplex
#
#        (nodes,edges,faces,volumes) = self.__createDualCells(primalComplex)
#
#        super().__init__(nodes,
#                         edges,
#                         faces,
#                         volumes)
#
#
#
#
#
#        primalComplex.dualComplex = self
#        for f in self.faces:
#            for n in f.geometricNodes:
#                if not n in self.geometricNodes:
#                    self.geometricNodes.append(n)
#            for e in f.geometricEdges:
#                if not e in self.geometricEdges:
#                    self.geometricEdges.append(e)
#
#
#        self.renumberList(self.geometricNodes)
##        _log.warning(self.geometricNodes)
#
#
#
#
#
#        self.sortPrimal()
##        self.__checkCategory2()
#        self.sortDual()



#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getPrimalComplex(self): return self.__primalComplex
    primalComplex = property(__getPrimalComplex)
    '''

    '''

    def __getUseCategory(self):
        if self.__primalComplex:
            return self.__primalComplex.useCategory
        else:
            _log.error('Cannot get useCategory: no dual defined')
            return None
    def __setUseCategory(self,u):
        if self.__primalComplex:
            self.__primalComplex.useCategory = u
        else:
            _log.error('Cannot set useCategory: no dual defined')
    useCategory = property(__getUseCategory,__setUseCategory)
    '''

    '''


    def __getChangedNumbering(self):
        if self.primalComplex:
            return self.primalComplex.changedNumbering
        else:
            _log.error('Cannot get changedNumbering: no primalComplex defined')
            return False
    changedNumbering = property(__getChangedNumbering)
    '''

    '''








#==============================================================================
#    MAGIC METHODS
#==============================================================================
    def  __repr__(self):
        return 'DualComplex3D with {} nodes, {} edges, {} faces and {} volumes'.format(len(self.nodes),len(self.edges),len(self.faces),len(self.volumes))

#==============================================================================
#    METHODS
#==============================================================================



    def setUp(self):
        '''

        '''
        _log.info('Called "Set Up" in DualComplex2D class')
        self.__construct()
        self.sortPrimal()
        self.sortDual()
        super().setUp()






#-------------------------------------------------------------------------
#    Method 1
#-------------------------------------------------------------------------
    def __construct(self):
        cc.printMagenta('Dual Complex 3D: Creating dual cells')
        dualNodes = []
        dualEdges = []
        dualFaces = []
        dualVolumes = []



        # Dual nodes
        if self.__createNodes:
            _log.info("Create 3D dual nodes")
            for v in self.__primalComplex.volumes:
                cc.printBlue("Create dual node of {}".format(v))
                dualNodes.append(DualNode3D(v))
            for f in self.__primalComplex.borderFaces1:
                dualNodes.append(DualNode2D(f))
        else:
            _log.warning('Creation of nodes has been disabled')

        # return None

        # Dual edges
        if self.__createEdges and self.__createNodes:
            for f in self.__primalComplex.innerFaces1 + self.__primalComplex.borderFaces1:
                dualEdges.append(DualEdge3D(f))
            for e in self.__primalComplex.borderEdges1:
                dualEdges.append(DualEdge2D(e))
        else:
            _log.warning('Creation of edges has been disabled')

        # Dual faces
        if self.__createFaces and self.__createEdges and self.__createNodes:
            for e in self.__primalComplex.innerEdges1 +  self.__primalComplex.borderEdges1:
                dualFaces.append(DualFace3D(e))
            for n in self.__primalComplex.borderNodes1:
                dualFaces.append(DualFace2D(n))
            for f in dualFaces:
                f.simplifyFace()
        else:
            _log.warning('Creation of faces has been disabled')


        # Dual volumes
        if self.__createVolumes and self.__createFaces and self.__createEdges and self.__createNodes:
            for n in self.__primalComplex.borderNodes1+self.__primalComplex.innerNodes1:
                dualVolumes.append(DualVolume3D(n))
        else:
            _log.warning('Creation of volumes has been disabled')




        # Geometric nodes

        geometricNodes = []

        for e in dualEdges:
            for n in e.geometricNodes:
                if not n in geometricNodes:
                    geometricNodes.append(n)
        for f in dualFaces:
            for n in f.geometricNodes:
                if not n in geometricNodes:
                    geometricNodes.append(n)


        self.renumberList(geometricNodes)






#
#
#
#
##                            cc.printMagenta('Dual Complex 3D: finished simplification of faces')
#
#                            if True:
#                                # Dual volumes
#                                for n in primalComplex.borderNodes+primalComplex.innerNodes:
#                                    volumes.append(DualVolume3D(n))
#
#
        self.nodes = dualNodes
        self.edges = dualEdges
        self.faces = dualFaces
        self.volumes = dualVolumes
        self.geometricNodes = geometricNodes




#    def reOrderAll(self):
#        if self.useCategory == 1:
#            super().innerNodes1.sort(key = lambda x: x.num)
#            super().borderNodes1.sort(key = lambda x: x.num)
#            super().additionalBorderNodes1.sort(key = lambda x: x.num)
#            super().innerEdges1.sort(key = lambda x: x.num)
#            super().borderEdges1.sort(key = lambda x: x.num)
#            super().additionalBorderEdges1.sort(key = lambda x: x.num)
#            super().innerFaces1.sort(key = lambda x: x.num)
#            super().borderFaces1.sort(key = lambda x: x.num)
#            super().additionalBorderFaces1.sort(key = lambda x: x.num)
#            super().innerVolumes1.sort(key = lambda x: x.num)
#            super().borderVolumes1.sort(key = lambda x: x.num)
#        elif self.useCategory == 2:
#            super().innerNodes2.sort(key = lambda x: x.num)
#            super().borderNodes2.sort(key = lambda x: x.num)
#            super().additionalBorderNodes2.sort(key = lambda x: x.num)
#            super().innerEdges2.sort(key = lambda x: x.num)
#            super().borderEdges2.sort(key = lambda x: x.num)
#            super().additionalBorderEdges2.sort(key = lambda x: x.num)
##            _log.warning('Reactivate the line above!!')
#            super().innerFaces2.sort(key = lambda x: x.num)
#            super().borderFaces2.sort(key = lambda x: x.num)
#            super().additionalBorderFaces2.sort(key = lambda x: x.num)
#            super().innerVolumes2.sort(key = lambda x: x.num)
#            super().borderVolumes2.sort(key = lambda x: x.num)
#        else:
#            _log.error('Unknown useCategory {}'.format(self.useCategory))





    def renumber(self):
        '''

        '''
        if self.primalComplex:
            self.primalComplex.renumber()
        else:
            _log.error('Cannot renumber: no primalComplex defined')



#-------------------------------------------------------------------------
#    Check category 2
#-------------------------------------------------------------------------


    def checkCategory2(self):

        if False:
            myPrintDebug = _log.debug
            myPrintInfo = _log.info
            myPrintWarning = _log.warning
            myPrintError = _log.error
        else:
            _log.warning('Using prints instead of logger!')
            myPrintDebug = cc.printGreen
            myPrintInfo = cc.printCyan
            myPrintWarning = cc.printYellow
            myPrintError = cc.printRed


#    Check volumes
#-------------------------------------------------------------------------

        if True:
            myPrintInfo('Checking volumes')

            # Go through all faces
            for v in super().volumes:

                if v.category2 == 'undefined':
                    myPrintError('Category2 of {} was not set'.format(v))



#    Check faces
#-------------------------------------------------------------------------

        if True:
            myPrintInfo('Checking faces')

            # Go through all faces
            for f in super().faces:
#                f.useCategory = 2
#
                if f.category2 == 'undefined':
                    myPrintError('Category2 of {} was not set'.format(f))
#
                # Uncategorized faces are categorized automatically
                if len(f.volumes) == 0:
                    myPrintError('Face {} does not belong to a volume'.format(f))

                # Faces that belong to only one volume must be at some kind of border
                elif len(f.volumes) == 1:


                    # If the face belongs to a single inner volume, it is a border face
                    if f.volumes[0].category2 == 'inner':
                        if f.category2 == 'border':
                            myPrintDebug('Face {} is categorized correctly'.format(f))
                        else:
                            myPrintError('Category2 of  {} is wrong it is {} but should be border'.format(f,f.category2))

                    # If the face belongs to a single border volume, it is an additional border face
                    elif f.volumes[0].category2 == 'border':
                        if f.category2 == 'additionalBorder':
                            myPrintDebug('Face {} is categorized correctly'.format(f))
                        else:
                            myPrintError('Category2 of  {} is wrong it is {} but should be additionalBorder'.format(f,f.category2))

#                        f.category1 = 'additionalBorder'
#                        myPrintDebug('Face {} is an additional border face'.format(f.info_text))
#
#                    # Anything else is not knwon
                    else:
                        myPrintError('Unknown category of volume %s',f.volumes[0].info_text)
#
                # Faces that belong to two volumes are inner faces
                elif len(f.volumes) == 2:
                    if f.category2 == 'inner':
                        myPrintDebug('Face {} is categorized correctly'.format(f))
                    else:
                        myPrintError('Category2 of  {} is wrong it is {} but should be inner'.format(f,f.category2))
#
#                # Faces cannot belong to more than 2 volumes - at least in 3 dimensions ;)
#                elif len(f.volumes) > 2:
#                    myPrintError('Face {} belongs to too many volumes'.format(f))
#
#

#    Check edges
#-------------------------------------------------------------------------

        if True:
            myPrintInfo('Checking edges')

            for e in super().edges:

                if e.category2 == 'undefined':
                     myPrintError('Category2 of {} was not set'.format(e))

                # Edges that belong to a border face are border edges
                if any([f.category2 == 'border' for f in e.faces]):
                    if e.category2 == 'border':
                        myPrintDebug('Edge {} is categorized correctly'.format(e))
                    else:
                        myPrintError('Category2 of  {} is wrong it is {} but should be border'.format(e,e.category2))
#

                # Edges that  belong to additional border faces are additional border edges
                elif any([f.category2 == 'additionalBorder' for f in e.faces]):
                    if e.category2 == 'additionalBorder':
                        myPrintDebug('Edge {} is categorized correctly'.format(e))
                    else:
                        myPrintError('Category2 of  {} is wrong it is {} but should be additionalBorder'.format(e,e.category2))
#
                # Edges that are not categorized so far are inner edges
                else:
                    if e.category2 == 'inner':
                        myPrintDebug('Edge {} is categorized correctly'.format(e))
                    else:
                        myPrintError('Category2 of  {} is wrong it is {} but should be inner'.format(e,e.category2))


#    Check nodes
#-------------------------------------------------------------------------
        if True:

            myPrintInfo('Checking nodes')

            for n in super().nodes:
                if n.category2 == 'undefined':
                     myPrintError('Category2 of {} was not set'.format(n))


                # Nodes that belong to border edges are border nodes
                if any([e.category2 == 'border' for e in n.edges]):
                    if n.category2 == 'border':
                        myPrintDebug('Node {} is categorized correctly'.format(n))
                    else:
                        myPrintError('Category2 of  {} is wrong it is {} but should be border'.format(n,n.category2))
#
                # Nodes that belong to additional border edges are additional border nodes
                elif any([e.category2 == 'additionalBorder' for e in n.edges]):
                    if n.category2 == 'additionalBorder':
                        myPrintDebug('Node {} is categorized correctly'.format(n))
                    else:
                        myPrintError('Category2 of  {} is wrong it is {} but should be additionalBorder'.format(n,n.category2))
#                    n.category2 = 'additionalBorder'
#                    myPrintDebug('Node {} is an additional border node'.format(n))

                # Nodes that are not categorized so far are inner nodes
                else:
                    if n.category2 == 'inner':
                        myPrintDebug('Node {} is categorized correctly'.format(n))
                    else:
                        myPrintError('Category2 of  {} is wrong it is {} but should be inner'.format(n,n.category2))
#                    n.category1 = 'inner'
#                    myPrintDebug('Node {} is an inner node'.format(n))
#



#    Check dualities
#-------------------------------------------------------------------------
        if True:
            myPrintInfo('Checking dual complex')
            for v in super().volumes:
                if v.category2 == v.dualCell3D.category2:
                    myPrintDebug('{} and {} are ok'.format(v,v.dualCell3D))
                else:
                    myPrintError('Category2 of {} is not set correctly'.format(v.dualCell3D))

            for f in super().faces:
                if f.category2 == 'additionalBorder':
                    pass
#                    if f.category2 == f.dualCell2D.category2:
#                        myPrintDebug('{} and {} are ok'.format(f,f.dualCell2D))
#                    else:
#                        myPrintError('Category2 of {} (2D dual of {}) is not set correctly it is {} but should be '.format(f.dualCell2D,f))
                else:
                    if f.category2 == f.dualCell3D.category2:
                        myPrintDebug('{} and {} are ok'.format(f,f.dualCell3D))
                    else:
                        myPrintError('Category2 of {} is not set correctly'.format(f.dualCell3D))

            for e in super().edges:
#                myPrintDebug('Cell: {} - 3D dual: {} - 2D dual:  {}'.format(e,e.dualCell3D,e.dualCell2D))
                if e.category2 == 'additionalBorder':
                    pass
#                    if e.category2 == e.dualCell2D.category2:
#                        myPrintDebug('{} and {} are ok'.format(e,e.dualCell2D))
#                    else:
#                        myPrintError('Category2 of {} (2D dual of {}) is not set correctly'.format(e.dualCell2D,e))
                else:
                    if e.category2 == e.dualCell3D.category2:
                        myPrintDebug('{} and {} are ok'.format(e,e.dualCell3D))
                    else:
                        myPrintError('Category2 of {} is not set correctly'.format(e.dualCell3D))

            for n in super().nodes:
#                myPrintDebug('Cell: {} - 3D dual: {} - 2D dual:  {}'.format(n,n.dualCell3D,n.dualCell2D))
                if n.category2 == 'additionalBorder':
                    pass
#                    if n.category2 == n.dualCell2D.category2:
#                        myPrintDebug('{} and {} are ok'.format(n,n.dualCell2D))
#                    else:
#                        myPrintError('Category2 of {} (2D dual of {}) is not set correctly'.format(n.dualCell2D,n))
                else:
                    if n.category2 == n.dualCell3D.category2:
                        myPrintDebug('{} and {} are ok'.format(n,n.dualCell3D))
                    else:
                        myPrintError('Category2 of {} is not set correctly'.format(n.dualCell3D))


        if True:
            myPrintInfo('Checking primal complex')
            for v in self.__primalComplex.volumes:
                if v.category2 == v.dualCell3D.category2:
                    myPrintDebug('{} and {} are ok'.format(v,v.dualCell3D))
                else:
                    myPrintError('Category2 of {} is not set correctly'.format(v.dualCell3D))

            for f in self.__primalComplex.faces:
                if f.category2 == 'additionalBorder':
                    pass
#                    if f.category2 == f.dualCell2D.category2:
#                        myPrintDebug('{} and {} are ok'.format(f,f.dualCell2D))
#                    else:
#                        myPrintError('Category2 of {} (2D dual of {}) is not set correctly'.format(f.dualCell2D,f))
                else:
                    if f.category2 == f.dualCell3D.category2:
                        myPrintDebug('{} and {} are ok'.format(f,f.dualCell3D))
                    else:
                        myPrintError('Category2 of {} is not set correctly'.format(f.dualCell3D))

            for e in self.__primalComplex.edges:
                if e.category2 == 'additionalBorder':
                    pass
#                    if e.category2 == e.dualCell2D.category2:
#                        myPrintDebug('{} and {} are ok'.format(e,e.dualCell2D))
#                    else:
#                        myPrintError('Category2 of {} (2D dual of {}) is not set correctly'.format(e.dualCell2D,e))
                else:
                    if e.dualCell3D:
                        if e.category2 == e.dualCell3D.category2:
                            myPrintDebug('{} and {} are ok'.format(e,e.dualCell3D))
                        else:
                            myPrintError('Category2 of {} is not set correctly'.format(e.dualCell3D))
                    else:
                         myPrintError('3D dual of {} is defined'.format(e))

            for n in self.__primalComplex.nodes:
                if n.category2 == 'additionalBorder':
                    pass
#                    if n.dualCell2D:
#                        if n.category2 == n.dualCell2D.category2:
#                            myPrintDebug('{} and {} are ok'.format(n,n.dualCell2D))
#                        else:
#                            myPrintError('Category2 of {} (2D dual of {}) is not set correctly'.format(n.dualCell2D,n))
#                    else:
#                         myPrintError('2D dual of {} is not defined'.format(n))

                else:
                    if n.category2 == n.dualCell3D.category2:
                        myPrintDebug('{} and {} are ok'.format(n,n.dualCell3D))
                    else:
                        myPrintError('Category2 of {} is not set correctly'.format(n.dualCell3D))



#        for c in super().nodes + super().edges + super().faces + super().volumes + self.__primalComplex.nodes+self.__primalComplex.edges+self.__primalComplex.faces+self.__primalComplex.volumes:
#            c.useCategory = 1












    def checkAllIncidenceMatrices(self,doPrints=True):
        '''

        '''
        checks = []

        self.useCategory = 1
        if doPrints:
            cc.printBlue()
            cc.printBlue('Checking incidence matrix dualities')
            cc.printBlue('='*35)
            cc.printBlue()
            cc.printBlue('Using category 1')
            cc.printBlue('-'*15)
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix3ii,-self.__primalComplex.incidenceMatrix1ii,'d̂3ii','-d1ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix3ib,-self.__primalComplex.incidenceMatrix1bi,'d̂3ib','-d1bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix3bi,-self.__primalComplex.incidenceMatrix1ib,'d̂3bi','-d1ib',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix3bb,-self.__primalComplex.incidenceMatrix1bb,'d̂3bb','-d1bb',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2ii,self.__primalComplex.incidenceMatrix2ii,'d̂2ii','d2ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2ib,self.__primalComplex.incidenceMatrix2bi,'d̂2ib','d2bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2bi,self.__primalComplex.incidenceMatrix2ib,'d̂2bi','d2ib',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2bb,self.__primalComplex.incidenceMatrix2bb,'d̂2bb','d2bb',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1ii,-self.__primalComplex.incidenceMatrix3ii,'d̂1ii','-d3ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1ib,-self.__primalComplex.incidenceMatrix3bi,'d̂1ib','-d3bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1bi,-self.__primalComplex.incidenceMatrix3ib,'d̂1bi','-d3ib',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1bb,-self.__primalComplex.incidenceMatrix3bb,'d̂1bb','-d3bb',doPrints))

#        checks.append(self.checkIncidenceMatrixZero(self.incidenceMatrix1bb,'d̂1bb',doPrints))
#        checks.append(self.checkIncidenceMatrixZero(self.__primalComplex.incidenceMatrix1bb,'d1bb',doPrints))


        if doPrints:
            cc.printBlue()
            cc.printBlue('Using category 2')
            cc.printBlue('-'*15)

        self.useCategory = 2

        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix3ii,-self.__primalComplex.incidenceMatrix1ii,'d̂3ii','-d1ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix3ib,-self.__primalComplex.incidenceMatrix1bi,'d̂3ib','-d1bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix3bi,-self.__primalComplex.incidenceMatrix1ib,'d̂3bi','-d1ib',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix3bb,-self.__primalComplex.incidenceMatrix1bb,'d̂3bb','-d1bb',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2ii,self.__primalComplex.incidenceMatrix2ii,'d̂2ii','d2ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2ib,self.__primalComplex.incidenceMatrix2bi,'d̂2ib','d2bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2bi,self.__primalComplex.incidenceMatrix2ib,'d̂2bi','d2ib',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix2bb,self.__primalComplex.incidenceMatrix2bb,'d̂2bb','d2bb',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1ii,-self.__primalComplex.incidenceMatrix3ii,'d̂1ii','-d3ii',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1ib,-self.__primalComplex.incidenceMatrix3bi,'d̂1ib','-d3bi',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1bi,-self.__primalComplex.incidenceMatrix3ib,'d̂1bi','-d3ib',doPrints))
        checks.append(self.checkIncidenceMatrixEqual(self.incidenceMatrix1bb,-self.__primalComplex.incidenceMatrix3bb,'d̂1bb','-d3bb',doPrints))




        if doPrints:
            cc.printGreen()

            if all(checks):
                cc.printGreen('-'*50)
                cc.printGreen('All incidence matrix dualities are correct')
                cc.printGreen('-'*50)
            else:
                cc.printRed('-'*50)
                cc.printRed('Not all incidence matrix dualities are correct')
                cc.printRed('-'*50)
            cc.printGreen()
        return checks





# =============================================================================
#    TEST FUNCTIONS
# =============================================================================

if __name__ == '__main__':

    set_logging_format(logging.DEBUG)

    # --------------------------------------------------------------------
    #    Create sample data
    # --------------------------------------------------------------------

    _log.info('Create nodes')

    n000 = Node(0, 0, 0)
    n001 = Node(1, 0, 0)
    n002 = Node(1.5, 0, 0)
    n003 = Node(0, 1, 0)
    n004 = Node(1, 1, 0)
    n005 = Node(0, 1.5, 0)
    n006 = Node(1.5, 1.5, 0)
    n007 = Node(0, 0, 1)
    n008 = Node(1, 0, 1)
    n009 = Node(0, 1, 1)
    n010 = Node(1, 1, 1)
    n011 = Node(0, 0, 1.5)
    n012 = Node(1.5, 0, 1.5)
    n013 = Node(0, 1.5, 1.5)
    n014 = Node(1.5, 1.5, 1.5)

    nodes = [
        n000, n001, n002, n003, n004, n005, n006, n007, n008, n009,
        n010, n011, n012, n013, n014,
    ]

    _log.info('Create edges')

    e000 = Edge(n000, n001)
    e001 = Edge(n001, n002)
    e002 = Edge(n003, n004)
    e003 = Edge(n005, n006)
    e004 = Edge(n000, n003)
    e005 = Edge(n001, n004)
    e006 = Edge(n002, n006)
    e007 = Edge(n003, n005)
    e008 = Edge(n004, n006)
    e009 = Edge(n007, n008)
    e010 = Edge(n008, n010)
    e011 = Edge(n010, n009)
    e012 = Edge(n009, n007)
    e013 = Edge(n011, n012)
    e014 = Edge(n012, n014)
    e015 = Edge(n014, n013)
    e016 = Edge(n013, n011)
    e017 = Edge(n000, n007)
    e018 = Edge(n001, n008)
    e019 = Edge(n004, n010)
    e020 = Edge(n003, n009)
    e021 = Edge(n002, n012)
    e022 = Edge(n006, n014)
    e023 = Edge(n005, n013)
    e024 = Edge(n007, n011)
    e025 = Edge(n008, n012)
    e026 = Edge(n010, n014)
    e027 = Edge(n009, n013)

    edges = [
        e000, e001, e002, e003, e004, e005, e006, e007, e008, e009,
        e010, e011, e012, e013, e014, e015, e016, e017, e018, e019,
        e020, e021, e022, e023, e024, e025, e026, e027,
    ]

    _log.info('Create faces')

    f000 = Face([e000, e005, -e002, -e004])
    f001 = Face([e001, e006, -e008, -e005])
    f002 = Face([e002, e008, -e003, -e007])
    f003 = Face([e000, e018, -e009, -e017])
    f004 = Face([e005, e019, -e010, -e018])
    f005 = Face([e002, e019, e011, -e020])
    f006 = Face([e004, e020, e012, -e017])
    f007 = Face([e009, e010, e011, e012])
    f008 = Face([e009, e025, -e013, -e024])
    f009 = Face([e001, e021, -e025, -e018])
    f010 = Face([e006, e022, -e014, -e021])
    f011 = Face([e025, e014, -e026, -e010])
    f012 = Face([e008, e022, -e026, -e019])
    f013 = Face([e003, e022, e015, -e023])
    f014 = Face([e026, e015, -e027, -e011])
    f015 = Face([e007, e023, -e027, -e020])
    f016 = Face([e027, e016, -e024, -e012])
    f017 = Face([e013, e014, e015, e016])

    faces = [
        f000, f001, f002, f003, f004, f005, f006, f007, f008, f009,
        f010, f011, f012, f013, f014, f015, f016, f017,
    ]

    _log.info('Create volumes')

    v000 = Volume([-f000, f003, f004, -f005, -f006, f007])
    v001 = Volume([-f001, -f004, f009, f010, f011, -f012])
    v002 = Volume([-f002, f005, f012, -f013, f014, -f015])
    v003 = Volume([-f007, f008, -f011, -f014, -f016, f017])

    volumes = [
        v000, v001, v002, v003,
    ]

    for v in [v001, v002, v003]:
        v.category1 = "border"

    pc = PrimalComplex3D(nodes, edges, faces, volumes)
    dc = DualComplex3D(primalComplex=pc)

    # --------------------------------------------------------------------
    #    Plotting
    # --------------------------------------------------------------------

    # Choose plotting method. Possible choices: pyplot, VTK, TikZ, plotly, None
    PLOTTING_METHOD = "plotly"

    match PLOTTING_METHOD:
        case "pyplot":
            _log.info("Plotting with pyplot selected.")
            (figs, axes) = pf.getFigures()
            pc.plotComplex(axes[0])
            pc.plotFaces(axes[1])
            pc.plotVolumes(axes[2])
            for f in figs:
                f.show()

        case "VTK":
            _log.info("Plotting with VTK selected.")
            myVTK = pc.plotComplexVTK(showLabel=False, showArrow=False)
            myVTK.start()

        case "TikZ":
            _log.info("Plotting with TikZ selected.")
            pic = pc.plotComplexTikZ()
            pic.scale = 5
            file = True
            pic.writeLaTeXFile(
                'latex',
                'primalComplex3D',
                compileFile=file,
                openFile=file,
            )

            picNodes = pc.plotNodesTikZ()
            picNodes.scale = 2
            picNodes.writeTikZFile(filename='Complex3D0Nodes')

            picEdges = pc.plotEdgesTikZ()
            picEdges.scale = 2
            picEdges.writeTikZFile(filename='Complex3D1Edges')

            picFaces = pc.plotFacesTikZ()
            picFaces.scale = 2

            picFaces.writeTikZFile(filename='Complex3D2Faces')

        case "plotly":
            _log.info("Plotting with plotly selected.")

            node_plotly = NodePlotly(pc.nodes)
            edge_plotly = EdgePlotly(pc.edges)
            face_plotly = FacePlotly(pc.faces)

            plotly_fig_nodes_edges = node_plotly.plot_nodes_plotly(
                show_label=True
            )
            edge_plotly.plot_edges_plotly(
                plotly_fig_nodes_edges,
                show_label=True,
                show_barycenter=False,
                cone_size=0.05,
            )
            plotly_fig_nodes_edges.show()

            plotly_fig_edges_faces = edge_plotly.plot_edges_plotly(
                show_label=False,
                show_barycenter=False,
                cone_size=0.05,
            )
            face_plotly.plot_faces_plotly(
                plotly_fig_edges_faces,
                show_label=True,
                show_barycenter=False,
            )
            plotly_fig_edges_faces.show()

        case "None":
            _log.info("No plotting selected.")

        case _:
            _log.error(
                "Unknown plotting '%s' method selected.",
                PLOTTING_METHOD,
            )
