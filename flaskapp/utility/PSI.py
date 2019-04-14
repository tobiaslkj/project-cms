from flask import Flask, request
import requests

def getPSI():
    r = requests.get('https://api.data.gov.sg/v1/environment/psi')
    data = r.json()

    firstPart = data['region_metadata']
    secondPart = data['items'][0]['readings']
    plist=[]
    for item in firstPart:
        pitem = {}
        pitem['type']= "Feature"
        pitem['geometry']={"type":"Point"}
        pitem['geometry']['coordinates']=[item['label_location']["longitude"],item['label_location']["latitude"]]
        properties = {}
        area = item['name']
        properties['area'] = area
        properties['o3_sub_index'] = secondPart['o3_sub_index'][area]
        properties['pm10_twenty_four_hourly'] = secondPart['pm10_twenty_four_hourly'][area]
        properties['pm10_sub_index'] = secondPart['pm10_sub_index'][area]
        properties['co_sub_index'] = secondPart['co_sub_index'][area]
        properties['pm25_twenty_four_hourly'] = secondPart['o3_sub_index'][area]
        properties['so2_sub_index'] = secondPart['so2_sub_index'][area]
        properties['co_eight_hour_max'] = secondPart['co_eight_hour_max'][area]
        properties['no2_one_hour_max'] = secondPart['no2_one_hour_max'][area]
        properties['so2_twenty_four_hourly'] = secondPart['so2_twenty_four_hourly'][area]
        properties['pm25_sub_index'] = secondPart['pm25_sub_index'][area]
        properties['psi_twenty_four_hourly'] = secondPart['psi_twenty_four_hourly'][area]
        properties['o3_eight_hour_max'] = secondPart['o3_eight_hour_max'][area]
        pitem['properties']=properties
        plist.append(pitem)

    return plist