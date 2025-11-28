# -*- coding: utf-8 -*-
#==============================================================================
# MyVTK
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Dec  7 14:16:21 2017

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
import vtk
import numpy as np
import math

import pyCellFoamCore.tools.colorConsole as cc
import pyCellFoamCore.tools.tumcolor as tc


#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class MyVTK:
    '''
    This is the explanation of this class.

    '''

#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__renderer',
                 '__rendererWindow',
                 '__renderWindowInteractor',
                 '__sampleFunction',
                 '__booleanUnion',
                 '__aviWriter',
                 '__windowToImageFilter',
                 '__actors',
                 '__points',
                 '__pointSize',
                 '__vertices',
                 '__scatterPolydata',
                 '__doScatter',
                 '__pointColors',
                 '__pointsForPolygons',
                 '__pointIDPolygon',
                 '__polygons',
                 '__doPolygons',
                 '__polygonOpacity',
                 '__extract',
                 '__arrowActors',
                 '__lineActors'
                 )

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,pointSize=None,backgroundColor=[0,0,0],polygonOpacity=0.5):
        '''
        This is the explanation of the __init__ method.

        All parameters should be listed:

        :param int a: Some Number
        :param str b: Some String

        '''

        try:
            import localConfig
            vtkWindowSize = localConfig.vtkWindowSize
            vtkTopLeftCorner = localConfig.vtkTopLeftCorner
        except:
            vtkWindowSize = (1920,1080)
            vtkTopLeftCorner = (0,0)
            cc.printRed('place Figures: No local configuration file found, using standard')


        # create a rendering window and renderer
        self.__renderer = vtk.vtkRenderer()
        self.__renderer.SetBackground(*backgroundColor)
        self.__rendererWindow = vtk.vtkRenderWindow()
        self.__rendererWindow.AddRenderer(self.__renderer)
        self.__rendererWindow.SetPosition(*vtkTopLeftCorner)
        self.__rendererWindow.SetSize(*vtkWindowSize)

        # Prepare scatter plot
        self.__points = vtk.vtkPoints()
        self.__vertices = vtk.vtkCellArray()
        self.__scatterPolydata = vtk.vtkPolyData()
        self.__doScatter = False
        self.__pointColors = vtk.vtkUnsignedCharArray()
        self.__pointColors.SetNumberOfComponents(3)

        # Prepare Polygon
        self.__pointsForPolygons = vtk.vtkPoints()
        self.__polygons = vtk.vtkCellArray()
        self.__pointIDPolygon = 0
        self.__polygonOpacity = polygonOpacity
        self.__doPolygons = False



#
        # create a renderwindowinteractor
        self.__renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        self.__renderWindowInteractor.SetRenderWindow(self.__rendererWindow)

        # Prepare sampling
        self.__sampleFunction = None
        self.__booleanUnion = None

        # Prepare video export
        self.__aviWriter = None
        self.__windowToImageFilter = None

        self.__actors = []
        self.__arrowActors = []
        self.__lineActors = []


        if pointSize is None:
            self.__pointSize =  20
        else:
            self.__pointSize = pointSize



#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getRenderer(self): return self.__renderer
    renderer = property(__getRenderer)

    def __getRenderWindowInteractor(self): return self.__renderWindowInteractor
    renderWindowInteractor = property(__getRenderWindowInteractor)


    def __getActors(self): return self.__actors
    actors = property(__getActors)

    def __getSampleFunction(self): return self.__sampleFunction
    sampleFunction = property(__getSampleFunction)


    def __getExtract(self): return self.__extract
    extract = property(__getExtract)


    def __getPolygonOpacity(self): return self.__polygonOpacity
    def __setPolygonOpacity(self,p): self.__polygonOpacity = p
    polygonOpacity = property(__getPolygonOpacity,__setPolygonOpacity)



#==============================================================================
#    METHODS
#==============================================================================

#-------------------------------------------------------------------------
#    Method 1
#-------------------------------------------------------------------------


    def addLine(self,point1,point2,lineWidth = 4, color = [255,255,255]):

        lineSource = vtk.vtkLineSource()
        lineSource.SetPoint1(point1)
        lineSource.SetPoint2(point2)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(lineSource.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetLineWidth(lineWidth)
        actor.GetProperty().SetColor(color[0],color[1],color[2])
        self.addActor(actor)


    def addScatterPointNumpy(self,point,**kwargs):
        self.addScatterPoint(point[0],point[1],point[2],**kwargs)

    def addScatterPoint(self,x,y,z,text=None,color=[255,255,255],**kwargs):
        self.__doScatter = True
        id = self.__points.InsertNextPoint(x,y,z)
        self.__vertices.InsertNextCell(1)
        self.__vertices.InsertCellPoint(id)
        self.__pointColors.InsertNextTuple3(*color)


        if text:
            self.addTextAnnotation(x,y,z,text,**kwargs)





    def addTextAnnotationNumpy(self,point,*args,**kwargs):
        self.addTextAnnotation(point[0],point[1],point[2],*args,**kwargs)


    def addTextAnnotation(self,x,y,z,text,distToPoint = 0.02,color=None,fontSize=None):
        textActor = vtk.vtkBillboardTextActor3D()
        if color:
            textActor.GetTextProperty().SetColor(*color)
        if fontSize:
            textActor.GetTextProperty().SetFontSize(fontSize)

        textActor.SetInput(str(text))
        textActor.SetPosition(x+distToPoint,y+distToPoint,z+distToPoint)
        self.addActor(textActor)

    def addText3D(self,x,y,z,text,scale=1,extrude=None):
        textSource = vtk.vtkVectorText()
        textSource.SetText(text)
        textSource.Update()

        # Must store this as a local variables, raises error otherwise
        sf = extrude

        textMapper = vtk.vtkPolyDataMapper()


#        transform = vtk.vtkTransform()
#        transform.Translate(np.array([x,y,z]))
#        transform.RotateWXYZ(orientation,1,0,0)
#        transform.Scale(scale,scale,scale)


#        transformPD = vtk.vtkTransformPolyDataFilter()
#        transformPD.SetTransform(transform)
#        transformPD.SetInputConnection(textSource.GetOutputPort())
#        print(transformPD.GetProperty())



        if extrude:
            extrude = vtk.vtkLinearExtrusionFilter()
            extrude.SetInputConnection(textSource.GetOutputPort())
            extrude.SetExtrusionTypeToNormalExtrusion()
            extrude.SetVector(0, 0, 1 )
            extrude.SetScaleFactor(sf)

            triangleFilter = vtk.vtkTriangleFilter()
            triangleFilter.SetInputConnection(extrude.GetOutputPort())

            textMapper.SetInputConnection(textSource.GetOutputPort())
        else:
            textMapper.SetInputConnection(textSource.GetOutputPort())

        follower = vtk.vtkFollower()
        follower.SetMapper(textMapper)
        follower.SetPosition(x,y,z)
        follower.SetScale(scale)

#        print(follower.GetCenter())
#        centerOld=np.array(list(follower.GetCenter()))
#        centerGiven=np.array([x,y,z])
#        follower.AddPosition(*list(centerGiven-centerOld))
#
#        follower.SetOrientation(orientation[0],orientation[1],orientation[2])
#        print(follower.GetCamera())
#        print(follower.GetProperty())

        self.addActor(follower)




    def addText3DNew(self,x,y,z,text,scale=1,rotationWXYZ=None,color=None):
        textSource = vtk.vtkVectorText()
        textSource.SetText(text)
        textSource.Update()

#        print(text)
#        print('-'*20)
        textMapper = vtk.vtkPolyDataMapper()


        transform = vtk.vtkTransform()

        transform.Scale(scale,scale,scale)


        transformPD = vtk.vtkTransformPolyDataFilter()
        transformPD.SetTransform(transform)
        transformPD.SetInputConnection(textSource.GetOutputPort())

        textMapper.SetInputConnection(transformPD.GetOutputPort())


        textActor = vtk.vtkActor()
        textActor.SetMapper(textMapper)
        if color:
            textActor.GetProperty().SetColor(*color)


#        centerStart = np.array(list(textActor.GetCenter()))

#        print('center at start',centerStart)

        if rotationWXYZ is not None:
            transform.RotateWXYZ(*rotationWXYZ)

        centerRotation = np.array(list(textActor.GetCenter()))

#        print('center after rotation',centerRotation)

        centerDesired = np.array([x,y,z])

#        print('Wanted center:',centerDesired)

        translationWantedWorld = (centerDesired - centerRotation)

#        print('Requested translation in world coordinates:',translationWantedWorld)

        transform.Inverse()
        translationLocal = np.array(list(transform.TransformPoint(translationWantedWorld)))*scale
        transform.Inverse()



#        print('Requested translation in local coordinates',translationLocal)


        transform.Translate(translationLocal/scale)

#        centerFinal = np.array(list(textActor.GetCenter()))

#        print('center after translation',centerFinal)

#        translationActual = centerFinal-centerRotation
#
#        print('Actual translation:',translationActual)

#        print()
#        print()
        self.addActor(textActor)



    def addArrowCenterDirection(self,center,direction,length=1,**kwargs):
        directionNormalized = direction/np.linalg.norm(direction)
        start = center-0.5*directionNormalized*length
        end = center+0.5*directionNormalized*length
        self.addArrowStartEnd(start,end,**kwargs)

    def addArrowStartEnd(self,start,end,color=None,diameter=1):

        if color is None:
            color = [1,1,1]

        # Calculate geometry
        vecPoints = end-start
        vecStartNormalized = np.array([1,0,0])

        vecRotation = np.cross(vecPoints,vecStartNormalized)
        if np.linalg.norm(vecRotation)<1e-2:
            vecRotation = np.array([0,1,0])

        length = np.linalg.norm(vecPoints)
        if length>1e-3:
            vecPointsNormalized = vecPoints / length



            angle = np.arccos(np.clip(np.dot(vecPointsNormalized, vecStartNormalized), -1.0, 1.0))

            # Create VTK objects
            arrowSource = vtk.vtkArrowSource()
            transform = vtk.vtkTransform()
            transform.Translate(start)
            transform.RotateWXYZ(-angle*360/math.tau,vecRotation[0],vecRotation[1],vecRotation[2])
            transform.Scale(length,diameter*length,diameter*length)
            transformPD = vtk.vtkTransformPolyDataFilter()
            transformPD.SetTransform(transform)
            transformPD.SetInputConnection(arrowSource.GetOutputPort())
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(transformPD.GetOutputPort())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetColor(color)

            # Plot
            self.addActor(actor)
            self.__arrowActors.append(actor)

        else:
            pass
#            print('arrow is to short')


    def removeArrows(self):
        for a in self.__arrowActors:
            self.__renderer.RemoveActor(a)
            self.__actors.remove(a)
        self.__arrowActors= []


    def addCoordinateSystem(self,length=1):
        red = tc.TUMOrange().rgb01
        green = tc.TUMGreen().rgb01
        blue = tc.TUMBlue().rgb01
        self.addArrowStartEnd(np.array([0,0,0]),np.array([length,0,0]),color=red)
        self.addArrowStartEnd(np.array([0,0,0]),np.array([0,length,0]),color=green)
        self.addArrowStartEnd(np.array([0,0,0]),np.array([0,0,length]),color=blue)

        self.addTextAnnotationNumpy(np.array([length,0,0]),'x',color=red,fontSize=30)
        self.addTextAnnotationNumpy(np.array([0,length,0]),'y',color=green,fontSize=30)
        self.addTextAnnotationNumpy(np.array([0,0,length]),'z',color=blue,fontSize=30)



    def addPolygon(self,coordinates):
        self.__doPolygons = True
        polygon = vtk.vtkPolygon()
        polygon.GetPointIds().SetNumberOfIds(len(coordinates))
        for (num,coordinate) in enumerate(coordinates):
            self.__pointsForPolygons.InsertNextPoint(coordinate[0],coordinate[1],coordinate[2])
#            cc.printMagenta(num,self.__pointIDPolygon)
            polygon.GetPointIds().SetId(num,self.__pointIDPolygon)
            self.__pointIDPolygon += 1
        self.__polygons.InsertNextCell(polygon)






    def addSource(self,source):
        # mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())

        # actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # assign actor to the renderer
        self.__renderer.AddActor(actor)
        self.__actors.append(actor)


    def addActor(self,actor,shading=True):
        if not shading:
            prop = vtk.vtkProperty()
            prop.SetDiffuse(0.0)
            prop.SetSpecular(0.0)
            prop.SetAmbient(1.0)
            actor.SetProperty(prop)
        self.__renderer.AddActor(actor)
        self.__actors.append(actor)


    def removeActors(self):
        for a in self.__actors:
            self.__renderer.RemoveActor(a)
        self.__actors = []



        self.__points = vtk.vtkPoints()
        self.__vertices = vtk.vtkCellArray()
        self.__scatterPolydata = vtk.vtkPolyData()
        self.__doScatter = False
        self.__pointColors = vtk.vtkUnsignedCharArray()
        self.__pointColors.SetNumberOfComponents(3)

#        self.__pointsForPolygons = vtk.vtkPoints()
#        self.__polygons = vtk.vtkCellArray()
#        self.__pointIDPolygon = 0
#        self.__doPolygons = False


    def showPolygons(self):
        polygonPolyData = vtk.vtkPolyData()
        polygonPolyData.SetPoints(self.__pointsForPolygons)
        polygonPolyData.SetPolys(self.__polygons)
        polyMapper = vtk.vtkPolyDataMapper()
        polyMapper.SetInputData(polygonPolyData)
        polyActor = vtk.vtkActor()
        polyActor.SetMapper(polyMapper)
        polyActor.GetProperty().SetOpacity(self.polygonOpacity)
        self.addActor(polyActor)



    def start(self,startInteractor = True):
        # For Scatter plot
        if self.__doScatter:
            polydata = vtk.vtkPolyData()
            polydata.SetPoints(self.__points)
            polydata.SetVerts(self.__vertices)
            vertexFilter = vtk.vtkVertexGlyphFilter()
            vertexFilter.SetInputData(polydata)
            vertexFilter.Update()
            polydataFilter = vertexFilter.GetOutput()
            polydataFilter.GetPointData().SetScalars(self.__pointColors)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(polydataFilter)

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetPointSize(self.__pointSize)
            actor.GetProperty().RenderPointsAsSpheresOn()
            self.addActor(actor)


        # Dispay Polygons
        if self.__doPolygons:
            self.showPolygons()



        # Start vtk Window
        self.__renderWindowInteractor.Initialize()
        self.__rendererWindow.Render()
        if startInteractor:
            self.__renderWindowInteractor.Start()


    def end(self):
        self.__rendererWindow.Finalize()


    def createSampleFunction(self,resolution=100,limits=[-1,1]):
        if self.__sampleFunction == None:
            if not isinstance(resolution,list):
                resolution = [resolution,resolution,resolution]

            if len(limits) == 2:
                limits *= 3

            quadric = vtk.vtkQuadric()
            quadric.SetCoefficients(.5, 1, .2, 0, .1, 0, 0, .2, 0, 0)
            self.__sampleFunction = vtk.vtkSampleFunction()
            self.__sampleFunction.SetSampleDimensions(*resolution)
            self.__sampleFunction.SetModelBounds(*limits)
#            self.__sampleFunction.SetImplicitFunction(quadric)
            self.__sampleFunction.ComputeNormalsOff()

#            print(resolution,limits)

            self.__booleanUnion = vtk.vtkImplicitBoolean()

        else:
            cc.printRed('Sample function already existed!')

    def addBooleanFunction(self,fun):
        if self.__booleanUnion:
            self.__booleanUnion.AddFunction(fun)
        else:
            cc.printRed('Must create sample function before adding boolean function!')

    def plotSampleFunction(self,showOutline=False):
        if self.__sampleFunction:
            extract = vtk.vtkExtractGeometry()
            extract.SetInputConnection(self.__sampleFunction.GetOutputPort())
            extract.SetImplicitFunction(self.__booleanUnion)
            self.__extract = extract
            dataMapper = vtk.vtkDataSetMapper()
            dataMapper.SetInputConnection(extract.GetOutputPort())
            dataActor = vtk.vtkActor()
            dataActor.SetMapper(dataMapper)
            self.addActor(dataActor)

            if showOutline:
                outline = vtk.vtkOutlineFilter()
                outline.SetInputConnection(self.__sampleFunction.GetOutputPort())

                outlineMapper = vtk.vtkPolyDataMapper()
                outlineMapper.SetInputConnection(outline.GetOutputPort())

                outlineActor = vtk.vtkActor()
                outlineActor.SetMapper(outlineMapper)
                outlineActor.GetProperty().SetColor(1, 1, 1)

                self.addActor(outlineActor)


        else:
            cc.printRed('Must create sample function before plotting!')


    def prepareAvi(self,resolution=[1920,1080],fileName='myVideo.avi',frameRate=30):
        self.__rendererWindow.SetSize(*resolution)
        self.__rendererWindow.SetPosition(0,0)
        self.__aviWriter = vtk.vtkAVIWriter()
        self.__windowToImageFilter = vtk.vtkWindowToImageFilter()

        self.__windowToImageFilter.SetInput(self.__rendererWindow)
        self.__aviWriter.SetFileName(fileName)
        self.__aviWriter.SetRate(frameRate)
        self.__aviWriter.SetInputConnection(self.__windowToImageFilter.GetOutputPort())
        self.__aviWriter.Start()


    def recordAvi(self):
        # Dispay Polygons
        if self.__doPolygons:
            self.showPolygons

        if self.__doScatter:
            polydata = vtk.vtkPolyData()
            polydata.SetPoints(self.__points)
            polydata.SetVerts(self.__vertices)
            vertexFilter = vtk.vtkVertexGlyphFilter()
            vertexFilter.SetInputData(polydata)
            vertexFilter.Update()
            polydataFilter = vertexFilter.GetOutput()
            polydataFilter.GetPointData().SetScalars(self.__pointColors)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(polydataFilter)

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetPointSize(20)
            actor.GetProperty().RenderPointsAsSpheresOn()
            self.addActor(actor)


        self.__windowToImageFilter.Modified()
        self.__rendererWindow.Render()
        self.__aviWriter.Write()

    def finishAvi(self):
        self.__aviWriter.End()



    def exportPNG(self,filename='vtkExport'):
        # Source: https://lorensen.github.io/VTKExamples/site/Python/Utilities/Screenshot/

        # Dispay Polygons
        if self.__doPolygons:
            self.showPolygons()




        if self.__doScatter:
            polydata = vtk.vtkPolyData()
            polydata.SetPoints(self.__points)
            polydata.SetVerts(self.__vertices)
            vertexFilter = vtk.vtkVertexGlyphFilter()
            vertexFilter.SetInputData(polydata)
            vertexFilter.Update()
            polydataFilter = vertexFilter.GetOutput()
            polydataFilter.GetPointData().SetScalars(self.__pointColors)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(polydataFilter)

            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            actor.GetProperty().SetPointSize(self.__pointSize)
            actor.GetProperty().RenderPointsAsSpheresOn()
            self.addActor(actor)



        self.__rendererWindow.Render()

        self.__renderer.Modified()

        imageFilter = vtk.vtkWindowToImageFilter()
        imageFilter.SetInput(self.__rendererWindow)
#        imageFilter.SetScale(scale,scale)
#        imageFilter.SetInputBufferTypeToRGBA()
        imageFilter.ReadFrontBufferOff()
        imageFilter.Update()

        writer = vtk.vtkPNGWriter()
        writer.SetFileName(filename+'.png')
        writer.SetInputConnection(imageFilter.GetOutputPort())
        writer.Write()

#        self.start()
#


    def rotation_matrix(self,axis, theta):
        """
        Return the rotation matrix associated with counterclockwise rotation about
        the given axis by theta radians.
        """
        axis = np.asarray(axis)
        axis = axis / math.sqrt(np.dot(axis, axis))
        a = math.cos(theta / 2.0)
        b, c, d = -axis * math.sin(theta / 2.0)
        aa, bb, cc, dd = a * a, b * b, c * c, d * d
        bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
        return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                         [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                         [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])








#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':


    # Create instance of MyVTK
    myVTK = MyVTK()

    if True:
        myVTK.addCoordinateSystem(0.1)
        myVTK.addScatterPoint(0,0,0)
        myVTK.addScatterPoint(0,0,1)
        myVTK.addScatterPoint(0,1,0)
        myVTK.addScatterPoint(0,1,1)
        myVTK.addScatterPoint(1,0,0)
        myVTK.addScatterPoint(1,0,1)
        myVTK.addScatterPoint(1,1,0)
        myVTK.addScatterPoint(1,1,1)
#        myVTK.addText3D(0.5,0.5,0,'A',scale=0.1)
#        myVTK.addText3D(0,0.5,0.5,'B',scale=0.1)
#        myVTK.addText3D(0,0.5,0.5,'B',scale=0.1,extrude=1)
#        myVTK.addText3DNew(0.5,0.5,0,'A',scale=0.1)
        myVTK.addText3DNew(0.3,0.4,0.5,'A',scale=0.1)
        myVTK.addText3DNew(0.3,0.4,0.5,'B',scale=0.1,rotationWXYZ=[90,1,0,0])
        myVTK.addText3DNew(0.3,0.4,0.5,'C',scale=0.1,rotationWXYZ=[90,0,1,0])
        myVTK.addText3DNew(0.3,0.4,0.5,'D',scale=0.1,rotationWXYZ=[90,0,0,1],color=[0,0,1])
        myVTK.start()


    if False:
        # Crate a source
        source = vtk.vtkSphereSource()

        # Add source
        myVTK.addSource(source)


        # Create a function to sample in 3D space
        myVTK.createSampleFunction()

        # Create a sphere to be sampled
        sphere = vtk.vtkSphere()
        sphere.SetRadius(0.5)
        sphere.SetCenter(0,0.5,0.8)

        # Add sphere to sampling
        myVTK.addBooleanFunction(sphere)

        # Plot sampled geometry
        myVTK.plotSampleFunction(True)


        myVTK.start()

    if False:
        # Add some points
        myVTK.addScatterPoint(0,0,0)
        myVTK.addScatterPoint(0,0,1)
        myVTK.addScatterPoint(0,1,0)
        myVTK.addScatterPoint(0,1,1)
        myVTK.addScatterPoint(1,0,0)
        myVTK.addScatterPoint(1,0,1)

        # Add some text
        myVTK.addTextAnnotation(0.5,0.5,0.5,'Center',distToPoint=0)
        myVTK.addTextAnnotation(0,0,0,'Corner')

        # Add points with text
        myVTK.addScatterPoint(1,1,0,'n_0',color=[255,0,0])
        myVTK.addScatterPoint(1,1,1,'n_1',color=[0,255,0])




        n = 60
        xs = np.random.rand(n)
        ys = np.random.rand(n)
        zs = np.random.rand(n)
        for i in range(n):
            myVTK.addScatterPoint(xs[i]+2,ys[i],zs[i],i)

        myVTK.addText3D(0,3,0,'Flat 3D Text',scale=0.1)
        myVTK.addText3D(0,4,0,'Extruded 3D Text',scale=0.1,extrude=0.8)

        myVTK.addTextAnnotation(2.5,1.2,0.5,n)



    if False:


#        vecPoints = point2-point1
#        vecStart = np.array([1,0,0])
#        vecRotation = np.cross(vecPoints,vecStart)
#
#        length = np.linalg.norm(vecPoints)
#
#
#        v1_u = vecPoints / np.linalg.norm(vecPoints)
#        v2_u = vecStart / np.linalg.norm(vecStart)
#        angle = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
#



#
        myVTK.addScatterPoint(0,0,0)
#        myVTK.addScatterPoint(0,0,2)
#        myVTK.addScatterPoint(0,2,0)
#        myVTK.addScatterPoint(2,0,0)





#        numArrows = 8
#        for k in range(10):
#
#            for j in range(numArrows):
#                dir1 = math.cos(math.tau/numArrows*j)
#                dir2 = math.sin(math.tau/numArrows*j)
#
#                point1 = np.array([1,k,0])
#                point2 = np.array([1+dir1,k+dir2,0])
#                myVTK.addArrowStartEnd(point1,point2)
#
#                point3 = np.array([2,k,0])
#                point4 = np.array([2,k+dir1,dir2])
#                myVTK.addArrowStartEnd(point3,point4)
#
#                point5 = np.array([3,k,0])
#                point6 = np.array([3+dir1,k,dir2])
#                myVTK.addArrowStartEnd(point5,point6)


        myVTK.addArrowCenterDirection(center=np.array([3,3,3]),direction=np.array([1,2,3]),color = [1,0,0])
        myVTK.addArrowCenterDirection(center=np.array([3,3,3]),direction=np.array([1,0,0]),color = [1,0,0])
        myVTK.addArrowCenterDirection(center=np.array([3,3,3]),direction=np.array([-1,0,0]),color = [1,0,0])
#        myVTK.addArrowCenterDirection(center=np.array([0,3,3]),direction=np.array([1,2,3]),color = [1,0,0],length=3)




#        myVTK.addLine(np.array([1,1,1]),np.array([3,4,5]))
        myVTK.addPolygon([np.array([0,0,0]),np.array([0,1,0]),np.array([1,0,0])])
        myVTK.addPolygon([np.array([0,0,2]),np.array([2,3,2]),np.array([1,5,2])])


        myVTK.addLine([0,0,0],[1,1,1],color=[0,0,0])

#            myVTK.addScatterPoint(point1[0],point1[1],point1[2],color=[255,0,0])
#            myVTK.addScatterPoint(point2[0],point2[1],point2[2],color=[0,255,0])



#        arrowSource = vtk.vtkArrowSource()
#        arrowSource2 = vtk.vtkArrowSource()
#
#
#        transform = vtk.vtkTransform()
#        transform.Translate(point1)
#        transform.RotateWXYZ(-angle*360/math.tau,vecRotation[0],vecRotation[1],vecRotation[2])
#        transform.Scale(length,length,length)
#
#        transformPD = vtk.vtkTransformPolyDataFilter()
#        transformPD.SetTransform(transform)
#        transformPD.SetInputConnection(arrowSource2.GetOutputPort())
#        arrowSource2.SetLength(2)


    #    arrowSource.SetTipRadius(2)
    #    arrowSource2.SetTipRadius(1)
#        arrowSource.SetShaftRadius(0.01)
#        arrowSource.SetTipLength(.9)

        # Create a mapper and actor
#        mapper = vtk.vtkPolyDataMapper()
#        mapper.SetInputConnection(arrowSource.GetOutputPort())
#        actor = vtk.vtkActor()
#        actor.SetMapper(mapper)
#
#        mapper2 = vtk.vtkPolyDataMapper()
#        mapper2.SetInputConnection(transformPD.GetOutputPort())
#        actor2 = vtk.vtkActor()
#        actor2.SetMapper(mapper2)
#        actor2.SetPosition(point1[0],point1[1],point1[2])
#        actor2.RotateWXYZ(-angle*360/math.tau,vecRotation[0],vecRotation[1],vecRotation[2])



#        myVTK.addActor(actor)
#        myVTK.addActor(actor2)





        # Start visualization
#        myVTK.start()

        myVTK.exportPNG()
        myVTK.renderer.GetActiveCamera().Azimuth(45)
        myVTK.exportPNG()



    # Export as video
    if False:

        myVTK.addPolygon(np.array([[0,0,0],[1,0,0],[0,1,0]]))
        myVTK.showPolygons()
        lookupTable = vtk.vtkLookupTable()
        lookupTable.SetTableRange(0,100)
        lookupTable.Build()

        rgb = [0,0,0]
        myVTK.prepareAvi(fileName='myVTKtestVideo.avi')
        for i in range(100):

            lookupTable.GetColor(i,rgb)
#            colors.append(rgb[:])

            print('Render image {} with color {}'.format(i,rgb))
#            myVTK.actors[0].GetProperty().SetColor(rgb)
#            if i == 50:
#                myVTK.removeActors()

            myVTK.renderer.GetActiveCamera().Azimuth(1)
            myVTK.recordAvi()
        myVTK.finishAvi()
