# -*- coding: utf-8 -*-
# =============================================================================
# PLACE FIGURES
# =============================================================================
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
# =============================================================================
#    IMPORTS
# =============================================================================

# ------------------------------------------------------------------------
#    Standard Libraries
# ------------------------------------------------------------------------
import sys
import math

# ------------------------------------------------------------------------
#    Third-Party Libraries
# ------------------------------------------------------------------------
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------

#    Tools
# --------------------------------------------------------------------
import pyCellFoamCore.tools.colorConsole as cc

# =============================================================================
#    GET FIGURES
# =============================================================================

def getFigures(numFigHorizontal=0, numFigVertical=0,
               numTotal=6, aspect3D=True):
    plt.switch_backend("Qt5Agg")
    try:
        import localConfig
        pyplotWindowSize = localConfig.pyplotWindowSize
        pyplotTopLeftCorner = localConfig.pyplotTopLeftCorner
        try:
            pyplotPortrait = localConfig.pyplotPortrait
        except Exception as e:
            pyplotPortrait = False
            cc.printRed('Portrait mode not defined. ' +
                        'Using standard landscape mode. ' +
                        '(Message: {})'.format(e))
    except Exception as e:
        pyplotPortrait = False
        pyplotWindowSize = (1920, 1080)
        pyplotTopLeftCorner = (0, 0)
        cc.printRed('place Figures: No local configuration file found, ' +
                    'using standard. ' +
                    '(Message: {})'.format(e))

    if numTotal > 0:
        cc.printYellow('Portrait mode: {}'.format(pyplotPortrait))
        if pyplotPortrait:
            numFigHorizontal = math.floor(math.sqrt(numTotal))
            numFigVertical = math.ceil(numTotal/numFigHorizontal)
            cc.printYellow('Portraid mode activated')
        else:
            numFigVertical = math.floor(math.sqrt(numTotal))
            numFigHorizontal = math.ceil(numTotal/numFigVertical)

    # Close old windows
    closeFigures()

    xRes = pyplotWindowSize[0]
    yRes = pyplotWindowSize[1]

    # Create 2-dimensional list with all figures
    figuresXY = [[plt.figure() for _ in range(numFigHorizontal)]
                 for _ in range(numFigVertical)]

    width = xRes // numFigHorizontal
    height = yRes // numFigVertical
    for (i, row) in enumerate(figuresXY):
        for (j, fig) in enumerate(row):
            xPos = xRes // numFigHorizontal * j + pyplotTopLeftCorner[0]
            yPos = yRes // numFigVertical * i + pyplotTopLeftCorner[1]
            mngr = fig.canvas.manager
            mngr.window.setGeometry(xPos, yPos, width, height)

    # create list with all figures and axes
    figs = []
    axes = []
    for x in figuresXY:
        for y in x:
            figs.append(y)
            if aspect3D:
                if sys.version_info.minor < 10:
                    axes.append(Axes3D(y))
                else:
                    axes.append(y.add_subplot(projection='3d'))
            else:
                axes.append(y.add_subplot(111))

    if aspect3D:
        for ax in axes:
            ax.set_proj_type('ortho')
            ax.view_init(azim=135, elev=20)

    return (figs, axes)


# =============================================================================
#    SET AXES EQUAL
# =============================================================================


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


# =============================================================================
#    COPY LIMITS
# =============================================================================


def copylimits(fromax, toax):
    toax.set_xlim3d(fromax.get_xlim3d())
    toax.set_ylim3d(fromax.get_ylim3d())
    toax.set_zlim3d(fromax.get_zlim3d())


# =============================================================================
#    SET LABELS
# =============================================================================


def setLabels(ax, x='x', y='y', z='z'):
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_zlabel(z)


# =============================================================================
#    RETURN TO 2D
# =============================================================================


def returnTo2D(fig):
    fig.clf()
    ax = fig.add_subplot(111)
    return ax


# =============================================================================
#    MM TO INCH
# =============================================================================


def mm2inch(mm):
    MM_PER_INCH = 25.4
    return mm/MM_PER_INCH


# =============================================================================
#    EXPORT PNG
# =============================================================================


def exportPNG(fig, filename='export', width_mm=120, height_mm=100, dpi=300):
    folderpath = os.path.dirname(filename)
    if folderpath != '':
        os.makedirs(folderpath, exist_ok=True)

    plt.figure(fig.number)
    handle = plt.gcf()
    handle.set_size_inches(mm2inch(width_mm), mm2inch(height_mm))
    plt.savefig(filename, dpi=dpi, transparent=True)


# =============================================================================
#    GET VIDEO
# =============================================================================

def getVideo(title='My excellent animation',
             artist='Tobias Scheuermann',
             comment='Tobias Scheuermann\r\n\r\n' +
                     'E-Mail:\r\ntobias.scheuermann@tum.de\r\n\r\n' +
                     'Technical University of Munich\r\n' +
                     'Faculty of Mechanical Engineering\r\n' +
                     'Chair of Automatic Control',
             aspect3D=True,
             fps=15):
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

    plt.switch_backend('Agg')
    return (fig, ax, writer)


# =============================================================================
#    GET VIDEO 2
# =============================================================================


def getVideo2(title='My excellent animation',
              artist='Tobias Scheuermann',
              comment='Tobias Scheuermann\r\n\r\n' +
                      'E-Mail:\r\ntobias.scheuermann@tum.de\r\n\r\n' +
                      'Technical University of Munich\r\n' +
                      'Faculty of Mechanical Engineering\r\n' +
                      'Chair of Automatic Control',
              fps=15):
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
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    ax2 = fig.add_subplot(1, 2, 2)

    plt.switch_backend('Agg')
    return (fig, [ax1, ax2], writer)


# =============================================================================
#    CLOSE FIGURES
# =============================================================================


def closeFigures():
    plt.close('all')


# =============================================================================
#    TEST FUNCTIONS
# =============================================================================

if __name__ == '__main__':

    if True:
        (figs, axes) = getFigures()
        x = [0, 0, 0, 0, 1, 1, 1, 1]
        y = [0, 0, 1, 1, 0, 0, 1, 1]
        z = [0, 1, 0, 1, 0, 1, 0, 1]

        axes[0].scatter(x, y, z)

    if False:
        (figs, axes) = getFigures(aspect3D=False)
        x = np.arange(-math.tau, math.tau, 0.01)
        y = np.sin(x)

        axes[0].plot(x, y)

    if False:
        exportPNG(figs[0], 'testExport/test')
        exportPNG(figs[1],
                  'testExport2/testExport3/testExport4/testExport5/test')
        exportPNG(figs[2])

    if False:
        (fig, ax, writer) = getVideo(title='Example', aspect3D=False, fps=60)
        x = np.arange(0, math.tau, 0.1)
        t = np.arange(0, math.tau, 1/60)
        numSteps = len(t)
        with writer.saving(fig, 'exampleVideo.mp4', 120):
            for (i, now) in enumerate(t):
                y = math.sin(now)*np.sin(x)
                print('Visualizing timestep {} of {}'.format(i+1, numSteps))
                ax.clear()
                ax.plot(x, y)
                ax.set_title('time = {:3.2f}'.format(now))
                ax.set_ylim(-1.2, 1.2)
                writer.grab_frame()
