if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir
    path.append(dir(path[0]))
    __package__ = "Test"

import unittest
from flask import Flask
from flaskapp.validate.ValidateIc import validateNRIC


class TestValidIc(unittest.TestCase):
    
    def setUp(self):
        self.ic1=validateNRIC('u91')
        self.ic2=validateNRIC('u91a')
        self.ic3=validateNRIC('t9123451a')
        self.ic4=validateNRIC('s9111111a')
        self.ic5=validateNRIC('s9574591!')
        self.ic6=validateNRIC('*9574591a')
        self.ic7=validateNRIC('s9574591a')
        self.ic8=validateNRIC('g1107498m')
    
    def tearDown(self):
        pass
    
    def test_incorrect_length_ic(self):
        self.assertFalse(self.ic1)
        self.assertFalse(self.ic2)
    
    def test_not_exist_ic(self):
        self.assertFalse(self.ic3)
        self.assertFalse(self.ic4)
    
    def test_ic_with_special_char(self):
        self.assertFalse(self.ic5)
        self.assertFalse(self.ic6)
    
    def test_valid_ic(self):
        self.assertTrue(self.ic7)
        self.assertTrue(self.ic8)
        

if __name__ == '__main__':
    unittest.main()