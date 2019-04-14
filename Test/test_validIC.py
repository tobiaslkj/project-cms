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
        self.ic4=validateNRIC('s9574591a')
    
    def tearDown(self):
        pass
    
    def test_valid_ic(self):
        self.assertFalse(self.ic1)
        self.assertFalse(self.ic2)
        self.assertFalse(self.ic3)
        self.assertTrue(self.ic4)
        

if __name__ == '__main__':
    unittest.main()