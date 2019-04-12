from flask import Flask, request
import requests

def getPSI():
    r = requests.get('https://api.data.gov.sg/v1/environment/psi')
    json_object = r.text
    print(json_object)
    return json_object