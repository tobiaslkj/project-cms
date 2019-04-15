if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir
    path.append(dir(path[0]))
    __package__ = "Test"

import unittest
from flask import Flask
from flaskapp.validate.validateName import validateIncidentName


class Test(unittest.TestCase):
    
    def setUp(self):
        self.name1=validateIncidentName('Ken')
        self.name2=validateIncidentName('Yi Ern')
        self.name3=validateIncidentName('  ')
        self.name4=validateIncidentName('w$nglu')
        self.name5=validateIncidentName('harris0n')
        self.name6=validateIncidentName('tobi@s')
        self.name7=validateIncidentName('guanyu2n')
        self.name8=validateIncidentName('t')
        self.name9=validateIncidentName('terrance wan5')

    def tearDown(self):
        pass
        
    def test_invalid_name_specialChar(self):
        self.assertFalse(self.name4)
        self.assertFalse(self.name6)
    
    def test_invalid_name_number(self):
        self.assertFalse(self.name5)
        self.assertFalse(self.name7)
        self.assertFalse(self.name9)

    def test_invalid_name_whiteSpaces(self):
        self.assertFalse(self.name3)

    def test_invalid_name_length(self):
        self.assertFalse(self.name8)
   
    def test_valid_name(self):
        self.assertTrue(self.name1)
        self.assertTrue(self.name2)
       
    


if __name__ == '__main__':
    unittest.main()

        




