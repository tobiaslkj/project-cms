if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir
    path.append(dir(path[0]))
    __package__ = "Test"

import unittest
from flask import Flask
from flaskapp.validate.validateAddress import validateIncidentAddress


class Test(unittest.TestCase):
    
    def setUp(self):
        self.address1=validateIncidentAddress('648886')
        self.address2=validateIncidentAddress('NTU')
        self.address3=validateIncidentAddress(' ')
        self.address4=validateIncidentAddress('ma@!$!#$')
        self.address5=validateIncidentAddress('NTU%&*')
        self.address6=validateIncidentAddress('g')
        self.address7=validateIncidentAddress('ba')

    def tearDown(self):
        pass
        
    def test_invalid_address_specialChar(self):
        self.assertFalse(self.address4)
        self.assertFalse(self.address5)
    
    def test_invalid_address_length(self):
        self.assertFalse(self.address6)
        self.assertFalse(self.address7)

    def test_invalid_address_spaces(self):
        self.assertFalse(self.address3)
       
    def test_valid_address(self):
        self.assertTrue(self.address1)
        self.assertTrue(self.address2)
    
    


if __name__ == '__main__':
    unittest.main()

        




