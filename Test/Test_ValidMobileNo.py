if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir
    path.append(dir(path[0]))
    __package__ = "Test"

import unittest
from flask import Flask
from flaskapp.validate.ValidateMobileNo import validateMobileNo

class TestValidMobileNo(unittest.TestCase):
    def setUp(self):
        self.no1=validateMobileNo('8368279')
        self.no2=validateMobileNo('836927988')
        self.no3=validateMobileNo('B3682798')
        self.no4=validateMobileNo('83682798')
        self.no5=validateMobileNo('80@77838')
    
    def tearDown(self):
        pass

    def test_incorrect_length_mobileno(self):
        self.assertFalse(self.no1)
        self.assertFalse(self.no2)

    def test_not_exist_mobileno(self):
        self.assertFalse(self.no3)
        self.assertFalse(self.no5)

    def test_valid_mobileno(self):
        self.assertTrue(self.no4)

if __name__ == '__main__':
    unittest.main()