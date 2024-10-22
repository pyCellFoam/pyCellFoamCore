# -*- coding: utf-8 -*-
#==============================================================================
# TITLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Jul  9 11:21:13 2020

'''
Source: https://pynative.com/python-generate-random-string/

'''
#==============================================================================
#    IMPORTS
#==============================================================================
#-------------------------------------------------------------------------
#    Change to Main Directory
#-------------------------------------------------------------------------
import os
if __name__ == '__main__':
    os.chdir('../')


#-------------------------------------------------------------------------
#    Standard Libraries
#-------------------------------------------------------------------------


import random
import string


#==============================================================================
#    RANDOM LOWERCASE STRING
#==============================================================================

def random_lowercase_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


#==============================================================================
#    RANDOM STRING
#==============================================================================

def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))


#==============================================================================
#    RANDOM ALPHANUMERIC STRING
#==============================================================================

def random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for i in range(length)))



#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    
    print(random_string(10))    
    print(random_lowercase_string(40))
    print(random_alphanumeric_string(8))
