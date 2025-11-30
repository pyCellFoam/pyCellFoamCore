# -*- coding: utf-8 -*-
#==============================================================================
# SIMULATION OF KELVIN CELLS
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Sep 19 16:16:05 2019

'''


'''
#==============================================================================
#    IMPORTS
#==============================================================================



from grids import Grid3DKelvin
#from grids.grid3DCubic import PrimalComplex3DCubic
from tools import MyLogging
import tools.colorConsole as cc
import tools.placeFigures as pf
import numpy as np
import math
from tools.myVTK import MyVTK
import tools.tumcolor as tc
from complex import DualComplex3D
import scipy.io as io
import scipy.linalg as linalg

with MyLogging('Kelvin Simulation'):
 
    
    
#==============================================================================
#    FUNCTIONS
#==============================================================================      
    
#-------------------------------------------------------------------------
#    Temperature profile of upper boundary
#-------------------------------------------------------------------------      
    def tempBoundary(t):
        return 321.1 * math.exp(-0.000002946 * t) - 35.43 * math.exp(-0.07076 * t)
    
    
    
#==============================================================================
#    SETTINGS
#==============================================================================    
    
    dt = 0.001           # s - Start timestep length
    numSteps = 2000    # Number of timesteps that should be calculated
    maxError = 2e-4     # Maximal relative error for step length control
    maxTime = 200       # Maximal time that should be simulated
    
#==============================================================================
#    MATERIAL PARAMETERS
#==============================================================================     

    rhoS = 2700/1e6     # g/mm^3 for aluminium
    cVS = 8.97          # J / (g K) for aluminium
    laS = 200/1e3       # W / (mm K) for aluminium
    
    rhoF = 1.2041/1e6   # g / mm^3 for air
    cVF = 1.005         # J / (g K) for air
    laF = 0.026/1e3     # W / (mm K) for air
    
    alpha = 100/1e6     # W / (mm^2 K) for air    
    
    radiusEdge = 0.4    # mm
    radiusNode = 0.8    # mm
    
#==============================================================================
#    CREATE COMPLEX
#==============================================================================    
    
    
    # Primal complex: either kelvin cells or cubic cells
    if True:
        c = Grid3DKelvin(1, 
                           borderVolumesLeft = True,
                           borderVolumesRight = True,
                           borderVolumesFront = True,
                           borderVolumesBack=True)
#    else:
#        c = PrimalComplex3DCubic(3,
#                                 borderVolumesFront=True,
#                                 borderVolumesBack=True,
#                                 borderVolumesLeft=True,
#                                 borderVolumesRight=True)
     
        
        
    cc.printBlue('Finished calculating primal Complex')
        
    # Calculate dual complex
    dc = DualComplex3D(c)
    
    
    
    # Use category 2 because the balance volumes are used in the dual complex
    c.useCategory = 2
    
    cc.printBlue('Finished calculating dual Complex')
    
    

#==============================================================================
#    EXTRACT GEOMETRIC DATA
#==============================================================================          
        
    
#-------------------------------------------------------------------------
#    Nodes for measurement
#-------------------------------------------------------------------------    
    
    measurePosition1 = np.array([0,1/2*(c.yMax-c.yMin),1/3*(c.zMax-c.zMin)])
    measurePosition2 = np.array([0,1/2*(c.yMax-c.yMin),2/3*(c.zMax-c.zMin)])
    
    minDist1 = float('infinity')
    minDist2 = float('infinity')
    
    closestNode1 = None
    closestNode2 = None
    
    for n in c.innerNodes:
        distToMeasurePosition1 = np.linalg.norm(measurePosition1-n.coordinates)
        if distToMeasurePosition1 < minDist1:
            minDist1 = distToMeasurePosition1
            closestNode1 = n
        
        distToMeasurePosition2 = np.linalg.norm(measurePosition2-n.coordinates)
        if distToMeasurePosition2 < minDist2:
            minDist2 = distToMeasurePosition2
            closestNode2 = n
        
    print('Nodes for measurement:',closestNode1,closestNode2)
    
    
#-------------------------------------------------------------------------
#    Set radius of nodes and edges
#-------------------------------------------------------------------------     
    
    
    if True:
        
        for e in c.edges:
            e.radius = radiusEdge
        
        for n in c.nodes:
            n.radius = radiusNode
        
        for e in c.additionalBorderEdges:
            e.radius = 0
        for n in c.additionalBorderEdges:
            n.radius = 0
        
        
#-------------------------------------------------------------------------
#    Solid and fluid part of the volumes and contact surface
#-------------------------------------------------------------------------         
        
        
        # Inner volumes
        #--------------------------------------------------
    
        ViSList = []
        ViFList = []
        AiFSList = []
        for v in dc.innerVolumes:
            area = 0
            volTotal = v.volume
            volSolid = v.dualCell3D.sphere.volume
            for e in v.dualCell3D.edges:
                for se in e.simpleEdges:
                    volSolid += se.cylinder.volume/2
                    area += se.cylinder.area
            volFluid = volTotal-volSolid
            ViSList.append(volSolid)
            ViFList.append(volFluid)
            AiFSList.append(area)
        
        AiFS = np.diag(AiFSList)
        AiFSinv = np.diag([1/x for x in AiFSList])
        ViS = np.diag(ViSList)
        ViF = np.diag(ViFList)
        ViSinv = np.diag([1/v for v in ViSList])
        ViFinv = np.diag([1/v for v in ViFList])
        
        
        # Border volumes
        #--------------------------------------------------
        
        VbSList = []
        VbFList = []
        AbFSList = []
        for v in dc.borderVolumes:
            area = 0
            volTotal = v.volume
            volSolid = v.dualCell3D.sphere.volume
            for e in v.dualCell3D.edges:
                for se in e.simpleEdges:
                    volSolid += se.cylinder.volume/2
                    area += se.cylinder.area
            volFluid = volTotal-volSolid
            VbSList.append(volSolid)
            VbFList.append(volFluid)
            AbFSList.append(area)
        AbFS = np.diag(AbFSList) 
        
        AbFS = np.diag(AbFSList)
        VbS = np.diag(VbSList)
        VbF = np.diag(VbFList)
        VbSinv = np.diag([1/v for v in VbSList])
        VbFinv = np.diag([1/v for v in VbFList])
        
        
        # Some statistics
        #--------------------------------------------------
        
        volumeSolid = sum(ViSList) + sum(VbSList)
        volumeFluid = sum(ViFList) + sum(VbFList)
        
        massSolid = volumeSolid * rhoS
        massFluid = volumeSolid * rhoF
        
        
        print('Weight of the foam: {:.3f} g'.format(massSolid))
        print('Weight of the air encapsulated in the foam: {:.3e} g'.format(massFluid))
        
        
        xLen = c.xMax-c.xMin
        yLen = c.yMax-c.yMin
        zLen = c.zMax-c.zMin
        print('Size of the foam: {:.3f} mm × {:.3f} mm × {:.3f} mm'.format(xLen,yLen,zLen))
        
        

#-------------------------------------------------------------------------
#    Solid and fluid part of the faces
#-------------------------------------------------------------------------              
        
        AiSList = []
        AiFList = []
        for f in dc.innerFaces:
            areaTotal = f.area[-1]
            areaSolid = f.dualCell3D.radius**2*1/2*math.tau
            areaFluid = areaTotal - areaSolid
            AiSList.append(areaSolid)
            AiFList.append(areaFluid)
            
        AiS = np.diag(AiSList)
        AiF = np.diag(AiFList)
        AiSinv = np.diag([1/x for x in AiSList])
        AiFinv = np.diag([1/x for x in AiFList])
        
#-------------------------------------------------------------------------
#    Length of the edges
#-------------------------------------------------------------------------          
        
        Liinv = np.diag([1/np.linalg.norm(e.endNode.coordinates - e.startNode.coordinates) for e in c.innerEdges])
            
            
        
        
#==============================================================================
#    SIMULATION
#==============================================================================     
        
        
#-------------------------------------------------------------------------
#    Prepare matrices
#-------------------------------------------------------------------------         
            
        TiS = np.zeros((len(c.innerNodes),numSteps+1))
        TiF = np.zeros((len(c.innerNodes),numSteps+1))   
        TbS = np.zeros((len(c.borderNodes),numSteps+1))
        TbF = np.zeros((len(c.borderNodes),numSteps+1))   
        
        UiS = np.zeros((len(dc.innerVolumes),numSteps+1))
        UiF = np.zeros((len(dc.innerVolumes),numSteps+1))        
        
        
        PhiiS = np.zeros((len(dc.innerFaces),numSteps+1))
        PhiiF = np.zeros((len(dc.innerFaces),numSteps+1))
        
        
        TiS0 = np.ones(len(c.innerNodes)) * tempBoundary(0)
        TiF0 = np.ones(len(c.innerNodes)) * tempBoundary(0)
        
        UiS[:,0] = cVS*rhoS*TiS0 @ ViS
        UiF[:,0] = cVF*rhoF*TiF0 @ ViF
        
        TiS[:,0] = TiS0
        TiF[:,0] = TiF0
        
        boundaryTempBottom = np.zeros(numSteps+1)
        boundaryTempTop = np.zeros(numSteps+1)
    
        time = np.zeros(numSteps+1)
    
    
#-------------------------------------------------------------------------
#    Integrate
#-------------------------------------------------------------------------     
    if True:
        for i in range(numSteps):
            
            
            t = time[i]
            
            if t > maxTime:
                break
            
            cc.printGreenBackground('Calculating timestep {} of {} (t = {:.3f})'.format(i+1,numSteps,t))
            
            t_in = t if t<100 else 100
            boundaryTempTop[i] = tempBoundary(t_in)
            boundaryTempBottom[i] = tempBoundary(0)
            
            for n in c.borderNodes:
                if n.zCoordinate > 0:
                    TbS[n.num,i] = boundaryTempTop[i]
                    TbF[n.num,i] = boundaryTempTop[i]
                    
                else:
                    TbS[n.num,i] = boundaryTempBottom[i]
                    TbF[n.num,i] = boundaryTempBottom[i]
                    
            
            TiSi = 1/(cVS*rhoS)*ViSinv.dot(UiS[:,i])
            TiFi = 1/(cVF*rhoF)*ViFinv.dot(UiF[:,i])
            TbSi = TbS[:,i]
            TbFi = TbF[:,i]
            
            FiS = Liinv @ dc.incidenceMatrix3ii @ TiSi + Liinv @ dc.incidenceMatrix3ib @ TbSi
            FiF = Liinv @ dc.incidenceMatrix3ii @ TiFi + Liinv @ dc.incidenceMatrix3ib @ TbFi
            FiSF = TiFi-TiSi
            
            PhiiSi = laS*AiS @ FiS
            PhiiFi = laF*AiF @ FiF
            PhiiSFi = alpha * AiFS @ FiSF
            
            UdotS = -dc.incidenceMatrix3ii.transpose().dot(PhiiSi) + PhiiSFi # + dc.incidenceMatrix3bi.transpose() @ u
            UdotF = -dc.incidenceMatrix3ii.transpose().dot(PhiiFi) - PhiiSFi # + dc.incidenceMatrix3bi.transpose() @ u
            
            
            TiS[:,i+1] = TiSi
            TiF[:,i+1] = TiFi
            
            PhiiS[:,i] = PhiiSi
            PhiiF[:,i] = PhiiFi
            
            
            dt = 2*dt
            count = 0
            countLimit = 50
            error = maxError*10
            
            
            # Step length control
            #--------------------------------------------------
            while count < countLimit and error > maxError:
                count += 1
                
                UiS1 = UiS[:,i]+UdotS*dt
                UiF1 = UiF[:,i]+UdotF*dt
                UiS2 = UiS[:,i]+UdotS*dt*2
                UiF2 = UiF[:,i]+UdotF*dt*2
                
                
                absError = np.linalg.norm(np.absolute(UiS1-UiS2))
                relError = absError/np.linalg.norm(np.absolute(UiS1))
                error = relError
                
                cc.printGreen(' \tIteration {:2.0f}:\tdt = {:.4f}\trelErr = {:6.3f} %\tabsErr = {:.3f}'.format(count,dt,error*100,absError))
                if error > maxError:
                    dt = dt/2
                    
                    
            if count >= countLimit:
                break
                cc.printRed('ERROR: cannot find suitable step length')
            
            UiS[:,i+1] = UiS[:,i]+UdotS*dt
            UiF[:,i+1] = UiF[:,i]+UdotF*dt
            time[i+1] = time[i] + dt
         
            
            
            
        for j in range(i,numSteps+1):
            boundaryTempTop[j] = 321.1 * math.exp(-0.000002946 * t_in) - 35.43 * math.exp(-0.07076 * t_in)
            boundaryTempBottom[j] = 321.1 * math.exp(-0.000002946 * 0) - 35.43 * math.exp(-0.07076 * 0)
            
            for n in c.borderNodes:
                if n.zCoordinate > 0:
                    TbS[n.num,j] = boundaryTempTop[j]
                    TbF[n.num,j] = boundaryTempTop[j]
                    
                else:
                    TbS[n.num,j] = boundaryTempBottom[j]
                    TbF[n.num,j] = boundaryTempBottom[j]
            
            


#==============================================================================
#    VISUALIZATION
#==============================================================================     

#-------------------------------------------------------------------------
#    Complex with pyplot 
#-------------------------------------------------------------------------  

    if False:
        axNum = -1
        (figs,axes) = pf.getFigures()
        
        axNum += 1
        c.plotEdges(axes[axNum],showLabel=False,showArrow=False)
        pf.exportPNG(figs[0])
        
        axNum += 1
        for f in dc.borderFaces:
            f.plotFace(axes[axNum],showLabel=False,showNormalVec=False)
            
        axNum += 1
        for f in dc.innerFaces:
            f.plotFace(axes[axNum],showLabel=False,showNormalVec=False,showBarycenter=False)
        for n in c.borderNodes:
            n.plotNode(axes[axNum],showLabel=False)
        for e in c.innerEdges:
            e.plotEdge(axes[axNum],showLabel=False,showArrow=False)
    else:
        pf.closeFigures()
        
  

#-------------------------------------------------------------------------
#    Complex with VTK 
#------------------------------------------------------------------------- 
        
    if False:
        
        myVtk = c.plotComplexVTK(plotNodes=False,plotEdges=True,plotFaces=True,showArrow=False,backgroundColor=tc.TUMWhite())
        
#        myVtk.addCoordinateSystem(2)
        
        focalX = (c.xlim[0] + c.xlim[1])/2
        focalY = (c.ylim[0] + c.ylim[1])/2
        focalZ = (c.zlim[0] + c.zlim[1])/2
        
        myVtk.renderer.GetActiveCamera().SetFocalPoint(focalX,focalY,focalZ)
        myVtk.renderer.GetActiveCamera().SetPosition(0,0,140)
        
        myVtk.renderer.GetActiveCamera().Roll(120)
        myVtk.renderer.GetActiveCamera().Elevation(-70)
        myVtk.renderer.GetActiveCamera().Roll(-10)
        
#        myVtk.start()  
        myVtk.exportPNG('exampleCells')

#-------------------------------------------------------------------------
#    Dual Complex with VTK 
#------------------------------------------------------------------------- 
        
    if False:
        
        myVtk = dc.plotComplexVTK(plotNodes=False,plotEdges=True,plotFaces=True,showArrow=False,backgroundColor=tc.TUMWhite())
        
#        myVtk.addCoordinateSystem(2)
        
        focalX = (c.xlim[0] + c.xlim[1])/2
        focalY = (c.ylim[0] + c.ylim[1])/2
        focalZ = (c.zlim[0] + c.zlim[1])/2
        
        myVtk.renderer.GetActiveCamera().SetFocalPoint(focalX,focalY,focalZ)
        myVtk.renderer.GetActiveCamera().SetPosition(0,0,50)
        
        myVtk.renderer.GetActiveCamera().Roll(120)
        myVtk.renderer.GetActiveCamera().Elevation(-70)
        myVtk.renderer.GetActiveCamera().Roll(-10)
        
        myVtk.start()        
        
        
        
    if False:
        myVtk = MyVTK()
        for e in c.innerEdges:
            for se in e.simpleEdges:
                myVtk.addActor(se.cylinder.vtkActor)
        myVtk.start()   
        
#-------------------------------------------------------------------------
#    Complex and flows with VTK 
#-------------------------------------------------------------------------         
        
    if False:
        
        myVtk = c.plotComplexVTK(plotNodes=False,plotEdges=True,plotFaces=False,showArrow=False,edgeColor=tc.TUMGrayMedium(),pointSize = 50,backgroundColor = tc.TUMWhite())
        timeStep = 999
#            
        maxL = max(np.abs(PhiiS[:,timeStep]))
        print(maxL)
        for f in dc.innerFaces:
            f.plotFlowVtk(myVtk,PhiiS[f.num,timeStep]/maxL*3,color=tc.TUMGreen().rgb01)
#            print(l)
            
            
            
        color1 = np.array(tc.TUMBlue().rgb0255)
        color2 = np.array(tc.TUMRose().rgb0255)
        
        
        maxTemp = TbS.max()
        minTemp = TbS.min()            
        
        
        for n in c.borderNodes:
            temperature = TbS[n.num,timeStep]
            color = (color2-color1)/(maxTemp-minTemp)*(temperature-minTemp)+color1
            n.plotNodeVtk(myVtk,showLabel=False,color=color)
            print(temperature)
            
        for n in c.innerNodes:
            temperature = TiS[n.num,timeStep]
            color = (color2-color1)/(maxTemp-minTemp)*(temperature-minTemp)+color1
            n.plotNodeVtk(myVtk,showLabel=False,color=color)
        
#            
#       
        
        focalX = (c.xlim[0] + c.xlim[1])/2
        focalY = (c.ylim[0] + c.ylim[1])/2
        focalZ = (c.zlim[0] + c.zlim[1])/2
        
        myVtk.renderer.GetActiveCamera().SetFocalPoint(focalX,focalY,focalZ)
        myVtk.renderer.GetActiveCamera().SetPosition(0,0,100)
#        
        myVtk.renderer.GetActiveCamera().Roll(120)
        myVtk.renderer.GetActiveCamera().Elevation(-70)
        myVtk.renderer.GetActiveCamera().Roll(-10)
        
#        myVtk.exportPNG()
        
        myVtk.start()        
        
        
        
        
    if False:
        
        myVtk = MyVTK()
        
        for f in dc.innerFaces:
            f.plotFaceVtk(myVtk)
        
        for n in c.nodes:
            n.plotNodeVtk(myVtk,showLabel=False)
#        for f in dc.innerFaces:
#            f.plotFaceVtk(myVtk)
            
        for e in c.edges:
            e.plotEdgeVtk(myVtk,showLabel=False)
#        for n in c.innerNodes:
#            n.plotNodeVtk(myVtk,showLabel=False)
#        for e in c.innerEdges:
#            e.plotEdgeVtk(myVtk,showLabel=False)
#        maxL = max(PhiiS[:,0])
#        for f in dc.innerFaces:
#            f.plotFlowVtk(myVtk,PhiiS[f.num,0]/maxL)
#            print(l)
#        myVtk.start()  

        myVtk.renderer.GetActiveCamera().SetPosition(0,0,50)
        myVtk.renderer.GetActiveCamera().Roll(120)
        myVtk.renderer.GetActiveCamera().Elevation(-70)
        myVtk.renderer.GetActiveCamera().Roll(-5)
            
        myVtk.start()
        
        
    if False:
        myVtk = MyVTK()
        
        color1 = np.array(tc.TUMBlue().rgb0255)
        color2 = np.array(tc.TUMRose().rgb0255)
        
        
        maxTemp = TbS.max()
        minTemp = TbS.min()
        
        
        
        
        
        
        
        for n in c.borderNodes:
            temperature = TbS[n.num,-1]
            color = (color2-color1)/(maxTemp-minTemp)*(temperature-minTemp)+color1
            n.plotNodeVtk(myVtk,showLabel=False,color=color)
            
            
        myVtk.start()            
        
#        for f in dc.innerFaces:
            
        
        
        
    if False:
        myVTK = dc.plotComplexVTK(plotNodes=True,plotEdges=True,plotFaces=False,showArrow=False)
        myVTK.addCoordinateSystem(5)
        
        
        focalX = (c.xlim[0] + c.xlim[1])/2
        focalY = (c.ylim[0] + c.ylim[1])/2
        focalZ = (c.zlim[0] + c.zlim[1])/2
        
        myVTK.prepareAvi(fileName='KelvinVTKRotation.avi')
        myVTK.renderer.GetActiveCamera().SetPosition(0,0,100)
        myVTK.renderer.GetActiveCamera().SetFocalPoint(focalX,focalY,focalZ)
        
        myVtk.renderer.GetActiveCamera().SetPosition(0,0,50)
        myVtk.renderer.GetActiveCamera().Roll(120)
        myVtk.renderer.GetActiveCamera().Elevation(-70)
        myVtk.renderer.GetActiveCamera().Roll(-5)

            
        for i in range(120):
            myVTK.renderer.GetActiveCamera().Roll(1)
            print('Render image {} '.format(i))
            myVTK.recordAvi()
            
            
        for i in range(70):
            myVTK.renderer.GetActiveCamera().Elevation(-1)
            print('Render image {} '.format(i))
            myVTK.recordAvi()  
            
        for i in range(5):
            myVTK.renderer.GetActiveCamera().Roll(-1)
            print('Render image {} '.format(i))
            myVTK.recordAvi()            
            
        myVTK.finishAvi()
        
        
        
    if False:
        myVtk = MyVTK()
        
        color1 = np.array(tc.TUMBlue().rgb0255)
        color2 = np.array(tc.TUMRose().rgb0255)
        
        maxTemp = TbS.max()
        minTemp = TbS.min()
        
        focalX = (c.xMin + c.xMax)/2
        focalY = (c.yMin + c.yMax)/2
        focalZ = (c.zMin + c.zMax)/2
        
        
        
        myVtk.prepareAvi(fileName='KelvinVTK.avi')
        myVtk.renderer.GetActiveCamera().SetFocalPoint(focalX,focalY,focalZ)
        myVtk.renderer.GetActiveCamera().SetPosition(0,0,100)
        myVtk.renderer.GetActiveCamera().Roll(120)
        myVtk.renderer.GetActiveCamera().Elevation(-70)
        myVtk.renderer.GetActiveCamera().Roll(-5)
       
        
        numberOfImages = 300
        
        maxL = np.abs(PhiiS).max()
        print(maxL)
        
        for i in range(0,len(time),int(len(time)/numberOfImages)):
            print('Render timestep {} of {}'.format(i,len(time)))
            
            myVtk.removeActors()
            c.plotComplexVTK(oldVTK = myVtk, plotNodes=False,plotEdges=True,plotFaces=False,showArrow=False,edgeColor=tc.TUMGrayMedium(),pointSize = 50,backgroundColor = tc.TUMWhite())
            timeStep = i
    #            
            
            for f in dc.innerFaces:
                f.plotFlowVtk(myVtk,PhiiS[f.num,timeStep]/maxL*3,color=tc.TUMGreen().rgb01)
    #            print(l)
                
            
            
            for n in c.borderNodes:
                temperature = TbS[n.num,timeStep]
                color = (color2-color1)/(maxTemp-minTemp)*(temperature-minTemp)+color1
                n.plotNodeVtk(myVtk,showLabel=False,color=color)
#                print(temperature)
                
            for n in c.innerNodes:
                temperature = TiS[n.num,timeStep]
                color = (color2-color1)/(maxTemp-minTemp)*(temperature-minTemp)+color1
                n.plotNodeVtk(myVtk,showLabel=False,color=color)
    #            
            myVtk.recordAvi()
            
            

        myVtk.finishAvi()
        
        
        
    if True:
        (figs,axes) = pf.getFigures(aspect3D=False)
        
        TiSNode1 = TiS[closestNode1.num,:]
        TiSNode2 = TiS[closestNode2.num,:]
        
        
        exportComment = 'Weight of the foam: {:.3f} g \n'.format(massSolid)
        exportComment += 'Weight of the air encapsulated in the foam: {:.3e} g\n'.format(massFluid)
        exportComment += 'Size of the foam (x × y × z): {:.3f} mm × {:.3f} mm × {:.3f} mm\n'.format(xLen,yLen,zLen)
        exportComment += 'All measurements at x = 0 mm and y = {:.2f} mm\n'.format(yLen/2)
        exportComment += 'Columns:\n'
        exportComment += 'time [s] ; T0 (z = 0 mm) [K] ; T1 (z = {:.3f} mm) [K] ; T2 (z = {:.3f} mm) [K] ; T3 (z = {:.3f} mm) [K]\n'.format(closestNode1.zCoordinate-c.zMin,closestNode2.zCoordinate-c.zMin,zLen)
        exportComment += '''
#            +--------------+
#           /              /|
#          /              / |
#         /              /  |
#        /              /   |
#       /              /    |
#      +--------------+     |
#      |              |     |
#      |              |     |
#      |              |     |
#      |              |    /
#      |              |   / 
#  z   |              |  /   y
#  ^   |              | /   ^
#  |   |              |/   /
#  |   +--------------+   /
#      
#      ---> x'''
        
        
        
        exportTable = np.vstack((time,boundaryTempBottom,TiSNode1,TiSNode2,boundaryTempTop))
        
        
        np.savetxt('SimulationKelvin.txt',exportTable.transpose(),header = exportComment,delimiter=';',encoding='utf-8')
        
        
        axes[0].plot(time,boundaryTempBottom,
                     time,TiSNode1,
                     time,TiSNode2,
                     time,boundaryTempTop)
        
        
        legendText0 = 'T0 (0 mm)'
        legendText1 = 'T1 ({:.3f} mm)'.format(closestNode1.zCoordinate-c.zMin)
        legendText2 = 'T2 ({:.3f} mm)'.format(closestNode2.zCoordinate-c.zMax)
        legendText3 = 'T3 ({:.3f} mm)'.format(zLen)
        
        axes[0].legend((legendText0,legendText1,legendText2,legendText3))
        pf.exportPNG(figs[0],'Kelvin2')
#        axes[0].legend(('A','B'))
        
        
#        axes[0].plot(np.arange(0,totalTime+dt,dt),TbS.transpose())
#        axes[1].plot(np.arange(0,totalTime+dt,dt),TiS.transpose())
#        axes[2].plot(np.arange(0,totalTime+dt,dt),TbF.transpose())
#        axes[3].plot(np.arange(0,totalTime+dt,dt),TiF.transpose())
#        axes[4].plot(np.arange(0,totalTime+dt,dt),UiS.transpose())

    
    
    if True:
        J1 = np.concatenate((np.zeros((len(dc.innerVolumes),len(dc.innerVolumes))),
                             np.zeros((len(dc.innerVolumes),len(dc.innerVolumes))),
                             -dc.incidenceMatrix3ii.transpose(),
                             np.zeros((len(dc.innerVolumes),len(c.innerEdges))),
                             np.eye(len(dc.innerVolumes))),
            axis=1)
        J2 = np.concatenate((np.zeros((len(dc.innerVolumes),len(dc.innerVolumes))),
                             np.zeros((len(dc.innerVolumes),len(dc.innerVolumes))),
                             np.zeros((len(dc.innerVolumes),len(c.innerEdges))),
                             -dc.incidenceMatrix3ii.transpose(),
                             -np.eye(len(dc.innerVolumes))),
            axis=1)
        J3 = np.concatenate((dc.incidenceMatrix3ii,
                             np.zeros((len(c.innerEdges),len(dc.innerVolumes))),
                             np.zeros((len(c.innerEdges),len(c.innerEdges))),
                             np.zeros((len(c.innerEdges),len(c.innerEdges))),
                             np.zeros((len(c.innerEdges),len(dc.innerVolumes)))),
            axis=1)
        J4 = np.concatenate((np.zeros((len(c.innerEdges),len(dc.innerVolumes))),
                             dc.incidenceMatrix3ii,
                             np.zeros((len(c.innerEdges),len(c.innerEdges))),
                             np.zeros((len(c.innerEdges),len(c.innerEdges))),
                             np.zeros((len(c.innerEdges),len(dc.innerVolumes)))),
            axis=1)
        J5 = np.concatenate((np.eye(len(dc.innerVolumes)),
                             -np.eye(len(dc.innerVolumes)),
                             np.zeros((len(dc.innerVolumes),len(c.innerEdges))),
                             np.zeros((len(dc.innerVolumes),len(c.innerEdges))),
                             np.zeros((len(dc.innerVolumes),len(dc.innerVolumes)))),
            axis=1)
            
        J = np.concatenate((J1,J2,J3,J4,J5))
        
        CS = 1/(cVS*rhoS)*ViSinv
        CF = 1/(cVF*rhoF)*ViFinv
        LambdaS = laS*AiS
        LambdaF = laF*AiF
        AlphaFS = alpha * AiFS
        
#        Q = np.diag(np.diag(CS),np.diag(CF),np.diag(LambdaS),np.diag(LambdaF),np.diag(AlphaFS))
        Q = linalg.block_diag(CS,CF,LambdaS,LambdaF,AlphaFS)
        
        CS_R = np.zeros(CS.shape)
        CF_R = np.zeros(CF.shape)
        LambdaS_R = 1/laS*AiSinv
        LambdaF_R = 1/laF*AiFinv
        AlphaFS_R = 1/alpha * AiFSinv        
        
        R = linalg.block_diag(CS_R,CF_R,LambdaS_R,LambdaF_R,AlphaFS_R)
        
        
        
        
        
        G1 = np.concatenate((np.zeros((len(dc.innerVolumes),len(dc.borderVolumes))),
                             np.zeros((len(dc.innerVolumes),len(dc.borderVolumes)))),
            axis=1)
        G2 = np.concatenate((np.zeros((len(dc.innerVolumes),len(dc.borderVolumes))),
                             np.zeros((len(dc.innerVolumes),len(dc.borderVolumes)))),
            axis=1)

        G3 = np.concatenate((dc.incidenceMatrix3ib,
                             np.zeros((len(c.innerEdges),len(dc.borderVolumes)))),
            axis=1)            
            
        G4 = np.concatenate((np.zeros((len(c.innerEdges),len(dc.borderVolumes))),
                             dc.incidenceMatrix3ib),
            axis=1)            

        G5 = np.concatenate((np.zeros((len(dc.innerVolumes),len(dc.borderVolumes))),
                             np.zeros((len(dc.innerVolumes),len(dc.borderVolumes)))),
            axis=1) 

        G_Large = np.concatenate((G1,G2,G3,G4,G5))
        
        
        
        
        boundaryTop = np.zeros(len(c.borderNodes))
        boundaryBottom = np.zeros(len(c.borderNodes))
        
        for n in c.borderNodes:
            if n.zCoordinate > 0:
                boundaryTop[n.num] = 1
                
            else:
                boundaryBottom[n.num] = 1
                
                
        
        G_Red1 = np.zeros((len(dc.innerVolumes),2))
        G_Red2 = np.zeros((len(dc.innerVolumes),2))
        
        G_Red3 = np.column_stack((dc.incidenceMatrix3ib @ boundaryTop,dc.incidenceMatrix3ib @ boundaryBottom))
        G_Red4 = np.column_stack((dc.incidenceMatrix3ib @ boundaryTop,dc.incidenceMatrix3ib @ boundaryBottom))
        G_Red5 = np.zeros((len(dc.innerVolumes),2))
        
        G_Small = np.concatenate((G_Red1,G_Red2,G_Red3,G_Red4,G_Red5))
        
        
        
        
        
        
        
        
        E11 = np.eye(2*len(dc.innerVolumes))
        E12 = np.zeros((2*len(dc.innerVolumes),2*len(c.innerEdges)+len(dc.innerVolumes)))
        E1 = np.concatenate((E11,E12),axis=1)
        E21 = np.zeros((2*len(c.innerEdges)+len(dc.innerVolumes),2*len(dc.innerVolumes)))
        E22 = np.zeros((2*len(c.innerEdges)+len(dc.innerVolumes),2*len(c.innerEdges)+len(dc.innerVolumes)))
        E2 = np.concatenate((E21,E22),axis=1)
        
        E = np.concatenate((E1,E2))
        
        
        
        io.savemat('Kelvin.mat', dict(J=J,Q=Q,R=R,G_Small=G_Small,G_Large=G_Large,E=E))

        
        
        
        
#        J = np.concatenate(np.zeros(len(c.innerVolumes),len(c.innerVolumes)),np.zeros(len(c.innerVolumes),len(c.innerVolumes)))
        
    