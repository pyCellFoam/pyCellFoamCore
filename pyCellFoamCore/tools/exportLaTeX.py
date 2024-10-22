# -*- coding: utf-8 -*-
#==============================================================================
# TITLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Tue Sep 18 09:19:57 2018

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
if __name__== '__main__':
    import os
    os.chdir('../')
import numpy as np
    

    
#==============================================================================
#    METHODS
#==============================================================================
def array2Tabular(a):
    s = '\\begin{tabular}'
    s+= '{'
    s+= 'l'*a.shape[1]
    s+= '}\r\n'
    for i in range(a.shape[0]):
        for j in range(a.shape[1]):
            s += '\t{:.0f}'.format(a[i,j])
            if j != a.shape[1]-1:
                s+=' &'
        if i != a.shape[0]-1:
            s+= '\\\\'
        s+= '\r\n'
    s += '\\end{tabular}'
    return s

def array2bmatrix(a,addIndent=0):
    sa = array2strArray(a)
    s = addIndent*'\t'+'\\begin{bmatrix}\r\n'
    for i,line in enumerate(sa):
        s += (addIndent+1)*'\t'
        for j,cell in enumerate(line):
            s += cell
            if j != len(line)-1:
                s+=' & '
        if i != len(sa)-1:
            s+= '\\\\'
        s+= '\r\n'
    s += addIndent*'\t'+'\\end{bmatrix}'
    return s


def array2strArray(a):
    sa = []
    lengths = np.zeros(a.shape)
    for i in range(a.shape[0]):
        saLine = []
#        lenghtsLine = []
        for j in range(a.shape[1]):
            saCell = '{:.0f}'.format(a[i,j])
            saLine.append(saCell)
            lengths[i,j] = len(saCell)
        sa.append(saLine)
#        lengths.append(lenghtsLine)
    maxLengths = np.amax(lengths,axis=0)
    for i in range(len(sa)):
        for (j,length) in zip(range(len(sa[i])),maxLengths):
            sa[i][j] += ' '*(int(length)-len(sa[i][j]))
    return sa
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == "__main__":
    a = np.random.rand(2,3)*50-25
    print(a)
    print(array2Tabular(a))
    print(array2bmatrix(a))
    print(array2bmatrix(a,5))

#    test = array2strArray(a)