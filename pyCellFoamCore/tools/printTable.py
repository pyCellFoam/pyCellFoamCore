# -*- coding: utf-8 -*-
#==============================================================================
# PRINT TABLE TO CONSOLE
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Wed Jun 12 15:25:35 2019


#==============================================================================
#    IMPORTS
#==============================================================================
import math, re


#==============================================================================
#    CELL CLASS
#==============================================================================
class Cell:
    __slots__ = ('__content','__length','__lengthChanged','__columns','__row','__printWidth','__printWidthChanged','__align')
    
#-------------------------------------------------------------------------
#    Initialization of cell
#-------------------------------------------------------------------------    
    
    def __init__(self,content):
        self.__content = str(content)
        self.__lengthChanged = True
        self.__printWidth = None
        self.__printWidthChanged = True
        self.__row = None
        self.__columns = []
        self.__align = 'l'
        
#-------------------------------------------------------------------------
#    Magic Methods of cell
#-------------------------------------------------------------------------        
    def __repr__(self):
        return self.name
        
        
#-------------------------------------------------------------------------
#    Properties of cell
#-------------------------------------------------------------------------        
    def __getContent(self): return self.__content
    def __setContent(self,c): 
        self.__content = str(c)
        self.__lengthChanged = True
        self.__printWidthChanged = True
    content = property(__getContent,__setContent)

    def __getLength(self):
        if self.__lengthChanged:
            self.__calcLength()
        return self.__length
    length = property(__getLength)
    
    def __getLengthPerCol(self):
        return math.ceil(self.length/len(self.__columns))
    lengthPerCol = property(__getLengthPerCol)
    
    def __getRow(self): return self.__row
    row = property(__getRow)
    
    def __getColumns(self): return self.__columns
    columns = property(__getColumns)
    
    def __getPrintWidth(self):
        if self.__printWidthChanged:
            self.__calcPrintWidth()
        return self.__printWidth
    printWidth = property(__getPrintWidth)
    
    def __getAlign(self): return self.__align
    def __setAlign(self,a): 
        assert a in 'lcr', 'Unknnown alignment'
        self.__align = a
    align = property(__getAlign,__setAlign)
    
    
#-------------------------------------------------------------------------
#    Private Functions of cell
#-------------------------------------------------------------------------    
    
    def __calcPrintWidth(self):
        self.__printWidth = sum([x.width for x in self.columns])+3*(len(self.columns)-1)
        self.__printWidthChanged = False
    
    
    def __getName(self):
        if self.row is None:
            return 'NO ROW'
        else:
            if len(self.columns) == 0:
                return 'NO COL'
            if len(self.columns) == 1:
                return 'C{} R{}'.format(self.columns[0].num,self.row.num)
            else:
                return 'C{}-{} R{}'.format(self.columns[0].num,self.columns[-1].num,self.row.num)
    name = property(__getName)
    
    
    
    def __calcLength(self):
        self.__length = len(self.content)
        self.__lengthChanged = False
        
    

#-------------------------------------------------------------------------
#    Public functions of cell
#-------------------------------------------------------------------------    
    def printCell(self):
        blankSpaces =     self.printWidth-self.length    
        
        if self.align == 'c':
            print(' '*math.ceil(blankSpaces/2),end='')
        elif self.align == 'r':
            print(' '*blankSpaces,end='')
        
        print(self.content,end='')
        
        
        if self.align == 'c':
            print(' '*math.floor(blankSpaces/2),end=' | ')
        elif self.align == 'l':
            print(' '*blankSpaces,end=' | ')
        elif self.align == 'r':
            print(end=' | ')
        
        
    def addToRow(self,row):
        if self.__row is None:
            self.__row = row
        else:
            print('Cell already belongs to a row')
            
            
    def addToColumn(self,column):
        if not column in self.__columns:
            self.__columns.append(column)
        else:
            print('Cell already belongs to column')
        
        
        
#==============================================================================
#    ROW CLASS
#==============================================================================
class Row:
    rowNum = 0
    __slots__ = ('__cells','__num','__rowAbove','__rowBelow')
    
#-------------------------------------------------------------------------
#    Initialization of row
#-------------------------------------------------------------------------      
    def __init__(self,rowAbove=None):
        self.__cells = []
        self.__num = Row.rowNum
        Row.rowNum += 1
        self.__rowBelow = None
        self.__rowAbove = None
        if rowAbove:
            self.__rowAbove = rowAbove
            rowAbove.rowBelow = self
        
#-------------------------------------------------------------------------
#    Magic Methods of row
#-------------------------------------------------------------------------           
    def __repr__(self): return 'Row '+str(self.__num)
        
#-------------------------------------------------------------------------
#    Properties of row
#------------------------------------------------------------------------- 
    def __getCells(self): return self.__cells
    cells = property(__getCells)      
    
    def __getNum(self): return self.__num
    num = property(__getNum)
    
    def __getRowAbove(self): return self.__rowAbove
    rowAbove = property(__getRowAbove)
    
    def __getRowBelow(self): return self.__rowBelow
    def __setRowBelow(self,r): 
        assert self.__rowBelow is None, 'Row already as a row below it'
        self.__rowBelow = r
    rowBelow = property(__getRowBelow,__setRowBelow)
        
#-------------------------------------------------------------------------
#    Public functions of row
#-------------------------------------------------------------------------     
    def addCell(self,cell):
        assert not cell in self.__cells, 'Cell already in row'
        self.__cells.append(cell)
        cell.addToRow(self)
        
    def printRow(self):
        print('| ',end='')
        for c in self.cells:
            c.printCell()
        print()


#==============================================================================
#    COLUMN CLASS
#==============================================================================            
class Column:
    colNum = 0
    __slots__ = ('__cells','__width','__num','__columnLeft','__columnRight')
    
#-------------------------------------------------------------------------
#    Initialization of column
#-------------------------------------------------------------------------          
    def __init__(self,columnLeft=None):
        self.__cells = []
        self.__num = Column.colNum
        self.__columnLeft = None
        self.__columnRight = None
        Column.colNum += 1        
        if columnLeft:
            self.__columnLeft = columnLeft
            columnLeft.columnrRight = self

#-------------------------------------------------------------------------
#    Properties of column
#------------------------------------------------------------------------- 
    def __getColumnLeft(self): return self.__columnLeft
    columnLeft = property(__getColumnLeft)
    
    def __getColumnRight(self): return self.__columnRight
    def __setColumnRight(self,r): 
        assert self.__columnRight is None, 'Column already as a column right of it'
        self.__columnRight = r
    columnRight = property(__getColumnRight,__setColumnRight)

    def __getCells(self): return self.__cells
    cells = property(__getCells)    
        
    def __getNum(self): return self.__num
    num = property(__getNum)        
    
    def __getWidth(self):
        return max([c.lengthPerCol for c in self.__cells])
    width = property(__getWidth)
        
    
#-------------------------------------------------------------------------
#    Public functions of column
#-------------------------------------------------------------------------   
    def addCell(self,cell):
        assert not cell in self.__cells, 'Cell already in column'
        
        if cell.row.rowAbove:
            if cell.row.rowAbove.cells[-1].columns[-1].num < self.num:
                newCell = Cell('')
                cell.row.rowAbove.addCell(newCell)
                
                # Attention this recursively trigges the addCell function!!!
                self.addCell(newCell)
        self.__cells.append(cell)
        cell.addToColumn(self)
        
        
        
#==============================================================================
#    TABLE CLASS
#==============================================================================    
    
class Table:
    __slots__ = ('__rows','__columns','__cell')
    
#-------------------------------------------------------------------------
#    Initialization of table
#-------------------------------------------------------------------------     
    def __init__(self,tableContent):
        
        # Make sure that the input is a list
        assert isinstance(tableContent,list), 'tableContent must be a list of lists'
        
        # Initalize lists for rows and columns
        rows = []
        columns = []
        rowAbove = None
        
        for rawRow in tableContent:
            
            # Make sure that every row in the input is a list
            assert isinstance(rawRow,list), 'Every row in tableContent must be a list'
            colNum = 0
            row = Row(rowAbove = rowAbove)
            rowAbove = row
            rows.append(row)
            for c in rawRow:
                cell = Cell(c)
                row.addCell(cell)
                
                res = re.findall('!<(.*?)>',str(c))
                res2 = re.findall('\?<(.*?)>',str(c))
                
                assert len(res) <= 1, 'Wrong information for spanning columns'
                if len(res) == 1:
                    spanningCols = int(res[0])
                    cell.content = cell.content[len(res[0])+3:]
                else:
                    spanningCols = 1
                    
                assert len(res2) <= 1, 'Wrong information for alignment'
                if len(res2) == 1:
                    cell.align = res2[0]
                    cell.content = cell.content[len(res2[0])+3:]
                    
                
                for _ in range(spanningCols):
                    if colNum+1 > len(columns):
                        columns.append(Column())
                    columns[colNum].addCell(cell)
                    colNum+=1
            
        self.__rows = rows
        self.__columns = columns
        
        
        
#-------------------------------------------------------------------------
#    Public functions of table
#-------------------------------------------------------------------------   
    def printTable(self):
        iterLower = iter(self.__rows[0].cells)
        currentLowerCell = next(iterLower)
        print('┌',end='')
        for column,nextColumn in zip(self.__columns[:-1],self.__columns[1:]):
            if currentLowerCell in nextColumn.cells:
                myEnd = '─'
            else:
                myEnd = '┬'
                currentLowerCell = next(iterLower)
            
            print('─'*(column.width+2),end=myEnd)
        print('─'*(self.__columns[-1].width+2),end='┐')
        print()
        
        for row in self.__rows[:-1]:
            row.printRow()
            print('├',end='')
            
            
            iterUpper = iter(row.cells)
            currentUpperCell = next(iterUpper)
            iterLower = iter(row.rowBelow.cells)
            currentLowerCell = next(iterLower)
            
            for column,nextColumn in zip(self.__columns[:-1],self.__columns[1:]):
                if currentUpperCell in nextColumn.cells and currentLowerCell in nextColumn.cells:
                    myEnd = '─'
                    
                elif currentUpperCell in nextColumn.cells:
                    myEnd = '┬'
                elif currentLowerCell in nextColumn.cells:
                    myEnd = '┴'
                else:
                    myEnd = '┼'
                    
                    
                if not currentUpperCell in nextColumn.cells:
                    currentUpperCell = next(iterUpper)
                if not currentLowerCell in nextColumn.cells:
                    currentLowerCell = next(iterLower)
                print('─'*(column.width+2),end=myEnd)
            print('─'*(self.__columns[-1].width+2),'┤',sep='')
                
         
        self.__rows[-1].printRow()
        iterUpper = iter(self.__rows[-1].cells)
        currentUpperCell = next(iterUpper)
        print('┕',end='')
        for column,nextColumn in zip(self.__columns[:-1],self.__columns[1:]):
            if currentUpperCell in nextColumn.cells:
                myEnd = '─'
            else:
                myEnd = '┴'
                currentUpperCell = next(iterUpper)
            
            print('─'*(column.width+2),end=myEnd)
        print('─'*(self.__columns[-1].width+2),end='┘')
        print()                
                
                
        
        
#==============================================================================
#    TEST FUNCTIONS
#==============================================================================
if __name__ == '__main__':
    header = ['Header 1','Header 2 abc','Header 3','Header 4','!<3>Header 5']
    row1 = ['!<3>?<c>A','B','C']
    row2 = ['!<2>1','?<r>2',3]
    row3 = [1,'!<4>2']
    row4 = [1,2,3,4,5,'!<3>6']
    
    tableContent = [header,row1,row2,row3,row4]
    table = Table(tableContent)
    table.printTable()
    
    






