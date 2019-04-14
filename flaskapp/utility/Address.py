import requests, json

def getAddress(address):
    oneMap = "https://developers.onemap.sg/commonapi/search?searchVal=%s&returnGeom=Y&getAddrDetails=Y" %(address)
    # send get request and save as response object
    response = requests.get(oneMap)

    # extract result in json format
    result = response.json()
    data={}
    data['latitude'] = result['results'][0]['LATITUDE']
    data['longtitude'] = result['results'][0]['LONGTITUDE']
    data['postalCode'] = result['results'][0]['POSTAL']
    data['address'] = result['results'][0]['ADDRESS']
    return data