if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir
    path.append(dir(path[0]))
    __package__ = "Test"

# import app.flaskapp
import unittest
import requests
import json
import sys

# Extends the unittest.TestCase
class TestFlaskApiusingRequest(unittest.TestCase):
   
    # invalid userIC, other fields valid
    def test_invalid_userIC(self):
        payload = {'address': '331 Tah Ching Rd', 'name': 'Harrsion Wong', 'userIC':'S1234567Z', 'mobilePhone': '97969594', 'description': 'optional', 'assistance_type':['1'], 'emergency_type': ['1'], 'relevant_agencies':['1']}
        response = requests.post('http://localhost:5000/gpincident', data=payload)
        self.assertEqual(400, response.status_code)
        
    # invalid address, other fields valid
    def test_invalid_address(self):
        payload = {'address': '', 'name': 'Harrsion Wong', 'userIC':'S9648878E', 'mobilePhone': '97969594', 'description': 'optional', 'assistance_type':['1'], 'emergency_type': ['1'], 'relevant_agencies':['1']}
        response = requests.post('http://localhost:5000/gpincident', data=payload)
        self.assertEqual(400, response.status_code)
    
    # invalid name, other fields valid
    def test_invalid_name(self):
        payload = {'address': '331 Tah Ching Rd', 'name': 'R2D2', 'userIC':'S9648878E', 'mobilePhone': '97969594', 'description': 'optional', 'assistance_type':['1'], 'emergency_type': ['1'], 'relevant_agencies':['1']}
        response = requests.post('http://localhost:5000/gpincident', data=payload)
        self.assertEqual(400, response.status_code)
    
    # invalid name, other fields valid
    def test_invalid_phoneNo(self):
        payload = {'address': '331 Tah Ching Rd', 'name': 'Harrsion Wong', 'userIC':'S9648878E', 'mobilePhone': '9796959', 'description': 'optional', 'assistance_type':['1'], 'emergency_type': ['1'], 'relevant_agencies':['1']}
        response = requests.post('http://localhost:5000/gpincident', data=payload)
        self.assertEqual(400, response.status_code)
    
    # all valid fields
    def test_valid_incidentFields(self):
        payload = {'address': '331 Tah Ching Rd', 'name': 'Harrsion Wong', 'userIC':'S9648878E', 'mobilePhone': '97969594', 'description': 'optional', 'assistance_type':['1'], 'emergency_type': ['1'], 'relevant_agencies':['1']}
        response = requests.post('http://localhost:5000/gpincident', data=payload)
        self.assertEqual(201, response.status_code)


if __name__ == '__main__':
    unittest.main()