from flask import Flask, request
import requests

def getDengue():
    #r = requests.get('https://data.gov.sg/api/action/package_show?id=dengue-clusters')
    r = requests.get('https://geo.data.gov.sg/dengue-cluster/2019/04/05/geojson/dengue-cluster.geojson')
    json_object = r.text
    return json_object
