# -*- coding: utf-8 -*-
#==============================================================================
# COLOR CONSOLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Jan  4 17:25:08 2018

'''
This module offers functions to produce colored text in an iPython console.


'''

import sys

    
def printGray(*args,printImmediately=True,**kwargs):
    '''
    
    '''
    print('\033[1;30m',end='')
    print(*args,**kwargs)
    print('\033[0;0m',end='')
    if printImmediately:
        sys.stdout.flush()
        
    
def printRed(*args,printImmediately=True,**kwargs):
    '''
    
    '''    
    print('\033[1;31m',end='')
    print(*args,**kwargs)
    print('\033[0;0m',end='')
    if printImmediately:
        sys.stdout.flush()
    
def printGreen(*args,printImmediately=True,**kwargs):
    '''
    
    '''    
    print('\033[1;32m',end='')
    print(*args,**kwargs)
    print('\033[0;0m',end='')
    if printImmediately:
        sys.stdout.flush()
    
def printYellow(*args,printImmediately=True,**kwargs):
    print('\033[1;33m',end='')
    print(*args,**kwargs)
    print('\033[0;0m',end='')
    if printImmediately:
        sys.stdout.flush()  
   
def printBlue(*args,printImmediately=True,**kwargs):
    '''
    
    '''    
    print('\033[1;34m',end='')
    print(*args,**kwargs)
    print('\033[0;0m',end='')
    if printImmediately:
        sys.stdout.flush()

def printMagenta(*args,printImmediately=True,**kwargs):
    '''
    
    '''    
    print('\033[1;35m',end='')
    print(*args,**kwargs)
    print('\033[0;0m',end='')
    if printImmediately:
        sys.stdout.flush() 
    
def printCyan(*args,printImmediately=True,**kwargs):
    '''
    
    '''    
    print('\033[1;36m',end='')
    print(*args,**kwargs)
    print('\033[0;0m',end='')
    if printImmediately:
        sys.stdout.flush() 
    
def printWhite(*args,printImmediately=True,**kwargs):
    '''
    
    '''    
    print('\033[1;37m',end='')
    print(*args,**kwargs)
    print('\033[0;0m',end='')
    if printImmediately:
        sys.stdout.flush() 
    
def printDarkGrayBackground(*args,printImmediately=True,**kwargs):
    '''
    
    '''    
    print('\033[1;40m',end='')
    print('\033[1;37m',end='')
    print(*args,**kwargs)
    print('\033[0;0m',end='')
    if printImmediately:
        sys.stdout.flush()     

def printRedBackground(*args,printImmediately=True,**kwargs):
    '''
    
    '''    
    print('\033[1;41m',end='')
    print(*args,**kwargs)
    print('\033[0;0m',end='')
    if printImmediately:
        sys.stdout.flush()     
    
def printGreenBackground(*args,printImmediately=True,**kwargs):
    '''
    
    '''    
    print('\033[1;42m',end='')
    print('\033[2;38m',end='')
    print(*args,**kwargs)
    print('\033[0;0m',end='')
    if printImmediately:
        sys.stdout.flush()
    
def printYellowBackground(*args,printImmediately=True,**kwargs):
    '''
    
    '''    
    print('\033[1;43m',end='')
    print('\033[1;30m',end='')
    print(*args,**kwargs)
    print('\033[0;0m',end='')
    if printImmediately:
        sys.stdout.flush()
    
def printBlueBackground(*args,printImmediately=True,**kwargs):
    '''
    
    '''
    print('\033[1;44m',end='')
#    print('\033[1;30m',end='')
    print(*args,**kwargs)
    print('\033[0;0m',end='')
    if printImmediately:
        sys.stdout.flush()

def printMagentaBackground(*args,printImmediately=True,**kwargs):
    '''
    
    '''    
    print('\033[1;45m',end='')
#    print('\033[1;30m',end='')
    print(*args,**kwargs)
    print('\033[0;0m',end='')
    if printImmediately:
        sys.stdout.flush()
    
def printCyanBackground(*args,printImmediately=True,**kwargs):
    '''
    
    '''    
    print('\033[1;46m',end='')
    print('\033[1;30m',end='')
    print(*args,**kwargs)
    print('\033[0;0m',end='')
    if printImmediately:
        sys.stdout.flush()

def printLightGrayBackground(*args,printImmediately=True,**kwargs):
    '''
    
    '''    
    print('\033[1;47m',end='')
    print('\033[1;30m',end='')
    print(*args,**kwargs)
    print('\033[0;0m',end='')
    if printImmediately:
        sys.stdout.flush()
    
    
def printAllPossibleColors():
    '''
    
    '''
    
    # number3:     1 = light | 2 = dark | 3 = italic | 4 = underlined
    
    for number3 in range(1,5):
        print()
        print()
        print()
        print('number3 =',number3)
        print()
        ran2 = 70
        print('  ',end='')
        for number2 in range(ran2):
            print('\033[0;0m{:2}'.format(number2),end='',sep='')
        print()
        for number1 in range(55):
            print('\033[0;0m{:2}'.format(number1),end='',sep='')
            for number2 in range(ran2):
                printString = '\033[' # Start with escape character
                printString += str(number1) # 
                printString += ';'
                printString += str(number2)
                printString += ';'
                printString += str(number3)
                printString += 'm' # End with terminator
                printString += 'AB'
                print(printString,end='')
            print()
    print('\033[0;0m',end='')
            
            
        

    
    
    
    
    
#print('\033[1;30mGray like Ghost\033[1;m')
#print('\033[1;31mRed like Radish\033[1;m')
#print('\033[1;32mGreen like Grass\033[1;m')
#print('\033[1;33mYellow like Yolk\033[1;m')
#print('\033[1;34mBlue like Blood\033[1;m')
#print('\033[1;35mMagenta like Mimosa\033[1;m')
#print('\033[1;36mCyan like Caribbean\033[1;m')
#print('\033[1;37mWhite like Whipped Cream\033[1;m')
#print('\033[1;38mCrimson like Chianti\033[1;m')
#print('\033[1;41mHighlighted Red like Radish\033[1;m')
#print( '\033[1;42mHighlighted Green like Grass\033[1;m')
#print( '\033[1;43mHighlighted Brown like Bear\033[1;m')
#print( '\033[1;44mHighlighted Blue like Blood\033[1;m')
#print( '\033[1;45mHighlighted Magenta like Mimosa\033[1;m')
#print( '\033[1;46mHighlighted Cyan like Caribbean\033[1;m')
#print( '\033[1;47mHighlighted Gray like Ghost\033[1;m')
#print( '\033[1;48mHighlighted Crimson like Chianti\033[1;m')

if __name__ == '__main__':    
    print('normaler Text')
    b= 5
    printBlue('Hallo','Text in Blau',b)
    print('wieder normal')
    printGray('Hallo','Text in Grau',b)
    print('wieder normal')
    printRed('Hallo','Text in Rot',b)
    print('wieder normal')
    printGreen('Hallo','Text in Grün',b)
    print('wieder normal')
    printYellow('Hallo','Text in Gelb',b)
    print('wieder normal')
    printMagenta('Hallo','Text in Magenta',b)
    print('wieder normal')
    printCyan('Hallo','Text in Cyan',b)
    print('wieder normal')
    printWhite('Hallo','Text in Weiß',b)
    print('wieder normal')
    printDarkGrayBackground('Hallo','Text mit grauem Hintergrund',b)
    print('wieder normal')
    printLightGrayBackground('Hallo','Text mit grauem Hintergrund',b)
    print('wieder normal')
    printRedBackground('Hallo','Text mit rotem Hintergrund',b)
    print('wieder normal')
    printGreenBackground('Hallo','Text mit grünem Hintergrund',b)
    print('wieder normal')
    printYellowBackground('Hallo','Text mit gelbem Hintergrund',b)
    print('wieder normal')
    printBlueBackground('Hallo','Text mit blauem Hintergrund',b)
    print('wieder normal')
    printMagentaBackground('Hallo','Text mit magenta Hintergrund',b)
    print('wieder normal')
    printCyanBackground('Hallo','Text mit cyan Hintergrund',b)
    print('wieder normal')
    printAllPossibleColors()
    
