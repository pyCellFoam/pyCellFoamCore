# -*- coding: utf-8 -*-
#==============================================================================
# TITLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Thu Dec  7 15:03:39 2017


class TUMcolor:
    __slots__ = ('__color','__name')
    def __init__(self,color,name):
        self.__color = color
        self.__name = name
    
    def __getHTML(self): return '#{:02x}{:02x}{:02x}'.format(*self.__color).upper()
    html = property(__getHTML)
    
    def __getRGB01(self): return [c/255 for c in self.__color]
    rgb01 = property(__getRGB01)

    def __getRGB0255(self): return self.__color
    rgb0255 = property(__getRGB0255)
    
    def __getColor(self): return self.__color
    color = property(__getColor)
    
    def __getName(self): return self.__name
    name = property(__getName)
    
    def __getLatexColor(self): return ','.join(str(x) for x in self.__color)
    latexColor = property(__getLatexColor)
    
    def __getLatexDefinecolor(self): return '\\definecolor{{{}}}{{RGB}}{{{}}}\n'.format(self.name,self.latexColor)
    latexDefinecolor = property(__getLatexDefinecolor)
    
    def __repr__(self):
        return 'TUM Color "{}" - {} - {}'.format(self.__name,self.rgb0255,self.html)
    
    def __mul__(self,other):
        return TUMcolor([int(c*other) for c in self.color],'Mix')
    
    def __add__(self,other):
        return TUMcolor([int(c1+c2) for (c1,c2) in zip(self.color,other.color)],'Mix')
    
    
    
class TUMBlue(TUMcolor):
    def __init__(self):
        super().__init__([  0, 101, 189],'TUMBlue')
        
class TUMGreen(TUMcolor):
    def __init__(self):
        super().__init__([162, 173,   0],'TUMGreen')       
            
class TUMOrange(TUMcolor):
    def __init__(self):
        super().__init__([227, 114,  34],'TUMOrange')   

class TUMGrayMedium(TUMcolor):
    def __init__(self):
        super().__init__([156, 157, 159],'TUMGrayMedium')   

class TUMBlack(TUMcolor):
    def __init__(self):
        super().__init__([  0,   0,   0],'TUMBlack')   


class TUMWhite(TUMcolor):
    def __init__(self):
        super().__init__([255, 255, 255],'TUMWhite')   


class TUMRose(TUMcolor):
    def __init__(self):
        super().__init__([227, 130, 143],'TUMRose')   


class TUMMustard(TUMcolor):
    def __init__(self):
        super().__init__([202, 171,  41],'TUMMustard')   
        

class TUMLightBlue(TUMcolor):
    def __init__(self):
        super().__init__([ 91, 197, 242],'TUMLightBlue')
        

    

if __name__ == '__main__':
    tumBlue = TUMBlue()
    tumGreen = TUMGreen()
    tumRose = TUMRose()
#    tc = TUMcolor()
    print('TUM Blue in standard RGB values (0-255):',tumBlue.rgb0255) 
    print('TUM Blue in normalized RGB values (0-1):',tumBlue.rgb01) 
    print('TUM Blue in html notation:',tumBlue.html) 
    print('TUM Green in html notation:',tumGreen.html) 
    print(tumBlue)
    print(tumBlue.latexDefinecolor)
    
    print(tumRose.html)
    
    
    print(tumBlue*0.1)
    print(tumBlue+tumGreen)
    
