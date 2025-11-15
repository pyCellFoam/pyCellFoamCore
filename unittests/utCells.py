# -*- coding: utf-8 -*-
#==============================================================================
# UNITTEST OF CELL CLASSES
#==============================================================================
# Author:         Tobias Scheuermann
# Institution:    Chair of Automatic Control
#                 Department of Mechanical Engineering
#                 Technical University of Munich (TUM)
# E-Mail:         tobias.scheuermann@tum.de
# Created on:     Fri Oct 19 10:44:15 2018

'''

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
import unittest


#-------------------------------------------------------------------------
#    Local Libraries
#-------------------------------------------------------------------------

#    kCells
#--------------------------------------------------------------------
from kCells import SuperBaseCell, SuperCell, SuperReversedCell
from kCells import BaseCell, Cell, ReversedCell
from kCells import BaseSimpleCell, SimpleCell, ReversedSimpleCell
from kCells import DualCell

#    Tools
#--------------------------------------------------------------------
import tools.tumcolor as tc


#==============================================================================
#    CLASS DEFINITION
#==============================================================================
class TestCellMethods(unittest.TestCase):


#==============================================================================
#    TESTING METHODS
#==============================================================================
#-------------------------------------------------------------------------
#    Super Base Cell
#-------------------------------------------------------------------------
    def testSuperBaseCell(self):

        # Create a SuperBaseCell
        testSUPBC1 = SuperBaseCell(loggerName='test')

        # Create another SuperBaseCell that shall serve as the reversed of the first
        testSUPBC2 = SuperBaseCell(my_reverse=testSUPBC1,loggerName='test')

        # Check if the __neg__ function is set correctly
        self.assertEqual(testSUPBC1,-testSUPBC2)



#-------------------------------------------------------------------------
#    Super Cell
#-------------------------------------------------------------------------
    def testSuperCell(self):

        # Create a SuperCell
        testSUPC = SuperCell(loggerName='test')
        mtestSUPC = -testSUPC

        # Check if the reversedCell has been created as well
        self.assertIsInstance(mtestSUPC,SuperReversedCell)

        # Delete the SuperCell
        testSUPC.delete()

        # Check if the SuperCell and its reversed have been deleted
        self.assertTrue(testSUPC.is_deleted)
        self.assertTrue(mtestSUPC.is_deleted)

#-------------------------------------------------------------------------
#    Super Reversed Cell
#-------------------------------------------------------------------------
    def testSuperReversedCell(self):

        # Create a ReversedSuperCell
        testSUPRC = SuperReversedCell(loggerName='test')

        # Check that the reversed of a reversed is empty when beeing created alone
        self.assertIsNone(-testSUPRC)



#-------------------------------------------------------------------------
#    Base Cell
#-------------------------------------------------------------------------
    def testBaseCell(self):

        # Create a BaseCell
        testBC = BaseCell(loggerName='test')

        # Check if the label suffix is correctly set to an empty string
        self.assertEqual(testBC.label_suffix, '')



#-------------------------------------------------------------------------
#    Cell
#-------------------------------------------------------------------------
    def testCell(self):

        # Create a Cell
        testC = Cell(loggerName='test')

        # Change some properties
        testC.num = 12
        testC.label = 'a'
        testC.is_geometrical = False
        testC.category1 = 'inner'
        testC.category2 = 'border'

        # Get its ReversedCell
        mtestC = -testC

        # Check that the properties are correctly translated into the text variables
        self.assertEqual(testC.info_text,'a_i12')
        self.assertEqual(testC.labelText,'$a_{\mathrm{i}12}$')
        self.assertEqual(mtestC.info_text,'-a_i12')
        self.assertEqual(mtestC.labelText,'$-a_{\mathrm{i}12}$')

        # Change label
        testC.label = 'b'

        # Check that the XChanged variables are set correctly
        self.assertTrue(mtestC.labelTextChanged)
        self.assertTrue(mtestC.info_textChanged)

        # Set a color
        testC.color = tc.TUMRose()

        # Check the color output
        self.assertEqual(testC.color.html,'#E3828F')


        # Check that a standard cell is stored as non-dual
        self.assertFalse(testC.is_dual)



#-------------------------------------------------------------------------
#    Reversed Cell
#-------------------------------------------------------------------------
    def testReversedCell(self):

        # Create a ReversedCell
        testRC = ReversedCell(loggerName='test')

        # Check that the reversed of a reversed is empty when beeing created alone
        self.assertIsNone(-testRC)




#-------------------------------------------------------------------------
#    Base Simple Cell
#-------------------------------------------------------------------------
    def testBaseSimpleCell(self):

        # Create a Cell
        testC = Cell(loggerName='test')

        # Change some properties
        testC.num = 13
        testC.label = 'd'
        testC.is_geometrical = True

        # Create a BaseSimpleCell that belongs to the previously created Cell
        testBSC = BaseSimpleCell(belongsTo = testC,loggerName='test')

        # Check that the properties are equal
        self.assertEqual(testC.num,testBSC.num)
        self.assertEqual(testC.label,testBSC.label)
        self.assertEqual(testC.is_geometrical,testBSC.is_geometrical)




#-------------------------------------------------------------------------
#    Simple Cell
#-------------------------------------------------------------------------
    def testSimpleCell(self):

        # Create a SimpleCell
        testSC = SimpleCell(loggerName='test')
        mtestSC = -testSC

        # Check if the reversedSimpleCell has been created as well
        self.assertIsInstance(mtestSC,ReversedSimpleCell)




#-------------------------------------------------------------------------
#    Reversed Simple Cell
#-------------------------------------------------------------------------
    def testReversedSimpleCell(self):

        # Create a ReversedSimpleCell
        testRSC = ReversedSimpleCell(loggerName='test')

        # Check that the reversed of a reversed is empty when beeing created alone
        self.assertIsNone(-testRSC)


#-------------------------------------------------------------------------
#    Dual Cell
#-------------------------------------------------------------------------

    def testDualCell(self):

        # Create Dual Cell
        testDC = DualCell(loggerName='test')

        # Check that the variable is set correctly
        self.assertTrue(testDC.is_dual)






#==============================================================================
#    RUN TESTS
#==============================================================================
if __name__ == '__main__':
    from tools.myLogging import MyLogging

    with MyLogging('unittestCells'):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestCellMethods)
        unittest.TextTestRunner(verbosity=2).run(suite)
