import unittest

# import app.flaskapp
import requests
import json
import sys

# Extends the unittest.TestCase
class TestFlaskApiusingRequest(unittest.TestCase):
    def test_hello_world(self):
        response = requests.get("http://localhost")
        self.assertEqual(404, response.status_code)

