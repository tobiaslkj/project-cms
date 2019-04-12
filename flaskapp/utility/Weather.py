from flask import Flask, request
import requests

def getWeather():
    r = requests.get('https://api.data.gov.sg/v1/environment/air-temperature')
    json_object = r.text
    return json_object
