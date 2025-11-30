# -*- coding: utf-8 -*-

# =============================================================================
# NAME
# =============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     2025-11-30

# =============================================================================
#    IMPORTS
# =============================================================================

# ------------------------------------------------------------------------
#    Standard Libraries
# ------------------------------------------------------------------------
import logging
import math
import pickle

# ------------------------------------------------------------------------
#    Third-Party Libraries
# ------------------------------------------------------------------------
import numpy as np
from plotly import graph_objects as go

# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------

#    k-Cells
# -------------------------------------------------------------------

#    Complex
# -------------------------------------------------------------------
from pyCellFoamCore.complex.primalComplex3D import PrimalComplex3D
from pyCellFoamCore.complex.dualComplex3D import DualComplex3D

#    Grids
# -------------------------------------------------------------------
from pyCellFoamCore.grids.roi2_modified import get_k_cells

#    Bounding Box
# -------------------------------------------------------------------

#    Tools
# -------------------------------------------------------------------
from pyCellFoamCore.tools.logging_formatter import set_logging_format
from pyCellFoamCore.tools.myVTK import MyVTK
import pyCellFoamCore.tools.tumcolor as tc

# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)

set_logging_format(logging.INFO)

# ==============================================================================
#    SETTINGS
# ==============================================================================

dt = 0.001           # s - Start timestep length
numSteps = 8000      # Number of timesteps that should be calculated
maxError = 2e-5     # Maximal relative error for step length control
maxTime = 200       # Maximal time that should be simulated

# ==============================================================================
#    MATERIAL PARAMETERS
# ==============================================================================

rhoS = 2700/1e6     # g/mm^3 for aluminium
cVS = 8.97          # J / (g K) for aluminium
laS = 200/1e3       # W / (mm K) for aluminium

rhoF = 1.2041/1e6   # g / mm^3 for air
cVF = 1.005         # J / (g K) for air
laF = 0.026/1e3     # W / (mm K) for air

alpha = 100/1e6     # W / (mm^2 K) for air

radiusEdge = 0.4    # mm
radiusNode = 0.8    # mm




# =============================================================================
#    CREATE COMPLEX
# =============================================================================

(nodes, edges, faces, volumes) = get_k_cells()
_log.info("k-cells loaded.")

pc = PrimalComplex3D(nodes, edges, faces, volumes)
dc = DualComplex3D(pc)

_log.info("Primal and dual complex created.")

# =============================================================================
#    EXTRACT GEOMETRIC DATA
# =============================================================================

# ------------------------------------------------------------------------
#    Set radius of nodes and edges
# ------------------------------------------------------------------------



for e in pc.edges:
    e.radius = radiusEdge

for n in pc.nodes:
    n.radius = radiusNode

for e in pc.additionalBorderEdges:
    e.radius = 0
for n in pc.additionalBorderEdges:
    n.radius = 0

_log.info("Radii of edges and nodes set.")


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
    volSolid = v.dualCell3D.sphere_volume
    for e in v.dualCell3D.edges:
        for se in e.simpleEdges:
            volSolid += se.cylinder_volume/2
            area += se.cylinder_surface_area/2
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
    volSolid = v.dualCell3D.sphere_volume
    for e in v.dualCell3D.edges:
        for se in e.simpleEdges:
            volSolid += se.cylinder_volume/2
            area += se.cylinder_surface_area/2
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


xLen = pc.xMax-pc.xMin
yLen = pc.yMax-pc.yMin
zLen = pc.zMax-pc.zMin
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

Liinv = np.diag([1/np.linalg.norm(e.endNode.coordinates - e.startNode.coordinates) for e in pc.innerEdges])


#==============================================================================
#    SIMULATION
#==============================================================================


#-------------------------------------------------------------------------
#    Prepare matrices
#-------------------------------------------------------------------------

TiS = np.zeros((len(pc.innerNodes),numSteps+1))
TiF = np.zeros((len(pc.innerNodes),numSteps+1))
TbS = np.zeros((len(pc.borderNodes),numSteps+1))
TbF = np.zeros((len(pc.borderNodes),numSteps+1))

UiS = np.zeros((len(dc.innerVolumes),numSteps+1))
UiF = np.zeros((len(dc.innerVolumes),numSteps+1))


PhiiS = np.zeros((len(dc.innerFaces),numSteps+1))
PhiiF = np.zeros((len(dc.innerFaces),numSteps+1))


TiS0 = np.ones(len(pc.innerNodes)) * 293.15  # K
TiF0 = np.ones(len(pc.innerNodes)) * 293.15  # K

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
for i in range(numSteps):


    t = time[i]

    if t > maxTime:
        break

    _log.critical('Calculating timestep {} of {} (t = {:.3f})'.format(i+1,numSteps,t))


    for n in pc.borderNodes:
        TbS[n.num,i] = 323.15  # K
        TbF[n.num,i] = 323.15  # K

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

        _log.info(' \tIteration {:2.0f}:\tdt = {:.4f}\trelErr = {:6.3f} %\tabsErr = {:.3f}'.format(count,dt,error*100,absError))
        if error > maxError:
            dt = dt/2


    if count >= countLimit:
        _log.error('ERROR: cannot find suitable step length')
        break

    UiS[:,i+1] = UiS[:,i]+UdotS*dt
    UiF[:,i+1] = UiF[:,i]+UdotF*dt
    time[i+1] = time[i] + dt

fig = go.Figure()
for i in range(len(pc.innerNodes)):
    fig.add_trace(go.Scatter(x=time[:-1], y=TiS[i,:-1], mode='lines', name=f'Inner Solid Temperature Node {i}'))
for i in range(len(pc.borderNodes)):
    fig.add_trace(go.Scatter(x=time[:-1], y=TbS[i,:-1], mode='lines', name=f'Border Solid Temperature Node {i}'))


fig.update_layout(
    title='Temperature Evolution in Solid Phase over Time',
    xaxis_title='Time (s)',
    yaxis_title='Temperature (K)',
    showlegend=False
)
fig.show()

with open('simulation_roi2_results.pkl', 'wb') as f:
    pickle.dump({
        'time': time,
        'TiS': TiS,
        'TiF': TiF,
        'TbS': TbS,
        'TbF': TbF,
        'UiS': UiS,
        'UiF': UiF,
        'PhiiS': PhiiS,
        'PhiiF': PhiiF
    }, f)


# for j in range(i,numSteps+1):
#     # boundaryTempTop[j] = 321.1 * math.exp(-0.000002946 * t_in) - 35.43 * math.exp(-0.07076 * t_in)
#     # boundaryTempBottom[j] = 321.1 * math.exp(-0.000002946 * 0) - 35.43 * math.exp(-0.07076 * 0)

#     for n in c.borderNodes:
#         if n.zCoordinate > 0:
#             TbS[n.num,j] = boundaryTempTop[j]
#             TbF[n.num,j] = boundaryTempTop[j]

#         else:
#             TbS[n.num,j] = boundaryTempBottom[j]
#             TbF[n.num,j] = boundaryTempBottom[j]
