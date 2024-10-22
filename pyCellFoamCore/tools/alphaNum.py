# -*- coding: utf-8 -*-
#==============================================================================
# TITLE
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

import string
#==============================================================================
#    METHODS
#==============================================================================

def alphaNum(num):
    if num < 0:
        return 'NEG'
    
    num = num + 1
    
    count = 0
    erg = ''
    goOn = True
    while count < 50 and goOn:
        count += 1
#        print(25 % num)
        erg = string.ascii_lowercase[(num % 26) - 1]+erg
        if num > 26:
#            print(num)
            num = num - num % 26
#            print(num)
            num = int(num/26)
#            print(num)
#            print()
        else:
            goOn = False
    
        
    return erg
    
    
    
if __name__ == '__main__':
    for a in range(3000):
        print(alphaNum(a))
