# -*- coding: utf-8 -*-
#==============================================================================
# PLACE FIGURES
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu May 24 14:22:01 2018


'''
Installation
--------------------------------------------------------------------------

1.  Install the ffmpeg movie writer:
    https://www.wikihow.com/Install-FFmpeg-on-Windows
2.  Choose Qt5 Backend to display interactable windows instead of showing 
    the plot inline:
    Tools --> Preferences --> IPython console --> Graphics --> Backend --> Qt5






'''
import os
if __name__ == '__main__':
    os.chdir('../')

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tools.colorConsole as cc
import math
import numpy as np



def getFigures(numFigHorizontal=0,numFigVertical=0,numTotal=6,aspect3D=True):
    plt.switch_backend("Qt5Agg")
    try:
        import localConfig
        pyplotWindowSize = localConfig.pyplotWindowSize
        pyplotTopLeftCorner = localConfig.pyplotTopLeftCorner
        try:
            pyplotPortrait = localConfig.pyplotPortrait
        except:
            pyplotPortrait = False
            cc.printRe('Portrait mode not defined. Using standard landscape mode')
    except:
        pyplotPortrait = False
        pyplotWindowSize = (1920,1080)
        pyplotTopLeftCorner = (0,0)
        cc.printRed('place Figures: No local configuration file found, using standard')
    
    if numTotal > 0:
        cc.printYellow('Portrait mode: {}'.format(pyplotPortrait))
        if pyplotPortrait:
            numFigHorizontal = math.floor(math.sqrt(numTotal));
            numFigVertical = math.ceil(numTotal/numFigHorizontal);
            cc.printYellow('Portraid mode activated')
        else:
            numFigVertical = math.floor(math.sqrt(numTotal));
            numFigHorizontal = math.ceil(numTotal/numFigVertical);

    # Close old windows
    plt.close('all')
    
    xRes = pyplotWindowSize[0]
    yRes = pyplotWindowSize[1]
    
    # Create 2-dimensional list with all figures
    figuresXY = ([([plt.figure() for _ in range(numFigHorizontal)]) for _ in range(numFigVertical)])    
    for i,row in enumerate(figuresXY):
        width = xRes//numFigHorizontal
        height = yRes//numFigVertical
        for j,fig in enumerate(row):
            
            xPos = xRes//numFigHorizontal*j+pyplotTopLeftCorner[0]
#            if moveLeft:
#                xPos -= xRes
            yPos = yRes//numFigVertical*i+pyplotTopLeftCorner[1]
            
            mngr = fig.canvas.manager
            mngr.window.setGeometry(xPos,yPos,width,height)  
            
        
    # create list with all figures and axes
    figs = []
    axes = []
    for x in figuresXY:
        for y in x:
            figs.append(y)
            if aspect3D:
                axes.append(Axes3D(y))
            else:
                axes.append(y.add_subplot(111))
          
    if aspect3D:
        for ax in axes:
            ax.set_proj_type('ortho')
            ax.view_init(azim = 135 ,elev = 20)
            
    return (figs,axes)
 

def setAxesEqual(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])
    
    
def copylimits(fromax,toax):
    toax.set_xlim3d(fromax.get_xlim3d())
    toax.set_ylim3d(fromax.get_ylim3d())
    toax.set_zlim3d(fromax.get_zlim3d())
    
    
def setLabels(ax,x='x',y='y',z='z'):
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_zlabel(z)
    
def returnTo2D(fig):
    fig.clf()
    ax = fig.add_subplot(111)
    return ax

def mm2inch(mm):
    MM_PER_INCH = 25.4
    return mm/MM_PER_INCH
    

def exportPNG(fig,filename = 'export',width_mm = 120, height_mm = 100, dpi=300):
    if '/' in filename:
        folders = filename.split('/')
        path = ''
        for f in folders[:-1]:
            path += f
            if not os.path.isdir(path):
                os.mkdir(path)
            path += '/'
        
    plt.figure(fig.number)
    handle = plt.gcf()
    handle.set_size_inches(mm2inch(width_mm),mm2inch(height_mm))
    plt.savefig(filename,dpi=dpi,transparent=True)        
    
    
    

def getVideo(title='My excellent animation',
             artist='Tobias Scheuermann',
             comment='Tobias Scheuermann\r\n\r\nE-Mail:\r\ntobias.scheuermann@tum.de\r\n\r\nTechnical University of Munich\r\nFaculty of Mechanical Engineering\r\nChair of Automatic Control',
             aspect3D = True,
             fps = 15):
    import matplotlib.animation as manimation
    import datetime
    today = datetime.date.today()
    FFMpegWriter = manimation.writers['ffmpeg']
    metadata = dict(title=title, 
                    artist=artist,
                    comment=comment,
                    date=str(today))
    writer = FFMpegWriter(fps=fps, metadata=metadata)
    
    fig = plt.figure(figsize=(16, 9), dpi=120)
    if aspect3D:
        ax = Axes3D(fig)
    else:
        ax = fig.add_subplot(111)
    
    
    plt.switch_backend("Agg")
    return(fig,ax,writer)
    
    
def getVideo2(title='My excellent animation',
             artist='Tobias Scheuermann',
             comment='Tobias Scheuermann\r\n\r\nE-Mail:\r\ntobias.scheuermann@tum.de\r\n\r\nTechnical University of Munich\r\nFaculty of Mechanical Engineering\r\nChair of Automatic Control',
             fps = 15):
    import matplotlib.animation as manimation
    import datetime
    today = datetime.date.today()
    FFMpegWriter = manimation.writers['ffmpeg']
    metadata = dict(title=title, 
                    artist=artist,
                    comment=comment,
                    date=str(today))
    writer = FFMpegWriter(fps=fps, metadata=metadata)
    
    fig = plt.figure(figsize=(16, 9), dpi=120)
    ax1 = fig.add_subplot(1,2,1,projection='3d')
    ax2 = fig.add_subplot(1,2,2)
    
    
    plt.switch_backend("Agg")
    return(fig,[ax1,ax2],writer)    
    
    
    
def closeFigures():
    plt.close('all')
    
if __name__ == '__main__':
    (fig,ax) = getFigures()
    
    if False:
        exportPNG(fig[0],'testExport/test')
        exportPNG(fig[1],'testExport2/testExport3/testExport4/testExport5/test')
        
    
    
    if False:
    
        (fig,ax,writer) = getVideo(title = 'Example',aspect3D = False,fps=60)
        x = np.arange(0,math.tau,0.1)
        t = np.arange(0,math.tau,1/60)
        numSteps = len(t)
        with writer.saving(fig,'exampleVideo.mp4',120):
            for (i,now) in enumerate(t):
                y = math.sin(now)*np.sin(x)
                print('Visualizing timestep {} of {}'.format(i+1,numSteps))
                ax.clear()
                ax.plot(x,y)
                ax.set_title('time = {:3.2f}'.format(now))
                ax.set_ylim(-1.2,1.2)
                writer.grab_frame()

