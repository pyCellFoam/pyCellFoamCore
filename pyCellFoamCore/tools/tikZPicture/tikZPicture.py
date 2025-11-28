# -*- coding: utf-8 -*-
#==============================================================================
# TIKZ PICTURE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Oct  3 16:44:31 2019

'''
This class is used to manage all elements of a drawing and exports it as TikZ
code.


'''
# =============================================================================
#    IMPORTS
# =============================================================================

# ------------------------------------------------------------------------
#    Standard Libraries
# ------------------------------------------------------------------------
import os
import logging
from pathlib import Path

# ------------------------------------------------------------------------
#    Third-Party Libraries
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
#    Local Libraries
# ------------------------------------------------------------------------

#    kCells
# -------------------------------------------------------------------

#    Tools
# -------------------------------------------------------------------
import pyCellFoamCore.tools.colorConsole as cc
from pyCellFoamCore.tools.tikZPicture.tikZEnvironment import TikZEnvironment
from pyCellFoamCore.tools.tikZPicture.tikZCoSy2D import TikZCoSy2D
import pyCellFoamCore.tools.randomString as rs



# =============================================================================
#    LOGGING
# =============================================================================

_log = logging.getLogger(__name__)
_log.setLevel(logging.INFO)


#==============================================================================
#    CLASS DEFINITION
#==============================================================================

class TikZPicture(TikZEnvironment):
    '''

    '''

#==============================================================================
#    SLOTS
#==============================================================================
    __slots__ = ('__scale')

#==============================================================================
#    INITIALIZATION
#==============================================================================
    def __init__(self,scale=1,**kwargs):
        '''
        :param float scale: scale of the tikzpicture
        :param str name: A name for the tikzpicture

        '''
        super().__init__(**kwargs)
        self.__scale = scale
        self.logger.info('Created TikZPicture')



#==============================================================================
#    SETTER AND GETTER
#==============================================================================
    def __getScale(self): return self.__scale
    def __setScale(self,s): self.__scale = s
    scale = property(__getScale,__setScale)





    def __getLibraryOptions(self): return ['decorations.markings','arrows']
    libraryOptions = property(__getLibraryOptions)

    def __getPictureOptions(self):
        options = []
        if self.scale != 1:
            options.append('scale = {}'.format(self.scale))
        return options
    pictureOptions = property(__getPictureOptions)


    def __getEnvironmentName(self): return 'tikzpicture'
    environmentName = property(__getEnvironmentName)


    def __getTikzsets(self): return ['\t->-/.style={decoration={\n\t\tmarkings,\n\t\tmark=at position 0.5 with {\\arrow[scale=2]{latex}}},postaction={decorate}\n\t}',]
    tikzsets = property(__getTikzsets)


    def __getTikZCoSy2DUsed(self): return any([type(x) == TikZCoSy2D for x in self.tikZCoSys])
    tikZCoSy2DUsed = property(__getTikZCoSy2DUsed)

    def __getCircledArrowsUsed(self): return self.tikZCircledArrows
    circledArrowsUsed = property(__getCircledArrowsUsed)


    def __getNewcommands(self):
        newcommandsTemp = []
        if self.tikZCoSy2DUsed:
            newcommandsTemp.append('''\\newcommand{\\CoSyTwoD}[2][1]{% #1 Arrow length, #2 Center
    \\draw[TUMOrange,-stealth] (#2) -- +(#1,0);
    \\draw[TUMGreen,-stealth] (#2) -- +(0,#1);
}
''')
        if self.circledArrowsUsed:
            newcommandsTemp.append('''\\newcommand{\\circledarrow}[3][]{% #1 Style, #2 Center, #3 Radius
    \\draw[#1,-latex] (#2) +(-90:#3) arc(-90:180:#3);
}
''')
        return newcommandsTemp
    newcommands = property(__getNewcommands)




    def __getLatexPreamble(self):

        text = '\\usepackage{tikz}\n'
        if len(self.libraryOptions) != 0:
            text += '\\usetikzlibrary{{{}}}\n'.format(','.join(self.libraryOptions))

        for n in self.newcommands:
            text += n


        text += '\\tikzset{\n' + ',\n'.join(self.tikzsets) + '\n}\n'
        return text


    latexPreamble=property(__getLatexPreamble)

#==============================================================================
#    METHODS
#==============================================================================




#-------------------------------------------------------------------------
#    write TikZ file
#-------------------------------------------------------------------------
    def writeTikZFile(self,filepath='latex',filename=None):
        if filename is None:
            filename = self.name

        p = Path(filepath)
        p.mkdir(parents=True,exist_ok=True)
        f = p.joinpath(filename+'.tex')


        with open(f,'w') as file:
            file.write(self.tikZText)
            self.logger.info('Written TikZFile file {}'.format(filepath+filename+'.tex'))




#-------------------------------------------------------------------------
#    write LaTeX file
#-------------------------------------------------------------------------
    def writeLaTeXFile(self,filepath='latex',filename=None,compileFile=False,openFile=False):

        if filename is None:
            filename = self.name


        p = Path(filepath)
        p.mkdir(parents=True,exist_ok=True)
        fileTex = p.joinpath(filename+'.tex')
        filePdf = p.joinpath(filename+'.pdf')


        if openFile and not compileFile:
            self.logger.warning('Opening pdf file without compiling LaTeX file first. An old version will be opened')


        with open(fileTex,'w') as file:
            file.write('\\documentclass{TUMnote}\n')
            file.write(self.latexPreamble)
            file.write('\\begin{document}\n')
            file.write(self.tikZText)
            file.write('\\end{document}\n')
            self.logger.info('Written LaTeX file {}'.format(fileTex))



        if compileFile:
            # Change current directory to export path
            os.chdir(filepath)

            # Compile tex file
            os.system('pdflatex {}.tex -interaction batchmode'.format(filename))

            # Change current directory back to original location
            os.chdir('../'*len(p.parents))
        if openFile:
            os.startfile('{}'.format(filePdf))


#        levelsOfExportPath = filepath.count('/')
#        os.chdir('../'*levelsOfExportPath)


#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':



    import numpy as np
    import logging

    from tools import MyLogging

    with MyLogging('TikZPicture',shLevel=logging.DEBUG):

        cc.printBlue('Create picture')
        tikzpicture = TikZPicture()

        cc.printBlue('Create coordinates')
        c1 = tikzpicture.addTikZCoordinate('c1',np.array([0,0]))
        c2 = tikzpicture.addTikZCoordinate('c2',np.array([1,0]))

        cc.printBlue('Create node')
        n1 = tikzpicture.addTikZNode('n1',np.array([0,1]))

        cc.printBlue('Create polygon')
        tikzpicture.addTikZPolygon([c1,c2,n1])

        cc.printBlue('Create coordinate system')
        tikzpicture.addTikZCoSy2D(c2)

        cc.printGreen('Preamble:')
        print(tikzpicture.latexPreamble)

        cc.printGreen('TikZ text:')
        print(tikzpicture.tikZText)

        tikzpicture.writeTikZFile()
        tikzpicture.writeTikZFile('latex/'+rs.random_alphanumeric_string(20),rs.random_alphanumeric_string(10))
