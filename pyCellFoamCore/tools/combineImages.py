# -*- coding: utf-8 -*-
#==============================================================================
# TITLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Mon Aug  6 15:25:06 2018

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
#import sys
from PIL import Image

#==============================================================================
#    FUNCTION DEFINITION
#==============================================================================

def combineImages(source,target):

    #images = map(Image.open, ['Test1.png', 'Test2.png', 'Test3.png'])
    #    image_names = ['Test1.png', 'Test2.png', 'Test3.png']
    images = [Image.open(im) for im in source]
    widths, heights = zip(*(i.size for i in images))
    
    total_width = sum(widths)
    max_height = max(heights)
    
    new_im = Image.new('RGB', (total_width, max_height), 'white')
    
    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]
    #
    new_im.save(target)
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == "__main__":
    sourceFiles = ['puppy.jpg','kitten.jpeg']
    targetFile = 'combination.jpeg'
    combineImages(sourceFiles,targetFile)
    
    
    
    

